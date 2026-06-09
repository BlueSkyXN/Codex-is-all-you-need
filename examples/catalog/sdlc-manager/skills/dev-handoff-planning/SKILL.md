---
name: dev-handoff-planning
description: Use to turn approved or clearly scoped SDLC materials, issues, SRS, NFR, SPEC slices, and constraints into a dev-readable implementation handoff with task cards, validation expectations, and blocker reporting rules.
---

# Dev Handoff Planning

Use this workflow when SDLC manager work must be converted into a package that dev agents can execute.

The handoff is the boundary between the specification control plane and the implementation execution plane:

```text
sdlc-manager creates the delivery contract.
dev executes the delivery contract.
```

SDLC materials are preferred inputs, not a universal prerequisite for development. When no SDLC materials exist and the task is already narrow, dev may continue through a direct-dev path using the issue, bug report, user request, repository evidence, and validation notes. In that case, do not fabricate missing BRD, URS, PRD, SRS, or SPEC artifacts; mark the implementation risk and route to dev with the smallest sufficient task brief.

## Use when

- SRS, NFR, HLD, LLD, ADR, Domain Boundary Map, SPEC slices, PRD, issue, bug report, change request, or roadmap input must be converted into implementation tasks.
- A feature, fix, refactor, migration, release change, or platform work needs explicit scope, non-scope, validation, and suggested dev ownership.
- Several implementation areas, dev agents, or validation levels must be coordinated.
- Dev needs a concise source-of-truth entry point instead of reading every upstream document from scratch.
- Existing handoff material must be normalized, checked, or split into executable task cards.

## Do not use when

- The user is asking to write BRD, URS, PRD, SRS, NFR, or SPEC content rather than handoff tasks.
- The request is direct implementation and already contains enough scope, target files, and validation instructions; route to dev directly.
- The work is repo exploration only; use `repo-onboarding` in dev.
- The user asks for code edits, test execution, PR review, or release publishing.
- The upstream scope is still unresolved; use `sdlc-readiness-review`, `requirements-workflow`, `srs-workflow`, or `spec-slice-writer` first.

## Inputs

Use the best available material. Do not require all items for every task.

### Preferred SDLC inputs

- Scope baseline and non-goals
- SRS with requirement IDs
- NFR matrix
- HLD
- LLD
- ADR
- Domain Boundary Map
- Modular monolith or Directory SPEC constraints
- SPEC slices: UI, API, Data, Permission, Admin, Directory, Observability, Release, Integration, or Copy
- Requirements traceability matrix
- Change control record
- Readiness review verdict
- Project research or repo map

### Direct-dev inputs

Use these when formal SDLC materials are absent but the task is still actionable:

- Issue or bug report
- User request
- Error message or reproduction steps
- Existing test failure
- Target files or affected area
- Acceptance criteria
- Existing project conventions
- Known validation command

If the input set is weak, continue only by making the risk explicit.

## Workflow

### 1. Classify the handoff path

Choose one path:

| Path | Use when | Output depth |
|---|---|---|
| `sdlc-backed` | SRS/SPEC/NFR/RTM or approved planning artifacts exist | Full dev handoff |
| `issue-backed` | Issue or task is clear, but formal SDLC artifacts are absent | Task handoff |
| `bugfix-backed` | Reproduction or observed failure exists | Bugfix handoff |
| `exploration-first` | Repository or implementation area is unclear | Onboarding handoff |
| `blocked` | Scope, target, or acceptance is too ambiguous | Blocker report |

Do not turn every direct-dev request into a formal SDLC project. If the task can safely proceed without SDLC materials, state that explicitly and route to dev.

### 2. Establish source references

Create a source table:

| Source | Type | Status | Relevant IDs | Notes |
|---|---|---|---|---|

Source types may include:

```text
BRD
URS
PRD
SRS
NFR
HLD
LLD
ADR
Domain Boundary
SPEC
RTM
Issue
Bug report
User request
Repository evidence
Test failure
Change request
```

Rules:

- Prefer stable IDs when available.
- If no IDs exist, create temporary handoff IDs such as `TASK-SRC-001`.
- Do not invent approval status.
- Mark contradictory sources before writing tasks.

### 3. Define scope and non-scope

Write two short lists:

```text
Must implement:
Must not implement:
```

For direct-dev tasks, this section may be brief but must still exist. It prevents dev from expanding the work beyond the request.

### 4. Identify affected work areas

List likely implementation areas without pretending certainty:

| Area | Evidence | Confidence | Suggested dev agent |
|---|---|---:|---|

Examples:

- frontend route or component
- backend endpoint or service
- CLI command
- Python package
- database migration
- data pipeline
- auth or permission layer
- docs or release notes
- tests or fixtures

If repo evidence is missing, route first to `repo-onboarding`.

### 5. Convert requirements into task cards

Each task card must be executable by a dev agent.

