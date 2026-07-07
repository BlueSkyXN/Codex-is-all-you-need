---
name: dev-bugfix
description: Use for difficult bug fixes and regressions that require a real reproduction loop, root-cause work, and validation. Triggers when the user says "debug"/"diagnose"/"fix", or reports broken, failing, flaky, throwing, or slow behavior.
---

# Bugfix workflow

Use this for defects where guessing is likely to waste time. Move through the
phases in order unless you can state why a phase is already satisfied.

Before editing, read nearby repo instructions and any relevant `local/sdlc`
architecture or domain notes if they exist.

## Phase 0 - Define the Observed Failure

First pin the observed failure:

- Error message or wrong output.
- Reproduction steps from the user or current evidence.
- Affected file, feature, endpoint, CLI command, or behavior.

Then map likely code paths, nearby tests, and the smallest command that could
prove the failure.

## Phase 1 - Build a Feedback Loop

The first job is a `tight` pass/fail loop that can go `red` for this exact bug.
Without that signal, code reading turns into speculation. Spend more effort
building the loop than feels comfortable.

Use `references/feedback-loop-menu.md` to choose the smallest loop that reaches
the symptom: test, HTTP check, CLI fixture, browser assertion, replayed payload,
temporary harness, property/fuzz run, bisect, differential comparison, or HITL
script.

### Tighten the Loop

Improve the loop before relying on it. Narrow setup, assert the exact symptom,
cache slow prerequisites, pin time/randomness, and isolate filesystem or network
state. For flaky failures, the target is a high reproduction rate, not a perfect
single repro. Raise the rate until it is debuggable: repeat the trigger in bulk,
run copies in parallel, add load or stress, shrink timing windows, and inject
delays at suspected races. A failure on half the runs is workable; one in a
hundred is not yet a loop.

### Completion Criterion - Red-Capable Tight Loop Evidence

Name one command you have already run and show its decisive output. It must be:

- [ ] **Red-capable** - reaches the real bug path and checks the user's symptom
- [ ] **Repeatable** - same verdict each run, or a pinned high repro rate for flaky bugs
- [ ] **Fast** - seconds, not minutes
- [ ] **Agent-runnable** - runs unattended, except for encoded HITL prompts

If you are forming a root-cause theory before this command exists, stop and
build the loop first.

### When You Genuinely Cannot Build a Loop

Say so directly, list the attempts, and ask for one missing input: access to a
reproducing environment, a captured artifact such as logs/HAR/video/core dump,
or permission for temporary instrumentation. Do not present a speculative fix as
diagnosis.

## Phase 2 - Reproduce and Minimise

Run the loop and confirm:

- [ ] It produces the user-reported failure, not an adjacent failure
- [ ] It is reproducible across runs, or flaky at a high enough rate to debug
- [ ] The exact symptom is captured: message, wrong output, state, or timing

Then reduce the scenario. Remove inputs, callers, config, and data one at a
time, re-running after each cut. Minimisation is done when every remaining
piece is load-bearing: removing any one of them turns the loop green. The
minimised scenario shrinks the Phase 3 hypothesis space and becomes the Phase 5
regression test.

## Phase 3 - Hypothesise

List 3-5 ranked hypotheses before probing. Each must predict what evidence or
change would confirm or falsify it. Share the ranking before testing when the
user can cheaply re-rank it; continue with your ranking if they are unavailable.

## Phase 4 - Instrument

Each probe must test one prediction. Change one variable per run. Prefer a
debugger or REPL when available; otherwise add targeted logs at the boundary
that separates hypotheses. Tag temporary logs with a unique prefix for cleanup.

For slowdowns, spikes, latency regressions, or memory growth, use
`dev-performance-diagnosis` for baseline-first measurement and bisection.

## Phase 5 - Fix and Regression Test

Add a regression test before or alongside the fix when there is a valid `seam`:
a test point that exercises the real failure pattern through the relevant call
path. If every available seam is too shallow, record that as a testability
finding.

With a valid seam: watch the regression fail, apply the fix, watch it pass, then
rerun the original loop.

## Phase 6 - Cleanup and Post-mortem

- [ ] Original repro no longer reproduces after re-running the Phase 1 loop
- [ ] Regression test passes, or the absence of a correct seam is documented
- [ ] All `[DEBUG-...]` instrumentation is removed by grep
- [ ] Throwaway harnesses are deleted or clearly kept as intentional tests
- [ ] The correct hypothesis is stated in the commit, PR, or final report

After the fix, name the prevention lesson. If the lesson is architectural, such
as hidden coupling or no valid seam, record a follow-up and hand off to
`dev-refactor-plan`.

## Output

1. Feedback loop: the one command and its red/green evidence
2. Root cause and the hypothesis that held
3. Fix summary and files changed
4. Regression test, or documented absence of a correct seam
5. Residual risk and any architectural recommendation

## Do not

- Do not assert a root cause before a red-capable loop exists.
- Do not blanket-log a whole path and search the noise afterwards; every probe
  maps to one hypothesis boundary.
- Do not weaken tests to make them pass.
- Do not hide failing or inconclusive validation.
- Do not leave `[DEBUG-...]` tags or throwaway harnesses behind.
