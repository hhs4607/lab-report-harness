#!/usr/bin/env bash
set -euo pipefail

echo "[test] starting"

if [[ -n "${SKILL_TEST_CMD:-}" ]]; then
  echo "[test] running override command from SKILL_TEST_CMD"
  bash -lc "${SKILL_TEST_CMD}"
  echo "[test] completed"
  exit 0
fi

if [[ -f "pyproject.toml" || -f "requirements-dev.txt" || -f "requirements.txt" ]]; then
  echo "[test] running: python -m pytest -q"
  python -m pytest -q
  echo "[test] completed"
  exit 0
fi

if [[ -f "package.json" ]] && command -v npm >/dev/null 2>&1 && npm run -s | grep -q "^  test$"; then
  echo "[test] running: npm run -s test"
  npm run -s test
  echo "[test] completed"
  exit 0
fi

echo "[test] skipped: no test command configured yet"
echo "[test] TODO: set SKILL_TEST_CMD or add a package script"
