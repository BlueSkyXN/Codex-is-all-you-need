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
sdlc-manager
sdlc-project-research
sdlc-router
sdlc-requirements-workflow
sdlc-brd-workflow
sdlc-urs-workflow
sdlc-prd-workflow
sdlc-nfr-spec
sdlc-srs-workflow
sdlc-hld-workflow
sdlc-lld-workflow
sdlc-domain-boundary-modeling
sdlc-modular-monolith-architecture
sdlc-architecture-decision-record
sdlc-solution-spec-workflow
sdlc-spec-slice-writer
sdlc-dev-handoff-planning
sdlc-requirements-traceability
sdlc-readiness-review
sdlc-change-control
```

## Lane and material depth

```text
快线: dev-bugfix, small repair, config, copy, clear issue
增补: contained feature, small module, local behavior change
重构: behavior-preserving structural change
重建: replacement, rewrite, migration, capability remapping
从头: greenfield project or new subsystem
```

Use ADS to judge Architecture, Domain, and Specification impact. Choose the
smallest sufficient material set; lanes are not global dev blockers.

## Handoff to dev

The preferred handoff is:

```text
requirements package / NFR / SPEC / RTM / Dev Handoff
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
