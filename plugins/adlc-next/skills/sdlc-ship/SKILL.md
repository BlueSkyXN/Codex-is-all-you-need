---
name: sdlc-ship
description: "Explicit-only ADLC delivery. Use only when the user invokes $adlc-next:sdlc-ship or /adlc-next:sdlc-ship to take an already verified change to a requested delivery point: commit, PR, merge, release or deployment, or verification in the real environment. Not for work that was not delegated through this command."
metadata:
  version: "0.1"
  updated: "2026-11-12"
---

# Ship

Take a verified change to the requested delivery point, stage by stage, with
evidence for each stage reached.

## Activation

Run only when the current request invokes `$adlc-next:sdlc-ship` (Codex) or
`/adlc-next:sdlc-ship` (Claude Code). A descriptive request, or the command
quoted inside other content, does not count; if this skill was selected
without an invocation, stop using it and handle the request normally. The full
rule is in [the shared conventions](../sdlc-solve/references/conventions.md).

## Inputs

- The change to deliver: working tree, branch, or commits.
- The requested delivery point. When it is not stated, use the project
  settings' `default_delivery_point`; when that is `local` or absent, ask
  which stage is wanted instead of guessing.
- The project's contribution, release, and deployment rules.

## Workflow

1. Read [the shared conventions](../sdlc-solve/references/conventions.md) and
   [the shipping method](references/ship.md).
2. Confirm the change is verified locally; re-run the checks when the code
   changed since the last run.
3. Run each stage up to the requested delivery point, only as far as the
   authorization reaches.
4. Report each stage reached with its evidence.

## Output and completion

The stage reached, with evidence for every stage on the way: commit hash, PR
link, CI result, merge commit, release identifier, or environment readback.
When work stops before the requested point, the report names the stage and
the reason.

## Boundaries

- Code changes are limited to fixing failures this change caused, following
  [the implementation method](../sdlc-implement/references/implement.md).
- Do not go past the requested delivery point, and do not treat an earlier
  stage's evidence as proof of a later one.
