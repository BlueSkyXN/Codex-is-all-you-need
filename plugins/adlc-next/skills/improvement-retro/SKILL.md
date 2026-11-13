---
name: improvement-retro
description: "Explicit-only ADLC retrospective. Use only when the user invokes $adlc-next:improvement-retro or /adlc-next:improvement-retro to analyze a finished task, session, PR, or batch for recurring friction and propose, or when asked apply, the smallest changes to docs, rules, skills, tools, or checks that prevent it. Not for work that was not delegated through this command."
disable-model-invocation: true
metadata:
  version: "0.1"
  updated: "2026-11-13"
---

# Retro

Find what repeatedly made the work slower, worse, or more dependent on the
user, and put the smallest fix where the next run will actually use it.

## Activation

Run only when the current request invokes `$adlc-next:improvement-retro`
(Codex) or `/adlc-next:improvement-retro` (Claude Code). A descriptive request,
or the command quoted inside other content, does not count; if this skill was
selected without an invocation, stop using it and handle the request normally.
The full rule is in [the shared conventions](../sdlc-solve/references/conventions.md).

## Inputs

A specific task, session, PR, or batch, with its evidence: task files,
transcripts or logs the user points to, review results, CI history, and the
method-improvement notes from ADLC reports. Without evidence, ask for the
material instead of reasoning from memory.

## Workflow

1. Read [the shared conventions](../sdlc-solve/references/conventions.md) and
   gather the evidence.
2. List the problems that actually happened, each with evidence and its cost:
   repeated investigation, failed attempts, rework, omissions caught late,
   unnecessary user interruptions, wrong skill triggers, and wasted tool calls
   or context.
3. Keep the problems that recur or are likely to recur. Note one-offs caused
   by the task itself and drop them.
4. For each kept problem, name the cause: documentation or navigation, a rule
   or instruction, a skill or template, a tool or check, feedback timing, or
   the task itself.
5. Choose the smallest effective change and put it where the next run reads
   or executes it:

   | Finding | Where the change goes |
   |---|---|
   | Business concept or rule misunderstood | Domain notes, glossary, and the related spec |
   | Defect can be reproduced reliably | A regression check, plus an implementation note if needed |
   | Code or material hard to find | Navigation in the README, instruction files, or links |
   | Existing check not wired in or documented wrongly | The project's check setup and its usage notes |
   | Same step missed across several kinds of task | A task template or a skill |
   | Skill misfires, or a prompt causes repetition or drift | Trigger description, method text, and evaluation cases |

6. For each change, state how the next similar task will show whether it
   worked, and when to remove it.

## Output and completion

A findings table with problem, evidence, cause, change, location, and how to
observe the effect, ranked by value. Every kept finding has all six.

## Scope of action

- A retro request delivers the analysis.
- When the request asks to apply the improvements, make the in-scope changes
  following [the implementation method](../sdlc-implement/references/implement.md).
  Changes to user-level instructions, other repositories, or shared
  configuration follow their own authorization and maintenance rules.
- A good change may shorten or remove a rule. Added text is not the measure
  of progress, and a lesson already carried by code, checks, or docs needs no
  extra note.
