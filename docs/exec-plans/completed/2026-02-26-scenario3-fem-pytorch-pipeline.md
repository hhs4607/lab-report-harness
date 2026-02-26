# Execution Plan

## Metadata
- Plan ID: `scenario3-fem-pytorch-pipeline`
- Title: Implement FEM-style synthetic parser and PyTorch pipeline
- Owner: `codex`
- Status: `done`
- Created: `2026-02-26`
- Target completion: `2026-02-26`

## Objective
Implement Scenario 3 end-to-end: strict FEMRES parser, deterministic feature extraction, Basquin-like PyTorch life prediction, CLI pipeline outputs, skill script, tests, and documentation updates.

## Scope
- In scope:
  - Strict parser with section validation, numeric checks, and line-aware errors.
  - Feature engineering (von Mises + aggregate metrics).
  - Basquin-like torch model using pure torch ops.
  - Deterministic CLI outputs (`features.json`, `prediction.json`, `report.md`).
  - Skill script (`skills/run_fem_pipeline.sh`).
  - Tests for parser errors, invariance, monotonicity, autograd, and e2e outputs.
  - Docs updates (`docs/runbooks/fem-pipeline.md`, docs index, architecture).
- Out of scope:
  - Multi-step loading histories.
  - Model fitting/training loop.
  - Production deployment/runtime orchestration.

## Assumptions
- Single-step synthetic fixture is sufficient for current acceptance coverage.
- Determinism is achieved via fixed model constants and rounded JSON outputs.
- Parser must reject malformed input early with file+line+reason details.

## Acceptance Criteria
- Parser validates required sections: `META`, `NODES`, `ELEMENTS`, `STEP`, `STRESS`.
- Parser errors include file path, 1-based line, and reason text.
- Element connectivity must reference existing node IDs.
- STRESS rows must reference existing element IDs.
- Feature set includes `n_nodes`, `n_elements`, `sigma_vm_max`, `sigma_vm_mean`, `sigma_vm_p95`.
- Feature/prediction results are invariant to row ordering.
- Torch model implements `log10N = A - B*log10(sigma_vm_max)` with fixed constants and autograd support.
- CLI entry `python -m lab_report.fem.pipeline --input <path> --outdir <dir>` writes deterministic files.
- Skill script runs pipeline against low fixture and prints output paths.
- Docs are updated and links remain repo-relative.
- `./skills/pr_check.sh` passes.

## Steps
1. Implement strict parser and FEM dataclasses.
2. Implement von Mises and aggregate features.
3. Implement Basquin-like torch model.
4. Implement deterministic pipeline CLI outputs.
5. Add skill script and comprehensive tests.
6. Update docs and architecture.
7. Run quality gate and fix issues.

## Validation
- Invariants to check:
  - `./skills/pr_check.sh` green.
  - Tests cover required scenario checks.
- Quality score target:
  - No regressions in existing checks.
- Evidence to collect (commands + outputs):
  - `python -m pytest -q tests/test_fem_pipeline.py`
  - `PYTHONPATH=src python -m lab_report.fem.pipeline --input tests/fixtures/fem/cantilever_low.femres --outdir /tmp/fem_pipeline_check`
  - `./skills/run_fem_pipeline.sh`
  - `./skills/pr_check.sh`

## Evidence Log
- `python -m pytest -q tests/test_fem_pipeline.py`
  - `5 passed, 1 warning in 0.66s`
- `PYTHONPATH=src python -m lab_report.fem.pipeline --input tests/fixtures/fem/cantilever_low.femres --outdir /tmp/fem_pipeline_check`
  - `features: /tmp/fem_pipeline_check/features.json`
  - `prediction: /tmp/fem_pipeline_check/prediction.json`
  - `report: /tmp/fem_pipeline_check/report.md`
- `./skills/run_fem_pipeline.sh`
  - `features: artifacts/fem_pipeline/features.json`
  - `prediction: artifacts/fem_pipeline/prediction.json`
  - `report: artifacts/fem_pipeline/report.md`
- `./skills/pr_check.sh`
  - `ruff check: All checks passed!`
  - `mypy: Success: no issues found in 4 source files`
  - `pytest: 14 passed, 1 warning`
  - `doc_check: markdown links ok (14 files scanned)`
  - `[pr_check] all checks finished`

## Risks and Mitigations
- Risk: parser strictness may reject future fixture variants.
  - Mitigation: keep explicit error reasons and extend fixtures/tests before relaxing parser behavior.
- Risk: PyTorch precision differences can affect exact numeric comparisons.
  - Mitigation: round serialized outputs and compare with tolerance in tests.

## Decision Log
- Date: `2026-02-26`
  - Decision: set Basquin constants to `A=12.0`, `B=3.0`.
  - Rationale: deterministic monotonic baseline for harness validation.
- Date: `2026-02-26`
  - Decision: keep deterministic JSON output using stable key ordering and rounded floats.
  - Rationale: avoids non-functional diffs and simplifies golden-style assertions.

## Completion
- Outcome summary: End-to-end FEM parser/features/model/pipeline delivered with test coverage and docs/runbook support.
- Follow-ups:
  - Add multi-element fixtures to stress percentile behavior more deeply.
  - Add optional `numpy` to suppress torch warning in environments that need it.
- Archive location in `docs/exec-plans/completed/`: `docs/exec-plans/completed/2026-02-26-scenario3-fem-pytorch-pipeline.md`
