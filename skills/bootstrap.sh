#!/usr/bin/env bash
set -euo pipefail

echo "[bootstrap] starting environment bootstrap"
echo "[bootstrap] repository root: $(pwd)"

if [[ -f "package.json" ]]; then
  echo "[bootstrap] detected Node project markers"
  echo "[bootstrap] TODO: define Node package manager and install command"
fi

if [[ -f "pyproject.toml" || -f "requirements.txt" ]]; then
  echo "[bootstrap] detected Python project markers"
  echo "[bootstrap] TODO: define Python environment and dependency install command"
fi

if [[ ! -f "package.json" && ! -f "pyproject.toml" && ! -f "requirements.txt" ]]; then
  echo "[bootstrap] no stack markers detected yet"
  echo "[bootstrap] TODO: choose stack and update this script"
fi

echo "[bootstrap] completed (no-op until stack is configured)"

