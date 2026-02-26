# Quality Score

Use this lightweight rubric to evaluate readiness of major changes.

## Rubric (0-2 each, total 10)
- Documentation clarity:
  - `0` missing/outdated docs
  - `1` partial docs
  - `2` clear, linked, current docs
- Mechanical compliance:
  - `0` invariants ignored
  - `1` partial compliance
  - `2` full compliance or documented waiver
- Operational readiness:
  - `0` no runbook updates
  - `1` runbook unclear/incomplete
  - `2` runbook updated with actionable steps
- Risk visibility:
  - `0` risks not tracked
  - `1` some risks tracked
  - `2` risks and debt logged with owners/TODOs
- Reproducibility:
  - `0` work cannot be repeated
  - `1` repeatability depends on memory
  - `2` repeatable via docs/scripts/skills

## Suggested Thresholds
- `9-10`: Ready to ship
- `7-8`: Ship with tracked follow-ups
- `<=6`: Improve before release

## Baseline Quality Gates
For Python harness changes, the expected local and CI quality gates are:
- `./skills/format.sh`
- `./skills/lint.sh`
- `./skills/typecheck.sh`
- `./skills/test.sh`
- `./skills/doc_check.sh`

`./skills/doc_check.sh` now enforces:
- `TODO` budget in `docs/` via `HARNESS_TODO_BUDGET` (default `999`)
- Relative markdown link validation for `docs/**/*.md`

## Open Work Tracking
Open quality-system follow-ups are tracked in [`docs/tech-debt-tracker.md`](/Users/hyeonseok/Projects/harness-lab/docs/tech-debt-tracker.md).
