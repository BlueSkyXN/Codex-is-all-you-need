---
name: dev-pr-review
description: Use for reviewing a branch, pull request, local diff, or implementation plan before merge, including alignment of existing PR metadata with the diff and delivery state.
---

# PR review workflow

Use this workflow to review code changes and their reviewer-facing PR metadata
for correctness, regressions, security, compatibility, and test coverage.

## Review checklist

1. Remote PR context, when a PR exists
   - Resolve the base/head branches and current head SHA.
   - Read the draft/state, mergeability, checks, review decision, requested
     changes, and unresolved review conversations when available.
   - Treat absent checks or reviews as none reported until applicable repository
     rules confirm that no gate is required.

2. PR metadata alignment, when a PR or draft metadata exists
   - Read `../dev-git-workflow/references/pr-metadata-contract.md` completely.
   - Does the title summarize the complete diff in the required language and
     repository convention?
   - Can a reviewer understand the purpose, impact, boundaries, validation, and
     important constraints without the agent session or a previous PR?
   - Do metadata claims match the current head, checks, merge state, release,
     and runtime evidence?
   - Does the copy avoid internal traces, private data, and implementation-diary
     narration?

3. Scope
   - What changed?
   - Is the diff limited to the stated goal?
   - Are unrelated files modified?

4. Correctness
   - Does the implementation satisfy the requirement?
   - Are edge cases handled?
   - Are error paths correct?

5. Contracts and compatibility
   - Public API behavior
   - CLI flags and exit behavior
   - Database schema and migration risk
   - Auth and permission semantics
   - Backward compatibility

6. Tests
   - Existing coverage
   - Missing tests
   - Test commands run
   - Flaky or inconclusive results

7. Security and data integrity
   - Input validation
   - Secrets and sensitive data
   - Race conditions
   - Data loss or corruption risk

8. Minimality
   - Abstractions, layers, or indirection not required by the stated goal
   - Speculative features, config, flags, or extension points nobody requested
   - Whether the same goal could be achieved with a materially smaller diff
   - Treat repository-mandated mirrors, generated artifacts, tests, migrations,
     version updates, and compatibility docs as constraints rather than
     overhead by default
   - Confirm that a smaller alternative still satisfies the repository contract
   - Name a concrete smaller alternative for each finding

## Output

Return:

1. Blocking findings
2. Existing review or merge-gate state
3. PR metadata or scope-alignment findings
4. Important non-blocking findings
5. Simplification findings
6. Test gaps
7. Contract or compatibility risks
8. Verdict: block / proceed / proceed with notes

## Do not

- Do not treat inaccurate scope, state, risk, or validation metadata as a mere
  style issue.
- Do not focus on prose style that does not affect reviewer understanding.
- Do not suggest unrelated redesigns.
- Simplification findings must name a concrete smaller alternative within the
  current scope; do not use them to propose redesigns.
- Do not assume tests passed if they were not run.
