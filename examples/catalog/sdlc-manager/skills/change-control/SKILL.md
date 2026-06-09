---
name: change-control
description: Use to manage requirement baseline changes, scope changes, artifact updates, traceability impacts, and dev handoff revisions without forcing change control onto every direct development task.
---

# Change Control

Use this workflow when a requirement, baseline, scope, SRS, SPEC, NFR, handoff package, or traceability chain changes after it has been used for planning or development.

Change control protects the delivery contract:

```text
what changed
why it changed
who owns the decision
what artifacts and tasks are affected
whether dev can continue
```

Not every code change needs formal change control. Direct-dev work may proceed without this skill when no SDLC baseline exists and the change is scoped to an issue, bugfix, or local task. Use change control when a prior agreement, source artifact, scope baseline, or implementation contract is affected.

## Use when

- A scoped or baselined requirement changes.
- SRS, NFR, SPEC, RTM, dev handoff, or acceptance criteria must be updated after development planning starts.
- Dev reports a contradiction between artifacts and repository evidence.
- Scope expands, shrinks, or shifts across tasks or releases.
- A change affects release risk, compliance, security, privacy, data, permissions, API compatibility, or user-visible behavior.
- Multiple downstream artifacts or implementation tasks must be re-synchronized.

## Do not use when

- No baseline or prior agreement exists and the user is still drafting requirements.
- A direct-dev bugfix or local task proceeds from a clear issue with no formal SDLC artifacts.
- The user asks for implementation, testing, review, or release publication.
- The change is only editorial and has no effect on scope, acceptance, downstream tasks, or traceability.
- The appropriate action is to write the missing artifact rather than record a change.

## Inputs

Use available materials:

- original request or issue
- scope baseline
- BRD, URS, PRD
- SRS
- NFR
- SPEC slices
- dev handoff
- RTM
- readiness review
- implementation blocker report
- PR review finding
- release issue
- stakeholder decision
- repository evidence

If no formal baseline exists, state that this is not change control; route to the relevant authoring or dev skill.

## Workflow

### 1. Determine whether change control applies

Ask:

| Question | If yes |
|---|---|
| Was there a baseline, approved scope, SRS, SPEC, handoff, or task package? | change control may apply |
| Does the change affect requirement meaning, acceptance, validation, or release risk? | change control applies |
| Does the change only clarify wording without altering intent? | record as editorial update |
| Is this a direct-dev issue with no SDLC baseline? | route to dev or task handoff |

Classify:

```text
formal-change
editorial-update
implementation-blocker
scope-clarification
direct-dev-no-change-control
```

### 2. Capture change request metadata

Create a record:

| Field | Required |
|---|---:|
| Change ID | yes |
| Requested by | yes if known |
| Date | yes |
| Source artifact | yes when available |
| Current baseline | yes when available |
| Change type | yes |
| Reason | yes |
| Impact summary | yes |
| Decision owner | yes if known |
| Status | yes |

Recommended status values:

```text
proposed
accepted
rejected
deferred
needs-owner-decision
implemented
superseded
```

### 3. Classify change type

Use these types:

| Type | Meaning |
|---|---|
| `scope-addition` | new behavior or requirement added |
| `scope-removal` | previous requirement removed |
| `scope-shift` | target behavior or user path changed |
| `acceptance-change` | validation or done criteria changed |
| `nfr-change` | performance, security, privacy, reliability, accessibility, compatibility, or operational requirement changed |
| `spec-change` | UI/API/Data/Permission/Admin/Directory/Release/etc. spec changed |
| `implementation-blocker` | repository evidence prevents implementation as written |
| `release-risk-change` | launch, rollback, migration, or support risk changed |
| `editorial-update` | wording changed without delivery impact |

### 4. Assess impact

Assess impact across artifacts and execution.

