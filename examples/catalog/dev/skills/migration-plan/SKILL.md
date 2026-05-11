---
name: migration-plan
description: Use for legacy modernization, framework upgrades, incremental rewrites, service extraction, schema migrations, and risky technical migration planning.
---

# Migration plan workflow

Use this workflow when changing technology, framework, architecture, schema, or large legacy behavior must be planned safely.

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

3. Choose migration strategy.
   - Incremental replacement
   - Adapter/facade
   - Strangler pattern
   - Parallel run
   - Feature flag rollout
   - Backward-compatible schema transition

4. Build safety rails.
   - Characterization tests
   - Contract tests
   - Data backup or rollback
   - Observability
   - Stop conditions

5. Break into phases.
   - Small milestones
   - Validation after each phase
   - Rollback path
   - Owner and dependency assumptions

## Output

Return:

1. Current-state map
2. Target state
3. Phased migration plan
4. Validation and rollback strategy
5. Risks and open decisions

## Do not

- Do not propose a big-bang rewrite unless explicitly requested.
- Do not ignore current behavior just because the legacy code is messy.
- Do not start implementation before the safety path is clear.
