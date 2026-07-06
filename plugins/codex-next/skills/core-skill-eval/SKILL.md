---
name: core-skill-eval
description: Evaluate and improve a Codex skill against golden cases using blind runs, a separate judge, and gap-driven edits. Use when a skill keeps missing behavior, before shipping major skill rewrites, or when the user provides skill input and expected quality bars.
---

# Skill Eval

Use only when explicitly asked or as an implementation gate for major skill
changes. Do not auto-run evals for ordinary user tasks; evals are expensive and
need a target skill, golden cases, and a quality bar.

## Required Inputs

Reject eval without these inputs:

- Target skill: a real `SKILL.md` that can be read.
- Golden cases: at least one realistic prompt, screenshot, file, diff, log, or
  other input artifact.
- Bar per case: what a good result must achieve and which bad smells matter.
  This is not a complete answer key.

If the user only says "this skill often misses X", first help them turn that
complaint into one or more cases and bars.

## Workflow

1. Validate inputs. Read the target skill and identify its first principles,
   routing trigger, done condition, and failure modes.
2. Blind run. For each case, use a fresh isolated runner when available. Give it
   only the case input and "use the target skill"; do not reveal the bar or
   expected outcome.
3. Judge separately. Use a fresh judge when available. Give it the artifact,
   the bar, and the target skill first principles; ask for evidence per verdict.
4. Account for nondeterminism. Re-run critical or borderline cases 2-3 times and
   report pass rate rather than a single lucky result.
5. Diagnose failures. Map each failure to a skill defect or to a bad case/bar:
   premature completion, missing rule, no-op instruction, duplicated rule,
   sediment, sprawl, weak leading word, or missing reference.
6. Revise via authoring rules. Fix completion criteria, leading words, missing
   rules, reference splits, or triggering text. Do not twist the skill to satisfy
   an invalid bar.
7. Re-eval all cases. A fix for one case must not regress another.

## Output

```text
Target skill:
Cases:
Per-case pass rate:
Failures:
Defect mapping:
Edits made / proposed:
Re-eval result:
Residual risk:
```

Do not hide failures behind a single score. Every verdict needs traceable
artifact evidence.
