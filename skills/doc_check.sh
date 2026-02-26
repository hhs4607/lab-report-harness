#!/usr/bin/env bash
set -euo pipefail

echo "[doc_check] starting"

if [[ ! -f "docs/index.md" ]]; then
  echo "[doc_check] error: docs/index.md is required" >&2
  exit 1
fi

echo "[doc_check] policy: fix-me markers are not allowed in tracked docs/scripts"
needle="FIX""ME"
if grep -R -n --include="*.md" --include="*.sh" --exclude="doc_check.sh" "${needle}" docs skills AGENTS.md ARCHITECTURE.md >/tmp/doc_check_fixme.txt; then
  echo "[doc_check] error: found forbidden fix-me entries:" >&2
  cat /tmp/doc_check_fixme.txt >&2
  exit 1
fi

todo_count="$(grep -R -n --include="*.md" --include="*.sh" "TODO" docs skills AGENTS.md ARCHITECTURE.md | wc -l | tr -d ' ')"
todo_budget="${HARNESS_TODO_BUDGET:-0}"
template_todo_budget="${HARNESS_TEMPLATE_TODO_BUDGET:-999}"
todo_report="$(python skills/count_doc_todos.py docs)"
docs_total_markers="$(printf '%s\n' "${todo_report}" | awk -F= '/^docs_total_markers=/{print $2}')"
docs_template_markers="$(printf '%s\n' "${todo_report}" | awk -F= '/^docs_template_markers=/{print $2}')"
docs_real_markers="$(printf '%s\n' "${todo_report}" | awk -F= '/^docs_real_markers=/{print $2}')"

echo "[doc_check] TODO count (all tracked docs/scripts): ${todo_count}"
echo "[doc_check] TODO breakdown (docs): total_markers=${docs_total_markers}, template_markers=${docs_template_markers}, real_markers=${docs_real_markers}"
echo "[doc_check] TODO budgets: real_markers=${docs_real_markers}/${todo_budget}, template_markers=${docs_template_markers}/${template_todo_budget}"

if (( docs_real_markers > todo_budget )); then
  echo "[doc_check] error: real docs TODO marker count ${docs_real_markers} exceeds HARNESS_TODO_BUDGET=${todo_budget}" >&2
  exit 1
fi

if (( docs_template_markers > template_todo_budget )); then
  echo "[doc_check] error: template docs TODO marker count ${docs_template_markers} exceeds HARNESS_TEMPLATE_TODO_BUDGET=${template_todo_budget}" >&2
  exit 1
fi

echo "[doc_check] checking markdown relative links under docs/"
python skills/check_md_links.py

echo "[doc_check] completed"
