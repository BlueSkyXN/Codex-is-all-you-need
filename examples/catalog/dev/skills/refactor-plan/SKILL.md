---
name: refactor-plan
description: Use for planning software refactors before editing files, especially when behavior must be preserved.
---

# Refactor plan workflow

Use this workflow when the task is to refactor code while preserving behavior.

## Steps

1. State the refactor goal.
   - What should improve?
   - What behavior must remain unchanged?

2. Map current structure.
   - Relevant files and modules
   - Entry points and call paths
   - Tests and validation commands

3. Identify contracts.
   - Public APIs
   - CLI behavior
   - Database schema
   - External integrations
   - User-visible behavior

4. Propose an incremental plan.
   - Step 1
   - Step 2
   - Step 3
   - Validation after each step

5. Define rollback and stop conditions.

## Output

Return:

1. Current structure
2. Behavior contracts
3. Proposed plan
4. Validation strategy
5. Risks and stop conditions

## Do not

- Do not edit files before the plan is clear.
- Do not combine unrelated refactors.
- Do not change public behavior unless explicitly requested.
