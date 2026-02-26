# FEM Synthetic Pipeline Example

## What This Project Does
This project demonstrates an end-to-end synthetic FEM workflow:
- Parse sectioned `.femres` files with strict validation.
- Compute stress-derived features, including von Mises aggregates.
- Predict fatigue life cycles with a Basquin-like PyTorch model.
- Write deterministic output artifacts for repeatable checks.

## Repo Structure
- `src/lab_report/fem/`
  - `format.py`: typed data structures
  - `parser.py`: strict parsing and boundary validation
  - `features.py`: von Mises and aggregate feature extraction
  - `model.py`: PyTorch fatigue life predictor
  - `pipeline.py`: CLI pipeline entrypoint
- `skills/run_fem_pipeline.sh`
  - one-command local run for the sample low-load fixture
- `tests/fixtures/fem/`
  - sample FEMRES inputs (`cantilever_low`, `cantilever_high`, shuffled low)

## Quickstart
### Option A: conda env
```bash
conda env create -f environment.yml
conda activate harness-lab
pip install -r requirements-dev.txt
```

### Run the pipeline
```bash
./skills/run_fem_pipeline.sh
```

### Direct CLI run
```bash
PYTHONPATH=src python -m lab_report.fem.pipeline \
  --input tests/fixtures/fem/cantilever_low.femres \
  --outdir artifacts/fem_pipeline
```

## Validation
Run tests:
```bash
python -m pytest -q
```

Run full local quality gate:
```bash
./skills/pr_check.sh
```

## Outputs
Pipeline outputs are written to `artifacts/fem_pipeline/`:
- `features.json`
- `prediction.json`
- `report.md`

## Design Notes
- Strict boundary parsing: required sections, numeric checks, and reference integrity checks.
- Deterministic outputs: stable JSON key ordering, rounded floats, no timestamps.
- Meaningful tests:
  - order invariance (shuffled rows produce same features/predictions)
  - monotonicity (higher stress yields lower predicted life)
  - autograd sign (negative gradient for life-vs-stress in log space)