| Field | Required |
|---|---:|
| Task ID | yes |
| Source requirement or issue | yes |
| Goal | yes |
| Suggested agent | yes |
| Suggested skill | yes when known |
| Affected area | yes when known |
| Architecture constraints | when relevant |
| Domain ownership | when relevant |
| Allowed dependencies | when relevant |
| Forbidden dependencies | when relevant |
| Related HLD / LLD / ADR / Domain Boundary / Directory SPEC | when available |
| Allowed scope | yes |
| Forbidden scope | yes |
| Validation | yes |
| Done criteria | yes |
| Risk | yes |

Task ID pattern:

```text
TASK-001
TASK-002
TASK-003
```

Avoid task cards such as “implement the feature.” Split until each task has one primary goal and one clear validation path.

### 6. Define execution order

Create an order section:

```text
1. Read repository context or run repo-onboarding.
2. Implement prerequisite changes.
3. Implement behavior changes.
4. Add or update tests.
5. Run validation.
6. Prepare review notes.
```

For small direct-dev work, the order may be shorter:

```text
1. Inspect target files.
2. Apply scoped change.
3. Run smallest relevant validation.
4. Report changed files and residual risk.
```

### 7. Create validation plan

Write validation at three levels:

| Level | Purpose | Required? |
|---|---|---:|
| Smallest relevant check | Fast feedback | yes |
| Broader regression check | Confidence beyond local change | when risk warrants |
| Manual or release smoke | User or deployment path | when user-facing or release-bound |

Tie validation to SRS IDs, SPEC IDs, acceptance criteria, issue criteria, or reproduction steps when available.
Also tie validation to HLD, LLD, ADR, Domain Boundary Map, or Directory SPEC constraints when implementation must preserve architecture structure, data ownership, allowed dependencies, or forbidden dependencies.

### 8. Add blocker reporting rules

Dev may discover that the specification does not match repository reality. Define how to report that:

```text
If implementation evidence conflicts with SRS, SPEC, or handoff, report:
1. Artifact ID or source section
2. Conflicting repository evidence
3. Why implementation cannot proceed as written
4. Suggested resolution options
5. Whether work can continue safely in a reduced scope
```

This is not dev approval of SDLC materials. It is implementation feedback.

If implementation evidence conflicts with HLD, LLD, ADR, Domain Boundary Map, Directory SPEC, or modular-monolith constraints, report the affected artifact ID or section, the repository evidence, and whether a reduced-scope direct-dev path remains safe.

### 9. Mark fallback when SDLC materials are absent

When there are no SDLC materials, include a section:

```text
SDLC material status: absent
Proceed path: direct-dev / repo-onboarding-first / blocked
Risk: low / medium / high
Reason development may continue:
Required safeguards:
```

Use this when the task is a bugfix, maintenance change, small local implementation, or already clear issue.

## Output

Return or write a handoff document:

```markdown
# Dev Handoff: <Change Name>

## 1. Handoff Path
## 2. Source References
## 3. Scope and Non-scope
## 4. Affected Areas
## 5. Task Cards
## 6. Execution Order
## 7. Validation Plan
## 8. Architecture and Domain Constraints
## 9. Blockers and Contradictions
## 10. Traceability Notes
## 11. Dev Start Recommendation
```

Dev start recommendation must be one of:

```text
ready-for-dev
repo-onboarding-first
ready-for-direct-dev
revise-before-dev
blocked
```

## Validation

Before declaring the handoff ready, check:

- Every task has a clear source, goal, scope, validation, and done criteria.
- Forbidden scope is explicit.
- Tasks are small enough for dev execution.
- Suggested agents and skills match the work type.
- Validation does not claim tests have passed before dev runs them.
- SDLC-backed tasks link to SRS/SPEC/NFR/RTM where available.
- Architecture-sensitive tasks link to HLD/LLD/ADR/Domain Boundary/Directory SPEC where available.
- Architecture constraints, domain ownership, allowed dependencies, and forbidden dependencies are explicit when relevant.
- Direct-dev tasks state why formal SDLC materials are not required for this change.
- Blockers and contradictions are separated from implementation tasks.

## Boundaries

- Do not edit source code.
- Do not execute implementation tasks.
- Do not approve business scope or release readiness.
- Do not require SDLC materials for every dev task.
- Do not fabricate SRS, SPEC, or RTM just to satisfy a process shape.
- Do not hide risk when development proceeds without SDLC artifacts.
- Do not let dev handoff replace `requirements-traceability`, `sdlc-readiness-review`, or `change-control` when those are needed.

## Handoff

Route downstream:

| Condition | Next step |
|---|---|
| repo unknown | `repo-onboarding` |
| clear implementation package | `spec-driven-implementation` or relevant dev skill |
| bugfix | `bugfix` |
| API contract work | `api-contract-review` and backend/API dev agent |
| UI work | `frontend-ui-implementation` |
| tests needed | `test-strategy` |
| review needed | `pr-review` |
| release-bound | `release-check` |
| traceability missing | `requirements-traceability` |
| change affects baseline | `change-control` |
| architecture/domain constraints need authoring | `hld-workflow`, `lld-workflow`, `domain-boundary-modeling`, or `architecture-decision-record` |
