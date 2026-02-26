---
name: pr-check
description: Run ./skills/pr_check.sh, summarize failures, and propose practical fixes in priority order.
---

# Skill: pr-check

## When to use
- The user asks to validate repo readiness before PR/merge.
- The user asks for a single-command quality gate run.
- CI failed and local reproduction is needed.

## When not to use
- The user only wants a docs-only review without running checks.
- The repository has no `skills/pr_check.sh` and user asks not to create tooling.

## Steps
1. Verify `skills/pr_check.sh` exists and is executable.
2. Run:
   - `./skills/pr_check.sh`
3. If it fails:
   - Capture failing step(s)
   - Extract first actionable error(s)
   - Propose minimal fixes with file references
4. If it passes:
   - Report success and any skipped checks/TODO markers.

## Evidence format
- `Commands run:` list each command in backticks.
- `Key output:` include pass/fail and first actionable error lines.
- `Assessment:` include probable cause and prioritized fix list.
