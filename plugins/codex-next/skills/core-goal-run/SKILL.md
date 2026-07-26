---
name: core-goal-run
description: Use only when the user explicitly invokes this skill to create or resume a persistent file-based goal tracker across sessions.
metadata:
  version: "1.0"
  updated: "2026-07-26"
---

# Goal Run

Execute or resume an explicitly requested long-running goal while keeping its
state recoverable across sessions. Do not use this workflow for ordinary work
that can finish in the current turn.

## Tracker Contract

Use three plain Markdown files in the goal directory:

```text
<goal-dir>/
├── goal-plan-list.md  # original plan or source, read-only
├── goal-tasks.md      # compact current status
└── goal-log.md        # evidence and handoff notes
```

If the source plan has another name, keep that name and create only
`goal-tasks.md` and `goal-log.md` beside it.

Do not create tracker scripts, hooks, run IDs, registries, dashboards, or hidden
state unless the user explicitly requests a heavier system.

## `goal-tasks.md`

Keep this file short enough to understand at a glance:

```markdown
# Goal Tasks

Source: `goal-plan-list.md`

| ID | Task | Status | Auto | Evidence | Notes |
|---|---|---|---|---|---|
| T001 | Inspect current state | DONE | yes | `goal-log.md#t001` | current baseline read |
| T002 | Implement the next slice | DOING | yes | pending | scoped to current slice |
| T003 | Approve production rollout | HUMAN_PENDING | no | pending | user decision required |
```

Use only these statuses unless the user's existing tracker defines another
taxonomy:

- `TODO`
- `DOING`
- `VERIFYING`
- `DONE`
- `BLOCKED`
- `HUMAN_PENDING`
- `SKIPPED_HUMAN`

Do not paste command output, long rationale, PR bodies, or full logs into the
table.

## `goal-log.md`

Record concise evidence and the next handoff:

```markdown
# Goal Log

## YYYY-MM-DD Run

Request:
- Resume automatic work from the source plan.

## T001

Status: DONE

Evidence:
- Reviewed the current source and repository state.
- Relevant check completed successfully.

## Handoff

Read first:
- `goal-tasks.md`
- `goal-log.md`

Next:
- Continue T002.
- Keep T003 pending until the user decides.
```

Evidence should be a pointer such as a command and exit status, test result,
changed path, commit SHA, PR or CI URL, deployment readback, screenshot path, or
reviewed source section. The tracker itself is not proof of completion.

## Workflow

1. Confirm that the user explicitly requested persistent goal tracking or
   resumption. Otherwise stop using this skill and complete the task normally.
2. Read the source goal and existing tracker files.
3. Create tracker files only when they are missing and persistent tracking is
   part of the request.
4. Extract actionable tasks, not every paragraph or improvement idea.
5. Continue the current safe task. Do not invent new work merely to keep the
   goal active.
6. Update tracker files only at a meaningful phase boundary, a status change,
   or before stopping. Do not interrupt implementation after every small unit
   to rewrite the tracker.
7. Before stopping, ensure completed work has evidence, blockers are concrete,
   and `Handoff` says what to read and do next.

## Human and External Boundaries

- Mark business decisions, credentials, permissions, irreversible actions,
  production changes, and external approvals as `HUMAN_PENDING` unless the
  user has already authorized the exact action.
- Never mark a human action complete without current evidence.
- Keep implementation, testing, Git, release, and deployment behavior under
  their normal task rules. This skill owns only the tracker files.
- Subagents may work on scoped tasks, but the main thread remains the only
  tracker writer.

## Stop Conditions

Stop and report when:

- no actionable automatic task remains;
- the next step requires a user decision, credential, permission, or
  irreversible action;
- the source plan conflicts with current repository or external evidence;
- verification has a concrete blocker;
- the user asks to pause, change scope, or replace the tracking method.

Do not treat a difficult, slow, or incomplete task as blocked while meaningful
authorized work can still continue.
