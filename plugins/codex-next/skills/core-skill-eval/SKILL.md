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

- **Target skill**: a real `SKILL.md` that can be read.
- **Golden cases**: at least one realistic prompt, screenshot, file, diff, log,
  or other input artifact. Do not invent cases or guess intent.
- **Bar per case**: the outcome a good artifact achieves and the smells that
  would make it bad — not an exhaustive parts list. The skill's **judgment** is
  what is under test. State the bar and the smells; let the judge apply them.
  If the skill is conformance-style (exact task hit exactly), then the explicit
  criteria are the bar. Match the bar's shape to the skill's nature; ask the
  user if ambiguous.

If the user only says "this skill often misses X", first help them turn that
complaint into one or more cases and bars before spending agents.

## Workflow

1. **Validate inputs and surface first principles.** Read the target skill and
   identify its first principles, routing trigger, done condition, and failure
   modes. Settle the eval mode: judgment (a bar the judge applies) vs
   conformance (an exact task hit exactly). Done when you can state the skill's
   first principles in a sentence and every case has a concrete input and a bar
   a competent judge could hold an artifact to.
2. **Blind run — one fresh agent per case.** Blind is non-negotiable: the runner
   sees only the case input and the instruction to use the target skill. Never
   reveal the bar, the smells, the other cases, or why you are asking. Use a
   fresh isolated runner per case so no cross-case learning inflates a later
   result. When the skill must write files, give the runner a throwaway sandbox
   directory, not the live checkout. After every run, sweep the live checkout
   (`git status`) and clean anything the run leaked — isolation is best-effort,
   the sweep is the guarantee.
3. **Judge separately.** Use a fresh judge. Give it the artifact, the bar, and
   the skill's first principles — so it grades against the skill's own intent,
   not personal taste. Never give the judge the expected output or "make this
   pass." The judge must cite specific evidence (a quote or pointer) for each
   verdict; a numeric score that hides which part of the bar failed is not
   acceptable.
4. **Account for nondeterminism.** Re-run critical or borderline cases 2-3 times
   and report pass rate rather than a single lucky result. A skill that passes
   1 of 3 is not fixed.
5. **Diagnose failures.** Each miss means either the skill failed to drive the
   behavior (fixable here) or the bar was wrong — it punished a defensible
   judgment call the skill was right to make. Name the defect: premature
   completion, vague completion criterion, missing rule, no leading word,
   no-op instruction, duplicated rule, sediment, sprawl, or missing reference.
   Do not edit the skill to chase a wrong bar.
6. **Revise via authoring rules.** Fix completion criteria, leading words,
   missing rules, reference splits, or triggering text. The failure is the spec
   for the edit; change only what the failure points at.
7. **Re-eval all cases.** A fix for one case must not regress another. Loop
   until every case clears its rate bar, or until you can show the skill
   structurally cannot express a case — then report that instead of forcing it.

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

## Do not

- Do not bend the skill to pass a case you cannot defend. A failing case that
  exposes a bad bar is a finding, not a bug.
- Do not grade against other artifacts or on a numeric score that hides which
  part of the bar failed.
