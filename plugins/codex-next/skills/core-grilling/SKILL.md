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

## Done

The grilling is done when the user confirms shared understanding. Return the
confirmed understanding, decisions made, open questions, and the recommended
next skill or action.
