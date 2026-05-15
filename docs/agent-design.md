# Agent Design / Agent 设计

This guide turns broad Claude Code style subagent libraries into smaller Codex agent presets.

本文档说明如何把 Claude Code 风格的大型 subagent 库，转成更适合 Codex 的轻量 agent 预设。

## Core Idea / 核心思路

Claude-style agents often combine three things in one Markdown file:

Claude 风格 agent 往往把三类信息写在一个 Markdown 文件里：

```text
trigger examples / 触发场景
role identity / 角色定位
workflow and checklist / 工作流与检查清单
```

For Codex, keep the agent narrow and let skills carry repeatable workflows.

在 Codex 中，agent 应保持角色边界清晰，把可复用工作流交给 skills。

```text
Agent = role, judgment, boundaries, delegation style
Skill = reusable procedure, file-format workflow, deterministic helper scripts
Suite = visible package of agents and skills for one runtime domain
```

## Recommended TOML Shape / 推荐 TOML 形态

```toml
name = "dev_code_reviewer"
description = "Review code changes for correctness, maintainability, security, tests, and release risk."
nickname_candidates = ["Reviewer"]

developer_instructions = """
You are a pragmatic code reviewer.

Prioritize findings over summaries. Ground every finding in a concrete file,
line, behavior, or test gap. Prefer existing project conventions.

Recommended skills: bugfix.
Do not treat recommended skills as bundled dependencies. Use them only when
the user request and runtime-visible skills make them relevant.
"""
```

Conventions:

约定：

```text
name
  EN: Stable snake_case identifier.
  CN: 稳定的 snake_case 标识。

description
  EN: Explain when to use the agent. Keep it operational.
  CN: 说明何时使用该 agent，避免抽象口号。

nickname_candidates
  EN: Keep one short nickname.
  CN: 只放一个短名称。

developer_instructions
  EN: Put behavior, boundaries, quality gates, and skill hints here.
  CN: 写入行为规则、边界、质量门槛和 skill 使用建议。
```

## Learning From Claude Agents / 从 Claude Agent 中学习

Useful patterns to keep:

值得保留的模式：

- Trigger examples that explain when a role is useful.
- Clear role boundaries such as frontend, backend, reviewer, analyst, or project manager.
- Quality checklists tied to the role.
- Handoff expectations and deliverable formats.

需要保留的模式：

- 触发示例：说明什么时候该用这个角色。
- 角色边界：例如 frontend、backend、reviewer、analyst、project manager。
- 质量清单：和角色真实职责绑定。
- 交接要求：包括交付物格式、验证方式和风险说明。

Patterns to reduce:

需要压缩的模式：

- Long universal engineering advice that Codex already knows.
- Hard-coded references to Claude-only tools or context-manager protocols.
- Large multi-role checklists that make one agent behave like an entire department.
- Private business process, internal project names, credentials, or machine paths.

## Domain Packs / 领域包

For a small and maintainable preset system, group agents by work domain.

为了让 preset 系统可维护，建议按任务域组织 agent：

| Pack | Purpose | Example Agents |
|---|---|---|
| `common` | General planning, synthesis, review, context management | `common_task_planner` |
| `product-engineering` | Pre-implementation product engineering, scope control, specs, delivery planning | `product_engineering_requirements_lead` |
| `dev` | Software development, code review, debugging, API/CLI verification | `dev_code_reviewer` |
| `data` | Table, database, metric, and notebook analysis | `data_profile_analyst` |
| `office` | Reports, slides, project updates, management writing | `office_report_writer` |
| `research` | Source synthesis, evidence review, material integration | `research_synthesis_writer` |

## Skill Hints Are Not Bundles / Skill 提示不是捆绑

Codex agents cannot force-load a private bundle of skills by TOML field alone. The runtime-visible filesystem decides which skills are discoverable.

Codex agent 不能单靠 TOML 字段强制捆绑某组 skills。实际可见技能由 runtime 目录中的文件结构决定。

Use `developer_instructions` for soft guidance:

可以在 `developer_instructions` 中做软性建议：

```text
Recommended skills: bugfix, tabular-analysis.
Use these only when they are visible in the current runtime and match the task.
```

The dashboard detects these hints from the explicit `Recommended skills:` line and only keeps names that exist in the scanned skill catalog.

面板会从显式的 `Recommended skills:` 行识别推荐技能，并且只保留扫描到的真实 skill 名称。

## Orchestrator Agents / 编排 Agent

An orchestrator agent is useful when a task spans multiple domains or needs several specialist agents. Keep it lightweight.

当任务跨多个领域，或需要多个专家 agent 协作时，可以使用编排 agent。但它必须保持轻量。

Good responsibilities:

合理职责：

- Classify the task domain.
- Recommend a small agent lineup.
- Define handoffs, boundaries, validation gates, and stop conditions.
- Merge findings into a next-action plan.

Avoid:

避免：

- Treating the orchestrator as an external scheduler, message bus, queue system, or state store.
- Assuming nested subagents are always available.
- Replacing specialist agents such as implementers, reviewers, analysts, or writers.
- Creating large agent teams for small tasks.

In Codex, the main/default agent remains responsible for actual tool calls, subagent spawning, file edits, verification, and final delivery.

在 Codex 中，实际工具调用、subagent 拉起、文件修改、验证和最终交付仍由 main/default agent 负责。

## Review Checklist / 检查清单

Before publishing an agent:

发布 agent 前检查：

- The agent has one clear job.
- It does not mention private paths, clients, credentials, or non-public project names.
- It does not set model policy fields by default; inherit runtime configuration unless there is a documented reason to override.
- `nickname_candidates` has one entry.
- Recommended skills are hints, not claims of guaranteed availability.
- The instructions say how to verify work or report missing verification.
