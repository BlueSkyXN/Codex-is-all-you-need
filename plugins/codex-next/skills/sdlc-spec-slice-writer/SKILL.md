---
name: sdlc-spec-slice-writer
description: Use to write focused implementation SPEC slices for UI, API, data, admin, permissions, directory, observability, or release.
metadata:
  version: "0.4"
  updated: "2026-06-12"
---

# SPEC Slice Writer

Use this workflow when a requirement must be turned into one or more implementation-facing specification slices.

A SPEC slice is a narrow contract for one technical or product surface. It should be precise enough for dev agents to implement and validate, while remaining owned by the SDLC manager as a requirements artifact.

## Use when

- SRS requirements need UI, API, Data, Admin, Permission, Directory, Observability, Release, or other SPEC slices.
- A feature crosses frontend, backend, data, permissions, operations, or release surfaces.
- Dev needs surface-level contracts before building.
- Existing PRD/SRS material is too broad for direct implementation.
- A change affects external contracts, data shape, role behavior, auditability, rollout, or support.

## Do not use when

- The task only needs BRD, URS, PRD, or SRS.
- The task requires code implementation or direct repository edits.
- The needed artifact is a measurable NFR matrix. Use `sdlc-nfr-spec`.
- The needed artifact is a standalone HLD. Use `sdlc-hld-workflow`.
- The needed artifact is a standalone LLD. Use `sdlc-lld-workflow`.
- The needed artifact is a solution package that coordinates HLD/LLD/ADR/SPEC. Use `sdlc-solution-spec-workflow`.
- The task is to create dev tasks. Use `sdlc-dev-handoff-planning`.

## Inputs

Use the strongest available inputs:

- SRS
- NFR spec
- HLD
- LLD
- ADR
- Domain Boundary Map
- PRD
- approved scope baseline
- user flows and state tables
- field rules
- existing API or data docs
- repository map
- platform guidelines
- admin workflow requirements
- security and privacy constraints
- release or rollout requirements
- traceability seed

If inputs conflict, record the conflict and identify the controlling source.

## SPEC slice types

Choose only the slices required by the delivery profile and risk.

| Slice | Use for |
|---|---|
| UI SPEC | screens, components, states, copy, interactions, accessibility, responsive behavior |
| API SPEC | endpoints, payloads, auth, errors, idempotency, compatibility, rate limits |
| Data SPEC | fields, schema, lifecycle, retention, migration, import/export, data quality |
| Admin SPEC | admin workflows, support actions, moderation, operational controls |
| Permission SPEC | roles, visibility, access rules, ownership, tenant boundaries |
| Directory SPEC | module boundaries, file organization, package layout, naming constraints |
| Observability SPEC | events, logs, metrics, traces, alerts, audit events, dashboards |
| Release SPEC | rollout, feature flags, migration, rollback, app store or deployment notes |
| Copy SPEC | product copy, empty/loading/error/success/warning states, localization notes |
| Integration SPEC | external services, webhooks, partner APIs, sync behavior, failure modes |

## Workflow

### 1. Select SPEC slices

Create a slice routing table:

| Requirement / source | Required slice | Reason | Priority | Blocks dev? |
|---|---|---|---|---|

Do not create slices that are not needed. Each slice should have an implementation or validation purpose.

### 2. Assign slice IDs

Use stable IDs:

| Prefix | Slice |
|---|---|
| `UI` | UI SPEC |
| `API` | API SPEC |
| `DATA` | Data SPEC |
| `ADMIN` | Admin SPEC |
| `PERM` | Permission SPEC |
| `DIR` | Directory SPEC |
| `OBS` | Observability SPEC |
| `REL` | Release SPEC |
| `COPY` | Copy SPEC |
| `INT` | Integration SPEC |

Example:

```text
UI-001
API-001
DATA-001
PERM-001
```

### 3. Write UI SPEC when needed

Use this structure:

```markdown
## UI-001: <Screen / flow / component>

- Source REQ / VAL IDs:
- User goal:
- Entry points:
- Exit points:
- Screens / components:
- Primary flow:
- Alternate flows:
- State requirements:
- Field requirements:
- Copy requirements:
- Accessibility requirements:
- Responsive / platform behavior:
- Analytics / events:
- Acceptance criteria:
- Open questions:
```

