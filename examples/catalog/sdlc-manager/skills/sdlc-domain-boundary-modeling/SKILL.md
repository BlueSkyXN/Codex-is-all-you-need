---
name: sdlc-domain-boundary-modeling
description: Use to model bounded contexts, capabilities, ownership, domain data/language, allowed interactions, and forbidden dependencies.
---

# Domain Boundary Modeling


Use this skill to model business-domain boundaries for a modular system.

In the lightweight SDLC-ADS model, durable domain knowledge should usually land in `local/sdlc/领域.md` as ownership, data, allowed dependency, forbidden dependency, glossary, or open-question updates. A standalone Domain Boundary Map is still valid for larger work, but small direct-dev tasks should not be forced into full DDD artifacts.

## Use when

- The system has multiple business capabilities.
- Modules should be organized by domain rather than only technical layers.
- There is risk of business rules spreading across unrelated modules.
- The user asks for DDD, bounded contexts, domain model, domain boundary map, or module ownership.

## Inputs

- BRD/URS/PRD/SRS.
- Existing project capability map.
- Current modules, routes, APIs, schemas, and terminology.
- Business workflows, roles, states, and rules.
- Existing `local/sdlc/_资产.md`, `local/sdlc/架构.md`, `local/sdlc/领域.md`, and current `00-状态.md` when present.

## Workflow

1. Extract business capabilities.
2. Identify candidate domains and bounded contexts.
3. Define each domain's responsibility.
4. Define data ownership.
5. Define exposed interfaces.
6. Define allowed dependencies and forbidden access.
7. Build a shared domain glossary.
8. Identify ambiguous concepts that need owner decisions.
9. Decide whether the output is a standalone boundary map, an incremental `领域.md` update, or both.

## Validation

Check:

- Each domain has one clear business responsibility.
- Data ownership is not duplicated without reason.
- Cross-domain calls are explicit.
- Shared concepts are named consistently.
- Forbidden dependencies are documented.
- The model supports modular monolith first unless microservices are justified.

## Output

Return:

1. Domain boundary map
2. Bounded context list
3. Data ownership map
4. Allowed dependency map
5. Forbidden dependency list
6. Domain glossary
7. Module naming proposal
8. Open questions

For lightweight ADS state, return or update:

```markdown
# 领域

## 能力归属
- DOM-001：

## 数据归属
- DOM-002：

## 允许依赖
- DOM-003：

## 禁止依赖
- DOM-004：

## 术语
-

## 推断 / 未确认
- Q-001：
```

## Boundaries

- Do not implement code.
- Do not force DDD patterns into a simple script or small local task.
- Do not create microservices merely because domains exist.
- Do not require full DDD artifacts for direct-dev tasks.
- Do not duplicate durable domain constraints in per-delivery specs when they should live in `local/sdlc/领域.md`.

## Handoff

Use `sdlc-modular-monolith-architecture` to map domains into repository structure, `sdlc-hld-workflow` for architecture, and `sdlc-dev-handoff-planning` for tasks.

Dev fallback: Dev can use SDLC / ADD / DDD / SDD materials when they exist, but dev can also continue without them when the task is clear, bounded, and testable from user request, issue, bug report, failing test, local diff, or repository evidence. Missing artifacts are risk/context, not automatic refusal.
