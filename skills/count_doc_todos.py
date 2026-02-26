#!/usr/bin/env python3
"""Count TODO markers in markdown docs with policy-aware filtering."""

from __future__ import annotations

import re
import sys
from pathlib import Path

FENCE_RE = re.compile(r"^\s*(```|~~~)")
TODO_MARKER_RE = re.compile(r"TODO(?::|\(([^)\n]+)\):)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")


def split_non_fenced_lines(text: str) -> list[str]:
    in_fence = False
    lines: list[str] = []
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            lines.append(line)
    return lines


def count_markers(md_path: Path) -> tuple[int, int, int]:
    text = md_path.read_text(encoding="utf-8")
    lines = split_non_fenced_lines(text)

    template_markers = 0
    real_markers = 0

    for line in lines:
        for match in TODO_MARKER_RE.finditer(line):
            marker_type = match.group(1)
            if marker_type == "template":
                template_markers += 1

    for line in lines:
        no_inline_code = INLINE_CODE_RE.sub("", line)
        for match in TODO_MARKER_RE.finditer(no_inline_code):
            marker_type = match.group(1)
            if marker_type != "template":
                real_markers += 1

    total_markers = template_markers + real_markers
    return total_markers, template_markers, real_markers


def main() -> int:
    docs_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs")
    if not docs_dir.exists():
        print("error: docs directory not found", file=sys.stderr)
        return 1

    total_markers = 0
    template_markers = 0
    real_markers = 0

    for md_path in sorted(docs_dir.rglob("*.md")):
        total, template, real = count_markers(md_path)
        total_markers += total
        template_markers += template
        real_markers += real

    print(f"docs_total_markers={total_markers}")
    print(f"docs_template_markers={template_markers}")
    print(f"docs_real_markers={real_markers}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
