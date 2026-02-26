# Release Runbook

Purpose: describe how changes move from completed work to a recoverable release.

## 1) Prepare
- Confirm scope and status in active execution plan.
- Check invariants and quality score.
- Ensure unresolved risk items are visible.

## 2) Version
- Versioning strategy: `TODO(template): choose SemVer or date-based`.
- Tag/label command: `TODO(template): add command`.
- Release notes location: `TODO(template): add path`.

## 3) Ship
- Build command: `TODO(template): add command`.
- Validation command: `TODO(template): add command`.
- Deploy command: `TODO(template): add command`.

## 4) Verify Post-Release
- Health check method: `TODO(template): define method`.
- Observability checks: `TODO(template): define checks`.
- Record outcome in plan and archive.

## 5) Rollback
- Trigger conditions for rollback: `TODO(template): define conditions`.
- Rollback command/process: `TODO(template): define process`.
- Post-rollback validation: `TODO(template): define validation`.

## Required Records
- Link to plan in `docs/exec-plans/completed/`.
- Link to key risk/debt updates in [`docs/tech-debt-tracker.md`](/Users/hyeonseok/Projects/harness-lab/docs/tech-debt-tracker.md).
