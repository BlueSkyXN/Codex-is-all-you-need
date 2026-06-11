---
name: sdlc-nfr-spec
description: Use to define measurable non-functional requirements for performance, reliability, availability, security, privacy, accessibility, compatibility, observability, maintainability, compliance, and operational readiness.
---

# NFR Spec

Use this workflow when a software feature, system, release, or integration needs measurable non-functional requirements.

NFRs are quality and constraint requirements. They must be explicit, measurable where possible, and connected to validation. They should not be left as vague claims inside a PRD or SRS.

When an NFR changes architecture, it must be resolved before or during HLD. Do not leave performance, reliability, security, privacy, observability, or compatibility constraints as late implementation notes if they affect module boundaries, data flow, trust boundaries, deployment shape, or rollback strategy.

## Use when

- A requirement mentions performance, security, privacy, reliability, availability, scalability, compatibility, accessibility, maintainability, compliance, monitoring, logging, auditability, data retention, localization, rollout, or rollback.
- A product requirement must become verifiable engineering quality criteria.
- The release or platform has app store, compliance, privacy, security, SLO, SLA, or operational constraints.
- Dev needs thresholds, validation methods, or release gates.
- An existing NFR section is too vague to test.
- Architecture, HLD, LLD, or ADR work needs measurable quality inputs before design choices can be justified.

## Do not use when

- The task only needs product framing, BRD, URS, or PRD.
- The work is direct implementation, debugging, or PR review.
- The user asks for architecture decisions without a requirement source. Use `sdlc-hld-workflow`, `sdlc-architecture-decision-record`, or `sdlc-solution-spec-workflow` after NFRs are identified.
- The quality requirement cannot be evaluated yet because the product behavior is still undefined. Use `sdlc-srs-workflow` or `sdlc-prd-workflow` first.

## Inputs

Prefer these sources:

- PRD, SRS, or scope baseline
- platform constraints
- security/privacy requirements
- legal or compliance notes
- operational incident history
- existing SLO/SLA documents
- support requirements
- usage forecast
- expected traffic or data volume
- device/browser/platform support matrix
- launch plan or release requirements
- known production constraints
- prior performance, reliability, or security findings

If the input lacks measurable data, write a decision-needed NFR rather than inventing a target.

## NFR categories

Use only the categories relevant to the requested work.

| Category | Examples |
|---|---|
| Performance | latency, response time, startup time, page load, throughput, QPS, memory, CPU, energy |
| Scalability | users, tenants, data volume, concurrency, growth assumptions |
| Availability | uptime, maintenance window, degradation behavior |
| Reliability | failure handling, retries, consistency, durability, backup, recovery |
| Security | authn, authz, injection, secrets, threat model, abuse resistance |
| Privacy | PII, data minimization, consent, retention, deletion, third-party sharing |
| Compliance | audit, legal, platform policy, data residency, export or industry constraints |
| Accessibility | screen reader, keyboard, contrast, dynamic text, focus order, touch target |
| Compatibility | browser, OS, devices, API versions, backward compatibility |
| Maintainability | configuration, modularity, upgrade path, documentation, ownership |
| Observability | logs, metrics, traces, alerts, dashboards, audit trail |
| Operability | feature flags, rollout, rollback, support tools, runbook |
| Localization | language, date/time, currency, RTL, regional rules |
| Data quality | freshness, completeness, accuracy, lineage, reconciliation |

## Architecture impact

Route NFRs into architecture work when they affect structure or ownership:

| NFR area | Architecture impact |
|---|---|
| Performance | cache, async processing, indexing, queues, pagination, resource budgets |
| Reliability / availability | retry, fallback, circuit breaker, recovery, idempotency, backup strategy |
| Security | authentication, authorization, tenant isolation, secrets, audit, abuse controls |
| Privacy | data minimization, retention, deletion, anonymization, third-party boundaries |
| Observability | logs, metrics, traces, alerts, dashboards, audit trail |
| Compatibility | API versioning, schema migration, deprecation, feature flags, rollout strategy |

If the NFR implies a long-lived architecture decision or meaningful trade-off, create or request an ADR via `sdlc-architecture-decision-record`.

## Workflow

### 1. Confirm NFR scope

Write:

```text
Feature/system:
Delivery profile:
Target users:
Deployment or platform:
Release target:
Critical risk areas:
NFR categories in scope:
NFR categories out of scope:
```

If the system is consumer-facing, enterprise-facing, regulated, AI-driven, financial, health-related, or admin/security-sensitive, make the risk category explicit.

### 2. Extract quality claims

Read source materials and extract every quality claim, such as:

```text
fast
secure
reliable
low latency
privacy friendly
accessible
works offline
highly available
supports many users
safe for children
enterprise ready
app store ready
```

For each claim, decide whether it is:

| Type | Action |
|---|---|
| measurable requirement | convert to NFR |
| design principle | record as guidance |
| unresolved target | mark decision needed |
| unsupported claim | remove or flag |
| implementation detail | move to solution/design material |

### 3. Create NFR IDs

Use stable IDs:

| Prefix | Category |
|---|---|
| `NFR-PERF` | Performance |
| `NFR-SCALE` | Scalability |
| `NFR-AVAIL` | Availability |
| `NFR-REL` | Reliability |
| `NFR-SEC` | Security |
| `NFR-PRIV` | Privacy |
| `NFR-COMP` | Compliance |
| `NFR-A11Y` | Accessibility |
| `NFR-COMPAT` | Compatibility |
| `NFR-MAINT` | Maintainability |
| `NFR-OBS` | Observability |
| `NFR-OPS` | Operability |
| `NFR-L10N` | Localization |
| `NFR-DQ` | Data quality |

