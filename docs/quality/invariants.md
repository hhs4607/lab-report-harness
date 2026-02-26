# Mechanical Invariants

These are hard checks or expected conditions that should hold at all times unless explicitly waived.

## Repository Invariants
- `AGENTS.md` remains a concise map/TOC.
- `docs/index.md` exists and links to primary records.
- Execution plans are tracked under `docs/exec-plans/`.
- Completed work is archived to `docs/exec-plans/completed/`.

## Change Invariants
- Changes should be small and reversible.
- Significant decisions are documented in `docs/`.
- Template placeholders must use `TODO(template): ...`.
- Plain `TODO:` is reserved for real unfinished work and should be zero in template docs.
- Real unfinished work must be tracked in `docs/tech-debt-tracker.md`.

## Quality Invariants
- No contradictory guidance across core docs.
- Runbooks describe at least one local path for debugging and release.
- Open gaps are listed in `docs/tech-debt-tracker.md`.
- `./skills/typecheck.sh` must pass for Python harness changes.
- `./skills/doc_check.sh` must pass.
- Relative markdown links in `docs/**/*.md` must resolve to existing files.
- `TODO` count in `docs/` must not exceed `HARNESS_TODO_BUDGET` (default: `999`).

## Automation Invariants
- If a manual workflow is repeated, add or update a script/skill (`TODO(template): define exact threshold`).
- CI checks should eventually enforce the highest-value invariants (`TODO(template): prioritize checks`).

## Waiver Policy
- Temporary exceptions must include:
  - Reason
  - Owner
  - Expiry/review date (`TODO(template): define date format standard`)
