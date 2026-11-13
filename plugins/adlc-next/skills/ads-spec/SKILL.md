---
name: ads-spec
description: "Explicit-only ADLC spec writer. Use only when the user invokes $adlc-next:ads-spec or /adlc-next:ads-spec to turn confirmed goals and design decisions into observable behaviors, edge and failure cases, and completion criteria with a verification method for each. Not for work that was not delegated through this command."
disable-model-invocation: true
metadata:
  version: "0.1"
  updated: "2026-11-13"
---

# Spec

Turn confirmed goals and design decisions into observable behaviors and
completion criteria that implementation and review both use.

## Activation

Run only when the current request invokes `$adlc-next:ads-spec` (Codex) or
`/adlc-next:ads-spec` (Claude Code). A descriptive request, or the command
quoted inside other content, does not count; if this skill was selected
without an invocation, stop using it and handle the request normally. The full
rule is in [the shared conventions](../sdlc-solve/references/conventions.md).

## Inputs

Confirmed requirements, design decisions, domain rules, and the existing
behavior that must stay.

## Workflow

1. Read [the shared conventions](../sdlc-solve/references/conventions.md) and
   [the spec method](references/spec.md).
2. Write each behavior with its source and verification method, then run the
   method's checks.
3. Record the spec as a design record, or in the task file for task-sized
   work.

## Output and completion

A spec in which every in-scope requirement maps to observable items, each
with a verification method, covering normal, edge, failure, and preserved
behavior; its location is recorded.

## Boundaries

- The spec states behavior, not implementation, unless the implementation is
  itself the requirement.
- Gaps or conflicts in the confirmed requirements go to the user; do not fill
  them with new scope.
- When the spec is ready, name the next command, `sdlc-implement` or
  `sdlc-solve`, in the current host's form, and stop.
