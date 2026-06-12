---
name: sdlc-solution-spec-workflow
description: Use to coordinate solution specs across HLD, LLD, domain, ADR, NFR, and SPEC slices; use leaf skills for details.
---

# Solution Spec Workflow

Use this workflow when SDLC manager materials need a solution-level package before dev execution.

A solution package connects SRS/NFR/HLD/LLD/ADR/Domain Boundary Map/SPEC materials to an implementation approach. This workflow coordinates and summarizes those artifacts; it should not replace the dedicated `sdlc-hld-workflow`, `sdlc-lld-workflow`, `sdlc-domain-boundary-modeling`, `sdlc-modular-monolith-architecture`, or `sdlc-architecture-decision-record` workflows when those artifacts need to be authored in full.

Dev consumes the solution package, maps it to the repository, implements, and reports contradictions or blockers.

## Use when

- A feature affects architecture, modules, integration, data flow, API contracts, permission boundaries, migration, observability, release strategy, or multiple code areas.
- SRS, NFR, HLD, LLD, ADR, Domain Boundary Map, or SPEC slices exist, but dev still needs a coherent implementation context.
- The user asks to assemble or normalize a solution design package, technical design package, design doc, implementation approach, or system design material.
- There are alternatives, trade-offs, dependencies, or platform constraints that must be captured before implementation.
- A prior technical bridge must be upgraded into a delivery-grade solution spec.

## Do not use when

- The task only needs BRD, URS, PRD, or SRS.
- The implementation is already local, scoped, and clear enough for dev.
- The user wants code edits, tests, debugging, or PR review.
- The user asks only to author a standalone HLD. Use `sdlc-hld-workflow`.
- The user asks only to author a standalone LLD. Use `sdlc-lld-workflow`.
- The user asks only to model domains, bounded contexts, or data ownership. Use `sdlc-domain-boundary-modeling`.
- The user asks only to record an architecture decision. Use `sdlc-architecture-decision-record`.
- Required behavior is not specified yet. Use `sdlc-srs-workflow` or `sdlc-spec-slice-writer` first.
- The task is only to generate dev task cards. Use `sdlc-dev-handoff-planning`.

## Inputs

Prefer:

- SRS
- NFR spec
- HLD
- LLD
- ADR
- Domain Boundary Map
- SPEC slices
- scope baseline
- non-goals
- repository map or project research
- current architecture notes
- API/data docs
- previous design decisions
- incident or bug history
- dependency and platform constraints
- rollout or migration requirements
- open questions from sdlc-manager artifacts

If repo evidence is unavailable, mark solution material as proposed. Do not claim it reflects current code reality.

## Solution package levels

Choose the required level.

| Level | Use for |
|---|---|
| HLD coordination | summarize or link system boundaries, components, flows, integrations, data movement, major dependencies from `sdlc-hld-workflow` |
| LLD coordination | summarize or link module responsibilities, interfaces, algorithms, state transitions, error handling, migration steps from `sdlc-lld-workflow` |
| Domain coordination | summarize or link domain ownership, data ownership, allowed dependencies, and forbidden dependencies from `sdlc-domain-boundary-modeling` |
| ADR coordination | summarize or link architecture decisions, alternatives, consequences, and review conditions from `sdlc-architecture-decision-record` |
| Constraint spec | technical constraints, non-goals, forbidden approaches, compatibility requirements |
| Implementation guide | ordered implementation approach for dev handoff without editing code |

A solution package may include multiple levels, but do not include sections with no decision or implementation value.

## Workflow

### 1. Establish design scope

Write:

```text
Feature/system:
Source SRS:
Source NFR:
Source HLD:
Source LLD:
Source ADR:
Source Domain Boundary Map:
Source SPEC slices:
Delivery profile:
Repository evidence available:
Design level needed:
Implementation areas:
Out-of-scope technical areas:
```

Make clear whether the spec is:

```text
evidence-grounded
proposed
decision-needed
```

### 2. Identify source requirements

Create a requirement intake table:

| Source ID | Requirement summary | Quality constraint | SPEC slice | Solution impact |
|---|---|---|---|---|

Every major solution element should trace back to a requirement, NFR, or explicit constraint.

If HLD, LLD, ADR, or Domain Boundary Map is missing but needed, mark it as a required upstream artifact rather than writing a full replacement inside this workflow.

### 3. Define goals and non-goals

Use goals and non-goals for the solution, not product scope.

Examples:

| Type | Examples |
|---|---|
| Solution goal | preserve API compatibility, isolate new module, avoid data loss, support rollback |
| Solution non-goal | redesign unrelated service, migrate all old state, replace auth system |

Do not use solution goals to expand product scope.

### 4. Map system context

For HLD-oriented material, describe:

- user/client actors
- external systems
- internal systems or modules
- data stores
- third-party dependencies
- trust boundaries
- critical flows
- deployment or runtime boundaries if relevant

If this information is substantial or contested, route to `sdlc-hld-workflow` and link the resulting HLD here.

Recommended table:

| Component / system | Role | Owned by | Inputs | Outputs | Constraints |
|---|---|---|---|---|---|

### 5. Describe architecture approach

Include only what is needed for dev execution.

```markdown
## Architecture Approach

- Current state:
- Proposed state:
- Components affected:
- Integration points:
- Data flow:
- Permission model impact:
- Error handling approach:
- Rollout / rollback approach:
- Operational impact:
```

When there are alternatives, write a decision matrix:

| Option | Description | Pros | Cons | Risks | Decision |
|---|---|---|---|---|---|

If the decision is long-lived or affects HLD, LLD, SPEC, RTM, or future implementation, route it to `sdlc-architecture-decision-record` and link the ADR here.

