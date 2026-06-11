---
name: git-workflow
description: Use for branch strategy, isolated worktrees, commits, PR preparation, merge/rebase decisions, conflict handling, tags, and release-oriented Git hygiene.
---

# Git workflow

Use this workflow when the task involves non-trivial Git state, branch management, PR preparation, merge strategy, or release history.

## Steps

1. Inspect state first.
   - `git status --short`
   - Current branch
   - Remotes
   - Worktree/linked worktree status
   - Diff and untracked files

2. Preserve user work.
   - Do not reset or checkout away changes that you did not make.
   - Separate unrelated changes from the current task.
   - Use isolated branches or worktrees for risky work when possible.

3. Choose the operation.
   - Commit local changes
   - Prepare PR diff
   - Rebase or merge
   - Resolve conflict
   - Tag release
   - Audit branch usefulness

4. Validate history and diff.
   - Check staged files.
   - Check `git diff --check`.
   - Read the final diff before commit.
   - Confirm remote state when push/PR is requested.

5. Communicate exact boundaries.
   - Local commit only
   - Pushed branch
   - PR opened/updated
   - Checks passed/pending/failed
   - Mergeability status

## Output

Return:

1. Git operation performed or recommended
2. Branch and commit details
3. Files included
4. Validation
5. Remaining remote or review state

## Do not

- Do not use destructive commands without explicit instruction.
- Do not mix unrelated diffs into a commit.
- Do not claim a push, PR, or check result without reading it back.
