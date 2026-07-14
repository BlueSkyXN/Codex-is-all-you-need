---
name: sdlc-requirements-traceability
description: Use to build or audit RTM links across requirements, design, validation, tasks, PRs, commits, releases, and evidence gaps.
metadata:
  version: "0.4"
  updated: "2026-06-12"
---

# Requirements Traceability

Use this workflow to create, update, or inspect a requirements traceability matrix.

Traceability connects intent to execution:

```text
Business / User / Product / Software Requirement
-> HLD / LLD / ADR / Domain Boundary / SPEC / Validation Plan / Handoff / Task
-> Test / Review / PR / Release
```

Traceability is strongest when SDLC materials exist. When no SDLC materials exist, traceability can still start from an issue, bug report, task ID, test failure, or direct-dev handoff. Do not block small development work solely because a full RTM is absent; create a traceability seed and mark the evidence level.

For lightweight SDLC-ADS work, use the operating-model contract as the default:

```text
REQ -> TASK -> VAL
ARCH / DOM / DEC -> TASK
ITEM -> TASK / VAL / Q
```

Do not require BRD/URS/PRD/SRS prefixes before a clear direct-dev, handoff-lite, or refactor task can proceed.

## Use when

- Requirements, specs, tasks, tests, PRs, or release notes must be connected.
- A feature has BRD, URS, PRD, SRS, NFR, HLD, LLD, ADR, Domain Boundary Map, SPEC, Validation Plan, or dev handoff artifacts.
- Work spans multiple tasks, modules, agents, or validation paths.
- You need to detect orphan requirements, orphan tasks, missing tests, or untracked changes.
- A change request modifies a prior requirement baseline.
- Dev needs requirement IDs to reference in task cards, commits, PRs, or review notes.

## Do not use when

- The task is a small direct code change with no need for formal tracking beyond issue and validation notes.
- The user only asks to implement, debug, test, or review code.
- No stable source material exists and the immediate task is safe to route to dev; create a task handoff instead.
- The request is to approve scope or release readiness. Use `sdlc-readiness-review` or `dev-release-check` as appropriate.

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
- validation plan, acceptance test matrix, smoke checklist, regression scope, or evidence expectations
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

Use the depth that matches the lane and risk.

| Depth | Use when | Matrix shape |
|---|---|---|
| `seed` | direct-dev, issue-backed, bugfix, early draft | Source -> TASK -> VAL |
| `standard` | contained feature delivery | REQ -> TASK -> VAL -> Test |
| `architecture` | architecture/domain-sensitive delivery | REQ + ARCH/DOM/DEC -> TASK -> VAL -> Test |
| `extended` | system, rebuild, multi-wave, or release-bound delivery | REQ + ARCH/DOM/DEC -> TASK -> VAL -> Test -> PR -> Release |
| `audit` | baseline, compliance, high-risk, or release-bound evidence | Same chain plus owner, status, evidence, change record |

Do not force `extended` or `audit` depth on every change.

### 2. Inventory source IDs

Collect stable IDs from available artifacts.

Use these prefixes:

| Prefix | Meaning |
|---|---|
| `REQ` | Requirement from requirements package or scope decision table |
| `DEC` | Durable decision |
| `ARCH` | Architecture constraint |
| `DOM` | Domain, ownership, data, or dependency constraint |
| `TASK` | Dev task |
| `VAL` | Validation item |
| `Q` | Open question or blocker |
| `ITEM` | Midstream intake item |

If an input has no ID, create a lightweight local ID and mark it as generated. Use only the prefixes above.

### 3. Normalize requirement rows

Each row should represent one traceable item or one traceable chain.

Base columns:

```markdown
| Trace ID | Source | Requirement | Type | Priority | Downstream | Task | Validation | Status |
|---|---|---|---|---|---|---|---|---|
```

Extended columns:

```markdown
| Trace ID | Source | REQ | ARCH/DOM/DEC | TASK | VAL | Test | PR/Commit | Release | Owner | Status | Evidence | Change |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
```

Use compact rows. A traceability matrix should help dev and review, not become an unreadable archive.

### 4. Link source to software-facing requirements

Map source materials to `REQ`, `TASK`, and `VAL`.

Examples:

```text
REQ-001 -> TASK-001 -> VAL-001
ARCH-001 -> TASK-002
DOM-001 -> TASK-003
Issue-123 -> TASK-001
Bug-456 -> TEST-REG-001
```

Rules:

- One upstream item may map to several downstream requirements.
- One downstream task may satisfy several requirements only if the task scope is still coherent.
- Mark inferred links explicitly.
- Do not hide many-to-many relationships by collapsing unrelated items.

### 5. Link requirements to architecture/domain artifacts and SPEC slices

For each `REQ` or task item, identify needed architecture/domain and specification evidence:

| Requirement | Needed architecture/domain constraint | Needed specification detail | Status |
|---|---|---|---|
| `REQ-001` | `ARCH-001`, `DOM-001`, `DEC-001` | `20-规格.md` API section | present / missing / not applicable |

If no specification detail is required, state why.
If no HLD, LLD, ADR, or Domain Boundary Map is required, state why when the work is architecture-sensitive.

### 6. Link validation plan to tasks and tests

Each implementation task should have a validation path. When a Validation Plan or acceptance matrix exists, link tasks to the relevant validation IDs before linking to executed test evidence.

| Task | Validation Plan item | Test or check | Type | Status |
|---|---|---|---|---|
| `TASK-001` | `VAL-001` | `pytest path/test_name` | unit / integration / e2e / manual / smoke / NFR | planned / passed / failed / not run |

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
| missing validation plan | feature, system, release, NFR, architecture, or domain-sensitive work lacks explicit proof-of-correctness plan |
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
- Validation Plan items link to tasks and execution evidence where a validation plan exists.
- Architecture-sensitive requirements point to HLD, LLD, ADR, Domain Boundary Map, or an explicit accepted gap.
- SPEC-dependent requirements point to the relevant SPEC slice or missing-SPEC gap.
- Change-related rows point to `sdlc-change-control` records when baseline is affected.
- Status values are consistent.
- Direct-dev work is not misrepresented as full SDLC-backed work.

## Boundaries

- Do not approve requirements.
- Do not execute tests or claim validation success without evidence.
- Do not block safe direct-dev work solely because a full matrix is absent.
- Do not create fake BRD, URS, PRD, SRS, or SPEC IDs to make the matrix look complete.
- Do not use traceability as a substitute for `sdlc-dev-handoff-planning`.
- Do not overwrite existing tracking conventions without user approval.

## Handoff

Route findings:

| Finding | Next step |
|---|---|
| source not ready | `sdlc-requirements-workflow`, `sdlc-prd-workflow`, or `sdlc-srs-workflow` |
| HLD missing | `sdlc-hld-workflow` |
| LLD missing | `sdlc-lld-workflow` |
| ADR missing | `sdlc-architecture-decision-record` |
| domain boundary missing | `sdlc-domain-boundary-modeling` |
| SPEC missing | `sdlc-spec-slice-writer` |
| validation plan missing | `sdlc-validation-plan-workflow` |
| handoff missing | `sdlc-dev-handoff-planning` |
| baseline changed | `sdlc-change-control` |
| readiness uncertain | `sdlc-readiness-review` |
| implementation ready | dev skill such as `dev-spec-driven-implementation`, `dev-bugfix`, or `dev-test-strategy` |
| direct-dev safe but untracked | create traceability seed and proceed to dev |
