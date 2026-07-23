---
name: sdlc-modular-monolith-architecture
description: Use to design modular monolith boundaries, module layout, dependency rules, shared/platform seams, and extraction triggers.
metadata:
  version: "0.5"
  updated: "2026-07-23"
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
- When boundaries or split decisions are contested, read
  [Modularity and Coupling Heuristics](references/modularity-and-coupling.md).

## Workflow

1. Confirm why modular monolith is appropriate.
2. Map domains to modules using business capability, data invariants, reasons to
   change, and corroborating co-change evidence as cohesion signals.
3. Classify material code, data, control, temporal, semantic, deployment,
   runtime, and organizational coupling.
4. Distinguish intentional coupling that protects a required constraint from
   accidental coupling caused by leakage, implicit order, or unclear ownership.
5. Define each module's internal layers.
6. Define shared/platform boundaries.
7. Define allowed and forbidden dependencies.
8. Define public module interfaces.
9. Define data ownership and migration boundaries.
10. Define future extraction criteria for microservices.

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
- An ordinary change does not fan out across unrelated modules.
- The module dependency graph is acyclic, or a temporary cycle and its removal
  plan are explicit.
- Shared/platform areas have coherent consumers, owners, and reasons to change.
- Material temporal, semantic, data, and deployment coupling is visible rather
  than hidden behind an interface or service boundary.
- Future microservice extraction is possible but not premature.

## Output

Return:

1. Modular monolith rationale
2. Proposed directory structure
3. Module responsibility map
4. Dependency rules
5. Data ownership rules
6. Shared/platform rules
7. Coupling assessment: coupling type, evidence, risk, and recommended seam
8. Migration notes
9. Future extraction triggers

## Boundaries

- Do not recommend microservices without operational and organizational reasons.
- Do not redesign unrelated modules.
- Do not require modular-monolith design for small direct-dev fixes.
- Do not edit code.

## Handoff

Use `directory-spec` via `sdlc-spec-slice-writer`, then `sdlc-dev-handoff-planning` for executable tasks.

Dev fallback: Dev can use SDLC / ADD / DDD / SDD materials when they exist, but dev can also continue without them when the task is clear, bounded, and testable from user request, issue, bug report, failing test, local diff, or repository evidence. Missing artifacts are risk/context, not automatic refusal.