State coverage table:

| State | Trigger | UI behavior | Copy | User action | System action |
|---|---|---|---|---|---|

Required UI states when relevant:

```text
initial
empty
loading
success
failure
validation error
permission denied
offline / timeout
conflict / duplicate
disabled / unavailable
```

### 4. Write API SPEC when needed

Use this structure:

```markdown
## API-001: <API contract>

- Source REQ / VAL IDs:
- Related HLD / domain owner:
- Purpose:
- Actor / client:
- Method and path:
- Authentication:
- Authorization:
- Request headers:
- Request body:
- Response body:
- Error responses:
- Idempotency:
- Rate limits:
- Compatibility:
- Observability:
- Acceptance criteria:
- Open questions:
```

Request / response table:

| Field | Type | Required | Validation | Notes |
|---|---|---|---|---|

Error table:

| Code | Condition | User/system meaning | Retryable? | Logging |
|---|---|---|---|---|

Do not define implementation framework or internal storage unless required by an approved constraint.
Do not invent API ownership or cross-module dependency direction when HLD or Domain Boundary Map is missing; mark the owner or boundary as a decision-needed gap.

### 5. Write Data SPEC when needed

Use this structure:

```markdown
## DATA-001: <Data object / dataset / event>

- Source REQ / VAL IDs:
- Related Domain Boundary / data owner:
- Related NFR / migration constraint:
- Data owner:
- Entity / table / document / event:
- Fields:
- Lifecycle:
- Retention:
- Privacy classification:
- Migration needs:
- Import/export:
- Data quality rules:
- Backfill or reconciliation:
- Acceptance criteria:
- Open questions:
```

Field table:

| Field | Type | Required | Default | Constraints | Retention | Privacy note |
|---|---|---|---|---|---|---|

Data lifecycle table:

| Event | State before | State after | Actor/system | Audit/log note |
|---|---|---|---|---|

### 6. Write Admin SPEC when needed

Use this structure:

```markdown
## ADMIN-001: <Admin workflow>

- Source REQ / VAL IDs:
- Admin roles:
- User/customer impact:
- Admin actions:
- Required confirmation:
- Audit log:
- Error handling:
- Abuse prevention:
- Support escalation:
- Acceptance criteria:
- Open questions:
```

Admin actions table:

| Action | Role | Preconditions | Result | Audit event | Reversible? |
|---|---|---|---|---|---|

### 7. Write Permission SPEC when needed

Use this structure:

```markdown
## PERM-001: <Permission area>

- Source REQ / VAL IDs:
- Related Domain Boundary:
- Related Security / Privacy NFR:
- Role model:
- Resource ownership:
- Visibility rules:
- Action rules:
- Tenant/account boundaries:
- Delegation rules:
- Audit requirements:
- Acceptance criteria:
- Open questions:
```

Permission matrix:

| Role / actor | View | Create | Edit | Delete | Export | Admin | Notes |
|---|---|---|---|---|---|---|---|

### 8. Write Directory SPEC when needed

Use this structure:

```markdown
## DIR-001: <Directory / module boundary>

- Source REQ / VAL IDs:
- Related HLD:
- Related LLD:
- Related Domain Boundary:
- Related ADR:
- Target repository or package:
- Existing convention:
- Proposed module boundary:
- Files or directories in scope:
- Files or directories out of scope:
- Naming constraints:
- Import / dependency constraints:
- Allowed dependencies:
- Forbidden dependencies:
- Migration notes:
- Acceptance criteria:
- Open questions:
```

Directory SPEC should constrain organization only when it reduces implementation ambiguity or protects existing architecture. It must reference HLD, LLD, Domain Boundary Map, ADR, modular-monolith guidance, or repository evidence when those materials exist. Do not invent a repository structure, module ownership, or dependency direction without evidence.

### 9. Write Observability SPEC when needed

Use this structure:

