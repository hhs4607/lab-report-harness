# Local Debugging Runbook

Purpose: provide a predictable way to diagnose issues locally without stack assumptions.

## 1) Triage
- Confirm expected behavior vs actual behavior.
- Capture exact error text and reproduction steps.
- Check recent changes in docs/plans before code deep dive.

## 2) Minimal Reproduction
- Create the smallest repeatable case.
- Record inputs, outputs, and environment notes.
- If command is unknown, write `TODO(template): <command>` explicitly.

## 3) Inspect
- Validate assumptions against:
  - [`ARCHITECTURE.md`](/Users/hyeonseok/Projects/harness-lab/ARCHITECTURE.md)
  - [`docs/quality/invariants.md`](/Users/hyeonseok/Projects/harness-lab/docs/quality/invariants.md)
- Review active execution plan for scope drift.

## 4) Fix
- Apply the smallest reversible change.
- Update related docs/runbooks if behavior changed.
- Add follow-up items to [`docs/tech-debt-tracker.md`](/Users/hyeonseok/Projects/harness-lab/docs/tech-debt-tracker.md) when needed.

## 5) Verify
- Re-run reproduction steps.
- Re-check invariants and quality rubric.
- Archive findings in the active plan.

## Command Placeholders
- Start app/service: `TODO(template): add command`
- Run tests: `TODO(template): add command`
- Run lint/static checks: `TODO(template): add command`
