# Execution Plan: CI, Typecheck, and Doc Check Hardening

## Metadata
- Plan ID: `EP-20260226-ci-typecheck-doccheck`
- Title: CI green + typecheck enabled + doc_check strengthened
- Owner: `agent`
- Status: `active`
- Created: `2026-02-26`
- Target completion: `2026-02-26`

## Objective
Deliver a harness template where CI and local checks are aligned, Python typechecking is enabled and enforced in the skill pipeline, and documentation checks are mechanically meaningful.

## Goal
CI green + typecheck enabled + doc_check strengthened.

## Scope
- In scope:
  - CI parity for Python harness checks using `setup-python` + `pip`.
  - Integrate `mypy` into dev dependencies and `./skills/typecheck.sh`.
  - Strengthen `./skills/doc_check.sh` with markdown relative-link validation and TODO budget enforcement.
  - Update relevant runbook and quality docs.
  - Collect reproducible command/output evidence.
- Out of scope:
  - Migrating toolchain away from current scripts.
  - Adding heavy documentation tooling dependencies.
  - Rewriting all existing docs to remove all TODOs immediately.

## Non-scope
- Add conda-based CI flow.
- Add external link checker requiring network.
- Broad architectural refactors outside CI/typecheck/doc_check.

## Assumptions
- Python runtime target is `3.11` for CI and local parity.
- Repository quality gate entrypoint remains `./skills/pr_check.sh`.
- Current docs TODO volume is temporarily acceptable if budget is explicit and enforced.

## Acceptance Criteria (testable)
- [ ] `.github/workflows/ci.yml` uses Python `3.11`, installs `requirements-dev.txt`, and runs `./skills/pr_check.sh`.
- [ ] `requirements-dev.txt` includes `mypy`.
- [ ] `mypy` config exists (`pyproject.toml` or `mypy.ini`) and `./skills/typecheck.sh` runs `python -m mypy .`.
- [ ] `./skills/doc_check.sh` runs `python skills/check_md_links.py` and fails on broken relative links in `docs/**/*.md`.
- [ ] `./skills/doc_check.sh` enforces `HARNESS_TODO_BUDGET` (default `999`) against `TODO` count in `docs/`.
- [ ] `docs/runbooks/bootstrap.md` includes typecheck and conda reproducibility path via `environment.yml`.
- [ ] `docs/quality/invariants.md` and `docs/quality/quality-score.md` document the new doc gate behavior.
- [ ] Local command `./skills/pr_check.sh` exits `0` in the target environment.

## Plan Phases

### Phase 1: Baseline & repo scan
- Capture current CI workflow, skill scripts, and docs quality rules.
- Measure current docs TODO count and note baseline value.
- Identify existing placeholders vs enforceable checks.

### Phase 2: CI parity
- Update CI to:
  - setup Python 3.11
  - install dev dependencies from `requirements-dev.txt`
  - run `./skills/pr_check.sh`
- Keep workflow changes minimal and add pip cache when straightforward.

### Phase 3: Typecheck (mypy)
- Add `mypy` to `requirements-dev.txt`.
- Add minimal `mypy` configuration targeting currently typed surface.
- Update `./skills/typecheck.sh` to run `python -m mypy .`.
- Confirm inclusion in `./skills/pr_check.sh` flow.

### Phase 4: Doc checks
- Add lightweight link checker at `skills/check_md_links.py`.
- Validate relative markdown links under `docs/**/*.md`.
- Update `./skills/doc_check.sh` to execute the checker.
- Add TODO budget gate using `HARNESS_TODO_BUDGET` with default `999`.

### Phase 5: Clean up TODOs or track debt
- Reduce docs TODOs where low-effort and high-value.
- For remaining TODOs, ensure they are visible and actionable in `docs/tech-debt-tracker.md`.
- Keep budget realistic while enabling gradual tightening.

### Phase 6: Validation (local + CI)
- Validate locally with `./skills/pr_check.sh`.
- Validate negative path examples (e.g., strict TODO budget failure).
- Confirm CI config and docs reflect actual behavior.

## Validation
- Invariants to check:
  - `docs/index.md` exists
  - `./skills/doc_check.sh` passes under default budget
  - relative doc links resolve
  - TODO budget policy is enforceable
- Quality score target:
  - `>=9/10`
- Evidence to collect (commands + outputs):
  - `python -V`
  - `python -m pip install -r requirements-dev.txt`
  - `python -m mypy --version`
  - `./skills/typecheck.sh`
  - `./skills/doc_check.sh`
  - `HARNESS_TODO_BUDGET=0 ./skills/doc_check.sh`
  - `./skills/pr_check.sh`
  - `git status --short`

## Evidence Log
- Record command, exit code, and key output excerpts for each validation command.
- Include at least one failure-mode example showing the doc TODO budget gate.

## Risks and Mitigations
- Risk: New checks create friction from pre-existing TODO volume.
  - Mitigation: Start with default budget `999`, then ratchet down intentionally.
- Risk: Mypy introduces false positives on untyped legacy code.
  - Mitigation: Start with minimal config scope and expand coverage incrementally.
- Risk: CI/local drift returns over time.
  - Mitigation: Keep `./skills/pr_check.sh` as single CI entrypoint.

## Decision Log
- Date: `2026-02-26`
  - Decision: Use lightweight custom markdown relative-link checker without heavy dependencies.
  - Rationale: Fast, deterministic, and sufficient for current invariants.
- Date: `2026-02-26`
  - Decision: Enforce docs TODO budget via environment variable.
  - Rationale: Enables gradual tightening while making policy checkable.

## Completion
- Outcome summary:
  - CI/local parity established; typecheck and doc gates are enforceable and documented.
- Follow-ups:
  - Gradually lower `HARNESS_TODO_BUDGET`.
  - Extend mypy coverage beyond current minimal scope.
- Archive location in `docs/exec-plans/completed/`:
  - `docs/exec-plans/completed/ci-typecheck-doccheck.md`
