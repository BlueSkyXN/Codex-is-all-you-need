# Handoff method

Shared by `sdlc-handoff` and `sdlc-solve`. Location, status, and reachability
rules are in [the shared conventions](../../sdlc-solve/references/conventions.md).

## Collect the state

From the conversation, the task file, and the repository:

- goal, scope, delivery point, and authorization;
- current requirements and decisions, with superseded ones marked;
- code state: repository, branch, commit, uncommitted changes, and new
  untracked files;
- progress and evidence pointers, including what was tried and failed;
- the first next step, dependencies, blockers, and open decisions with who
  decides;
- external state: PRs, CI runs, deployments, and tickets, with links.

## Write it down

Create or update the task file from
[the template](../../sdlc-solve/assets/task-template.md). Set the status to
`paused` when work stops waiting for something, or `in-progress` when the
receiver should continue at once. Replace conversational references such as
"as discussed above" with the actual content.

## Make it reachable

- **Same workspace:** the task file path and the branch name are enough.
- **Another workspace or machine:** the receiver needs the commit, the
  uncommitted changes, and the new files. Use a transfer the authorization
  allows: a pushed branch, a patch file beside the task file, or a copy of the
  files. A commit hash alone does not carry uncommitted work.
- **External links:** confirm the receiver can open them; note any that are
  private or local.

## Receiver test

Read the result as someone who never saw the conversation:

1. Can they state the goal and the delivery point?
2. Is the first next step concrete enough to start without asking?
3. Can they reach the code state the file describes?

Revise the file until all three hold.

## Done

The task file is written, the code state is reachable or the gap is named, and
the receiver test passes.
