# Execution Plan

## Metadata
- Plan ID: `scenario2-sample-module`
- Title: Build a typed sample Python module with validation, stats, and markdown rendering
- Owner: `codex`
- Status: `active`
- Created: `2026-02-26`
- Target completion: `2026-02-26`

## Objective
Add a meaningful, importable Python module under `src/` that reads numeric series data from CSV with boundary validation, computes summary statistics via a typed dataclass, renders markdown output, and is verified by tests and repo quality gates.

## Scope
- In scope:
  - Create `src/lab_report/` package structure and implementation.
  - Implement `parse_csv_series(path) -> list[float]` with schema validation at file boundary.
  - Implement `summary_stats(values) -> Summary` dataclass output (`count/min/max/mean/stdev`).
  - Implement `render_summary_markdown(summary) -> str`.
  - Add tests for boundary validation and statistics correctness.
  - Update architecture and docs index links per acceptance criteria.
  - Run `./skills/pr_check.sh` and capture evidence.
- Out of scope:
  - CLI wrappers, web APIs, or persistence layers.
  - Non-CSV input formats.

## Assumptions
- CSV input schema for `parse_csv_series` is one required numeric column named `value`.
- Empty input for `summary_stats` should fail fast with `ValueError`.
- Standard deviation uses sample standard deviation (`statistics.stdev`) and is `0.0` for single-value input.

## Steps
1. Phase 1: scaffold package + implement CSV boundary validation and importability checks.
2. Phase 2: implement typed summary statistics + markdown renderer.
3. Phase 3: add tests, update docs (`ARCHITECTURE.md`, `docs/index.md`), and run quality gates.

## Validation
- Invariants to check:
  - `./skills/typecheck.sh`
  - `./skills/test.sh`
  - `./skills/doc_check.sh`
  - `./skills/pr_check.sh`
- Quality score target:
  - No regressions; all automated checks pass.
- Evidence to collect (commands + outputs):
  - File tree checks, test output, and full `pr_check` output summary.

## Risks and Mitigations
- Risk: CSV schema assumptions mismatch expected harness scenario.
  - Mitigation: make schema explicit in docstrings and test boundary behavior clearly.
- Risk: Relative-link policy failures in docs.
  - Mitigation: update `docs/index.md` links to repo-relative paths and verify with `doc_check`.

## Decision Log
- Date: `2026-02-26`
  - Decision: enforce CSV schema as a required `value` column.
  - Rationale: clear, deterministic boundary contract for validation tests.
- Date: `2026-02-26`
  - Decision: use sample standard deviation with single-item fallback to `0.0`.
  - Rationale: avoids runtime errors while preserving conventional statistics behavior.

## Completion
- Outcome summary: `TODO(template): fill at completion`
- Follow-ups: `TODO(template): fill at completion`
- Archive location in `docs/exec-plans/completed/`: `TODO(template): fill at completion`
