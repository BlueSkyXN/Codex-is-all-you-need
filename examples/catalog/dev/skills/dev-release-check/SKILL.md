---
name: dev-release-check
description: Use for pre-release validation, versioning, changelogs, artifacts, smoke tests, rollback notes, and release risk.
metadata:
  version: "0.3"
  updated: "2026-06-12"
---

# Release check workflow

Use this workflow when preparing, reviewing, or validating a software release.

## Steps

1. Identify release target.
   - Version or tag
   - Branch or commit
   - Package or app artifact
   - Deployment target
   - Release notes audience

2. Read release sources.
   - Diff since last release
   - Changelog
   - Package metadata
   - CI status
   - Build scripts
   - Docs and migration notes

3. Validate readiness.
   - Tests
   - Typecheck/lint/build
   - Artifact generation
   - Smoke test
   - Dependency/security checks if relevant
   - Backward compatibility and migration notes

4. Prepare release material.
   - Version bump
   - Tag plan
   - Release notes
   - Known issues
   - Rollback path
   - Verification commands

5. Read back final state.
   - Commit SHA
   - Tag
   - Artifact path or URL
   - CI/check results if remote release is involved

## Output

Return:

1. Release target
2. Change summary
3. Validation performed
4. Artifact/tag/state
5. Known risks or rollback notes

## Do not

- Do not create tags or publish artifacts unless explicitly asked.
- Do not claim CI or release success without reading back the final state.
- Do not overstate stability beyond the checks actually run.
