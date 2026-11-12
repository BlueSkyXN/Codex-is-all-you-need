---
name: ads-survey
description: "Explicit-only ADLC project survey. Use only when the user invokes $adlc-next:ads-survey or /adlc-next:ads-survey to establish, with sources, how an existing project currently works on a question: structure, entry points, commands, existing decisions, constraints, and unknowns. Read-only. Not for work that was not delegated through this command."
metadata:
  version: "0.1"
  updated: "2026-11-12"
---

# Survey

Establish how the project currently stands on a question, with a source for
every finding and the unknowns named.

## Activation

Run only when the current request invokes `$adlc-next:ads-survey` (Codex) or
`/adlc-next:ads-survey` (Claude Code). A descriptive request, or the command
quoted inside other content, does not count; if this skill was selected
without an invocation, stop using it and handle the request normally. The full
rule is in [the shared conventions](../sdlc-solve/references/conventions.md).

## Inputs

The question to answer and the decision or task it serves; the project to
survey.

## Workflow

1. Read [the shared conventions](../sdlc-solve/references/conventions.md) and
   [the survey method](references/survey.md).
2. Frame the question, read the project in the method's order, and record
   findings with sources.
3. Report in the reply, or in the task file when the survey serves an ADLC
   task.

## Output and completion

The answer or the remaining unknowns; findings split into confirmed facts,
inferences, and unknowns, each with its source; the relevant entry points and
real commands; disagreements between documentation and code.

## Boundaries

- Read-only: read files and run read-only commands. Do not edit, install, or
  start services that change state.
- When the findings call for design or implementation, name the next ADLC
  command and stop.
