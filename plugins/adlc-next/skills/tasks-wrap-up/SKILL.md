---
name: tasks-wrap-up
description: "Explicit-only ADLC batch wrap-up. Use only when the user invokes $adlc-next:tasks-wrap-up or /adlc-next:tasks-wrap-up to review a batch of work items or tasks against evidence: what finished, what is blocked, what was learned, what to adjust, and what the next batch should be. Not for work that was not delegated through this command."
disable-model-invocation: true
metadata:
  version: "0.1"
  updated: "2026-11-13"
---

# Wrap-Up

Review a batch of work against evidence and set up the next one.

## Activation

Run only when the current request invokes `$adlc-next:tasks-wrap-up` (Codex)
or `/adlc-next:tasks-wrap-up` (Claude Code). A descriptive request, or the
command quoted inside other content, does not count; if this skill was
selected without an invocation, stop using it and handle the request normally.
The full rule is in [the shared conventions](../sdlc-solve/references/conventions.md).

## Inputs

The batch: work items, ADLC task files, PRs, or a time period, plus the
location where the work items live.

## Workflow

1. Read [the shared conventions](../sdlc-solve/references/conventions.md) and
   [the work-item format](../tasks-intake/references/work-items.md). Establish
   which items belong to the batch.
2. For each item, establish the actual state from evidence: merged PRs,
   branches, verified results, and blockers. A status written in a file is not
   evidence on its own.
3. Collect what the batch revealed: defects, assumptions that failed,
   requirement changes, and external changes.
4. Decide what to adjust: items to re-scope, split, or drop, and decisions to
   revisit. Give the user the adjustments that change goals or priorities.
5. Turn follow-ups from task files and reviews into new items in the
   work-item format.
6. Note repeated friction, such as repeated investigation, rework, or
   unnecessary interruptions, as candidates for `improvement-retro`.
7. Update the item statuses at their location and write the wrap-up.

## Output and completion

A table of the batch's items with evidence-backed status, the blocked items
with what unblocks them, the new items, the decisions needed from the user, a
proposed next batch, and the method-improvement candidates.

## Boundaries

- Wrap-up does not start the next batch. To start an item, name the
  `sdlc-solve` command with it, in the current host's form, and stop.
- Writing to an external tracker follows the conventions' authorization rule.
