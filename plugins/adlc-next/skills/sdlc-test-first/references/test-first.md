# Test-first method

Shared by `sdlc-test-first`, `sdlc-implement`, and `sdlc-solve`.

## When it fits

Use it for new or changed behavior, and for bug fixes, when the behavior can
get a stable automated check. For other changes, use the matching approach in
[the implementation method](../../sdlc-implement/references/implement.md).

## The loop

For one observable behavior at a time:

1. **Pick the slice.** The next behavior a user or caller can observe,
   smallest first. One behavior per cycle.
2. **Red.** Write a test through the public interface that expresses the
   behavior. Run it and confirm it fails for the right reason: the assertion
   fails, not an import error, a typo, or a missing fixture.
3. **Green.** Write the minimum code that makes it pass. Run it with the
   nearby tests.
4. **Refactor.** Improve names and structure while every test stays green, and
   run them again.
5. Record the behavior and its test, then take the next slice.

## Test quality

- Test behavior, not implementation details; a refactor should not break the
  test.
- Keep tests deterministic: control time, ordering, randomness, and network.
- Mock only at boundaries you do not own or that are slow or unsafe; do not
  mock the unit under test.
- Use the project's existing framework, helpers, and naming.

## Missing test infrastructure

When the project cannot run the needed test, add the smallest harness that
fits its conventions if that is inside the task's scope. When it is not,
report it and verify with another approach.

## Done

Every delivered behavior has a test that was seen failing and then passing,
the tests for the area pass after refactoring, and the commands and results
are recorded.