| Area | Impact |
|---|---|
| BRD / URS / PRD | business, user, product scope |
| SRS | functional or software requirement IDs |
| NFR | measurable quality constraints |
| SPEC | UI, API, data, permission, admin, directory, release, observability |
| Handoff | task cards, execution order, suggested agent, validation |
| RTM | source-to-task/test links |
| Dev work | changed files, in-progress tasks, PRs |
| Tests | planned, added, or invalidated tests |
| Release | rollout, rollback, support, documentation |

Mark each item:

```text
none
minor
material
blocking
unknown
```

### 5. Decide action

Choose one action:

| Action | Meaning |
|---|---|
| `accept-and-update` | update affected artifacts and handoff |
| `reject` | keep baseline unchanged |
| `defer` | move change to future scope |
| `split` | separate into current and future changes |
| `request-owner-decision` | cannot decide from available evidence |
| `route-to-dev-blocker` | dev evidence blocks implementation; clarify or revise spec |
| `direct-dev-no-control` | change control is not needed |

Do not silently accept scope expansion.

### 6. Update downstream map

If accepted, list required updates:

```text
SRS IDs to update:
SPEC IDs to update:
NFR IDs to update:
Task cards to add/change/remove:
Validation to add/change/remove:
RTM rows to update:
Release notes / rollout notes to update:
```

If rejected or deferred, list what remains unchanged.

### 7. Preserve dev continuity

State whether dev can continue:

| Dev status | Meaning |
|---|---|
| `continue` | change does not block current work |
| `continue-with-limits` | dev may continue unaffected tasks only |
| `pause-affected-tasks` | only affected tasks pause |
| `pause-all` | contradiction or scope change blocks all implementation |
| `direct-dev` | no formal baseline; dev can proceed from issue/task |

This avoids unnecessary global stoppage.

### 8. Record traceability update

Every accepted material change should update traceability.

Add or update:

```text
CHG-ID -> affected source IDs -> affected SRS/SPEC/NFR IDs -> affected TASK/TEST/PR/REL IDs
```

If traceability does not exist yet, create a traceability seed instead of blocking the change.

## Output

Return or write a change record:

```markdown
# Change Control Record: CHG-<ID>

## 1. Change Summary
## 2. Baseline or Source Artifact
## 3. Change Type
## 4. Reason
## 5. Impact Assessment
## 6. Decision
## 7. Required Artifact Updates
## 8. Dev Continuity
## 9. Traceability Update
## 10. Follow-up Actions
```

Use this decision block:

```text
Decision: accept-and-update | reject | defer | split | request-owner-decision | route-to-dev-blocker | direct-dev-no-control
Reason:
Affected artifacts:
Affected dev tasks:
Dev continuity:
Traceability action:
Next skill / agent:
```

## Validation

Before declaring change control complete, check:

- A baseline or source artifact was identified, or the record states why none exists.
- Change type is explicit.
- Impact assessment covers SRS, NFR, SPEC, Handoff, RTM, Dev, Tests, and Release when relevant.
- Decision is explicit and not hidden in prose.
- Accepted changes have downstream update actions.
- Rejected or deferred changes state what remains unchanged.
- Dev continuity is clear.
- Traceability is updated or explicitly seeded.
- Direct-dev tasks are not forced into formal change control when no baseline exists.

## Boundaries

- Do not approve business decisions unless the user provides that decision.
- Do not edit code or execute implementation.
- Do not use change control for every direct-dev task.
- Do not turn editorial comments into formal scope changes.
- Do not accept scope expansion silently.
- Do not block unrelated dev tasks when only one task is affected.
- Do not rewrite all SDLC artifacts when only a targeted update is required.

## Handoff

Route by decision:

| Decision | Route |
|---|---|
| `accept-and-update` | update relevant authoring skill, then `requirements-traceability` and `dev-handoff-planning` |
| `reject` | return to current baseline and continue dev if ready |
| `defer` | record future scope and update RTM/deferred list |
| `split` | create current-scope and future-scope artifacts/tasks |
| `request-owner-decision` | ask for owner decision before dev continues affected tasks |
| `route-to-dev-blocker` | revise SRS/SPEC/handoff or route to repo evidence review |
| `direct-dev-no-control` | route to dev skill or direct task handoff |
