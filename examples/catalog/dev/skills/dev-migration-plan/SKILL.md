---
name: dev-migration-plan
description: Use to plan modernization, framework upgrades, service extraction, schema migrations, rewrites, and rollback paths.
metadata:
  version: "0.5"
  updated: "2026-07-08"
---

# Migration plan workflow

Use this workflow when changing technology, framework, architecture, schema, or large old-system behavior must be planned safely.

When present, consume the SDLC-ADS state before planning:

- `local/sdlc/_资产.md`
- `local/sdlc/架构.md` for `as-built` and `to-be` architecture.
- `local/sdlc/领域.md` for ownership, data, allowed dependencies, and forbidden dependencies.
- current `local/sdlc/<slug>/00-状态.md` for lane, stage, decisions, blockers, and validation state.

For pure refactor or migration, prefer behavior baseline, `as-built`, `to-be`, phases, validation, and rollback. Do not require Product Pack material unless the migration changes user behavior, business semantics, permissions, data ownership, or release commitments.

## Steps

1. Define target and non-goals.
   - What is being migrated
   - What must remain compatible
   - What can change
   - Constraints and deadlines

2. Map current behavior.
   - Entry points
   - Core business flows
   - Data model
   - External integrations
   - Tests and monitoring
   - Known risk areas
   - Existing `as-built` notes from `架构.md` or repository evidence

3. Choose migration strategy.
   - Incremental replacement
   - Adapter/facade
   - Strangler pattern
   - Parallel run
   - Feature flag rollout
   - Backward-compatible schema transition
   - Architecture/domain constraint preservation
   - If the trade-off set is still contested, run `core-grilling` on it before
     freezing the decision.

4. Build safety rails.
   - Characterization tests
   - Contract tests
   - Data backup or rollback
   - Observability
   - Stop conditions
   - Behavior baseline for externally visible behavior
   - Dependency and ownership checks from `领域.md`

5. Break into phases.
   - Small milestones
   - Validation after each phase
   - Rollback path
   - Owner and dependency assumptions

6. Update durable ADS only when needed.
   - New durable architecture constraints -> `local/sdlc/架构.md`
   - New ownership or dependency constraints -> `local/sdlc/领域.md`
   - New decisions or validation baseline -> `local/sdlc/_资产.md`
   - Current delivery state -> `local/sdlc/<slug>/00-状态.md`

## Output

Return:

1. Current-state map
2. Target state
3. Phased migration plan
4. Validation and rollback strategy
5. ADS impact and durable state updates needed
6. Risks and open decisions

## Do not

- Do not propose a big-bang rewrite unless explicitly requested.
- Do not ignore current behavior just because the old code is messy.
- Do not start implementation before the safety path is clear.
- Do not treat refactor/migration as a PRD problem unless product or domain semantics change.
