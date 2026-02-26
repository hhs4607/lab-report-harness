"""Feature engineering for FEM stress-derived metrics."""

from __future__ import annotations

import math

from .format import FemRecord, StressTensor


def _von_mises(stress: StressTensor) -> float:
    term_normal = (stress.sxx - stress.syy) ** 2
    term_normal += (stress.syy - stress.szz) ** 2
    term_normal += (stress.szz - stress.sxx) ** 2
    term_shear = stress.sxy**2 + stress.syz**2 + stress.szx**2
    return math.sqrt(0.5 * (term_normal + 6.0 * term_shear))


def compute_von_mises(record: FemRecord) -> list[float]:
    """Compute per-element von Mises stress values."""

    ordered_ids = sorted(record.stress.keys())
    return [_von_mises(record.stress[element_id]) for element_id in ordered_ids]


def _percentile(values: list[float], percentile: float) -> float:
    if not values:
        raise ValueError("percentile requires non-empty values")
    if len(values) == 1:
        return values[0]

    sorted_values = sorted(values)
    pos = (len(sorted_values) - 1) * (percentile / 100.0)
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return sorted_values[lo]
    weight = pos - lo
    return sorted_values[lo] * (1.0 - weight) + sorted_values[hi] * weight


def aggregate_features(record: FemRecord) -> dict[str, float]:
    """Compute deterministic aggregate features."""

    von_mises = compute_von_mises(record)
    vm_max = max(von_mises)
    vm_mean = sum(von_mises) / len(von_mises)
    vm_p95 = _percentile(von_mises, 95.0)

    return {
        "n_nodes": float(len(record.nodes)),
        "n_elements": float(len(record.elements)),
        "sigma_vm_max": vm_max,
        "sigma_vm_mean": vm_mean,
        "sigma_vm_p95": vm_p95,
    }
