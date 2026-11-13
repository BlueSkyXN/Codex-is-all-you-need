# Implementation method

Shared by `sdlc-implement` and `sdlc-solve`. The input is a clear task
description, spec, handoff, or the current requirements of a solve task.
Authorization, task-file, and reporting rules are in
[the shared conventions](../../sdlc-solve/references/conventions.md).

## Before editing

1. Read the project instructions for the paths you will touch and, in a Git
   repository, run `git status`. Existing work is protected as the
   conventions describe.
2. Read the code you will change, its callers, and its tests. Take build,
   test, and lint commands from the project's own configuration, scripts, or
   CI; do not guess them.
3. Confirm the completion criteria: behaviors, checks, and delivery point.
   When a criterion is missing but the intent is clear, write it down as an
   assumption. When the intent itself is unclear, `sdlc-implement` asks and
   `sdlc-solve` investigates.

## Making the change

- Make the smallest sufficient change and follow the existing structure,
  naming, and style; put new code where code of the same kind already lives.
  Add no unrelated refactors, formatting sweeps, or new dependencies; when the
  task does require one, state why.
- Before creating a top-level directory, a package, a new kind of entry point,
  or a shared area such as `utils` or `common`, and when the change has to be
  repeated in several copies of one rule, size the decision with
  [the architecture method](../../ads-architecture/references/architecture.md).
- Work in small verified steps ordered by dependency.
- Choose verification by the kind of change:

| Change | Approach |
|---|---|
| New or changed behavior with a stable automated check | [The test-first method](../../sdlc-test-first/references/test-first.md) |
| Bug fix | [The bug-fix method](../../sdlc-bugfix/references/bugfix.md) |
| Behavior-preserving refactor | Existing tests, plus focused additions where coverage is thin; when code moves between modules or packages, the move steps in [the codebase structure method](../../ads-architecture/references/structure.md#move-code-safely) |
| Configuration, generated content, or documentation | Validate with the tool that consumes it: parser, generator, build, or link check |
| Exploratory experiment | State the question and how the result will be judged before running it |

## When the plan meets reality

- If the code, an interface, or a dependency differs from the plan, adjust the
  technical approach within existing constraints and record the deviation.
- If the difference affects the goal, a business rule, compatibility, or the
  acceptance criteria, stop that part. `sdlc-implement` reports concrete
  options; `sdlc-solve` applies its pause rule.

## Self-check

1. Run the project's checks for the changed area, then the broader checks the
   project expects, such as lint, type check, and build.
2. Read your own diff: scope limited to the task, no debug leftovers, no
   secrets, no unrelated files.
3. Fix failures caused by your change now. For a failure that may predate it,
   check whether it also fails on the base revision, for example in a separate
   worktree or from CI history, without disturbing the user's working tree.
   Report pre-existing failures instead of fixing them, unless the task covers
   them.
4. Re-read the original request and confirm that the checks show the user's
   problem is solved, not only that the code runs.

## Done

Every specified behavior is implemented, the self-check ran and its results are
recorded, the diff is limited to the task, and deviations are recorded. When a
task file exists, it reflects this state.
