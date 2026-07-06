---
name: dev-bugfix
description: Use for hard bug fixes and regressions that need reproduction, root-cause analysis, and validation. Triggers when the user says "debug"/"diagnose"/"fix", or reports something broken/throwing/failing/flaky/slow.
---

# Bugfix workflow

A discipline for hard defects. Skip a phase only when explicitly justified.

Before editing, if `local/sdlc` state exists, read the relevant domain or
architecture notes to get a mental model of the modules in play, and check any
decisions in the area.

## Phase 0 - Define the Observed Failure

Before anything else, pin down what is actually broken:

- Error message or wrong output.
- Reproduction steps the user gave or you inferred.
- Affected file, feature, endpoint, CLI command, or behavior.

Then explore before editing: map likely files and execution paths, identify
existing tests, and identify the smallest validation command.

## Phase 1 - Build a Feedback Loop

**This is the skill. Everything else is mechanical.** If you have a `tight`
pass/fail signal that goes `red` on this bug, you will find the cause. If you
do not, no amount of reading code will save you. Spend disproportionate effort
here. **Be aggressive. Be creative. Refuse to give up.**

Consult `references/feedback-loop-menu.md` for the full menu of loop types and
when each fits. Try them roughly in order: failing test, HTTP script, CLI
fixture diff, headless browser, replay trace, throwaway harness, property/fuzz,
bisection, differential, HITL script (last resort).

### Tighten the Loop

Treat the loop as a product: make it faster, sharper, and more deterministic.
Cache setup, narrow scope, assert the exact symptom rather than "did not crash",
pin time, seed randomness, and isolate filesystem or network state. A 2-second
deterministic loop is a superpower; a 30-second flaky one is barely a loop.
For nondeterministic bugs, raise the reproduction rate until it is debuggable;
do not wait for a perfect repro.

### Completion Criterion - a Tight Loop That Goes Red

Name one command you have already run at least once, with invocation and output,
that is:

- [ ] **Red-capable** - drives the real bug path and asserts the user's exact symptom
- [ ] **Deterministic** - same verdict every run, or a pinned high repro rate for flaky bugs
- [ ] **Fast** - seconds, not minutes
- [ ] **Agent-runnable** - runs unattended, with human input only through the HITL template

If you catch yourself theorising before this command exists, stop. Jumping to a
hypothesis is the exact failure this skill prevents. No red command, no Phase 2.

### When You Genuinely Cannot Build a Loop

Stop and say so explicitly. List what you tried. Ask the user for: (a) access to
whatever environment reproduces it, (b) a captured artifact (HAR file, log dump,
core dump, screen recording with timestamps), or (c) permission to add temporary
production instrumentation. Do not proceed to hypothesise without a loop.

## Phase 2 - Reproduce and Minimise

Run the loop and watch it go red. Confirm:

- [ ] It produces the failure the user described, not a nearby one
- [ ] It is reproducible across runs, or flaky at a high enough rate to debug
- [ ] The exact symptom is captured: message, wrong output, state, or timing

Then shrink to the smallest scenario still going red: cut inputs, callers,
configuration, and data one at a time, re-running after each cut. Done means
every remaining element is `load-bearing`: removing any one turns the loop green.

## Phase 3 - Hypothesise

Generate 3-5 ranked, falsifiable hypotheses before testing any. Each states its
prediction: "if X is the cause, changing Y makes it disappear." No prediction
means it is only a vibe; discard or sharpen it. Show the ranked list to the user
before testing — cheap checkpoint, big time saver. Proceed on your ranking if
the user is AFK.

## Phase 4 - Instrument

Each probe maps to one Phase-3 prediction. Change one variable at a time.
Prefer debugger or REPL, then targeted logs at distinguishing boundaries. Never
"log everything and grep". Tag every debug log with a unique prefix such as
`[DEBUG-a4f2]` so cleanup is one grep.

Performance-flavoured symptoms such as slow, spike, latency regression, or
memory growth should route to `dev-performance-diagnosis`; its
baseline-and-bisect method lives there, not here.

## Phase 5 - Fix and Regression Test

Write the regression test before the fix, but only when a correct `seam` exists:
one that exercises the real bug pattern at the call site. If the only seam is
too shallow, that itself is the finding; note it and flag for Phase 6.

With a correct seam: red -> apply fix -> green -> re-run the Phase 1 loop
against the original, un-minimised scenario.

## Phase 6 - Cleanup and Post-mortem

- [ ] Original repro no longer reproduces after re-running the Phase 1 loop
- [ ] Regression test passes, or the absence of a correct seam is documented
- [ ] All `[DEBUG-...]` instrumentation is removed by grep
- [ ] Throwaway harnesses are deleted or clearly kept as intentional tests
- [ ] The correct hypothesis is stated in the commit, PR, or final report

Then ask: what would have prevented this bug? If the answer is architectural
(no good seam, tangled callers, hidden coupling), record a recommendation and
hand off to `dev-refactor-plan` after the fix is in, not before.

## Output

1. Feedback loop: the one command and its red/green evidence
2. Root cause and the hypothesis that held
3. Fix summary and files changed
4. Regression test, or documented absence of a correct seam
5. Residual risk and any architectural recommendation

## Do not

- Do not theorise before a red-capable loop exists.
- Do not weaken tests to make them pass.
- Do not hide failing or inconclusive validation.
- Do not leave `[DEBUG-...]` tags or throwaway harnesses behind.
