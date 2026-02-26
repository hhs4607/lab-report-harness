---
name: create-exec-plan
description: Create a new execution plan in docs/exec-plans/active/ from the repo template and collect required inputs from the user.
---

# Skill: create-exec-plan

## When to use
- The user asks to start a new implementation effort.
- The user asks to open/create a plan before coding.
- Work requires explicit scope, acceptance criteria, and tracked steps.

## When not to use
- The user asks for a tiny one-off change that does not need planning.
- A suitable active plan already exists and only needs updates.
- The user explicitly asks to skip planning.

## Steps
1. Confirm template exists at `docs/exec-plans/active/_TEMPLATE.md`.
2. Ask for plan title, acceptance criteria, and scope (in-scope / out-of-scope).
3. Create new file at:
   - `docs/exec-plans/active/YYYY-MM-DD-<kebab-title>.md`
4. Copy template structure and fill known fields:
   - `Title`
   - `Objective`
   - `Scope`
   - `Validation` acceptance criteria
5. Keep unknowns explicit as `TODO`.
6. Return created file path and a short summary.

## Evidence format
- `Commands run:` list each command in backticks.
- `Key output:` include only the decisive lines (file created path, validation status, TODO markers).
- `Result:` include the created file path and a one-line completion summary.
