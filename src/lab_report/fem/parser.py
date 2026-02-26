"""Strict FEMRES parser with line-aware validation errors."""

from __future__ import annotations

from pathlib import Path

from .format import Element, FemMeta, FemRecord, Node, StressTensor

REQUIRED_SECTIONS = ("META", "NODES", "ELEMENTS", "STEP", "STRESS")


class _ParseError(ValueError):
    pass


def _error(path: Path, line_number: int, reason: str) -> _ParseError:
    return _ParseError(f"{path}:{line_number}: {reason}")


def _split_csv(line: str) -> list[str]:
    return [part.strip() for part in line.split(",")]


def _parse_int(path: Path, line_number: int, raw: str, field_name: str) -> int:
    try:
        return int(raw)
    except ValueError as exc:
        raise _error(path, line_number, f"non-numeric {field_name}") from exc


def _parse_float(path: Path, line_number: int, raw: str, field_name: str) -> float:
    try:
        return float(raw)
    except ValueError as exc:
        raise _error(path, line_number, f"non-numeric {field_name}") from exc


def parse_femres(path: str | Path) -> FemRecord:
    """Parse a `.femres` file with strict section and reference validation."""

    file_path = Path(path)
    raw_lines = file_path.read_text(encoding="utf-8").splitlines()

    lines: list[tuple[int, str]] = []
    for line_number, raw_line in enumerate(raw_lines, start=1):
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        lines.append((line_number, stripped))

    if not lines:
        raise _error(file_path, 1, "empty file")

    cursor = 0
    first_line_number, first_line = lines[cursor]
    cursor += 1
    signature = _split_csv(first_line)
    if len(signature) != 2 or signature[0] != "FEMRES":
        raise _error(file_path, first_line_number, "invalid FEMRES header")
    version = signature[1]

    section_positions: dict[str, int] = {}
    parsed_sections: dict[str, list[tuple[int, str]]] = {}

    current_section: str | None = None
    for line_number, text in lines[cursor:]:
        if text in REQUIRED_SECTIONS or text == "END":
            if text == "END":
                current_section = None
                continue
            current_section = text
            if current_section in section_positions:
                raise _error(file_path, line_number, f"duplicate section {current_section}")
            section_positions[current_section] = line_number
            parsed_sections[current_section] = []
            continue

        if current_section is None:
            raise _error(file_path, line_number, "content outside a section")
        parsed_sections[current_section].append((line_number, text))

    for section in REQUIRED_SECTIONS:
        if section not in parsed_sections:
            line_hint = len(raw_lines) if raw_lines else 1
            raise _error(file_path, line_hint, f"missing required section {section}")

    meta = _parse_meta(file_path, parsed_sections["META"])
    nodes = _parse_nodes(file_path, parsed_sections["NODES"])
    elements = _parse_elements(file_path, parsed_sections["ELEMENTS"], nodes)
    step_name = _parse_step(file_path, parsed_sections["STEP"])
    stress = _parse_stress(file_path, parsed_sections["STRESS"], elements)

    return FemRecord(
        path=str(file_path),
        version=version,
        meta=meta,
        step_name=step_name,
        nodes=nodes,
        elements=elements,
        stress=stress,
    )


def _parse_meta(path: Path, rows: list[tuple[int, str]]) -> FemMeta:
    if not rows:
        raise _error(path, 1, "META section is empty")

    entries: dict[str, str] = {}
    for line_number, text in rows:
        parts = _split_csv(text)
        if len(parts) != 2:
            raise _error(path, line_number, "invalid META row")
        key, value = parts
        entries[key] = value

    case_id = entries.get("case_id")
    load_level = entries.get("load_level")
    if case_id is None:
        first_line = rows[0][0]
        raise _error(path, first_line, "META missing case_id")
    if load_level is None:
        first_line = rows[0][0]
        raise _error(path, first_line, "META missing load_level")
    return FemMeta(case_id=case_id, load_level=load_level)


