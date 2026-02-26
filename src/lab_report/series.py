"""Utilities for parsing numeric CSV series and reporting summary statistics."""

from __future__ import annotations

import csv
import statistics
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Summary:
    """Summary statistics for a numeric series."""

    count: int
    min: float
    max: float
    mean: float
    stdev: float


def parse_csv_series(path: str | Path) -> list[float]:
    """Parse a CSV file containing a single required numeric `value` column."""

    csv_path = Path(path)
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = [name.strip() for name in reader.fieldnames or [] if name is not None]
        if fieldnames != ["value"]:
            raise ValueError(
                "CSV schema mismatch: expected exactly one header column named 'value'."
            )

        values: list[float] = []
        for line_number, row in enumerate(reader, start=2):
            raw = row.get("value")
            if raw is None or not raw.strip():
                raise ValueError(f"Row {line_number}: missing required 'value'.")
            try:
                values.append(float(raw))
            except ValueError as exc:
                raise ValueError(f"Row {line_number}: non-numeric 'value'={raw!r}.") from exc

    return values


def summary_stats(values: Sequence[float]) -> Summary:
    """Compute count/min/max/mean/stdev for a non-empty numeric sequence."""

    if not values:
        raise ValueError("values must be non-empty")

    series = [float(value) for value in values]
    count = len(series)
    stdev = 0.0 if count == 1 else statistics.stdev(series)
    return Summary(
        count=count,
        min=min(series),
        max=max(series),
        mean=statistics.fmean(series),
        stdev=stdev,
    )


def render_summary_markdown(summary: Summary) -> str:
    """Render summary statistics as a markdown table."""

    return "\n".join(
        [
            "## Series Summary",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            f"| count | {summary.count} |",
            f"| min | {summary.min:.6g} |",
            f"| max | {summary.max:.6g} |",
            f"| mean | {summary.mean:.6g} |",
            f"| stdev | {summary.stdev:.6g} |",
        ]
    )
