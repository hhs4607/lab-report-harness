from __future__ import annotations

from pathlib import Path

import pytest

from lab_report import parse_csv_series, render_summary_markdown, summary_stats


def _write_csv(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path


def test_parse_csv_series_parses_valid_value_column(tmp_path: Path) -> None:
    csv_path = _write_csv(tmp_path / "series.csv", "value\n1.5\n2\n3.25\n")
    assert parse_csv_series(csv_path) == [1.5, 2.0, 3.25]


def test_parse_csv_series_rejects_wrong_header(tmp_path: Path) -> None:
    csv_path = _write_csv(tmp_path / "series.csv", "amount\n1\n2\n")
    with pytest.raises(ValueError, match="schema mismatch"):
        parse_csv_series(csv_path)


def test_parse_csv_series_rejects_non_numeric_value(tmp_path: Path) -> None:
    csv_path = _write_csv(tmp_path / "series.csv", "value\n1\nabc\n")
    with pytest.raises(ValueError, match="non-numeric"):
        parse_csv_series(csv_path)


def test_parse_csv_series_rejects_blank_value(tmp_path: Path) -> None:
    csv_path = _write_csv(tmp_path / "series.csv", "value\n1\n \n")
    with pytest.raises(ValueError, match="missing required"):
        parse_csv_series(csv_path)


def test_summary_stats_returns_expected_values() -> None:
    summary = summary_stats([1.0, 2.0, 3.0, 4.0])
    assert summary.count == 4
    assert summary.min == 1.0
    assert summary.max == 4.0
    assert summary.mean == pytest.approx(2.5)
    assert summary.stdev == pytest.approx(1.2909944487358056)


def test_summary_stats_single_value_has_zero_stdev() -> None:
    summary = summary_stats([42.0])
    assert summary.count == 1
    assert summary.stdev == 0.0


def test_summary_stats_rejects_empty_input() -> None:
    with pytest.raises(ValueError, match="non-empty"):
        summary_stats([])


def test_render_summary_markdown_outputs_table() -> None:
    summary = summary_stats([1.0, 2.0, 3.0])
    rendered = render_summary_markdown(summary)
    assert "## Series Summary" in rendered
    assert "| Metric | Value |" in rendered
    assert "| count | 3 |" in rendered
    assert "| mean | 2 |" in rendered
