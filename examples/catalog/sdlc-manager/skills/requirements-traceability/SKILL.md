---
name: requirements-traceability
description: Use to map business, user, product, software, NFR, HLD, LLD, ADR, Domain Boundary, SPEC, handoff, task, test, PR, commit, and release evidence into a requirements traceability matrix without turning traceability into a blocking ceremony for direct development.
---

# Requirements Traceability

Use this workflow to create, update, or inspect a requirements traceability matrix.

Traceability connects intent to execution:

```text
Business / User / Product / Software Requirement
-> HLD / LLD / ADR / Domain Boundary / SPEC / Handoff / Task
-> Test / Review / PR / Release
```

Traceability is strongest when SDLC materials exist. When no SDLC materials exist, traceability can still start from an issue, bug report, task ID, test failure, or direct-dev handoff. Do not block small development work solely because a full RTM is absent; create a traceability seed and mark the evidence level.

## Use when

- Requirements, specs, tasks, tests, PRs, or release notes must be connected.
- A feature has BRD, URS, PRD, SRS, NFR, HLD, LLD, ADR, Domain Boundary Map, SPEC, or dev handoff artifacts.
- Work spans multiple tasks, modules, agents, or validation paths.
- You need to detect orphan requirements, orphan tasks, missing tests, or untracked changes.
- A change request modifies a prior requirement baseline.
- Dev needs requirement IDs to reference in task cards, commits, PRs, or review notes.

## Do not use when

- The task is a small direct code change with no need for formal tracking beyond issue and validation notes.
- The user only asks to implement, debug, test, or review code.
- No stable source material exists and the immediate task is safe to route to dev; create a task handoff instead.
- The request is to approve scope or release readiness. Use `sdlc-readiness-review` or `release-check` as appropriate.

## Inputs

Use what exists. Do not require all artifact families.

### Source artifacts

- BRD or business brief
- URS or user scenarios
- PRD or product requirements
- NFR matrix
- SRS
- HLD
- LLD
- ADR
- Domain Boundary Map
- SPEC slices
- solution spec
- change control record

### Execution artifacts

- dev handoff
- task cards
- issue tracker items
- test plan or test cases
- validation command logs
- PRs, commits, branches, or release notes
- bug reports or incidents

### Direct-dev traceability sources

When SDLC artifacts are absent, trace from:

- issue ID
- bug ID
- user request
- reproduction step
- failing test
- file path or symbol
- task handoff ID

## Workflow

### 1. Choose traceability depth

Use the depth that matches the delivery profile and risk.

| Depth | Use when | Matrix shape |
|---|---|---|
| `seed` | direct-dev, issue-backed, bugfix, early draft | Source -> Task -> Validation |
| `standard` | feature delivery with SRS/SPEC | Requirement -> SPEC -> Task -> Test |
| `architecture` | architecture-sensitive delivery | SRS/NFR -> HLD/LLD/ADR/Domain Boundary -> SPEC -> Task -> Test |
| `extended` | system or program delivery | BRD/URS/PRD/SRS/NFR/HLD/LLD/ADR/Domain Boundary/SPEC -> Task -> Test -> PR -> Release |
| `audit` | baseline, compliance, high-risk, release-bound | Full chain plus owner, status, evidence, change record |

Do not force `extended` or `audit` depth on every change.

### 2. Inventory source IDs

Collect stable IDs from available artifacts.

Recommended prefixes:

| Prefix | Meaning |
|---|---|
| `BRD` | Business requirement |
| `URS` | User requirement |
| `PRD` | Product requirement |
| `SRS-FR` | Functional software requirement |
| `SRS-NFR` | Non-functional software requirement reference |
| `NFR` | Non-functional requirement |
| `HLD` | High-level architecture design |
| `LLD` | Low-level detailed design |
| `ADR` | Architecture decision record |
| `DOMAIN` | Domain boundary or ownership item |
| `SPEC-UI` | UI specification |
| `SPEC-API` | API specification |
| `SPEC-DATA` | Data specification |
| `SPEC-PERM` | Permission specification |
| `SPEC-ADMIN` | Admin specification |
| `SPEC-DIR` | Directory specification |
| `TASK` | Dev task |
| `TEST` | Test or validation item |
| `PR` | Pull request |
| `REL` | Release item |
| `CHG` | Change control record |

If an input has no ID, create a temporary local ID and mark it as generated.

### 3. Normalize requirement rows

Each row should represent one traceable item or one traceable chain.

Base columns:

```markdown
| Trace ID | Source | Requirement | Type | Priority | Downstream | Task | Validation | Status |
|---|---|---|---|---|---|---|---|---|
```

Extended columns:

```markdown
| Trace ID | BRD/URS/PRD | SRS/NFR | HLD/LLD/ADR/Domain | SPEC | Handoff Task | Test | PR/Commit | Release | Owner | Status | Evidence | Change |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
```

Use compact rows. A traceability matrix should help dev and review, not become an unreadable archive.

### 4. Link source to software-facing requirements

Map upstream material to SRS or equivalent issue/task material.

Examples:

