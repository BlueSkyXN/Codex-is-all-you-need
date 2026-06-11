# Common Catalog / 通用目录

[English](README.md) | 中文

这里存放规划、协调、本地文档核对、文件整理、质量复核、上下文交接和 Codex 项目指令设计相关的通用 agents 与 skills。这些角色不绑定具体领域，可与 `dev`、`data`、`office`、`research` 组合使用。

## 内容清单

```text
agents/
  common_context_summarizer.toml
  common_docs_researcher.toml
  common_file_organizer.toml
  common_orchestrator.toml
  common_quality_reviewer.toml
  common_task_planner.toml
skills/
  core-codex-agents-md-builder/
  core-goal-run/
```

## Agent 角色

- `common_task_planner`：拆解复杂任务，定义阶段、交付物和验证步骤。
- `common_orchestrator`：协调多步骤或跨领域任务，并整合发现。
- `common_context_summarizer`：从长上下文中生成简洁交接摘要。
- `common_docs_researcher`：核对本地文档、官方文档、CLI 参数和配置键。
- `common_file_organizer`：整理目录、草稿、素材和索引，不删除源文件。
- `common_quality_reviewer`：复核产物的完整性、正确性、约束遗漏和无依据结论。

## Skills

- `core-codex-agents-md-builder`：按 Codex 加载模型设计、审计或重构仓库的 `AGENTS.md` 文件。
- `core-goal-run`：基于本地 goal/plan 文件推进、恢复和交接任务，用 `goal-tasks.md` 记录状态，用 `goal-log.md` 记录证据和过程说明。

## 维护说明

本分组应保持通用可复用。不要把明显属于 `dev`、`data`、`office` 或 `research` 的领域实现细节放在这里。维护时遵循 `../PUBLIC-SUBSET.md` 的发布边界和 `../AGENTS.md` 的 catalog 规则。
