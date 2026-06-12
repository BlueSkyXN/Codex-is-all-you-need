---
name: sdlc-srs-workflow
description: Use to draft or audit SRS with requirement IDs, functional requirements, acceptance criteria, constraints, NFR hooks, and traceability.
---

# SRS Workflow

Use this workflow when the SDLC manager must produce or update a Software Requirements Specification before implementation.

The SRS is the software-facing contract between requirements work and development execution. It turns business, user, and product intent into precise, testable, traceable software requirements that dev agents can consume without taking ownership of upstream requirement management.

## Use when

- A BRD, URS, PRD, feature brief, issue, or product scope baseline must be converted into software requirements.
- The work needs functional requirements, requirement IDs, acceptance criteria, traceability, or explicit software behavior.
- A feature affects behavior, permissions, data, interfaces, user states, error handling, or multiple modules.
- Dev needs an implementation-ready contract, not only a product narrative.
- Existing SRS content must be reviewed, normalized, or updated after an approved change.

## Do not use when

- The task is direct code implementation, debugging, test execution, PR review, or release publishing.
- The user only needs business justification, user research, or PRD-level framing.
- There is no approved or clearly marked requirement source; use `sdlc-requirements-workflow` or `sdlc-prd-workflow` first.
- The request is to decide final architecture, implementation libraries, database technology, or repository refactor strategy. Use `sdlc-solution-spec-workflow` for structured solution material and let dev handle execution.

## Inputs

Prefer the most authoritative available sources:

1. Scope baseline
   - Approved scope
   - Non-goals
   - deferred scope
   - target lane and modifier
2. Requirement sources
   - BRD
   - URS
   - PRD
   - feature brief
   - issue or customer request
   - project research output
3. Product behavior material
   - user flows
   - state machine
   - field rules
   - copy rules
   - exception handling
   - acceptance criteria
4. Engineering constraints
   - NFR draft
   - known platform constraints
   - dependency list
   - existing API or data contracts
   - repository map if available
5. Prior decisions
   - decision log
   - change log
   - open questions
   - previous SRS versions

If required inputs are missing, continue only when the missing items do not block the requested delivery grade. Mark missing items explicitly.

## Workflow

### 1. Establish the source baseline

Identify the current authoritative input set:

```text
BRD / URS / PRD / issue / scope baseline / change request / research evidence
```

Then record:

- source document names or links
- version or date
- owner if known
- status: draft, reviewed, approved, superseded, or unknown
- scope this SRS covers
- scope this SRS does not cover

Do not silently merge conflicting source material. Record the conflict and identify which source should control.

### 2. Define SRS metadata

Create a document header:

| Field | Required |
|---|---|
| Document ID | yes |
| Feature / system name | yes |
| Source requirement links | yes |
| Owner | yes if known |
| Status | yes |
| Version | yes |
| Last updated | yes |
| Lane / modifier | yes |
| Related artifacts | as available |

Recommended status values:

```text
draft
review-ready
baseline
change-pending
superseded
```

### 3. Normalize requirement IDs

Create stable IDs before writing detailed requirements.

Use these prefixes:

| Prefix | Meaning |
|---|---|
| `REQ` | Software-facing functional, interface, data, permission, operational, compliance, or quality requirement |
| `VAL` | Acceptance or validation item |
| `Q` | Open question |
| `DEC` | Durable decision |
| `ARCH` | Architecture constraint |
| `DOM` | Domain, ownership, data, or dependency constraint |

Rules:

- One ID means one requirement.
- Do not reuse a retired ID for a different requirement.
- Split compound requirements when they contain separate behaviors or acceptance paths.
- Link each `REQ` ID to at least one source input when possible.
- If a requirement is inferred, mark it as inferred and explain the basis.

### 4. Separate requirement classes

Classify requirements before writing.

| Class | Description |
|---|---|
| Functional | User-visible or system behavior |
| Interface | API, CLI, SDK, integration, event, or contract behavior |
| Data | fields, storage, lifecycle, migration, retention, import/export |
| Permission | roles, access, visibility, editability, audit |
| Operational | logging, monitoring, support, admin, rollout, rollback |
| Compliance | legal, policy, privacy, security, audit, platform review |
| NFR reference | measurable quality constraint managed by `sdlc-nfr-spec` |

Keep NFR detail in `sdlc-nfr-spec` when the NFR is substantial. The SRS should reference NFR IDs rather than duplicating the full matrix.

### 5. Write functional requirements

For each functional requirement, use this structure:

```markdown
### REQ-001: <Requirement name>

- Source:
- Priority:
- User / actor:
- Preconditions:
- Trigger:
- System behavior:
- Normal flow:
- Alternate flow:
- Exception flow:
- State impact:
- Data impact:
- Permission impact:
- Related SPEC:
- Acceptance criteria:
- Open issues:
```

Write requirements as observable behavior:

```text
The system shall ...
```

