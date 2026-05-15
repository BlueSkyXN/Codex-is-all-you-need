# Product Engineering Catalog

[中文](README_CN.md) | English

Agents and skills for pre-implementation product engineering: requirements, scope control, functional behavior, technical bridge drafts, delivery planning, readiness review, and change-spec handoff.

This catalog is separate from `dev`. It prepares implementation-ready artifacts, but it does not perform repository-aware implementation, testing, PR review, security review, or release checks.

## Contents

```text
agents/   6 product-engineering agents
skills/   6 public skills
```

## Agent Roles

- `product_engineering_requirements_lead`: turn product intent and source materials into PRD, scope lock, and spec handoff artifacts.
- `product_engineering_functional_specifier`: turn approved PRD scope into behavior, state, field, permission, UI-state, and acceptance specs.
- `product_engineering_technical_bridge`: draft engineering bridge artifacts without acting as the final architecture authority.
- `product_engineering_delivery_planner`: convert approved specs into implementation tasks, dependency order, validation expectations, and agent handoff.
- `product_engineering_readiness_reviewer`: review PRD/spec/tech/task/change artifacts before the next phase.
- `product_engineering_change_adapter`: adapt approved planning artifacts into repository change-spec or OpenSpec-style assets.

## Skills

- `prd-workflow`: idea to PRD, scope lock, detailed PRD, and spec handoff.
- `functional-spec`: behavior spec from PRD: flows, states, fields, permissions, UI states, errors, and ACs.
- `technical-spec-bridge`: engineering bridge artifacts: architecture brief, API/data drafts, NFRs, test draft, and open questions.
- `delivery-task-planning`: implementation plan, task breakdown, dependency graph, test tasks, and agent handoff.
- `readiness-review`: phase-gate review for PRD, functional spec, technical bridge, task plan, or change-spec artifacts.
- `change-spec-adapter`: convert approved artifacts into proposal, design, tasks, and behavior delta documents.

## Usage Notes

Use this catalog when the work is between product intent and implementation. The handoff point is a clear `agent-handoff.md`, `task-breakdown.md`, `review-report.md`, or equivalent change-spec artifact.

Use `dev` after the handoff when the task requires codebase mapping, API compatibility review, architecture review, implementation, testing, PR review, security review, performance diagnosis, or release validation.

## Maintenance Notes

Keep this group focused on engineering management and planning. Do not add code-editing workflows, real internal templates, private roadmap details, customer names, or machine-specific paths. Technical decisions should be marked as drafts unless they are backed by repository evidence and accepted by an implementation owner.
