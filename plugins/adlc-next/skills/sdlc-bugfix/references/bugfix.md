# Bug-fix method

Shared by `sdlc-bugfix`, `sdlc-implement`, and `sdlc-solve`.

## 1. Understand the report

Record expected versus actual behavior, where and when it happens, versions,
frequency, and what changed recently. Facts only the reporter has are asked
once, batched; the rest are investigated.

## 2. Build a signal

Get a fast, repeatable signal that shows the bug: a failing test, a script, a
command, or a log line. Prefer the tightest loop available. When the bug does
not reproduce:

- vary the conditions the report names: data, configuration, version, load,
  and concurrency;
- collect evidence: logs, stack traces, versions, and recent changes;
- bound the effort, then state what is known, what is suspected, and how
  confident you are. Do not substitute an unrelated failing test.

## 3. Localize

- For a regression, find the change that introduced it by comparing versions
  or bisecting the history locally.
- Otherwise trace data and control flow from the symptom back toward the
  cause.
- Keep a short list of hypotheses ranked by likelihood and cost to test. Test
  one at a time, each with a prediction that could prove it wrong.

## 4. Fix the cause

Explain the mechanism: which condition produces the wrong behavior. Fix it at
the cause, not at the symptom, with the smallest change. Look for the same
pattern nearby, and for copies of the faulty rule or value elsewhere: a copy
usually carries the same defect. Copies that must behave the same are part of
the fix; when merging them is outside the task, record the merge as a
follow-up.

## 5. Verify

Re-run the signal and confirm it passes; keep it as a regression test when it
can be automated. Run the nearby tests. When the fix covered several copies,
check each copy that still stands with its own regression input; after a
merge, check the shared rule and each entry point whose call path changed.
Confirm that the scenario in the original report is resolved, not only the
reduced case.

## Done

The cause is explained, the fix is in place, the original signal and nearby
checks pass, and residual risk is stated.
