---
name: improvement-skill-eval
description: "Explicit-only ADLC skill evaluation. Use only when the user invokes $adlc-next:improvement-skill-eval or /adlc-next:improvement-skill-eval to test whether an agent skill triggers correctly and improves task outcomes, using representative cases written before running, a baseline, and judged results. Not for work that was not delegated through this command."
disable-model-invocation: true
metadata:
  version: "0.1"
  updated: "2026-11-13"
---

# Skill Eval

Test whether a skill triggers when it should, stays out when it should, and
improves the result of the tasks it is for.

## Activation

Run only when the current request invokes `$adlc-next:improvement-skill-eval`
(Codex) or `/adlc-next:improvement-skill-eval` (Claude Code). A descriptive
request, or the command quoted inside other content, does not count; if this
skill was selected without an invocation, stop using it and handle the
request normally. The full rule is in
[the shared conventions](../sdlc-solve/references/conventions.md).

## Inputs

The skill to evaluate (path or name), optional variants such as a proposed
edit, and optional cases from the user or from real use.

## Workflow

1. Read [the shared conventions](../sdlc-solve/references/conventions.md) and
   [the evaluation method](references/evaluation.md).
2. Read the skill completely, including its references, and any platform
   adapter that controls invocation.
3. Follow the method: define, build cases, run, judge, report. Include
   trigger cases from the skill's `description` and behavior cases from its
   body.

## Output and completion

The per-case results for each variant, the aggregate, notable failures with
excerpts, the smallest recommended edits, and the evidence type and sample
size.

## Scope of action

- The evaluation reports; it edits the skill only when the request asks for
  the fixes.
- When editing, follow the target repository's rules for skill versions and
  mirrors, and re-run the affected cases.
