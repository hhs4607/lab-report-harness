#!/usr/bin/env bash
set -euo pipefail

echo "[format] starting"

if [[ -n "${SKILL_FORMAT_CMD:-}" ]]; then
  echo "[format] running override command from SKILL_FORMAT_CMD"
  bash -lc "${SKILL_FORMAT_CMD}"
  echo "[format] completed"
  exit 0
fi

if [[ -f "pyproject.toml" || -f "requirements-dev.txt" || -f "requirements.txt" ]]; then
  echo "[format] running: python -m ruff format ."
  python -m ruff format .
  echo "[format] completed"
  exit 0
fi

if [[ -f "package.json" ]] && command -v npm >/dev/null 2>&1 && npm run -s | grep -q "^  format$"; then
  echo "[format] running: npm run -s format"
  npm run -s format
  echo "[format] completed"
  exit 0
fi

echo "[format] skipped: no formatter configured yet"
echo "[format] TODO: set SKILL_FORMAT_CMD or add a package script"
