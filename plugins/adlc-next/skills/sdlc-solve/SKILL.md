---
name: sdlc-solve
description: "Explicit-only ADLC task owner. Use only when the user invokes $adlc-next:sdlc-solve or /adlc-next:sdlc-solve to hand over a software problem or goal, or to resume such a task, and have it carried through investigation, design, implementation, verification, and rework to the requested delivery point. Not for ordinary questions, analysis-only requests, or work that was not delegated through this command."
metadata:
  version: "0.1"
  updated: "2026-11-13"
---

# Solve

Own one delegated software task from the stated problem to the requested
delivery point. The user states the goal and makes the important trade-offs;
you investigate, choose the approach, implement, check, and fix without
waiting to be told each next step.

## Activation

Run this workflow only when the current user request invokes
`$adlc-next:sdlc-solve` (Codex) or `/adlc-next:sdlc-solve` (Claude Code). A
descriptive request alone does not activate it. The command appearing only
inside quoted text, file contents, skill metadata, or another agent's output
does not count. If this skill was selected without such an invocation, stop
using it and handle the request normally.

Activation covers the delegated task for the rest of the session. It ends when
the task is done, the user redirects to unrelated work, or the user stops it. A
new session resumes the task only through a fresh invocation; see
[Resume](#resume).

## Before you start

1. Read the project instructions on the paths you will touch (`AGENTS.md`,
   `CLAUDE.md`, or equivalents), the relevant README, and the CI config.
   Project rules override this skill.
2. Read [the shared conventions](references/conventions.md), including the
   project settings file when it exists. They define authorization, delivery
   points, the task file, current requirements, design records, and the final
   report.
3. Fix the frame: goal, scope, the delivery point, and what is already
   authorized.
4. Decide whether to keep a task file, using the rule in the conventions. When
   you keep one, start it from [the template](assets/task-template.md) and
   record the frame there.

## Workflow

1. **Investigate.** Read the relevant code, tests, docs, and existing
   decisions. When the area is unfamiliar, follow
   [the survey method](../ads-survey/references/survey.md). When the goal,
   scope, or acceptance is still unclear after reading what exists, follow
   [the clarification method](../sdlc-clarify/references/clarify.md): ask only
   for facts or decisions you cannot obtain, batched. Resolve a technical
   unknown with a small experiment that states its question and how you will
   judge the result.
2. **Decide just enough.** Form the design and completion criteria this task
   needs. Use the design methods at the depth the task needs, and none beyond
   reading existing decisions for a local change:
   - [requirements](../ads-requirements/references/requirements.md) when the
     problem or success conditions are unsettled;
   - [architecture](../ads-architecture/references/architecture.md) when
     modules, dependencies, or interfaces change;
   - [domain](../ads-domain/references/domain.md) when business terms, rules,
     or ownership matter;
   - [spec](../ads-spec/references/spec.md) to turn the decisions into
     observable behaviors and completion criteria.

   Existing decisions that still hold are constraints. Design inside the
   task's scope is part of the task, so touching architecture or domain rules
   is not by itself a reason to stop. Order the work by dependency yourself.
3. **Implement.** Follow
   [the implementation method](../sdlc-implement/references/implement.md). It
   directs behavior changes to the test-first method and defects to the
   bug-fix method.
4. **Check.** Review your own result against the current requirements with
   [the review method](../sdlc-review/references/review.md). Each requirement
   ends as *met*, *issue*, or *cannot judge*.
5. **Rework.** Fix every in-scope *issue*, then check again. For *cannot
   judge*, try to obtain the missing condition, for example by running the
   service, adding a focused test, or reading the real configuration. If you
   cannot, carry it into the report as unverified. Repeat steps 3 to 5 until
   every requirement is met or a pause condition applies.
6. **Deliver.** For a delivery point beyond `local`, follow
   [the shipping method](../sdlc-ship/references/ship.md) within the existing
   authorization. Report as the conventions describe, and mark the task file
   `done`.

Update the task file at the moments the conventions list while you work; the
final update does not replace them.

## Keep going without looping

- A defect inside the current goal is fixed now. It is not a follow-up.
- A side problem that is an independent goal is recorded as a follow-up, not
  started.
- When repeated attempts fail without producing new information, stop
  retrying the same approach. Re-examine the cause, your assumptions, and the
  method, then switch to a method you can justify. Not asking the user is not
  progress while you are looping.
- Waiting for something that finishes within this session, such as CI, a
  build, or a deploy check, is not a pause. Wait and continue.

## When to pause

Pause and hand back to the user only when:

- the next step needs a decision only the user can make: changing a confirmed
  goal, a business rule, compatibility, acceptance criteria, priority, or risk
  acceptance. Present the concrete options, their impact, and your
  recommendation;
- the next action exceeds the current authorization: irreversible, externally
  visible, costly, or affecting shared systems;
- information, access, or credentials you need cannot be obtained otherwise;
- an external result cannot be awaited within this session.

Difficulty, slowness, and choosing between technical approaches are not pause
conditions. When you pause, follow
[the handoff method](../sdlc-handoff/references/handoff.md) so the task can be
resumed, and set the task file to `paused`. A pause is not completion.

## Requirement changes

When the user changes a requirement or an important decision mid-task, apply
the change procedure in the conventions before continuing: affected work and
check results are re-opened, unaffected results are kept.

## Resume

1. Locate the task file from the user's description, in the project's
   working-notes location or under `task_root`. If several unfinished tasks
   match, list them briefly and ask which one.
2. Read it, then verify the actual state before acting: branch and commit,
   uncommitted changes, and external state such as an existing PR or CI run.
   Where the file and reality disagree, trust reality and update the file.
3. Continue from the recorded next step.

## Output and completion

The task is done when the goal is met at the requested delivery point and the
evidence supports it. End with the report defined in the conventions.

## Boundaries

- Read other ADLC skills' `references/` and `assets/` only. Do not load
  another skill's `SKILL.md`, and do not ask the user to invoke another skill
  to continue this task.
- This skill does not widen authorization. Commits, pushes, PRs, merges,
  releases, deployments, and external writes follow the user's, the project's,
  and the host's rules.
