"""Data structures for FEMRES parsing and downstream pipeline steps."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FemMeta:
    """Metadata fields parsed from the META section."""

    case_id: str
    load_level: str


@dataclass(frozen=True, slots=True)
class Node:
    """Single mesh node."""

    id: int
    x: float
    y: float
    z: float


@dataclass(frozen=True, slots=True)
class Element:
    """Single element with 3-node connectivity."""

    id: int
    n1: int
    n2: int
    n3: int


@dataclass(frozen=True, slots=True)
class StressTensor:
    """Per-element stress tensor components."""

    element_id: int
    sxx: float
    syy: float
    szz: float
    sxy: float
    syz: float
    szx: float


@dataclass(frozen=True, slots=True)
class FemRecord:
    """Parsed FEMRES record."""

    path: str
    version: str
    meta: FemMeta
    step_name: str
    nodes: dict[int, Node]
    elements: dict[int, Element]
    stress: dict[int, StressTensor]
