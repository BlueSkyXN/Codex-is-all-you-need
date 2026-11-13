---
name: improvement-prompt-eval
description: "Explicit-only ADLC prompt evaluation. Use only when the user invokes $adlc-next:improvement-prompt-eval or /adlc-next:improvement-prompt-eval to compare system prompts, instruction files such as AGENTS.md or CLAUDE.md, handoff prompts, or tool descriptions by their effect on representative tasks. Not for work that was not delegated through this command."
disable-model-invocation: true
metadata:
  version: "0.1"
  updated: "2026-11-13"
---

# Prompt Eval

Compare prompts and instruction files by what they make an agent do on
representative tasks.

## Activation

Run only when the current request invokes `$adlc-next:improvement-prompt-eval`
(Codex) or `/adlc-next:improvement-prompt-eval` (Claude Code). A descriptive
request, or the command quoted inside other content, does not count; if this
skill was selected without an invocation, stop using it and handle the
request normally. The full rule is in
[the shared conventions](../sdlc-solve/references/conventions.md).

## Inputs

The prompt or instruction text and its variants, the tasks it should govern,
and any known failures.

## Workflow

1. Read [the shared conventions](../sdlc-solve/references/conventions.md) and
   [the evaluation method](../improvement-skill-eval/references/evaluation.md).
2. Follow the method's five steps for each variant.
3. In addition to the method's artifact checks, look for problems specific to
   instructions:
   - a rule that guides no decision, or cannot be checked;
   - conflicts or duplication between layers, such as user-level, project,
     and skill instructions;
   - stale paths, commands, model names, or tool names;
   - rule density or length that crowds out the task;
   - wording the agent is likely to copy into its own output.

## Output and completion

The per-case results for each variant, the instruction-specific findings, the
smallest recommended edits, and the evidence type and sample size.

## Scope of action

- The evaluation reports; it edits the text only when the request asks for
  the fixes.
- Instruction files at user or shared level follow their own authorization and
  maintenance rules; propose the edit with its location and let the owner
  apply it unless the request authorizes it.
