# SDLC Manager Catalog

`SDLC Manager` is the Architecture-first SDLC control plane for software delivery. It owns BRD, URS, PRD, NFR, SRS, HLD, LLD, ADR, domain boundaries, SPEC, traceability, change control, readiness review, and dev handoff.

```text
Architecture defines structure.
Domain boundaries define ownership.
Specifications define execution.
```

## Boundary

```text
sdlc-manager
  owns: delivery contract, requirements, architecture/design artifacts, domain boundaries, specs, traceability, readiness, handoff

dev
  owns: repository mapping, implementation, tests, review, release validation
```

`SDLC Manager` does not replace `dev`.

`dev` consumes SDLC materials when they exist, but may still continue through direct-dev paths when no formal SDLC materials exist and the task is clear enough.

## Agents

```text
sdlc_project_researcher
sdlc_requirements_manager
sdlc_srs_specifier
sdlc_solution_spec_manager
sdlc_delivery_planner
sdlc_readiness_reviewer
sdlc_change_manager
```

## Skills

```text
project-research
artifact-profile-router
requirements-workflow
brd-workflow
urs-workflow
prd-workflow
nfr-spec
srs-workflow
hld-workflow
lld-workflow
domain-boundary-modeling
modular-monolith-architecture
architecture-decision-record
solution-spec-workflow
spec-slice-writer
dev-handoff-planning
requirements-traceability
sdlc-readiness-review
change-control
```

## Delivery artifact profiles

```text
Profile A: Task Delivery
Profile B: Feature Delivery
Profile C: System Delivery
Profile D: Program Delivery
```

These profiles define material depth. They are not global dev blockers.

## Handoff to dev

The preferred handoff is:

```text
SRS / NFR / SPEC / RTM / Dev Handoff
HLD / LLD / ADR / Domain Boundary Map when relevant
-> dev repo onboarding
-> implementation
-> validation
-> review
-> release check when needed
```

A valid direct-dev path is also allowed:

```text
issue / bug report / user request / repo evidence
-> dev repo onboarding or direct implementation
-> validation
-> review
```
