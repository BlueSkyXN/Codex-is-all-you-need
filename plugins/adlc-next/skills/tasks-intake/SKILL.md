---
name: tasks-intake
description: "Explicit-only ADLC work intake. Use only when the user invokes $adlc-next:tasks-intake or /adlc-next:tasks-intake to turn ideas, defects, review findings, feedback, or task follow-ups into deduplicated work items with outcomes, done conditions, dependencies, and a proposed order. Not for work that was not delegated through this command."
metadata:
  version: "0.1"
  updated: "2026-11-13"
---

# Intake

Turn scattered inputs into work items that can each be finished and verified
on their own, with dependencies and a proposed order.

## Activation

Run only when the current request invokes `$adlc-next:tasks-intake` (Codex) or
`/adlc-next:tasks-intake` (Claude Code). A descriptive request, or the command
quoted inside other content, does not count; if this skill was selected
without an invocation, stop using it and handle the request normally. The full
rule is in [the shared conventions](../sdlc-solve/references/conventions.md).

## Inputs

Any mix of notes, issues, review results, follow-ups from ADLC task files, user
feedback, and monitoring findings, plus the existing work items.

## Workflow

1. Read [the shared conventions](../sdlc-solve/references/conventions.md) and
   [the work-item format](references/work-items.md). Find where the project's
   items live, and read the existing ones so nothing is duplicated.
2. Merge duplicates and split any input that holds more than one outcome.
   Each item should be a slice that can be finished and verified on its own.
3. Fill in every field of the format for each item.
4. Order the items: dependencies first; among ready items, follow the user's
   stated priorities and arrange the execution order yourself. Ask only where
   a different order would change a business outcome, a commitment, or the
   effort involved.
5. Write the items to their location and report.

## Output and completion

The new and changed items with all fields, the proposed order with the
dependency reasons, the decisions needed from the user, and where the items
were written.

## Boundaries

- Intake arranges work and does not start it. To work on an item, name the
  `sdlc-solve` command with that item, in the current host's form, and stop.
- Steps inside one task stay in that task's file; intake handles the
  relationships between tasks.
- Business priority is the user's. Without stated priorities, propose an order
  and mark it as a proposal.
