---
name: core-skill-eval
description: Test and improve a Codex skill with representative cases, isolated runs, independent judging, and edits driven by observed misses. Use when a skill repeatedly misses behavior, before shipping a major skill rewrite, or when the user supplies cases and quality bars.
metadata:
  version: "0.2"
  updated: "2026-07-08"
---

# Skill Eval

Use this only when requested or when a major skill change needs a behavior gate.
Do not run it for ordinary tasks: it needs a target skill, representative cases,
and a clear standard for judging each case.

## Required Inputs

Do not start until these inputs exist:

- **Target skill**: a real `SKILL.md` that can be read.
- **Representative cases**: at least one realistic prompt, screenshot, file, diff, log,
  or other input artifact. Do not invent cases or guess intent.
- **Case bar**: what good looks like and which smells would fail it. For
  judgment-heavy skills, keep the bar at outcome level rather than listing the
  exact answer. For conformance skills, exact criteria are appropriate. Ask when
  the distinction is unclear.

If the user only says "this skill often misses X", first help them turn that
complaint into concrete cases and bars before assigning runners.

## Workflow

1. **Validate inputs and state the governing standard.** Read the target skill and
   identify its purpose, trigger, done condition, and expected failure modes.
   Decide whether the eval is judgment-based or conformance-based. Continue only
   when each case has concrete input and a judgeable bar.
2. **Run isolated cases.** For each case, start a clean runner with only the case
   material and the target-skill invocation. Keep the bar, smells, other cases,
   and evaluation intent out of that run. If files must be written, restrict the
   runner to a throwaway directory. After each run, inspect the live checkout and
   clean accidental leaks.
3. **Judge independently.** Give a separate judge the artifact, the bar, and the
   target skill's purpose. Do not ask the judge to "make it pass." Require
   evidence for every verdict, such as a quote or artifact pointer.
4. **Handle variance.** Re-run important or borderline cases enough times to
   report a pass rate instead of a single anecdote.
5. **Classify misses.** A miss can be a skill defect or a bad case/bar. Name the
   defect before editing: premature completion, vague done condition, missing
   rule, weak trigger, no-op instruction, duplication, sediment, sprawl, or
   missing reference split. Do not encode a bad bar into the skill.
6. **Edit only for the observed defect.** Tighten the done condition, trigger,
   rule, behavior anchor, or reference split that caused the miss.
7. **Re-run the suite.** A fix for one case must not regress another. Stop only
   when the cases clear their bars or when you can explain why the skill cannot
   support a case.

## Output

```text
Target skill:
Cases:
Per-case pass rate or verdict:
Failures:
Defect mapping:
Edits made / proposed:
Re-eval result:
Residual risk:
```

Every verdict needs traceable artifact evidence. A single numeric score is not
enough.

## Do not

- Do not revise a skill to satisfy a case whose bar is wrong.
- Do not compare artifacts against each other when the bar is the standard.
