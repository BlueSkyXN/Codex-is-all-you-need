---
name: delivery-task-planning
description: Use to turn approved specs or tech briefs into task cards, dependency graph, test tasks, and agent handoff. Not for code.
---

# Delivery Task Planning

## Purpose

Convert approved specs and engineering bridge artifacts into small, bounded, verifiable tasks for developers or coding agents.

## Boundary

Delivery planning creates execution units and handoff artifacts. It does not implement code, run tests, or decide final architecture.

## Workflow

1. Read PRD, scope lock, functional spec, technical bridge, and readiness review if available.
2. Identify work streams: product behavior, UI, API, data, integration, tests, docs, and release support.
3. Order work by dependency and validation safety.
4. Create task cards with allowed scope, forbidden scope, inputs, outputs, test requirements, and done criteria.
5. Create dependency graph and test task list.
6. Produce `agent-handoff.md` for dev agents.

## Outputs

- `implementation-plan.md`
- `task-breakdown.md`
- `task-dependency-graph.md`
- `test-task-list.md`
- `agent-handoff.md`

Use templates in `references/` when a durable artifact is requested.

## References / Load When

- `references/implementation-plan-template.md` - load when producing a phased implementation plan.
- `references/task-card-template.md` - load when creating individual task cards with scope, constraints, tests, and done criteria.
- `references/task-dependency-graph-template.md` - load when sequencing tasks or identifying parallel work.
- `references/test-task-list-template.md` - load when turning acceptance criteria and test plan drafts into test tasks.
- `references/agent-handoff-template.md` - load when preparing `agent-handoff.md` for dev or coding agents.

## Validation

- Each task is small enough to execute without re-planning the whole feature.
- Each task has explicit inputs, allowed changes, forbidden changes, completion criteria, and test requirements.
- P0 behavior has implementation and validation tasks.
- Open decisions are not hidden inside task instructions.
- The handoff says which dev roles should review or implement next.
