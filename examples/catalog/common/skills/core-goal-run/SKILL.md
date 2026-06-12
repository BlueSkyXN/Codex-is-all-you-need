---
name: core-goal-run
description: Use to execute or resume a local goal plan while keeping the plan read-only and updating goal-tasks.md plus goal-log.md.
---

# Goal Run

Use this skill when the user provides a local goal or plan file and asks to
track completion, continue execution, skip human-only items, or leave a handoff.

Typical source file names include:

- `goal-plan-list.md`
- `current-plan.md`
- `todo.md`
- a dated local planning Markdown file

## Purpose

Keep long-running Codex work recoverable without turning it into a workflow
platform.

The goal directory uses three plain Markdown files:

```text
<goal-dir>/
├── goal-plan-list.md  # original input, read-only reference
├── goal-tasks.md      # current task list and status truth
└── goal-log.md        # execution notes, evidence, and handoff
```

If the source file is not named `goal-plan-list.md`, keep its original name and
still create `goal-tasks.md` and `goal-log.md` beside it.

Do not create `.goal-run/`, run-id directories, scripts, hooks, registries, or
automation unless the user explicitly asks for a heavier tracker.

## File Roles

### Source Goal File

Treat the original goal file as read-only source context after
`goal-tasks.md` exists.

Do not keep updating the original goal file as the status tracker. If it
contains old status notes, treat them as historical input and reconcile the
current state into `goal-tasks.md`.

### `goal-tasks.md`

This is the current status truth. Keep it short.

It should answer:

- What tasks exist?
- What is each task's current status?
- Is the task automatic or human-only?
- Where is the evidence or note?

Use this compact structure:

```markdown
# Goal Tasks

Source: `goal-plan-list.md`
Status truth: this file.
Execution log and evidence: `goal-log.md`

Allowed status:

- TODO
- DOING
- VERIFYING
- DONE
- BLOCKED
- HUMAN_PENDING
- SKIPPED_HUMAN

| ID | Source | Task | Status | Auto | Evidence | Notes |
|---|---|---|---|---|---|---|
| T001 | goal-plan-list.md §47 | Review current state | DONE | yes | goal-log.md#t001 | current authority confirmed |
| T002 | goal-plan-list.md §8 | Implement frontend task X | DOING | yes | pending | small reversible diff |
| T003 | goal-plan-list.md §12 | Manual credential validation | SKIPPED_HUMAN | no | goal-log.md#t003 | requires credential |
```

Do not put long command output, long rationale, PR bodies, screenshots, or full
logs in `goal-tasks.md`.

### `goal-log.md`

This is the execution record, evidence index, and human handoff.

It should answer:

- What did this run do?
- What evidence supports each completed or blocked task?
- What should the next Codex or the user read first?
- What remains risky, blocked, skipped, or pending?

Use simple sections:

```markdown
# Goal Log

Source: `goal-plan-list.md`
Task status truth: `goal-tasks.md`

## YYYY-MM-DD Run

Request:

- Continue automatic tasks from `goal-plan-list.md`.
- Skip human-only work.

## T001

Status: DONE

Evidence:

- Reviewed `goal-plan-list.md`.
- Confirmed current authority and stale context boundaries.

Notes:

- Older local directories are historical only.

## Handoff

Read first:

- `goal-tasks.md`
- `goal-log.md`

Next:

- Continue T002.
- Keep T003 as `SKIPPED_HUMAN` unless the user provides credentials.
```

## Status Values

Use only these statuses unless the user explicitly asks for a different local
taxonomy:

- `TODO`: known task, not started.
- `DOING`: currently being worked.
- `VERIFYING`: implementation or artifact is ready, proof is still running or incomplete.
- `DONE`: completed with evidence in `goal-log.md`.
- `BLOCKED`: cannot continue without a concrete blocker being resolved.
- `HUMAN_PENDING`: waits for human decision, credential, approval, or external action.
- `SKIPPED_HUMAN`: intentionally skipped because it is human-only and the user asked to skip human work.

Do not invent compound statuses such as `DONE_BUT_NEEDS_CI`. Put that detail in
`Notes` or `goal-log.md`.

## Workflow

1. Read the source goal file.
2. Read nearby documents only when they are relevant to the user's request.
3. Create `goal-tasks.md` and `goal-log.md` if missing.
4. If they already exist, resume from them instead of re-deriving status from
   the source goal file.
5. Extract only actionable items. Do not turn every paragraph into a task.
6. Mark human-only tasks as `HUMAN_PENDING` or `SKIPPED_HUMAN`; do not mark them
   `DONE` unless the user actually completed the human action and evidence is
   available.
7. Keep implementation, testing, PR, CI, deploy, and review work in the
   appropriate dev or SDLC skills. Use this skill only for the tracker files.
8. After each meaningful unit of work, update `goal-tasks.md` and append concise
   evidence or handoff notes to `goal-log.md`.
9. Before stopping, ensure every `DONE` task has evidence, every `BLOCKED` task
   names the blocker, and the `Handoff` section states what to read and do next.

## Evidence Rules

Evidence can be concise. Prefer pointers over pasted output.

Good evidence:

- command and exit status
- test or build result
- changed file path
- commit SHA
- PR URL
- CI run URL or status
- deployment URL
- health or ready endpoint result
- screenshot path
- reviewed source file or source section

Do not treat `goal-tasks.md` itself as proof of completion. It is a tracker, not
the evidence source.

## Subagent Rule

Subagents may investigate, implement, test, or review scoped work. The main
thread should remain the single writer for `goal-tasks.md` and `goal-log.md` to
avoid conflicting status edits.

If a subagent produces evidence, summarize it in `goal-log.md` and update the
matching row in `goal-tasks.md`.

## Stop Conditions

Stop and report clearly when:

- The source goal file and existing `goal-tasks.md` contradict each other.
- A task requires a business decision, credential, permission, or irreversible
  action.
- The user asks for a heavier tracker, script, hook, dashboard, or registry.
- The task scope is too broad to extract into a small status table without
  first clarifying priorities.
