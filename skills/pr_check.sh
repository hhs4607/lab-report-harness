#!/usr/bin/env bash
set -euo pipefail

echo "[pr_check] starting full local quality gate"

scripts=(
  "./skills/bootstrap.sh"
  "./skills/format.sh"
  "./skills/lint.sh"
  "./skills/typecheck.sh"
  "./skills/test.sh"
  "./skills/doc_check.sh"
)

for script in "${scripts[@]}"; do
  if [[ ! -x "${script}" ]]; then
    echo "[pr_check] error: ${script} is not executable" >&2
    exit 1
  fi

  echo "[pr_check] running ${script}"
  "${script}"
done

echo "[pr_check] all checks finished"

