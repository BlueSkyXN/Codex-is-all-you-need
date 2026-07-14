---
name: dev-dependency-upgrade
description: Use for dependency upgrades, vulnerability fixes, version conflicts, lockfiles, package managers, and migration risk.
metadata:
  version: "0.3"
  updated: "2026-06-12"
---

# Dependency upgrade workflow

Use this workflow when dependencies, lockfiles, package versions, or vulnerability fixes are in scope.

## Steps

1. Identify ecosystems.
   - npm/yarn/pnpm
   - Python pip/uv/poetry
   - Go modules
   - Rust cargo
   - Java/Maven/Gradle
   - Other package managers used by the repo

2. Read the source of truth.
   - Manifest files
   - Lockfiles
   - Workspace config
   - CI install commands
   - Vulnerability reports
   - Changelogs or migration notes for major updates

3. Classify the change.
   - Security patch
   - Version conflict
   - Major upgrade
   - Package replacement
   - Dependency removal
   - Bundle/build optimization

4. Plan safely.
   - Prefer smallest version bump that fixes the issue.
   - Note breaking changes.
   - Keep lockfile updates consistent with the package manager.
   - Define rollback path.

5. Validate.
   - Install or lockfile check
   - Unit/integration tests
   - Typecheck/lint/build
   - Security audit when available

## Output

Return:

1. Dependency issue
2. Selected upgrade path
3. Compatibility and security notes
4. Files changed
5. Validation run

## Do not

- Do not edit lockfiles manually unless the package manager cannot run and the reason is stated.
- Do not upgrade broad dependency sets when a targeted fix is enough.
- Do not ignore peer dependency or engine constraints.
