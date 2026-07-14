---
name: core-grilling
description: Stress-test a plan or design through a focused one-question-at-a-time interrogation. Use when the user asks to grill a plan, wants assumptions challenged before build, or another workflow needs a plan clarified before it can proceed.
metadata:
  version: "0.1"
  updated: "2026-07-07"
---

# Grilling

Run a narrow design interrogation until the plan is explicit enough to act on.
Trace the decisions that depend on each other, resolve the next unresolved branch,
and keep the conversation anchored on one live uncertainty at a time.

## Rules

1. Ask exactly one load-bearing question per turn, then wait. A batch of
   questions hides which decision matters now.
2. Include your proposed answer or default in the question so the user can edit
   a concrete position instead of inventing one from scratch.
3. If repository evidence, docs, logs, data, or local files can answer the point,
   inspect those first and bring back the answer with the evidence.
4. Do not start implementing from the grilled plan until the user confirms the
   decision set.

## Done

Finish with the confirmed decision set, the assumptions that survived, anything
still open, and the next workflow or action that should consume the result.
