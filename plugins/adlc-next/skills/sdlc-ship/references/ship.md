# Shipping method

Shared by `sdlc-ship` and `sdlc-solve`. Each stage runs only when it is
requested and authorized as described in
[the shared conventions](../../sdlc-solve/references/conventions.md), and each
stage needs its own evidence.

## Before any stage

- The change is verified locally; re-run the checks when the code changed
  since the last run.
- Read the project's contribution, branching, commit, PR, release, and
  deployment rules. They decide naming, message language, and process.

## Commit

- Stage only this task's files, path by path. Leave the user's other changes,
  the task file, and local evidence out.
- Check the staged diff for whitespace errors, secrets, and debug leftovers.
- Write the message in the project's convention: what changed and why.

## Pull request

- When on the default branch, create a branch first.
- Push the branch and open the PR against the intended base.
- Write the title and body in the project's convention: purpose, what
  changed, how it was verified with the actual results, what is not verified,
  risks, and the linked issue or task.
- Reviewers, labels, and draft status follow the project's rules.

## CI

Wait for the checks and read their results. Failures this change caused go
back to implementation. Failures that predate the change, or flaky ones, are
reported with evidence; do not hide them or retry them blindly.

## Merge

Merge only when authorized, respecting required reviews, checks, and the
project's merge method. Confirm the merge landed on the base branch.

## Release or deployment

Follow the project's documented process. Record the version, artifact, or
image identifier, and read the deployed state back from the target
environment.

## Verification in the real environment

Check that the user's original problem is gone where it occurred: the
scenario itself, health checks, logs, or metrics. A successful deployment
alone does not show this.

## Report

For each stage reached, what was done and its evidence. Name the stage where
work stopped and why.
