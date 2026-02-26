# Technical Debt Tracker

Keep this lightweight. Track only actionable items.

## Status Legend
- `open`
- `in-progress`
- `resolved`

## Items
| ID | Date | Area | Debt | Impact | Owner | Status | Next Action |
|---|---|---|---|---|---|---|---|
| TD-001 | 2026-02-25 | Release | Versioning strategy not defined | Inconsistent release process | unassigned | open | Define strategy in `docs/runbooks/release.md` |
| TD-002 | 2026-02-25 | Quality | CI enforcement for invariants missing | Manual drift risk | unassigned | open | Add baseline CI checks and prioritize invariant coverage |
| TD-003 | 2026-02-25 | Debugging | Standard local commands undefined | Slow onboarding | unassigned | open | Fill command placeholders in runbooks |

## Open Debt Checklist
- [ ] Define mandatory minimum quality score by change type.
- [ ] Define who can approve quality score exceptions.
- [ ] Add CI job to compute/check quality rubric inputs where possible.
- [ ] Add templates for attaching quality rubric to plans/PRs.
