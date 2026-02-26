---
name: doc-gardener
description: Run ./skills/doc_check.sh, then propose focused documentation improvements for stale TODOs, missing links, and unclear runbooks.
---

# Skill: doc-gardener

## When to use
- The user asks to improve doc quality or hygiene.
- The user asks to audit TODO-heavy docs.
- The user asks to review runbooks for clarity and completeness.

## When not to use
- The user requests only code fixes unrelated to docs.
- The user explicitly asks to skip documentation work.

## Steps
1. Verify `skills/doc_check.sh` exists and is executable.
2. Run:
   - `./skills/doc_check.sh`
3. Review docs for:
   - Stale `TODO` items lacking owner/next step
   - Missing or inconsistent internal links
   - Runbooks with unclear “how to run” sections
4. Propose smallest useful doc edits first; avoid broad rewrites.

## Evidence format
- `Commands run:` list each command in backticks.
- `Key output:` include doc check results and representative finding lines.
- `Recommendations:` separate required fixes from optional improvements, with file references.