Avoid vague terms unless a measurable definition follows. Do not write “fast”, “easy”, “secure”, “intuitive”, or “robust” without a linked NFR, rule, or acceptance criterion.

### 6. Write acceptance criteria

Each P0/P1 functional requirement must have acceptance criteria.

Recommended format:

```text
Given <precondition>
When <actor action or system event>
Then <observable system result>
And <data/state/permission result>
```

Cover at least:

- normal path
- primary exception path
- permission or access path
- data validation path
- state transition path when relevant

Assign acceptance IDs:

```text
VAL-001
VAL-002
```

### 7. Define state and lifecycle requirements

If behavior depends on status, progress, lifecycle, user session, order state, workflow state, or moderation state, include a state table:

| State | Enter condition | Allowed actions | Forbidden actions | Exit condition | Next state |
|---|---|---|---|---|---|

Rules:

- Every state must have entry and exit conditions.
- Every user action must be allowed, rejected, ignored, or deferred in each relevant state.
- State changes must identify data impact and user-visible feedback.

### 8. Define field and data-facing requirements

For user input, API payloads, stored records, forms, imports, exports, or configuration, link or draft a data requirement table:

| Field | Type | Required | Default | Limits | Validation | Error copy | Storage / display note |
|---|---|---|---|---|---|---|---|

For substantial data design, hand off to `sdlc-spec-slice-writer` for a Data SPEC.

### 9. Define permission requirements

If behavior differs by role, account type, ownership, tenant, plan, region, or admin status, include a permission matrix:

| Actor / role | View | Create | Edit | Delete | Export | Admin action | Audit note |
|---|---|---|---|---|---|---|---|

For substantial authorization behavior, hand off to `sdlc-spec-slice-writer` for a Permission SPEC.

### 10. Link NFRs and constraints

Reference quality requirements by ID:

```text
REQ-010
REQ-011
VAL-010
VAL-011
```

Do not hide quality constraints inside vague prose. Use `sdlc-nfr-spec` when measurements, thresholds, validation methods, or release gates are needed.

### 11. Produce a traceability seed

Create an initial mapping table:

| Source | REQ ID | Requirement summary | VAL ID | Spec detail needed | Task candidate | Test candidate |
|---|---|---|---|---|---|---|

This is not the final RTM. It is the seed for `sdlc-requirements-traceability`.

### 12. Record open questions

Separate open questions from decisions.

| ID | Question | Blocks dev? | Owner | Needed by | Notes |
|---|---|---:|---|---|---|

Do not convert unresolved questions into assumptions. Assumptions must be explicit and reversible.

## Output

Return or write an SRS with these sections:

```markdown
# SRS: <Feature / System>

## 1. Document Control
## 2. Source Baseline
## 3. Scope and Non-goals
## 4. Requirement Index
## 5. Functional Requirements
## 6. Interface / Data / Permission Requirements
## 7. State and Lifecycle Requirements
## 8. NFR References
## 9. Acceptance Criteria
## 10. Traceability Seed
## 11. Risks, Assumptions, and Open Questions
## 12. Handoff Notes
```

If writing into an existing repository, prefer the project’s established docs directory. If no convention exists, propose a path rather than creating files without approval.

## Validation

Before declaring the SRS ready, check:

- Every P0/P1 requirement has an ID.
- Every P0/P1 requirement has acceptance criteria.
- Every requirement traces back to a source or is marked inferred.
- Scope and non-goals are explicit.
- Requirements do not silently include implementation decisions.
- NFRs are referenced or marked as missing.
- State, field, permission, and exception behavior are covered when relevant.
- Open questions are separated from decisions.
- Dev handoff readiness is stated as ready, needs revision, or blocked.

## Boundaries

- Do not edit source code.
- Do not execute tests or modify repository configuration.
- Do not approve business scope.
- Do not finalize architecture when repository evidence is missing.
- Do not present assumptions as confirmed requirements.
- Do not expand scope beyond the approved baseline.
- Do not replace `sdlc-nfr-spec`, `sdlc-spec-slice-writer`, `sdlc-solution-spec-workflow`, or `sdlc-dev-handoff-planning` when those specialized outputs are needed.

## Handoff

Use the SRS to route downstream work:

| Need | Next skill |
|---|---|
| measurable quality constraints | `sdlc-nfr-spec` |
| UI/API/Data/Admin/Permission/Directory specs | `sdlc-spec-slice-writer` |
| HLD/LLD-oriented solution material | `sdlc-solution-spec-workflow` |
| implementation task package | `sdlc-dev-handoff-planning` |
| requirement-to-task/test traceability | `sdlc-requirements-traceability` |
| readiness judgment | `sdlc-readiness-review` |

When handing off to dev, provide:

1. SRS location
2. relevant REQ IDs
3. related spec details
4. acceptance criteria
5. constraints and non-goals
6. unresolved blockers
