"""Lab report sample module."""

from .series import Summary, parse_csv_series, render_summary_markdown, summary_stats

__all__ = [
    "Summary",
    "parse_csv_series",
    "summary_stats",
    "render_summary_markdown",
]
