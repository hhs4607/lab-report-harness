# FEM Pipeline Runbook

Purpose: run the FEM synthetic parser/features/model pipeline and inspect deterministic artifacts.

## Prerequisites
- Python environment prepared via [`bootstrap.md`](bootstrap.md)
- Dependencies installed from `requirements-dev.txt` (includes `torch`)

## Quick Run (Skill Button)
Run:

```bash
./skills/run_fem_pipeline.sh
```

This command uses `tests/fixtures/fem/cantilever_low.femres` and writes artifacts under `artifacts/fem_pipeline/`.

## Direct CLI Run
Run:

```bash
PYTHONPATH=src python -m lab_report.fem.pipeline \
  --input tests/fixtures/fem/cantilever_low.femres \
  --outdir artifacts/fem_pipeline
```

## Outputs
- `features.json`
  - `n_nodes`
  - `n_elements`
  - `sigma_vm_max`
  - `sigma_vm_mean`
  - `sigma_vm_p95`
- `prediction.json`
  - `sigma_vm_max`
  - `log10_life`
  - `life_cycles`
- `report.md`
  - Human-readable summary
  - Data quality checks

## Validation Path
After local pipeline runs, validate repository invariants:

```bash
./skills/pr_check.sh
```
