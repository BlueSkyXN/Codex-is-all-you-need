---
name: sdlc-test-first
description: "Explicit-only ADLC test-first driver. Use only when the user invokes $adlc-next:sdlc-test-first or /adlc-next:sdlc-test-first to build or change behavior through a red-green-refactor loop with automated tests. Not for work that was not delegated through this command."
disable-model-invocation: true
metadata:
  version: "0.1"
  updated: "2026-11-13"
---

# Test First

Build or change behavior one observable slice at a time: a failing test, the
minimal code that passes it, then a refactor with the tests green.

## Activation

Run only when the current request invokes `$adlc-next:sdlc-test-first`
(Codex) or `/adlc-next:sdlc-test-first` (Claude Code). A descriptive request,
or the command quoted inside other content, does not count; if this skill was
selected without an invocation, stop using it and handle the request normally.
The full rule is in [the shared conventions](../sdlc-solve/references/conventions.md).

## Inputs

The behaviors to build or change: a request, spec, issue, or task file. The
project's test framework and commands.

## Workflow

1. Read [the shared conventions](../sdlc-solve/references/conventions.md),
   [the test-first method](references/test-first.md), and
   [the implementation method](../sdlc-implement/references/implement.md) for
   scope and self-check rules.
2. List the behaviors as slices, smallest first.
3. Run the method's loop for each slice.
4. Run the implementation method's self-check, then report.

## Output and completion

Each delivered behavior with its test, the evidence that the test failed
before and passed after, the refactors made, and the checks run. Delivery
beyond `local` happens only when the request asks for it and it is authorized.

## Boundaries

- When a behavior cannot get a stable automated check, say why, verify it with
  the matching approach from the implementation method, and report the
  difference.
- The scope is the requested behaviors; other improvements become follow-ups.
