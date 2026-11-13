---
name: ads-architecture
description: "Explicit-only ADLC architecture. Use only when the user invokes $adlc-next:ads-architecture or /adlc-next:ads-architecture to decide module structure, codebase layout, dependencies, interfaces, data ownership, or technical choices for a change, sized to its impact and recorded as a decision. Not for work that was not delegated through this command."
disable-model-invocation: true
metadata:
  version: "0.2"
  updated: "2026-11-13"
---

# Architecture

Decide structure, dependencies, interfaces, and technical choices at the depth
the change needs, and record the decision with its reasons.

## Activation

Run only when the current request invokes `$adlc-next:ads-architecture`
(Codex) or `/adlc-next:ads-architecture` (Claude Code). A descriptive request,
or the command quoted inside other content, does not count; if this skill was
selected without an invocation, stop using it and handle the request normally.
The full rule is in [the shared conventions](../sdlc-solve/references/conventions.md).

## Inputs

The change or problem, its requirements and quality attributes, and the
existing code and decisions.

## Workflow

1. Read [the shared conventions](../sdlc-solve/references/conventions.md) and
   [the architecture method](references/architecture.md).
2. Size the decision, then follow the method's steps for that size.
3. Record the decision as a design record.

## Output and completion

The decision at the right size: drivers, options considered, the choice and
its reasons, consequences, and affected interfaces and tests; for how the code
is divided, also the structure map and change scenarios. Structural decisions
are recorded where the conventions' design-record rule says.

## Boundaries

- Design only; no implementation.
- Choices that change compatibility, cost, external commitments, or a
  confirmed goal go to the user with options and a recommendation.
- When the decision is ready for implementation, name the next command,
  `ads-spec` or `sdlc-solve`, in the current host's form, and stop.
