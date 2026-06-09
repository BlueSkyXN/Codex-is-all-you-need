---
name: hld-workflow
description: "Use to create or refine High-Level Design / high-level architecture design from SRS, NFR, domain boundaries, project evidence, and architecture goals before detailed design or implementation."
---

# HLD Workflow


Use this skill to write high-level architecture design.

## Use when

- A feature/system affects multiple modules, APIs, data boundaries, integrations, deployment, security, privacy, performance, or observability.
- SRS/NFR exists and must be turned into architecture.
- The user asks for HLD, high-level design, architecture design, architecture doc, or technical design overview.
- AI/dev would otherwise guess module boundaries or dependency direction.

## Inputs

- SRS, NFR, PRD, SPEC slices, project research, existing architecture docs.
- Current repo map, module layout, API/data contracts, deployment notes.
- Domain boundary map if available.
- NFR targets and constraints.

## Workflow

1. Confirm scope and non-scope.
2. Extract NFRs that affect architecture.
3. Identify system context and external dependencies.
4. Define module/component boundaries.
5. Define data ownership and data flow.
6. Define API/control flow between modules.
7. Define trust boundaries, security/privacy constraints, and operational concerns.
8. Record alternatives, trade-offs, and architecture decisions.
9. Route details to LLD or SPEC slices.

## Validation

Check:

- HLD links to SRS/NFR/source evidence.
- Module boundaries are explicit.
- Data ownership is explicit.
- Cross-module communication is explicit.
- NFR-driven decisions are visible.
- Trade-offs are recorded.
- Dev can use this without guessing system shape.

## Output

Return:

1. HLD summary
2. System context
3. Component/module map
4. Data and control flow
5. Trust/security/privacy boundaries
6. NFR-driven architecture decisions
7. Alternatives and trade-offs
8. Required LLD/SPEC follow-ups
9. Open questions

## Boundaries

- Do not write implementation code.
- Do not replace LLD or SPEC slices.
- Do not invent repo architecture without evidence.
- Do not require HLD for every small direct-dev task.

## Handoff

Use `lld-workflow` for module details, `domain-boundary-modeling` for business ownership, `spec-slice-writer` for concrete UI/API/Data/Permission/Directory specs, and `dev-handoff-planning` when implementation tasks are ready.

Dev fallback: Dev can use SDLC / ADD / DDD / SDD materials when they exist, but dev can also continue without them when the task is clear, bounded, and testable from user request, issue, bug report, failing test, local diff, or repository evidence. Missing artifacts are risk/context, not automatic refusal.