### 4. Write each NFR as a measurable requirement

Recommended structure:

```markdown
### NFR-PERF-001: <Requirement name>

- Source:
- Requirement:
- Measurement:
- Target:
- Floor threshold:
- Test or validation method:
- Environment:
- Frequency:
- Owner:
- Related REQ IDs:
- Related SPEC IDs:
- Architecture impact:
- Related HLD / LLD / ADR:
- Release impact:
```

A valid NFR should answer:

```text
What is constrained?
How is it measured?
What target must be met?
Where is it measured?
When is it measured?
Who owns validation?
What happens if it fails?
```

### 5. Define performance requirements

For performance-sensitive work, consider:

- user-perceived latency
- API latency
- p95 / p99 thresholds
- page load or app startup
- resource usage
- throughput
- concurrency
- data processing time
- background job timing
- battery or energy impact
- cold start and warm start differences

Use environment-specific targets. Do not compare local development timing with production requirements unless explicitly marked.

### 6. Define reliability and availability requirements

For reliability-sensitive work, consider:

- acceptable error rate
- retry behavior
- timeout behavior
- idempotency
- partial failure handling
- degraded mode
- backup and restore
- data durability
- queue or job recovery
- offline or weak network behavior
- manual recovery path

Distinguish:

```text
availability target
data correctness target
user-visible resilience
operator recovery
```

### 7. Define security and privacy requirements

For security-sensitive work, identify:

- authentication
- authorization
- role-based access
- tenant isolation
- input validation
- secret handling
- audit logging
- rate limiting or abuse protection
- data classification
- personal data fields
- consent and disclosure
- data retention and deletion
- third-party data sharing
- admin access
- compliance constraints

If security or privacy decisions are uncertain, record them as blocking open questions rather than guessing.

### 8. Define accessibility and compatibility requirements

For user-facing UI, consider:

- keyboard operation
- screen reader labels
- focus order
- color contrast
- dynamic text
- reduced motion
- error announcement
- touch target size
- browser and OS support
- mobile/desktop behavior
- viewport breakpoints
- localization impact

If accessibility is out of scope for a delivery profile, state who accepted that risk.

### 9. Define observability and operations requirements

For production-facing work, specify:

- logs to emit
- metrics to collect
- trace points
- dashboards
- alerts
- audit events
- operational runbook needs
- feature flag or config needs
- rollout and rollback monitoring
- support diagnostics

Observability requirements should be linked to user or business risk, not collected by default without purpose.

### 10. Build the NFR matrix

Use this table:

| NFR ID | Category | Requirement | Target / threshold | Validation | Release gate | Related SRS / SPEC |
|---|---|---|---|---|---|---|

Release gate values:

```text
blocker
required before full rollout
required before beta
recommended
monitor after launch
```

### 11. Record decisions and unknowns

Use:

| ID | Question / decision | Category | Blocks dev? | Blocks release? | Owner | Needed by |
|---|---|---|---:|---:|---|---|

Do not hide unknown thresholds. A requirement such as “performance must be good” is not ready; write it as an unresolved decision.

## Output

Return or write:

```markdown
# NFR Spec: <Feature / System>

## 1. NFR Scope
## 2. NFR Category Coverage
## 3. NFR Matrix
## 4. Performance Requirements
## 5. Reliability / Availability Requirements
## 6. Security / Privacy / Compliance Requirements
## 7. Accessibility / Compatibility Requirements
## 8. Observability / Operations Requirements
## 9. Release Gates
## 10. Decisions, Assumptions, and Open Questions
## 11. Handoff Notes
```

## Validation

Before calling the NFR spec ready, verify:

- Each NFR has an ID.
- Each P0/P1 NFR has a measurable target or a marked decision-needed gap.
- Each NFR has a validation method.
- Each release-blocking NFR has an owner or explicit owner-needed note.
- Architecture-impacting NFRs are marked for HLD, LLD, ADR, or solution package follow-up.
- Security, privacy, accessibility, and observability were considered when relevant.
- NFRs are linked to SRS/SPEC IDs when possible.
- Vague quality language has been removed or clarified.
- Unsupported compliance claims are not presented as facts.
- Release gates are explicit.

## Boundaries

- Do not implement code.
- Do not invent legal, compliance, security, or privacy requirements.
- Do not choose architecture merely to satisfy an NFR unless the architecture decision is already approved.
- Do not promise production performance without measurement or a defined test plan.
- Do not treat monitoring as a substitute for meeting a requirement.
- Do not replace `sdlc-solution-spec-workflow` or `sdlc-dev-handoff-planning`.

## Handoff

Route downstream:

| Need | Next skill |
|---|---|
| software requirement mapping | `sdlc-srs-workflow` |
| UI/API/Data/Admin/Permission/Directory slices | `sdlc-spec-slice-writer` |
| HLD | `sdlc-hld-workflow` |
| LLD | `sdlc-lld-workflow` |
| architecture decision record | `sdlc-architecture-decision-record` |
| solution package coordination | `sdlc-solution-spec-workflow` |
| implementation task package | `sdlc-dev-handoff-planning` |
| traceability | `sdlc-requirements-traceability` |
| readiness judgment | `sdlc-readiness-review` |

For dev handoff, provide:

1. NFR matrix
2. release-blocking NFRs
3. validation methods
4. environment assumptions
5. open decisions
6. architecture-impacting NFRs
7. links to related SRS/SPEC/HLD/LLD/ADR IDs
