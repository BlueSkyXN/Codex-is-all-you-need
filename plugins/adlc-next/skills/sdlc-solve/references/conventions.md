# ADLC shared conventions

These rules apply to `sdlc-solve`, `sdlc-implement`, and `sdlc-review`. Read
them at the start of a run. Project instructions and host settings take
precedence when they are stricter or more specific.

## Authorization

- Invoking an ADLC skill delegates reading the workspace, investigating,
  editing locally within the task's scope, and running local checks and
  builds.
- Everything else follows the authorization already given by the user's
  request, the project instructions, and the host settings: commits, pushes,
  PRs, merges, releases, deployments, deleting or overwriting existing content,
  external messages, spending, and credential or permission changes. Do not
  ask again for something already authorized. Before an action beyond it, name
  the action and its impact.
- Protect existing work. In a Git repository, run `git status` before
  editing. Treat uncommitted changes, stashes, and untracked files as the
  user's unless the task file records them as this task's. Do not reset,
  clean, stash, or overwrite them. Outside Git, do not overwrite files you
  have not read.

## Delivery points

The delivery point is where work stops for this request. Use the one the user
asked for:

1. local change verified
2. committed
3. PR opened
4. PR merged
5. released or deployed
6. verified in the real environment

Report the point actually reached. Each stage needs its own evidence: a local
check does not show that CI passed, a merge does not show a deployment, and a
deployment does not show that the user's problem is gone. A delivery method
not exercised in this task is reported as unverified.

## Task file

### When to keep one

Keep a task file when the task may span sessions, may be handed to another
agent or person, waits on external results, or has several stages. Short work
finished within one session needs none; create one later if the task grows,
pauses, or changes hands.

### Location and form

Use the project's existing location for working notes. Otherwise use
`local/<YYYYMMDD>-<topic>/TASK.md`. A task file is working state: do not stage
or commit it unless the project tracks such files, and name its location in
the report. Write it in the language the user works in, starting from
[the template](../assets/task-template.md).

Keep evidence where it lives (code, tests, CI, PR) and point to it. Raw output
worth keeping goes in an `evidence/` folder beside the task file.

### Status

- `in-progress`: work is being carried forward.
- `paused`: waiting for a user decision, an external result such as a PR
  review, CI, or deployment, or execution was interrupted. Under "Next and
  blockers", record what is awaited, where to check it, and the first step on
  resume.
- `done`: the goal is met at the requested delivery point.

### When to update

Update the task file when an important decision changes, after a piece of
work that can be described on its own, when you hit a blocker, and before a
handoff or a stop. Record decisions, progress, and evidence pointers, not
every command. The final update records the result; it does not replace the
progress saved along the way.

## Current requirements

- New explicit requirements and decisions from the user go into the task file
  when one exists.
- The task file records what this task changes. Project documentation holds
  shared rules and established facts.
- When an independent spec exists, reference its current sections from the
  task file and add only the delivery point and execution state. Otherwise
  write the required behaviors in the task file. Keep one set of completion
  criteria.
- Implementation details may change within existing constraints, and missing
  behavior details may be filled in. Changing a confirmed goal, business rule,
  compatibility promise, or acceptance criterion needs the user's decision.
  Never lower the criteria so that the current result passes.
- Rework toward the same goal stays in the same task. An independent new goal
  becomes a follow-up.

### Change procedure

When a requirement or an important decision changes:

1. Record the new version and mark the superseded one.
2. Identify the decisions, completed work, and check results that depend on
   it.
3. Re-open the affected work and mark the affected checks for re-running.
   Earlier passing results stay as history; they no longer prove the changed
   requirement.
4. Keep unaffected results.

## Handoff

A handoff is complete only when the material is enough to understand the task
and the receiver can actually reach it together with the matching code.

- In the same workspace, point to the task file.
- Across workspaces, state the commit, the uncommitted changes, and the new
  files, and how each is transferred. A commit hash does not carry
  uncommitted work.
- Report anything that could not be transferred.

## Where findings go

| Finding | Destination |
|---|---|
| Defect inside the current goal | Fix it in the current task |
| Independent goal, later requirement, or post-delivery feedback | Follow-up in the report and task file, or the project's tracker |
| Lasting architecture, business rule, or system behavior changed by this task | Project documentation, following project rules |
| Repeated friction in how the work was done | Method-improvement note in the report |

## Report

End every run with:

- the result and the delivery point reached;
- the checks run, with commands and outcomes;
- unverified items and why they are unverified;
- deviations from the plan or requirements and why;
- follow-ups;
- the task file location and status, when one is used.
