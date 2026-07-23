# Skill Design / Skill 设计

> 完整开发规范（单文件/标准/套件/群、目录、清单）见 **[skill-spec/SPEC.md](skill-spec/SPEC.md)**。
> 各平台调研证据见 **[skill-spec/research/](skill-spec/research/)**。
> 本文保留为公开安全、偏短的写法导读。

This guide defines a public-safe Codex skill style.

本文档定义一种适合公开分享的 Codex skill 写法。

## What A Skill Should Contain / Skill 应该包含什么

A skill is a small folder with a required `SKILL.md`.

skill 是一个小目录，必须包含 `SKILL.md`。

```text
skill-name/
  SKILL.md
  scripts/       optional deterministic helpers
  references/    optional details loaded only when needed
  assets/        optional output resources
```

Keep `SKILL.md` short. Put only trigger rules, workflow, validation gates, and navigation to optional resources.

`SKILL.md` 应保持精简，只写触发规则、工作流、验证门槛，以及可选资源的读取指引。

## Minimal SKILL.md / 最小模板

```markdown
---
name: tabular-analysis
description: Use when the task involves profiling, cleaning, summarizing, or validating CSV, TSV, database exports, or spreadsheet-like tables.
---

# Tabular Analysis

## Workflow

1. Identify the table source, encoding, delimiter, and row count.
2. Profile schema, missing values, duplicate keys, and suspicious outliers.
3. Separate factual findings from interpretation.
4. Produce a reproducible script or notebook when the result must be reused.

## Validation

- Re-run the script from a clean shell when code is created.
- Report row counts before and after filtering.
- Preserve raw inputs unless the user explicitly asks for destructive edits.
```

## Progressive Disclosure / 渐进披露

Use three levels:

使用三层结构：

```text
metadata
  EN: name and description, always visible to Codex.
  CN: name 和 description，始终可见。

SKILL.md body
  EN: Loaded only when the skill triggers.
  CN: 仅在 skill 触发后加载。

bundled resources
  EN: Scripts, references, or assets loaded or executed only when needed.
  CN: scripts、references、assets 按需读取或执行。
```

This keeps context small while preserving reliable procedures.

这样既能节省上下文，也能保留可靠流程。

## Public-Safe Skill Policy / 公开安全策略

Public examples may be minimal demo workflows or sanitized production-derived workflows.

公开示例可以是最小演示 workflow，也可以是从真实生产 skill 中抽取并脱敏后的通用工作流。

Do not publish:

不要发布：

- Private client, team, or project names.
- Internal report templates that reveal business process.
- Real machine paths, tokens, credentials, or account names.
- Private scripts that call internal services.
- Large copied skills whose license, origin, or sensitivity is unclear.

Publish instead:

可以发布：

- Generic skill anatomy.
- Small examples that show structure.
- Sanitized production-derived workflows that teach the pattern.
- Placeholder scripts with no private dependencies.
- Migration notes that describe how to extract reusable ideas.

## Designing From Existing Claude Skills / 从 Claude Skill 中学习

When learning from older Claude Code skills, extract the durable workflow:

从旧 Claude Code skills 学习时，只抽取稳定工作流：

```text
trigger -> required inputs -> procedure -> validation -> output format
```

Then remove:

然后移除：

- Claude-only assumptions.
- Tool names unavailable in Codex.
- Private templates and examples.
- Overly long background explanation that does not affect execution.

## Skill And Agent Relationship / Skill 与 Agent 的关系

An agent may recommend skills in `developer_instructions`, but installed
plugins and runtime-visible filesystem entrypoints control availability.

agent 可以在 `developer_instructions` 中推荐 skills，但是否可用由已安装插件和 runtime
可见文件入口共同决定。

Good pattern:

推荐模式：

```text
Agent: "For table-heavy analysis, prefer tabular-analysis when visible."
Skill: "When triggered, run the table profiling workflow and validation gates."
Plugin: "Package tabular-analysis for production shared use."
Suite: "Expose both the data agent and tabular-analysis skill only for V1 legacy/local-dev data-heavy runtimes."
```

## Review Checklist / 检查清单

Before publishing a skill:

发布 skill 前检查：

- `name` is stable and lowercase kebab-case.
- `description` clearly states trigger conditions.
- `SKILL.md` contains only essential workflow instructions.
- Detailed references are linked directly from `SKILL.md`.
- Scripts are deterministic and documented by usage, not by long essays.
- No private path, credential, team name, client name, or sensitive sample data is present.
