# Product Engineering Flow / 产品工程流程

This document defines the `product-engineering` catalog as a planning and engineering-management layer between office/product materials and development implementation.

本文档定义 `product-engineering` catalog：它位于办公/产品材料和开发实现之间，是规划与工程管理层。

## Boundary / 边界

```text
office
  EN: meeting notes, reports, product planning notes, roadmap framing.
  CN: 会议纪要、报告、产品规划笔记、roadmap 表述。

product-engineering
  EN: PRD, scope lock, functional behavior, technical bridge, delivery plan,
      readiness gates, and implementation handoff.
  CN: PRD、范围锁定、功能行为规格、技术桥接、交付计划、准备度门禁和开发交接。

dev
  EN: repository mapping, architecture/API review, implementation, tests,
      code review, security review, performance, and release validation.
  CN: 仓库映射、架构/API 审查、实现、测试、代码 review、安全 review、性能和发布验证。
```

`product-engineering` should not be automatically bundled into every `dev` suite. Some workspaces need only implementation agents; some planning workspaces need no code-editing agents at all.

`product-engineering` 不应自动塞进所有 `dev` suite。有些工作区只需要实现 agents，有些规划工作区完全不需要代码编辑 agents。

## Flow / 流程

```text
Idea or source materials
-> product_engineering_requirements_lead
-> product_engineering_functional_specifier
-> product_engineering_technical_bridge
-> product_engineering_delivery_planner
-> product_engineering_readiness_reviewer
-> agent-handoff.md / task-breakdown.md / review-report.md
-> dev catalog when implementation begins
```

Optional repository change-spec adaptation:

可选的 repository change-spec 转换：

```text
approved planning artifacts
-> product_engineering_change_adapter
-> changes/{change-id}/proposal.md
-> changes/{change-id}/design.md
-> changes/{change-id}/tasks.md
-> behavior/spec deltas
```

## Why Multiple Agents / 为什么不是一个总控 Agent

The previous one-agent-many-skills shape is too coarse for this repository's suite model. In this project:

之前的“一个 agent 挂多个 skills”形态对本仓库的 suite 模型来说过粗。在本项目中：

- Agent = role, judgment, boundaries, delegation style.
- Skill = reusable workflow and validation gate.
- Suite = runtime-visible composition chosen by directory.

Therefore `product-engineering` is split into role agents:

因此 `product-engineering` 拆成多个角色 agent：

| Phase | Agent | Primary Skill |
|---|---|---|
| Requirements | `product_engineering_requirements_lead` | `prd-workflow` |
| Behavior spec | `product_engineering_functional_specifier` | `functional-spec` |
| Engineering bridge | `product_engineering_technical_bridge` | `technical-spec-bridge` |
| Delivery planning | `product_engineering_delivery_planner` | `delivery-task-planning` |
| Gate review | `product_engineering_readiness_reviewer` | `readiness-review` |
| Change-spec adaptation | `product_engineering_change_adapter` | `change-spec-adapter` |

## Suite Guidance / Suite 建议

Recommended local suite shapes:

推荐的本机 suite 形态：

```text
planning
  common + product-engineering

github
  common + dev

github-planning
  common + product-engineering + selected dev reviewers

nondev-office
  common + office
```

Use `planning` when the directory holds PRDs, specs, taskbooks, or AI handoff packages. Use `github` when the directory is primarily a code repository ready for implementation. Use a mixed suite only when the same repo is actively moving from planning into implementation.

当目录主要放 PRD、规格、任务书或 AI 交接包时，使用 `planning`。当目录主要是已准备进入实现的代码仓库时，使用 `github`。只有同一个 repo 正从规划推进到实现时，才使用混合 suite。

## Handoff Standard / 交接标准

Before switching to `dev`, the planning layer should provide:

切换到 `dev` 前，规划层应提供：

- approved or clearly marked draft PRD/scope lock
- functional spec with state, fields, permissions, errors, and acceptance criteria
- technical bridge with draft decisions and owner-confirmation needs separated
- task breakdown with allowed scope, forbidden scope, dependencies, validation, and done criteria
- readiness review that says proceed, revise, or stop

If these are missing, `dev` agents may still help explore the repo, but implementation should be treated as higher risk.

如果这些内容缺失，`dev` agents 仍可帮助探索仓库，但实现风险应被明确标高。
