#!/usr/bin/env bash
set -euo pipefail

echo "[lint] starting"

if [[ -n "${SKILL_LINT_CMD:-}" ]]; then
  echo "[lint] running override command from SKILL_LINT_CMD"
  bash -lc "${SKILL_LINT_CMD}"
  echo "[lint] completed"
  exit 0
fi

if [[ -f "pyproject.toml" || -f "requirements-dev.txt" || -f "requirements.txt" ]]; then
  echo "[lint] running: python -m ruff check ."
  python -m ruff check .
  echo "[lint] completed"
  exit 0
fi

if [[ -f "package.json" ]] && command -v npm >/dev/null 2>&1 && npm run -s | grep -q "^  lint$"; then
  echo "[lint] running: npm run -s lint"
  npm run -s lint
  echo "[lint] completed"
  exit 0
fi

echo "[lint] skipped: no linter configured yet"
echo "[lint] TODO: set SKILL_LINT_CMD or add a package script"
