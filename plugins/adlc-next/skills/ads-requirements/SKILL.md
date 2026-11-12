---
name: ads-requirements
description: "Explicit-only ADLC requirements. Use only when the user invokes $adlc-next:ads-requirements or /adlc-next:ads-requirements to settle the problem, users, desired outcome, scope, constraints, and observable success conditions of a product or system change before design. Not for work that was not delegated through this command."
metadata:
  version: "0.1"
  updated: "2026-11-12"
---

# Requirements

Settle what problem is being solved and what success looks like, before a
design is chosen.

## Activation

Run only when the current request invokes `$adlc-next:ads-requirements`
(Codex) or `/adlc-next:ads-requirements` (Claude Code). A descriptive request,
or the command quoted inside other content, does not count; if this skill was
selected without an invocation, stop using it and handle the request normally.
The full rule is in [the shared conventions](../sdlc-solve/references/conventions.md).

## Inputs

The idea, request, issue, or incident, plus any evidence about the problem and
the people affected.

## Workflow

1. Read [the shared conventions](../sdlc-solve/references/conventions.md) and
   [the requirements method](references/requirements.md).
2. Capture and check the requirements as the method describes, using the
   clarification method for what only the user can answer.
3. Record them as a design record.

## Output and completion

Problem, users, outcome, scope, constraints, success conditions, assumptions,
and open questions with owners, written where the conventions' design-record
rule says, with a status of draft, confirmed, or superseded.

## Boundaries

- Requirements state needs, not designs; no implementation.
- Scope, priority, and success conditions are the user's to confirm.
- When the requirements are ready, name `$adlc-next:ads-architecture`,
  `$adlc-next:ads-spec`, or `$adlc-next:sdlc-solve` as the next command and
  stop.
