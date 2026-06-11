---
name: sdlc-modular-monolith-architecture
description: "Use to design a DDD-style modular monolith architecture, defining module layout, dependency rules, shared/platform boundaries, and future microservice extraction points."
---

# Modular Monolith Architecture


Use this skill to design or refine a modular monolith.

## Use when

- The system should be modular but not yet split into microservices.
- Domains are known and need repository structure.
- AI/dev needs directory and dependency rules before implementation.
- The user asks for modular monolith, module architecture, code structure, or service extraction path.

## Inputs

- Domain boundary map.
- HLD, SRS, NFR, Directory SPEC, existing repo map.
- Current framework and deployment model.

## Workflow

1. Confirm why modular monolith is appropriate.
2. Map domains to modules.
3. Define each module's internal layers.
4. Define shared/platform boundaries.
5. Define allowed and forbidden dependencies.
6. Define public module interfaces.
7. Define data ownership and migration boundaries.
8. Define future extraction criteria for microservices.

## Suggested structure

```text
src/
  modules/
    <domain>/
      api/
      application/
      domain/
      infrastructure/
  shared/
  platform/
```

## Validation

Check:

- Deployment remains simple.
- Modules are domain-aligned.
- Internal implementation is hidden from other modules.
- Shared code does not become a dumping ground.
- Future microservice extraction is possible but not premature.

## Output

Return:

1. Modular monolith rationale
2. Proposed directory structure
3. Module responsibility map
4. Dependency rules
5. Data ownership rules
6. Shared/platform rules
7. Migration notes
8. Future extraction triggers

## Boundaries

- Do not recommend microservices without operational and organizational reasons.
- Do not redesign unrelated modules.
- Do not require modular-monolith design for small direct-dev fixes.
- Do not edit code.

## Handoff

Use `directory-spec` via `sdlc-spec-slice-writer`, then `sdlc-dev-handoff-planning` for executable tasks.

Dev fallback: Dev can use SDLC / ADD / DDD / SDD materials when they exist, but dev can also continue without them when the task is clear, bounded, and testable from user request, issue, bug report, failing test, local diff, or repository evidence. Missing artifacts are risk/context, not automatic refusal.
