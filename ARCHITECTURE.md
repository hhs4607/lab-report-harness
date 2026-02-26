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
  - FEM pipeline: `docs/runbooks/fem-pipeline.md`
  - Release: `docs/runbooks/release.md`
- CSV sample module:
  - Package root: `src/lab_report/series.py`
  - Responsibilities:
    - `parse_csv_series(path)`: validate CSV boundary schema (`value` column) and parse numeric values.
    - `summary_stats(values)`: return typed `Summary` dataclass for count/min/max/mean/stdev.
    - `render_summary_markdown(summary)`: produce markdown output for report-style summaries.
- FEM pipeline modules:
  - Package root: `src/lab_report/fem/`
  - Responsibilities:
    - `format.py`: typed dataclasses for FEM entities (meta, nodes, elements, stress, parsed record).
    - `parser.py`: strict section parsing and reference validation with line-aware errors.
    - `features.py`: von Mises computation and deterministic aggregate features.
    - `model.py`: Basquin-like torch model (`log10(N) = A - B*log10(sigma_vm_max)`).
    - `pipeline.py`: CLI path to parse input and write deterministic artifacts.
  - Validation surface:
    - `tests/test_fem_pipeline.py`
    - `tests/fixtures/fem/*.femres`

## Boundaries
- In scope:
  - Repo-local process, docs, and lightweight governance.
  - Agent-readable operational rules.
  - Typed sample data-processing modules under `src/`.
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

CSV module flow:
1. CSV file is parsed at the boundary (`parse_csv_series`) with strict schema validation.
2. Numeric values are summarized into a typed dataclass (`summary_stats`).
3. Summary is rendered as markdown (`render_summary_markdown`) for report output.

FEM pipeline flow:
1. FEMRES input is parsed/validated (`lab_report.fem.parser`).
2. Stress-derived features are computed (`lab_report.fem.features`).
3. Life prediction is computed with torch (`lab_report.fem.model`).
4. Deterministic artifacts are written (`lab_report.fem.pipeline`) to `artifacts/fem_pipeline/`.

Operational telemetry and artifact routing are `TODO`.

## Deployment
No deployment mechanism is assumed yet.

Deployment policy placeholder:
- Build command: `TODO`
- Release command: `TODO`
- Rollback command: `TODO`

See [`docs/runbooks/release.md`](docs/runbooks/release.md).

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

Track gaps in [`docs/tech-debt-tracker.md`](docs/tech-debt-tracker.md).