def _parse_nodes(path: Path, rows: list[tuple[int, str]]) -> dict[int, Node]:
    if len(rows) < 2:
        line_hint = rows[0][0] if rows else 1
        raise _error(path, line_hint, "NODES section missing header or rows")

    header_line, header_text = rows[0]
    header = _split_csv(header_text)
    if header != ["id", "x", "y", "z"]:
        raise _error(path, header_line, "invalid NODES header")

    nodes: dict[int, Node] = {}
    for line_number, text in rows[1:]:
        parts = _split_csv(text)
        if len(parts) != 4:
            raise _error(path, line_number, "invalid NODES row")

        node_id = _parse_int(path, line_number, parts[0], "node id")
        if node_id in nodes:
            raise _error(path, line_number, "duplicate node id")

        nodes[node_id] = Node(
            id=node_id,
            x=_parse_float(path, line_number, parts[1], "x"),
            y=_parse_float(path, line_number, parts[2], "y"),
            z=_parse_float(path, line_number, parts[3], "z"),
        )

    if not nodes:
        raise _error(path, header_line, "NODES section has no data rows")
    return nodes


def _parse_elements(
    path: Path,
    rows: list[tuple[int, str]],
    nodes: dict[int, Node],
) -> dict[int, Element]:
    if len(rows) < 2:
        line_hint = rows[0][0] if rows else 1
        raise _error(path, line_hint, "ELEMENTS section missing header or rows")

    header_line, header_text = rows[0]
    header = _split_csv(header_text)
    if header != ["id", "n1", "n2", "n3"]:
        raise _error(path, header_line, "invalid ELEMENTS header")

    elements: dict[int, Element] = {}
    for line_number, text in rows[1:]:
        parts = _split_csv(text)
        if len(parts) != 4:
            raise _error(path, line_number, "invalid ELEMENTS row")

        element_id = _parse_int(path, line_number, parts[0], "element id")
        if element_id in elements:
            raise _error(path, line_number, "duplicate element id")

        n1 = _parse_int(path, line_number, parts[1], "n1")
        n2 = _parse_int(path, line_number, parts[2], "n2")
        n3 = _parse_int(path, line_number, parts[3], "n3")
        for node_ref in (n1, n2, n3):
            if node_ref not in nodes:
                raise _error(path, line_number, "element references unknown node id")

        elements[element_id] = Element(id=element_id, n1=n1, n2=n2, n3=n3)

    if not elements:
        raise _error(path, header_line, "ELEMENTS section has no data rows")
    return elements


def _parse_step(path: Path, rows: list[tuple[int, str]]) -> str:
    if not rows:
        raise _error(path, 1, "STEP section is empty")

    entries: dict[str, str] = {}
    for line_number, text in rows:
        parts = _split_csv(text)
        if len(parts) != 2:
            raise _error(path, line_number, "invalid STEP row")
        key, value = parts
        entries[key] = value

    step_name = entries.get("name")
    if step_name is None:
        first_line = rows[0][0]
        raise _error(path, first_line, "STEP missing name")
    return step_name


def _parse_stress(
    path: Path,
    rows: list[tuple[int, str]],
    elements: dict[int, Element],
) -> dict[int, StressTensor]:
    if len(rows) < 2:
        line_hint = rows[0][0] if rows else 1
        raise _error(path, line_hint, "STRESS section missing header or rows")

    header_line, header_text = rows[0]
    header = _split_csv(header_text)
    if header == ["element_id", "sxx", "syy", "szz", "txy", "tyz", "tzx"]:
        header = ["element_id", "sxx", "syy", "szz", "sxy", "syz", "szx"]
    expected = ["element_id", "sxx", "syy", "szz", "sxy", "syz", "szx"]
    if header != expected:
        raise _error(path, header_line, "invalid STRESS header")

    stress: dict[int, StressTensor] = {}
    for line_number, text in rows[1:]:
        parts = _split_csv(text)
        if len(parts) != 7:
            raise _error(path, line_number, "invalid STRESS row")

        element_id = _parse_int(path, line_number, parts[0], "element id")
        if element_id not in elements:
            raise _error(path, line_number, "unknown element id in STRESS")
        if element_id in stress:
            raise _error(path, line_number, "duplicate stress element id")

        stress[element_id] = StressTensor(
            element_id=element_id,
            sxx=_parse_float(path, line_number, parts[1], "sxx"),
            syy=_parse_float(path, line_number, parts[2], "syy"),
            szz=_parse_float(path, line_number, parts[3], "szz"),
            sxy=_parse_float(path, line_number, parts[4], "sxy"),
            syz=_parse_float(path, line_number, parts[5], "syz"),
            szx=_parse_float(path, line_number, parts[6], "szx"),
        )

    if not stress:
        raise _error(path, header_line, "STRESS section has no data rows")
    return stress
