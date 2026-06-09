---
name: domain-boundary-modeling
description: "Use to identify DDD-style bounded contexts, business capabilities, module ownership, domain data, domain language, allowed interactions, and forbidden dependencies before architecture or implementation."
---

# Domain Boundary Modeling


Use this skill to model business-domain boundaries for a modular system.

## Use when

- The system has multiple business capabilities.
- Modules should be organized by domain rather than only technical layers.
- There is risk of business rules spreading across unrelated modules.
- The user asks for DDD, bounded contexts, domain model, domain boundary map, or module ownership.

## Inputs

- BRD/URS/PRD/SRS.
- Existing project capability map.
- Current modules, routes, APIs, schemas, and terminology.
- Business workflows, roles, states, and rules.

## Workflow

1. Extract business capabilities.
2. Identify candidate domains and bounded contexts.
3. Define each domain's responsibility.
4. Define data ownership.
5. Define exposed interfaces.
6. Define allowed dependencies and forbidden access.
7. Build a shared domain glossary.
8. Identify ambiguous concepts that need owner decisions.

## Validation

Check:

- Each domain has one clear business responsibility.
- Data ownership is not duplicated without reason.
- Cross-domain calls are explicit.
- Shared concepts are named consistently.
- Forbidden dependencies are documented.
- The model supports modular monolith first unless microservices are justified.

## Output

Return:

1. Domain boundary map
2. Bounded context list
3. Data ownership map
4. Allowed dependency map
5. Forbidden dependency list
6. Domain glossary
7. Module naming proposal
8. Open questions

## Boundaries

- Do not implement code.
- Do not force DDD patterns into a simple script or small local task.
- Do not create microservices merely because domains exist.
- Do not require full DDD artifacts for direct-dev tasks.

## Handoff

Use `modular-monolith-architecture` to map domains into repository structure, `hld-workflow` for architecture, and `dev-handoff-planning` for tasks.

Dev fallback: Dev can use SDLC / ADD / DDD / SDD materials when they exist, but dev can also continue without them when the task is clear, bounded, and testable from user request, issue, bug report, failing test, local diff, or repository evidence. Missing artifacts are risk/context, not automatic refusal.
