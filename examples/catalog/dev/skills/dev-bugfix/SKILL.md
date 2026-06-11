---
name: dev-bugfix
description: Use for software bug fixes that need reproduction, root-cause analysis, minimal implementation, and validation.
---

# Bugfix workflow

Use this workflow when the task is to find and fix a defect in code.

## Steps

1. Define the observed failure.
   - Error message
   - Reproduction steps
   - Affected file, feature, endpoint, CLI command, or behavior

2. Explore before editing.
   - Map likely files and execution paths.
   - Identify existing tests.
   - Identify smallest validation command.

3. Reproduce or establish a validation path.
   - Run the smallest relevant test/check first.
   - If reproduction is impossible, state why and choose the closest validation.

4. Implement the smallest defensible fix.
   - Avoid unrelated changes.
   - Preserve public contracts unless explicitly asked.
   - Add or update tests when behavior changes.

5. Validate.
   - Run the smallest relevant checks.
   - Escalate to broader checks only if needed.

## Output

Return:

1. Root cause
2. Fix summary
3. Files changed
4. Tests or checks run
5. Residual risks

## Do not

- Do not rewrite architecture unless required.
- Do not weaken tests to make them pass.
- Do not hide failing or inconclusive validation.
- Do not modify unrelated files.
