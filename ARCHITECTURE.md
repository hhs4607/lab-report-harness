# ARCHITECTURE

## Overview
This repository is a harness-engineering workspace intended for agent-driven execution, documentation-first operation, and incremental hardening over time.

Primary architectural intent:
- Keep process and decisions versioned in-repo.
- Keep behavior predictable via explicit invariants.
- Keep execution work tracked through plan artifacts.

## Domains/Modules
- Documentation system of record: `docs/`
- Agent navigation and operating map: `AGENTS.md`
- Execution plans:
  - Active: `docs/exec-plans/active/`
  - Completed archive: `docs/exec-plans/completed/`
- Quality governance:
  - Invariants: `docs/quality/invariants.md`
  - Rubric: `docs/quality/quality-score.md`
- Runbooks:
  - Debugging: `docs/runbooks/debugging.md`
  - Release: `docs/runbooks/release.md`
- Python sample module:
  - Package root: `src/lab_report/`
  - Responsibilities:
    - `parse_csv_series(path)`: validate CSV boundary schema (`value` column) and parse numeric values.
    - `summary_stats(values)`: return typed `Summary` dataclass for count/min/max/mean/stdev.
    - `render_summary_markdown(summary)`: produce markdown output for report-style summaries.
  - Validation surface:
    - Tests in `tests/test_series.py`
    - Import bootstrap for `src/` layout in `tests/conftest.py`

## Boundaries
- In scope:
  - Repo-local process, docs, and lightweight governance.
  - Agent-readable operational rules.
  - Typed sample data-processing module under `src/`.
- Out of scope (current phase):
  - Stack-specific runtime assumptions.
  - Environment-specific deployment topology.
  - Provider-specific security controls.

Unknown boundary decisions should be captured as `TODO` in docs, then resolved via plans.

## Data flow
Current conceptual flow:
1. Inputs arrive as tasks/issues/requests.
2. Work is scoped in active execution plans.
3. Changes are implemented in code/docs.
4. Quality checks are evaluated against invariants/rubric.
5. Outputs are released and plans archived.

Sample module flow:
1. CSV file is parsed at the boundary (`parse_csv_series`) with strict schema validation.
2. Numeric values are summarized into a typed dataclass (`summary_stats`).
3. Summary is rendered as markdown (`render_summary_markdown`) for report output.

Operational telemetry and artifact routing are `TODO`.

## Deployment
No deployment mechanism is assumed yet.

Deployment policy placeholder:
- Build command: `TODO`
- Release command: `TODO`
- Rollback command: `TODO`

See [`docs/runbooks/release.md`](/Users/hyeonseok/Projects/harness-lab/docs/runbooks/release.md).

## Observability
Observability baseline is documentation-first until tooling is chosen.

Planned layers:
- Human-readable runbooks and plan logs (now)
- Automated checks and CI signals (`TODO`)
- Runtime metrics/traces (`TODO`)

## Security assumptions
Current assumptions are minimal and conservative:
- No secrets should be committed.
- Changes should be reviewable and attributable in version control.
- Unknown security posture for runtime/deployment until stack is defined (`TODO`).

Track gaps in [`docs/tech-debt-tracker.md`](/Users/hyeonseok/Projects/harness-lab/docs/tech-debt-tracker.md).
