---
name: dev-test-strategy
description: Use to design or validate test plans, unit/integration/e2e coverage, automation, CI checks, fixtures, and regression scope.
metadata:
  version: "0.3"
  updated: "2026-06-12"
---

# Test strategy workflow

Use this workflow when a software task needs test planning, test implementation, or validation triage.

## Steps

1. Map existing tests.
   - Test framework
   - Test directories
   - Fixtures and factories
   - CI commands
   - Coverage expectations
   - Known flaky tests

2. Identify changed behavior.
   - Public API or CLI behavior
   - UI behavior
   - Data model or migration
   - Auth/permissions
   - Error paths
   - Performance-sensitive path

3. Choose test levels.
   - Unit tests for isolated logic
   - Integration tests for components/services/databases
   - Contract/API tests for boundary behavior
   - UI/e2e tests for user workflows
   - Regression tests for bugs

4. Keep validation efficient.
   - Run the smallest relevant check first.
   - Broaden only when the change or failure requires it.
   - Capture exact command, status, and important output.

5. Handle failures honestly.
   - Separate failure caused by current change from pre-existing failure.
   - State flaky or inconclusive results.
   - Do not weaken tests to pass.

## Output

Return:

1. Behavior under test
2. Existing coverage
3. Added or recommended tests
4. Commands run
5. Remaining test gaps

## Do not

- Do not claim coverage without reading or running the relevant tests.
- Do not add brittle UI or timing tests when lower-level tests cover the behavior better.
- Do not skip changed behavior just because the current test suite is thin.