### 6. Define API and interface approach

If relevant, summarize interface behavior and link to API SPEC.

Include:

- public API surface
- internal interface surface
- versioning
- backward compatibility
- error model
- idempotency
- rate limit or abuse controls
- event/webhook behavior
- client migration impact

Do not duplicate the full API SPEC unless this document is the only artifact being produced.

### 7. Define data and state approach

If relevant, summarize:

- entities or records affected
- state transitions
- schema or field impact
- migration path
- backfill or reconciliation
- retention and deletion
- privacy classification
- data consistency model
- audit trail

Use `sdlc-spec-slice-writer` for detailed Data SPEC when needed.

### 8. Define module and directory approach

If repository evidence is available, map proposed work to existing conventions:

| Area | Existing convention | Proposed change | Reason | Risk |
|---|---|---|---|---|

If evidence is missing, write:

```text
Repository evidence needed before finalizing directory or module placement.
```

Do not invent paths as facts. You may propose candidate areas if clearly marked.
For modular-monolith directory and dependency rules, use `sdlc-modular-monolith-architecture` or Directory SPEC, then summarize the accepted constraints here.

### 9. Define LLD-oriented implementation notes

For each module or capability, use:

```markdown
### <Module / capability>

- Source requirement IDs:
- Responsibility:
- Inputs:
- Outputs:
- Main logic:
- State changes:
- Error handling:
- Data access:
- External calls:
- Observability:
- Tests needed:
- Open questions:
```

This is not code. It is a dev-readable implementation contract.
If the notes become detailed module design, route to `sdlc-lld-workflow` and link the LLD here.

### 10. Define validation strategy

Map requirements to validation types:

| Requirement / NFR | Validation type | Suggested check | Blocks release? |
|---|---|---|---|

Validation types:

```text
unit
integration
contract
UI / E2E
migration
security
privacy
performance
accessibility
manual smoke
observability
release rollback
```

### 11. Define rollout and rollback

If release risk exists, include:

- feature flag needs
- migration sequencing
- beta or staged rollout
- monitoring before expansion
- rollback conditions
- rollback steps
- data recovery considerations
- support notes

### 12. Record risks and decisions

Use two separate tables.

Decision log:

| ID | Decision | Basis | Alternatives rejected | Owner | Date / version |
|---|---|---|---|---|---|

Risk log:

| ID | Risk | Source | Impact | Mitigation | Owner | Blocks dev? |
|---|---|---|---|---|---|---|

Do not bury risks inside prose.

### 13. Prepare dev-facing handoff notes

Summarize what dev should use:

- implementation areas
- source artifacts
- non-goals
- constraints
- validation requirements
- open blockers
- contradictions to resolve
- suggested order of work

Hand off to `sdlc-dev-handoff-planning` for task card creation.

## Output

Return or write:

```markdown
# Solution Spec: <Feature / System>

## 1. Document Control
## 2. Source Requirements and Constraints
## 3. Goals and Non-goals
## 4. System Context
## 5. Architecture Approach
## 6. Interface / API Approach
## 7. Data and State Approach
## 8. Module / Directory Approach
## 9. LLD-oriented Implementation Notes
## 10. Validation Strategy
## 11. Rollout and Rollback
## 12. Architecture / Domain Artifact Links
## 13. Decision Log
## 14. Risk Log
## 15. Open Questions
## 16. Dev Handoff Notes
```

## Validation

Before calling the solution spec ready:

- Every major solution element links to SRS, NFR, SPEC, or an explicit constraint.
- Goals and non-goals are technical/solution-scoped, not product scope drift.
- Assumptions are marked as assumptions.
- Repo-dependent claims are evidence-grounded or marked as proposed.
- Alternatives are recorded for major decisions.
- HLD, LLD, ADR, Domain Boundary Map, and Directory SPEC are linked when present or marked missing when needed.
- Data, permission, security, privacy, observability, and release impact were considered when relevant.
- Validation strategy covers changed behavior and blocking NFRs.
- Rollout and rollback are included when release risk exists.
- Open questions are separated from decisions.
- Dev handoff notes are concrete enough for `sdlc-dev-handoff-planning`.

## Boundaries

- Do not edit code.
- Do not run tests as part of this skill.
- Do not approve or reject product scope.
- Do not override SRS, NFR, or SPEC artifacts without an explicit change-control path.
- Do not claim final repository fit without evidence.
- Do not use this workflow to hide missing HLD, LLD, ADR, or domain-boundary work that should be authored explicitly.
- Do not require dev sign-off for the SRS; dev should consume artifacts and report blockers or contradictions.
- Do not turn this skill into a project management plan. Use it to make implementation context precise.

## Handoff

Route downstream:

| Need | Next skill |
|---|---|
| missing software requirements | `sdlc-srs-workflow` |
| missing measurable quality requirements | `sdlc-nfr-spec` |
| missing HLD | `sdlc-hld-workflow` |
| missing LLD | `sdlc-lld-workflow` |
| missing domain boundary or ownership map | `sdlc-domain-boundary-modeling` |
| missing modular monolith structure | `sdlc-modular-monolith-architecture` |
| missing architecture decision record | `sdlc-architecture-decision-record` |
| missing UI/API/Data/Admin/Permission slices | `sdlc-spec-slice-writer` |
| executable implementation task package | `sdlc-dev-handoff-planning` |
| requirement-to-task/test traceability | `sdlc-requirements-traceability` |
| readiness judgment | `sdlc-readiness-review` |

When handing off to dev, provide:

1. source artifact list
2. solution goals and non-goals
3. component or module map
4. architecture and domain constraints
5. allowed and forbidden dependencies
6. validation requirements
7. risk log
8. open blockers
9. suggested implementation order
