---
name: dev-pr-review
description: Use for reviewing a branch, pull request, local diff, or implementation plan before merge.
---

# PR review workflow

Use this workflow to review code changes for correctness, regressions, security, compatibility, and test coverage.

## Review checklist

1. Scope
   - What changed?
   - Is the diff limited to the stated goal?
   - Are unrelated files modified?

2. Correctness
   - Does the implementation satisfy the requirement?
   - Are edge cases handled?
   - Are error paths correct?

3. Contracts and compatibility
   - Public API behavior
   - CLI flags and exit behavior
   - Database schema and migration risk
   - Auth and permission semantics
   - Backward compatibility

4. Tests
   - Existing coverage
   - Missing tests
   - Test commands run
   - Flaky or inconclusive results

5. Security and data integrity
   - Input validation
   - Secrets and sensitive data
   - Race conditions
   - Data loss or corruption risk

## Output

Return:

1. Blocking findings
2. Important non-blocking findings
3. Test gaps
4. Contract or compatibility risks
5. Verdict: block / proceed / proceed with notes

## Do not

- Do not focus on style unless it hides a real issue.
- Do not suggest unrelated redesigns.
- Do not assume tests passed if they were not run.
