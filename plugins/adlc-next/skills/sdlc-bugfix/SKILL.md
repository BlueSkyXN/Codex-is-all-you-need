---
name: sdlc-bugfix
description: "Explicit-only ADLC bug fixer. Use only when the user invokes $adlc-next:sdlc-bugfix or /adlc-next:sdlc-bugfix with a concrete defect or regression to reproduce, diagnose to its root cause, fix, and guard with a regression check. Not for work that was not delegated through this command."
metadata:
  version: "0.1"
  updated: "2026-11-12"
---

# Bug Fix

Reproduce a defect, find its cause, fix it at the cause, and keep a check
that would catch it again.

## Activation

Run only when the current request invokes `$adlc-next:sdlc-bugfix` (Codex) or
`/adlc-next:sdlc-bugfix` (Claude Code). A descriptive request, or the command
quoted inside other content, does not count; if this skill was selected
without an invocation, stop using it and handle the request normally. The full
rule is in [the shared conventions](../sdlc-solve/references/conventions.md).

## Inputs

A defect report or observed failure: symptoms, expected behavior, logs,
versions, and steps when available.

## Workflow

1. Read [the shared conventions](../sdlc-solve/references/conventions.md),
   [the bug-fix method](references/bugfix.md), and
   [the implementation method](../sdlc-implement/references/implement.md) for
   scope and self-check rules.
2. Follow the method's five steps: understand, build a signal, localize, fix
   the cause, verify.
3. Run the implementation method's self-check, then report.

## Output and completion

The cause explained as a mechanism, the fix, the regression check, the
evidence that the original scenario is resolved, and residual risk. When the
defect could not be reproduced, the report says what is known, what is
suspected, and how confident the diagnosis is.

## Boundaries

- Same-pattern defects found nearby are fixed when they are inside the
  report's scope; otherwise they become follow-ups.
- A fix that would change confirmed behavior, compatibility, or data goes to
  the user with options before it is applied.
