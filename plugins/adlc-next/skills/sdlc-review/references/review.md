# Review method

Shared by `sdlc-review` and `sdlc-solve`. Delivery points and current
requirements are defined in
[the shared conventions](../../sdlc-solve/references/conventions.md).

## Inputs

- **Current requirements:** the user's request, the task file, and referenced
  specs. Use the current version; superseded requirements are not acceptance
  criteria. When no requirement source exists, review against the user's
  stated intent and say so.
- **Actual result:** diff, branch, commits, PR, built artifact, or running
  behavior.
- **Evidence:** test output, CI results, logs, and screenshots.

## Order of review

Spend effort in proportion to risk:

1. **Outcome.** Does the result meet each current requirement, including the
   user's original problem? Passing checks can still miss it, for example a
   cache that makes repeated queries fast while the reported slow first query
   stays slow.
2. **Design constraints.** Module and dependency boundaries, placement of new
   code, domain rules and data ownership, interfaces, and compatibility. Size
   what the diff actually does with
   [the architecture method](../../ads-architecture/references/architecture.md),
   then:
   - Local: the checks above are enough.
   - Bounded or Structural: check the result against its recorded decision;
     for a structure decision, also run its dependency checks and change
     scenarios, as
     [the codebase structure method](../../ads-architecture/references/structure.md)
     describes. When no reason is recorded, in the task file, a design record,
     the PR description, or beside the code, report an issue that names the
     missing decision and what it must record for this change.
3. **Correctness.** Edge cases, error paths, concurrency, data integrity,
   security, and secrets.
4. **Evidence.** Were the claimed checks run, do they test the claim, and what
   was simulated versus exercised on the real path?
5. **Scope.** Unrelated changes and unnecessary abstraction. Name a concrete
   smaller alternative for each finding; repository-required tests, mirrors,
   migrations, and version updates are constraints, not overhead.

Verify claims that are cheap to check yourself: run the test, read the code
path. Do not accept "tests pass" without output.

## Classification

Give every current requirement and every finding exactly one result:

- **met:** the evidence shows it is satisfied; cite the evidence.
- **issue:** give the location, the evidence, the impact, and the direction of
  a minimal fix, marked blocking or non-blocking.
- **cannot judge:** name the missing condition, such as an environment, data,
  access, or a check that does not exist, and how it could be obtained.

Keep problems introduced by the change separate from problems that already
existed.

## Output

1. Verdict: meets requirements, needs changes, or cannot judge yet.
2. Blocking issues.
3. Non-blocking issues.
4. Cannot judge: the missing conditions.
5. Pre-existing problems found outside this change.
6. The checks you ran, with results.

## Who acts on the result

- Within `sdlc-solve`, the results return to the solve workflow, which fixes
  in-scope issues and re-checks.
- A standalone `sdlc-review` delivers the review and stops, unless the request
  also asks for fixes.
