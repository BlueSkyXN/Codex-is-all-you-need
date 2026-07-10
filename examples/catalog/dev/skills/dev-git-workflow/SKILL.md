---
name: dev-git-workflow
description: Use for branch strategy, worktrees, commits, opening or updating PRs, reviewer-facing PR titles and bodies, merge/rebase decisions, conflicts, tags, and release notes.
---

# Git workflow

Use this workflow when the task involves non-trivial Git state, branch management,
reviewer-facing PR preparation, merge strategy, or release history.

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
   - Draft, create, or update PR title and body
   - Rebase or merge
   - Resolve conflict
   - Tag release
   - Audit branch usefulness

4. Validate history and diff.
   - Check staged files.
   - Check `git diff --check`.
   - Read the final diff before commit.
   - Resolve the intended base and head branches.
   - Read the full base-to-head diff and commit range before describing a PR.

5. Prepare PR metadata when opening, updating, or rewriting a PR.
   - Read `references/pr-metadata-contract.md` completely before drafting the
     title or body.
   - Derive the copy from the current full diff, user goal, repository guidance,
     validation evidence, and delivery state.
   - Select the language using the contract, and apply it to both the title's
     descriptive text and the body. An English commit subject is not a repository
     language requirement.
   - Use an explicit title and body. Treat auto-filled metadata as a draft that
     must still pass the contract.
   - If the user only asks for a draft, return the draft without writing remote
     state.

6. Publish and read back remote state when requested.
   - Use the available GitHub connector or CLI after the branch is pushed.
   - Re-read the remote title, body, base, head, draft/state, mergeability, and
     checks after creation or update.
   - Compare the remote copy with the current head and the metadata contract;
     repair stale or unclear copy before declaring the PR complete.

7. Communicate exact boundaries.
   - Local commit only
   - Pushed branch
   - PR opened or updated against a base branch
   - Draft or ready for review
   - Merged or not merged
   - Checks passed/pending/failed
   - Released or deployed
   - Mergeability status

## Output

Return:

1. Git operation performed or recommended
2. Branch and commit details
3. Files included
4. PR title/body or remote PR URL when in scope
5. Validation
6. Remaining remote, review, release, or runtime state

## Do not

- Do not use destructive commands without explicit instruction.
- Do not mix unrelated diffs into a commit.
- Do not reuse a commit subject as final PR metadata without checking the full diff.
- Do not describe an open PR against `main` as already merged or submitted into
  `main`.
- Do not expose memory citations, agent process notes, private local paths,
  temporary files, or internal session links in PR-facing copy.
- Do not claim a push, PR, or check result without reading it back.