```text
BRD-001 -> PRD-003 -> SRS-FR-002
URS-002 -> PRD-004 -> SRS-FR-005
Issue-123 -> TASK-001
Bug-456 -> TEST-REG-001
```

Rules:

- One upstream item may map to several downstream requirements.
- One downstream task may satisfy several requirements only if the task scope is still coherent.
- Mark inferred links explicitly.
- Do not hide many-to-many relationships by collapsing unrelated items.

### 5. Link requirements to architecture/domain artifacts and SPEC slices

For each SRS or task item, identify needed architecture/domain and SPEC evidence:

| Requirement | Needed architecture/domain artifact | Needed SPEC | Status |
|---|---|---|---|
| `SRS-FR-001` | `HLD-001`, `DOMAIN-001`, `ADR-001` | `SPEC-UI-001`, `SPEC-API-001` | present / missing / not applicable |

If no SPEC is required, state why.
If no HLD, LLD, ADR, or Domain Boundary Map is required, state why when the work is architecture-sensitive.

### 6. Link tasks to validation

Each implementation task should have a validation path.

| Task | Validation | Type | Status |
|---|---|---|---|
| `TASK-001` | `TEST-001` | unit / integration / e2e / manual / smoke / NFR | planned / passed / failed / not run |

Do not mark validation as passed unless evidence exists.

### 7. Record execution evidence when available

When dev has started or finished, add:

- branch name
- PR number or link
- commit SHA if relevant
- test command and result
- review verdict
- release or deployment reference

If execution evidence is not yet available, leave it blank or mark `pending`.

### 8. Detect traceability gaps

Report gaps by type:

| Gap | Meaning |
|---|---|
| orphan source | requirement has no downstream SRS/task |
| orphan task | task has no source or issue link |
| missing validation | task or requirement has no test/validation |
| missing SPEC | requirement needs UI/API/Data/etc. spec but none exists |
| missing architecture artifact | requirement needs HLD, LLD, ADR, Domain Boundary Map, or Directory SPEC but none exists |
| boundary conflict | task or SPEC appears to violate ownership, dependency, or forbidden access rules |
| stale link | target artifact is superseded |
| unapproved change | task implements changed scope without change record |
| direct-dev risk | implementation proceeds from issue/task without formal SDLC materials |

Not every gap blocks dev. Classify severity:

```text
blocker
important
watch
accepted
```

### 9. Support direct-dev traceability

For a direct-dev task, produce a seed matrix:

```markdown
| Trace ID | Source | Task | Validation | Risk | Status |
|---|---|---|---|---|---|
| TRACE-001 | Issue-123 | TASK-001 | pytest path/test_name | low | planned |
```

This preserves evidence without pretending a full SDLC chain exists.

## Output

Return or write one of these outputs.

### Traceability seed

```markdown
# Traceability Seed: <Change Name>

| Trace ID | Source | Task | Validation | Risk | Status |
|---|---|---|---|---|---|
```

### Standard RTM

```markdown
# Requirements Traceability Matrix: <Feature / System>

## 1. Scope
## 2. Artifact Sources
## 3. Traceability Matrix
## 4. Gap Report
## 5. Execution Evidence
## 6. Change Notes
```

### Gap report

```markdown
# Traceability Gap Report

## Blocking gaps
## Important gaps
## Accepted gaps
## Recommended next action
```

## Validation

Before declaring traceability ready, check:

- Every P0/P1 SRS requirement has a downstream task or explicit deferment.
- Every implementation task has a source or direct-dev source note.
- Every requirement or task has a validation plan or explicit accepted gap.
- NFRs have validation methods, not only statements.
- Architecture-sensitive requirements point to HLD, LLD, ADR, Domain Boundary Map, or an explicit accepted gap.
- SPEC-dependent requirements point to the relevant SPEC slice or missing-SPEC gap.
- Change-related rows point to `change-control` records when baseline is affected.
- Status values are consistent.
- Direct-dev work is not misrepresented as full SDLC-backed work.

## Boundaries

- Do not approve requirements.
- Do not execute tests or claim validation success without evidence.
- Do not block safe direct-dev work solely because a full matrix is absent.
- Do not create fake BRD, URS, PRD, SRS, or SPEC IDs to make the matrix look complete.
- Do not use traceability as a substitute for `dev-handoff-planning`.
- Do not overwrite existing tracking conventions without user approval.

## Handoff

Route findings:

| Finding | Next step |
|---|---|
| source not ready | `requirements-workflow`, `prd-workflow`, or `srs-workflow` |
| HLD missing | `hld-workflow` |
| LLD missing | `lld-workflow` |
| ADR missing | `architecture-decision-record` |
| domain boundary missing | `domain-boundary-modeling` |
| SPEC missing | `spec-slice-writer` |
| handoff missing | `dev-handoff-planning` |
| baseline changed | `change-control` |
| readiness uncertain | `sdlc-readiness-review` |
| implementation ready | dev skill such as `spec-driven-implementation`, `bugfix`, or `test-strategy` |
| direct-dev safe but untracked | create traceability seed and proceed to dev |
