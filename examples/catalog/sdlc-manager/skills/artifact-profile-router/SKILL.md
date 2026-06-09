---
name: artifact-profile-router
description: Use to choose the smallest sufficient Delivery Artifact Profile and SDLC material set before creating requirements, specs, handoff packages, or implementation tasks.
---

# Artifact Profile Router

Use this skill before writing SDLC materials when the required artifact depth is unclear.

This skill decides which delivery artifacts are necessary. It does not write the artifacts themselves.

## Use when

- A request may require BRD, URS, PRD, NFR, SRS, HLD, LLD, Domain Boundary Map, ADR, SPEC, RTM, or dev handoff.
- The user asks whether a task needs formal requirements or can go directly to dev.
- The work involves multiple stakeholders, modules, APIs, data models, permissions, compliance, security, privacy, performance, release risk, or AI coding handoff.
- Existing materials are mixed, incomplete, or not clearly connected to implementation.

## Inputs

Read what is available:

- User request, issue, meeting notes, roadmap item, idea, support ticket, bug report, or business brief.
- Existing BRD / URS / PRD / SRS / NFR / HLD / LLD / ADR / Domain Boundary Map / SPEC / RTM / design docs / architecture notes.
- Existing repo evidence, if available.
- Delivery constraints: deadline, target release, stakeholders, platform, risk tolerance.
- Any stated must-haves, must-not-haves, acceptance criteria, or compliance constraints.

If inputs are missing, classify using the evidence available and mark assumptions explicitly.

## Delivery Artifact Profiles

### Profile A — Task Delivery

Use when the change is narrow, local, and already understandable.

Typical cases:

- Bug with clear reproduction or observed failure.
- Copy, config, small UI adjustment, or localized implementation task.
- Existing issue already has acceptance criteria.
- No meaningful product, API, data, security, or release ambiguity.

Required artifacts:

- Task brief.
- Acceptance criteria.
- Validation notes.

Usually skipped:

- BRD, URS, full PRD, HLD, LLD, RTM.

### Profile B — Feature Delivery

Use when a feature is product-facing or behavior-changing but contained.

Typical cases:

- Single feature or single module.
- New user flow, UI behavior, API endpoint, or data capture path.
- AI coding needs a stable scope and validation contract.
- Requirements are not yet precise enough for direct dev work.

Required artifacts:

- PRD or product requirement section.
- SRS requirement list with IDs.
- Needed SPEC slices, such as UI, API, Data, Permission, or Admin.
- Dev handoff with tasks and validation plan.

Usually optional:

- BRD, formal HLD, formal LLD, Domain Boundary Map, ADR, full RTM.

### Profile C — System Delivery

Use when the work affects multiple system boundaries.

Typical cases:

- Multi-module feature.
- API/data/permission changes.
- Non-functional requirements are material.
- Architecture or migration choices constrain implementation.
- Several dev agents or implementation phases are needed.

Required artifacts:

- BRD or business brief.
- URS.
- PRD.
- NFR.
- SRS.
- HLD when architecture, module, data, deployment, or trust boundaries are material.
- Domain Boundary Map when business ownership, data ownership, or cross-domain dependency risk exists.
- LLD for complex module internals, state, transactions, algorithms, or migration details.
- ADR for long-lived architecture decisions, meaningful alternatives, or rejected approaches.
- Needed SPEC slices.
- Requirements traceability matrix.
- Dev handoff.

### Profile D — Program Delivery

Use when the work is high-risk, multi-repo, multi-team, compliance-sensitive, launch-sensitive, or long-running.

Typical cases:

- Enterprise delivery, platform migration, security/privacy-sensitive work.
- Multiple releases or waves.
- Formal baseline and change control are needed.
- Release, rollback, support, metrics, or post-launch review is material.

Required artifacts:

- Full SDLC artifact set.
- Change control record.
- Requirements traceability matrix.
- Readiness review.
- Release and rollback criteria.
- Post-launch feedback plan.

## Workflow

1. Identify the work type.
   - Bugfix
   - Local task
   - Product feature
   - System feature
   - Refactor
   - Migration
   - Release
   - Compliance/security/privacy work
   - Research-to-spec work

2. Identify risk drivers.
   - User-visible behavior
   - Revenue or business impact
   - Data model or migration
   - Public API or SDK contract
   - Auth, permission, privacy, security, compliance
   - Performance, availability, reliability, accessibility
   - Architecture, module, dependency, or directory boundaries
   - Domain ownership, data ownership, or forbidden cross-domain access
   - NFR-driven architecture decision or ADR-worthy trade-off
   - Multi-team, multi-repo, or external dependency
   - Release, rollout, rollback, or support burden

3. Select a Delivery Artifact Profile.
   - Choose the lowest profile that fully covers the risk.
   - Do not escalate merely because a document family exists.
   - Do escalate when scope, validation, or ownership is ambiguous.

4. List required artifacts.
   - Required now
   - Required before dev
   - Required before release
   - Optional
   - Not needed for this profile

5. Route to next skills.
   - BRD: `brd-workflow`
   - URS: `urs-workflow`
   - PRD or combined requirements: `requirements-workflow` or `prd-workflow`
   - SRS: `srs-workflow`
   - NFR: `nfr-spec`
   - HLD: `hld-workflow`
   - LLD: `lld-workflow`
   - Domain Boundary Map: `domain-boundary-modeling`
   - Modular monolith structure: `modular-monolith-architecture`
   - ADR: `architecture-decision-record`
   - Solution package coordination: `solution-spec-workflow`
   - SPEC slices: `spec-slice-writer`
   - Dev handoff: `dev-handoff-planning`
   - RTM: `requirements-traceability`
   - Readiness: `sdlc-readiness-review`
   - Direct implementation: `spec-driven-implementation` or the relevant dev skill

## Validation

Before final routing, check:

- Is the chosen profile sufficient for all visible risk drivers?
- Are scope and non-scope clear enough for the next skill?
- Are acceptance criteria required before dev starts?
- Does the work need traceability to tasks, tests, PRs, or release?
- Does the work need HLD, LLD, ADR, Domain Boundary Map, or modular-monolith guidance before dev would otherwise guess structure or ownership?
- Are any documents being requested only out of habit rather than delivery need?
- Are any skipped artifacts actually required by risk, compliance, or cross-team coordination?

## Output

Return:

1. Delivery Artifact Profile: A / B / C / D
2. Rationale
3. Required artifacts
4. Optional artifacts
5. Artifacts not needed and why
6. Next skills to use
7. Required decisions before dev
8. Risks if implementation starts now

## Boundaries

- Do not write BRD, URS, PRD, SRS, NFR, SPEC, RTM, or handoff content here.
- Do not weaken artifact needs to accelerate coding.
- Do not inflate artifact needs to imitate a heavy process.
- Do not call an artifact optional when it is needed to make implementation testable, traceable, or safe.
