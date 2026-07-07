---
name: core-explore-unknowns
description: Build an unknowns map before implementation. Use when the request is underspecified, the repo or domain is unfamiliar, the user needs something concrete to react to, or new facts discovered midstream need to be captured before continuing. Pairs with core-grilling; this skill creates the map, while grilling interrogates an existing plan.
---

# Explore Unknowns

Treat the prompt and any plan as a rough map, not the ground itself. The ground
is the current code, domain constraints, and what the user actually means. This
workflow closes the gap before implementation turns vague assumptions into code.

The deliverable is a four-part unknowns map. Move through the quadrants in order,
collecting evidence and user decisions, then hand the map over as the input to
the next workflow. Do not treat the walk itself as permission to build.

Two moves apply at every stage:

- Prefer reactable material over abstract questioning: a small sample, option
  table, or concrete draft will surface taste and constraints faster than "what
  do you want?"
- Shape each artifact so the user's next reply is easy: short options, check
  boxes, or a draft message they can correct.

## The Quadrant Walk

Five stages run in order. **Open the reference file for the current stage before
working that stage.** Name the quadrant you are in, close it visibly, then move
on.

1. **[Known knowns](references/stage-1-known-knowns.md)** — scan the territory,
   then open with the settled ground.
2. **[Known unknowns](references/stage-2-known-unknowns.md)** — the questions
   you can name; resolve them one at a time.
3. **[Unknown knowns](references/stage-3-unknown-knowns.md)** — extract the
   taste and tacit context nobody has put into words.
4. **[Unknown unknowns](references/stage-4-unknown-unknowns.md)** — sweep the
   territory for landmines.
5. **[Hand over the map](references/stage-5-hand-over-the-map.md)** — assemble
   the complete map; this is the only finish line.

When the mapped work moves into build, review, or merge, read
[after the walk](references/after-the-walk.md): deviations found during
implementation are filed back into the map, reviewers get a buy-in package,
and long diffs get a merge-readiness check.

## Rules

- Preserve stage order, but do not hide useful information because "its stage"
  is later. Disclose decision-relevant facts immediately, then file them in the
  right quadrant.
- A decision is not closed until the user has seen the question and the proposed
  answer, even if local evidence supplied the answer.
- Ground repo or product claims in files, logs, docs, or data that were actually
  read. Label illustrative examples as illustrative.
- Pause at stage boundaries when the next step depends on user reaction. Do not
  implement from unconfirmed map entries.
