# Bootstrap Runbook

Purpose: prepare a local development environment for this repository.

## Prerequisites
- Git
- Bash-compatible shell
- Python 3.10+ (`python` command available)

## Current Bootstrap Command
Run:

```bash
./skills/bootstrap.sh
```

This script is intentionally conservative and does not install dependencies automatically.

## Create Python Environment

### Option A: `venv`

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

### Option B: `conda`

```bash
conda env create -f environment.yml
conda activate harness-lab
./skills/pr_check.sh
```

## Run Full Local Check
After creating the environment and installing dependencies, run:

```bash
./skills/pr_check.sh
```

This executes:
1. `./skills/bootstrap.sh`
2. `./skills/format.sh`
3. `./skills/lint.sh`
4. `./skills/typecheck.sh`
5. `./skills/test.sh`
6. `./skills/doc_check.sh`

Current Python commands used by the checks:
- `./skills/format.sh` -> `python -m ruff format .`
- `./skills/lint.sh` -> `python -m ruff check .`
- `./skills/typecheck.sh` -> `python -m mypy .`
- `./skills/test.sh` -> `python -m pytest -q`
