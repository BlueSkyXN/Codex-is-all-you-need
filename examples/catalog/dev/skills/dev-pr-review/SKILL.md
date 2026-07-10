---
name: dev-pr-review
description: Use for reviewing a branch, pull request, local diff, implementation plan, or PR metadata before merge.
---

# PR review workflow

Use this workflow to review code changes and their reviewer-facing PR metadata
for correctness, regressions, security, compatibility, and test coverage.

## Review checklist

1. PR metadata alignment, when a PR or draft metadata exists
   - Read `../dev-git-workflow/references/pr-metadata-contract.md`.
   - Does the title summarize the complete diff in the required language and
     repository convention?
   - Can a reviewer understand the purpose, impact, boundaries, validation, and
     important constraints without the agent session or a previous PR?
   - Do metadata claims match the current head, checks, merge state, release,
     and runtime evidence?
   - Does the copy avoid internal traces, private data, and implementation-diary
     narration?

2. Scope
   - What changed?
   - Is the diff limited to the stated goal?
   - Are unrelated files modified?

3. Correctness
   - Does the implementation satisfy the requirement?
   - Are edge cases handled?
   - Are error paths correct?

4. Contracts and compatibility
   - Public API behavior
   - CLI flags and exit behavior
   - Database schema and migration risk
   - Auth and permission semantics
   - Backward compatibility

5. Tests
   - Existing coverage
   - Missing tests
   - Test commands run
   - Flaky or inconclusive results

6. Security and data integrity
   - Input validation
   - Secrets and sensitive data
   - Race conditions
   - Data loss or corruption risk

## Output

Return:

1. Blocking findings
2. PR metadata or scope-alignment findings
3. Important non-blocking findings
4. Test gaps
5. Contract or compatibility risks
6. Verdict: block / proceed / proceed with notes

## Do not

- Do not treat inaccurate scope, state, risk, or validation metadata as a mere
  style issue.
- Do not focus on prose style that does not affect reviewer understanding.
- Do not suggest unrelated redesigns.
- Do not assume tests passed if they were not run.
