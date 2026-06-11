---
name: dev-repo-onboarding
description: "Use for first-pass software repository onboarding: map structure, entry points, tech stack, commands, tests, risks, and the smallest safe next actions before editing."
---

# Repository onboarding workflow

Use this workflow when entering an unfamiliar software repository or before a risky implementation.

## Steps

1. Identify repository basics.
   - Language and framework
   - Package manager
   - Main entry points
   - App/library/CLI boundaries
   - Build and test tools
   - Deployment or runtime hints

2. Read high-signal files first.
   - `AGENTS.md`
   - README and docs index
   - Package/project metadata
   - Makefile/task runner
   - CI config
   - Route/CLI entry points
   - Test config

3. Map the task area.
   - Relevant files and symbols
   - Call path
   - Data/control flow
   - Existing tests
   - Config and environment dependencies

4. Define safe validation.
   - Smallest relevant test
   - Typecheck/lint/build command
   - Manual or browser smoke path
   - Known expensive commands to avoid initially

5. Report uncertainty.
   - Missing docs
   - Unknown runtime assumptions
   - Risky generated files
   - Potential unrelated user changes

## Output

Return:

1. Repo map
2. Task-relevant files and symbols
3. Existing commands and tests
4. Risks and unknowns
5. Recommended next action

## Do not

- Do not edit files during onboarding unless explicitly asked.
- Do not run broad expensive commands before a narrow map exists.
- Do not infer framework behavior when local config or docs can answer it.
