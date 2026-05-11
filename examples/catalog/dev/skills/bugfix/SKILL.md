---
name: bugfix
description: Use when the user wants to diagnose and fix a software defect, failing test, regression, or broken CLI/API behavior.
---

# Bugfix

## Workflow

1. Reproduce or localize the defect from logs, tests, or user-provided steps.
2. Identify the smallest code path that explains the behavior.
3. Inspect surrounding conventions before editing.
4. Patch the root cause, not only the visible symptom.
5. Add or update the narrowest meaningful test when practical.
6. Run a verification command and report any gap.

## Guardrails

- Do not overwrite unrelated local changes.
- Do not introduce a new abstraction unless it reduces real complexity.
- Do not claim a fix is verified without a command, test, or direct observation.

## Output

Report:

- Root cause.
- Files changed.
- Verification run.
- Remaining risk, if any.
