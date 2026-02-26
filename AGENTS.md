# AGENTS.md

## Mission
Build and operate a harness-engineering style repository that is:
- Agent-first
- Repo-local and versioned
- Mechanically verifiable
- Easy for new contributors to navigate quickly

If it matters, encode it into `docs/`, `skills/`, or CI.

## Operating Loop
1. Read `AGENTS.md` and `docs/index.md`.
2. Pick or open an execution plan in `docs/exec-plans/active/`.
3. Make small, reversible changes with explicit assumptions.
4. Validate against quality invariants in `docs/quality/invariants.md`.
5. Record decisions and operational updates in docs before closing work.
6. Archive completed plans to `docs/exec-plans/completed/`.

## Where To Look First
- Entry point: [`docs/index.md`](/Users/hyeonseok/Projects/harness-lab/docs/index.md)
- Architecture: [`ARCHITECTURE.md`](/Users/hyeonseok/Projects/harness-lab/ARCHITECTURE.md)
- Core beliefs: [`docs/core-beliefs.md`](/Users/hyeonseok/Projects/harness-lab/docs/core-beliefs.md)
- Quality rules: [`docs/quality/invariants.md`](/Users/hyeonseok/Projects/harness-lab/docs/quality/invariants.md)
- Quality scoring: [`docs/quality/quality-score.md`](/Users/hyeonseok/Projects/harness-lab/docs/quality/quality-score.md)
- Debug runbook: [`docs/runbooks/debugging.md`](/Users/hyeonseok/Projects/harness-lab/docs/runbooks/debugging.md)
- Bootstrap runbook: [`docs/runbooks/bootstrap.md`](/Users/hyeonseok/Projects/harness-lab/docs/runbooks/bootstrap.md)
- Release runbook: [`docs/runbooks/release.md`](/Users/hyeonseok/Projects/harness-lab/docs/runbooks/release.md)
- Active plans template: [`docs/exec-plans/active/_TEMPLATE.md`](/Users/hyeonseok/Projects/harness-lab/docs/exec-plans/active/_TEMPLATE.md)
- Completed plans guide: [`docs/exec-plans/completed/README.md`](/Users/hyeonseok/Projects/harness-lab/docs/exec-plans/completed/README.md)
- Debt tracker: [`docs/tech-debt-tracker.md`](/Users/hyeonseok/Projects/harness-lab/docs/tech-debt-tracker.md)

## Decision Policy
- Prefer explicit docs over chat-only decisions.
- Prefer checkable rules over vague standards.
- Prefer automation over manual repetition.
- Prefer reversible changes over broad rewrites.

## Documentation Rules
- `AGENTS.md` is a map/TOC, not a full manual.
- `docs/` is the system of record.
- Keep pages concise and link outward instead of duplicating text.
- Mark unknown tools/commands as `TODO` instead of guessing.

## Change Checklist
Before finishing, confirm:
- Relevant docs are updated.
- Invariants are still satisfied.
- Open risks are tracked in `docs/tech-debt-tracker.md`.
- Execution plan status is current.