```markdown
## OBS-001: <Observability area>

- Source REQ / NFR / VAL IDs:
- User or business risk:
- Events:
- Logs:
- Metrics:
- Traces:
- Alerts:
- Dashboard:
- Audit trail:
- Retention:
- Acceptance criteria:
- Open questions:
```

Event table:

| Event | Trigger | Properties | Purpose | Privacy note |
|---|---|---|---|---|

Metric table:

| Metric | Type | Target / threshold | Dimension | Owner |
|---|---|---|---|---|

### 10. Write Release SPEC when needed

Use this structure:

```markdown
## REL-001: <Release / rollout>

- Source REQ / NFR / VAL IDs:
- Release target:
- Feature flag:
- Migration requirement:
- Rollout stages:
- Beta / dogfood:
- Monitoring:
- Rollback:
- Support readiness:
- App store / platform notes:
- Acceptance criteria:
- Open questions:
```

Rollout table:

| Stage | Audience | Entry criteria | Exit criteria | Rollback condition |
|---|---|---|---|---|

### 11. Cross-link slices

For each slice, add:

| Slice ID | Source REQ IDs | NFR / ARCH / DOM IDs | VAL IDs | Task candidate |
|---|---|---|---|---|

If two slices conflict, do not resolve silently. Record the conflict and the owner or decision needed.

When slices depend on architecture or domain ownership, cross-link them to related HLD, LLD, ADR, Domain Boundary Map, or Directory SPEC IDs.

## Output

Return or write one or more SPEC slices.

Recommended file names:

```text
ui-spec.md
api-spec.md
data-spec.md
admin-spec.md
permission-spec.md
directory-spec.md
observability-spec.md
release-spec.md
copy-spec.md
integration-spec.md
```

When writing a combined document, use:

```markdown
# SPEC Slices: <Feature / System>

## 1. Slice Routing
## 2. UI SPEC
## 3. API SPEC
## 4. Data SPEC
## 5. Admin SPEC
## 6. Permission SPEC
## 7. Directory SPEC
## 8. Observability SPEC
## 9. Release SPEC
## 10. Cross-slice Traceability
## 11. Open Questions
```

## Validation

Before calling slices ready:

- Each slice has a clear source requirement.
- Each slice has an ID.
- Each implementation-facing rule is testable or traceable.
- UI slices cover relevant states and copy.
- API slices cover auth, validation, errors, and compatibility.
- Data slices cover lifecycle, retention, migration, and privacy when relevant.
- Permission slices cover visibility and action rules.
- Directory, API, Data, and Permission slices reference HLD, LLD, Domain Boundary Map, ADR, or NFR inputs when those inputs exist.
- Observability slices collect only purposeful events and metrics.
- Release slices include rollback and monitoring when release risk exists.
- Cross-slice conflicts are recorded.
- Open questions are separated from decisions.

## Boundaries

- Do not edit repository code.
- Do not claim existing architecture conventions without reading evidence.
- Do not turn product requirements into unapproved architecture mandates.
- Do not duplicate full SRS or NFR content; link to it.
- Do not create every possible slice by default.
- Do not use a SPEC slice to bypass `sdlc-dev-handoff-planning`.

## Handoff

Route downstream:

| Need | Next skill |
|---|---|
| software requirement normalization | `sdlc-srs-workflow` |
| measurable quality constraints | `sdlc-nfr-spec` |
| standalone HLD | `sdlc-hld-workflow` |
| standalone LLD | `sdlc-lld-workflow` |
| domain ownership or boundary map | `sdlc-domain-boundary-modeling` |
| modular monolith directory/dependency structure | `sdlc-modular-monolith-architecture` |
| solution package coordination | `sdlc-solution-spec-workflow` |
| implementation task package | `sdlc-dev-handoff-planning` |
| traceability matrix | `sdlc-requirements-traceability` |
| readiness judgment | `sdlc-readiness-review` |

For dev handoff, provide:

1. selected slice IDs
2. source REQ IDs
3. related NFR IDs
4. acceptance criteria
5. related HLD, LLD, ADR, Domain Boundary, or Directory SPEC IDs
6. open questions
7. implementation constraints and forbidden scope
