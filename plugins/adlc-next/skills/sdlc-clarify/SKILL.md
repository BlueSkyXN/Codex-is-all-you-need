---
name: sdlc-clarify
description: "Explicit-only ADLC clarifier. Use only when the user invokes $adlc-next:sdlc-clarify or /adlc-next:sdlc-clarify to pin down the goal, scope, constraints, acceptance, or delivery point of a software request before work starts. Produces a clarified brief and does not implement. Not for work that was not delegated through this command."
disable-model-invocation: true
metadata:
  version: "0.1"
  updated: "2026-11-13"
---

# Clarify

Turn an unclear software request into a brief someone can act on: confirmed
points, assumptions, and open items with who decides.

## Activation

Run only when the current request invokes `$adlc-next:sdlc-clarify` (Codex) or
`/adlc-next:sdlc-clarify` (Claude Code). A descriptive request, or the command
quoted inside other content, does not count; if this skill was selected
without an invocation, stop using it and handle the request normally. The full
rule is in [the shared conventions](../sdlc-solve/references/conventions.md).

## Inputs

The request and the material around it: conversation, issue, task file,
documentation, and code.

## Workflow

1. Read [the shared conventions](../sdlc-solve/references/conventions.md) and
   [the clarification method](references/clarify.md).
2. Sort the unknowns as the method describes: cite what the material already
   answers, investigate what can be investigated, and ask the user only what
   needs their intent or decision.
3. Write the brief into the task file when one exists, otherwise in the reply.

## Output and completion

A brief with the goal, scope and out of scope, constraints, acceptance
conditions, delivery point, assumptions, and open items with who decides.
Every point is confirmed with its source, assumed with a reason, or open with
an owner.

## Boundaries

- Clarification only: no implementation, and no design beyond what the
  questions need.
- When the brief is ready, name the next command, `sdlc-solve` or
  `sdlc-implement`, in the current host's form, and stop.
