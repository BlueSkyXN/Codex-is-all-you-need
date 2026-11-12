# Evaluation method

Shared by `improvement-skill-eval` and `improvement-prompt-eval`. Judge whether
a skill, prompt, or instruction change improves task outcomes, using
representative cases rather than impressions.

## 1. Define what is evaluated

The artifact (skill, prompt, instruction file, or tool description), its
versions or variants, the behavior it should produce, and the failures it is
meant to prevent.

## 2. Build the cases

Write 5 to 15 representative cases, each with its input, context, and the
expected observable result:

- should-use cases, including paraphrases that avoid the trigger words;
- should-not-use cases that look similar;
- normal, edge, and failure cases for the behavior;
- at least one case from real past use when available.

Write the expected results before running anything.

## 3. Run

- Run each case against each variant, including a baseline without the change
  when possible.
- Isolate the runs: a fresh session or context for each, the same model and
  settings, and no leakage of expected results.
- When the host cannot run isolated sessions, walk through the artifact
  against each case and label the results as static review.
- Keep the raw outputs.

## 4. Judge

For each run, compare against the expected result: did it complete the task,
stop at the right place, trigger or stay silent correctly, and follow its
constraints? Count rework, the user interventions it needed, and tool or token
cost when visible. Use an independent judge, such as another session or the
user, for subjective criteria where practical.

Also check the artifact itself for premature completion, vague done
conditions, missing rules, weak or over-broad triggers, instructions that
change nothing, duplication, outdated content, sprawl, and detail that belongs
in a reference file.

## 5. Report

For each variant: the result per case, the aggregate, notable failures with an
excerpt of the output, and the smallest edits that address them. State the
evidence type, isolated runs or static review, and the number of cases; a
small sample shows a direction, not proof.

## Done

Cases with expected results were written before running, every case has a
judged result, and every recommendation traces to an observed failure.
