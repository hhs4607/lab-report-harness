#!/usr/bin/env bash
set -euo pipefail

echo "[typecheck] starting"

if [[ -n "${SKILL_TYPECHECK_CMD:-}" ]]; then
  echo "[typecheck] running override command from SKILL_TYPECHECK_CMD"
  bash -lc "${SKILL_TYPECHECK_CMD}"
  echo "[typecheck] completed"
  exit 0
fi

if [[ -f "pyproject.toml" || -f "requirements-dev.txt" || -f "requirements.txt" ]]; then
  targets=()
  if [[ -d "tests" ]]; then
    targets+=("tests")
  elif [[ -d "src" ]]; then
    targets+=("src")
  else
    targets+=(".")
  fi

  echo "[typecheck] detected Python project markers"
  echo "[typecheck] running: python -m mypy ${targets[*]}"
  set +e
  python -m mypy "${targets[@]}"
  status=$?
  set -e
  if [[ ${status} -ne 0 ]]; then
    echo "[typecheck] failed (exit ${status})" >&2
    exit "${status}"
  fi
  echo "[typecheck] success"
  exit 0
fi

if [[ -f "package.json" ]] && command -v npm >/dev/null 2>&1 && npm run -s | grep -q "^  typecheck$"; then
  echo "[typecheck] running: npm run -s typecheck"
  npm run -s typecheck
  echo "[typecheck] completed"
  exit 0
fi

echo "[typecheck] skipped: no typecheck configured yet"
echo "[typecheck] TODO: set SKILL_TYPECHECK_CMD or add a package script"
exit 0
