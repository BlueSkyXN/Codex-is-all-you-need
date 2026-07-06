---
name: core-grilling
description: Grill the user relentlessly about a plan or design, one question at a time, until shared understanding is reached. Use when the user wants to stress-test a plan before building, uses a "grill" trigger phrase, or when another skill needs to interrogate an ambiguous plan/design before proceeding.
---

# Grilling

Interview the user relentlessly about every aspect of the plan or design until
you reach shared understanding. Walk down each branch of the design tree,
resolving dependencies between decisions one by one.

## Rules

1. Ask one question at a time. Wait for feedback before the next; bundles of
   questions are bewildering.
2. Carry your recommended answer in every question. Do not ask open-endedly:
   propose, then let the user correct.
3. If code, docs, logs, data, or local files can answer the question, explore
   them instead of asking.
4. Do not enact the plan until the user confirms the shared understanding.

## Composition

Other skills can reach for grilling at ambiguous points:

- `sdlc-requirements-workflow` - after the three-perspective check
- `sdlc-readiness-review` - before the verdict
- `sdlc-prd-workflow` - when freezing the scope baseline
- `sdlc-hld-workflow` - at solution trade-offs
- `dev-migration-plan` - at strategy selection
- `dev-refactor-plan` - when confirming the behavior contract

## Output

When the grilling loop ends, return:

1. Confirmed understanding
2. Decisions made
3. Open questions
4. Recommended next skill or action
