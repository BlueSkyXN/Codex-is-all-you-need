---
name: sdlc-handoff
description: "Explicit-only ADLC handoff. Use only when the user invokes $adlc-next:sdlc-handoff or /adlc-next:sdlc-handoff to prepare an in-progress software task so another session, agent, or person can continue it without the original conversation. Not for work that was not delegated through this command."
metadata:
  version: "0.1"
  updated: "2026-11-12"
---

# Handoff

Prepare an in-progress task so that someone who never saw the conversation can
continue it: the state is written down and the matching code is reachable.

## Activation

Run only when the current request invokes `$adlc-next:sdlc-handoff` (Codex) or
`/adlc-next:sdlc-handoff` (Claude Code). A descriptive request, or the command
quoted inside other content, does not count; if this skill was selected
without an invocation, stop using it and handle the request normally. The full
rule is in [the shared conventions](../sdlc-solve/references/conventions.md).

## Inputs

The task in progress: the current conversation, an existing task file, the
repository state, and the receiver's situation when known (same workspace,
another workspace, another person).

## Workflow

1. Read [the shared conventions](../sdlc-solve/references/conventions.md) and
   [the handoff method](references/handoff.md).
2. Collect the state, write or update the task file, and make the code state
   reachable, as the method describes.
3. Run the method's receiver test and fix the file until it passes.

## Output and completion

The task file location, the transfer steps for code and material, and
anything that could not be transferred. The receiver test passes.

## Boundaries

- Record decisions and state that already exist; do not create new
  requirements or continue the implementation.
- Commits, pushes, or uploads needed for a transfer follow the conventions'
  authorization rule. When they are not authorized, describe the transfer and
  name the gap.
