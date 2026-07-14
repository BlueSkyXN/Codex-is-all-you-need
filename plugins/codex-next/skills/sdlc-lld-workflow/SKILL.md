---
name: sdlc-lld-workflow
description: Use to create or refine LLD for modules, interfaces, state machines, data structures, errors, transactions, and tests.
metadata:
  version: "0.3"
  updated: "2026-06-12"
---

# LLD Workflow


Use this skill to write detailed design for a bounded module or feature area.

## Use when

- HLD exists and module internals need design.
- A domain/module requires class/function/interface/data/state/error details.
- A complex feature needs implementation-near design before dev task cards.
- The user asks for LLD, detailed design, module design, algorithm design, or implementation design.

## Inputs

- HLD, SRS, NFR, SPEC slices, domain boundary map, directory spec.
- Existing code, interfaces, schemas, tests, and project conventions.
- Task constraints and validation expectations.

## Workflow

1. Select the module or bounded area.
2. Confirm related HLD/SRS/NFR/SPEC IDs.
3. Define module responsibilities and forbidden responsibilities.
4. Define interfaces, data structures, state transitions, and error behavior.
5. Define transaction, consistency, permission, and validation rules.
6. Define directory/file placement and dependency rules.
7. Define test points and expected validation.
8. Identify implementation risks and unresolved decisions.

## Validation

Check:

- Module responsibilities do not leak across domain boundaries.
- Data structures align with Data SPEC.
- API/interface details align with API SPEC.
- Permission checks align with Permission SPEC.
- State and error behavior are explicit.
- Tests can be derived from the design.

## Output

Return:

1. LLD summary
2. Module responsibility table
3. Interfaces and data structures
4. State/error/transaction rules
5. Directory and dependency notes
6. Test points
7. Implementation risks
8. Dev task candidates

## Boundaries

- Do not edit code.
- Do not expand beyond the selected module.
- Do not contradict HLD/SRS/SPEC without reporting it.
- Do not require LLD for small direct-dev bugfixes when repo evidence is enough.

## Handoff

Use `sdlc-dev-handoff-planning` to create implementation task cards. Use dev skills for coding.

Dev fallback: Dev can use SDLC / ADD / DDD / SDD materials when they exist, but dev can also continue without them when the task is clear, bounded, and testable from user request, issue, bug report, failing test, local diff, or repository evidence. Missing artifacts are risk/context, not automatic refusal.
