# Skill 平台调研（research）

本目录是 **调研证据**，不是 Skill 开发规范正文。
规范请读上一级 **[../SPEC.md](../SPEC.md)**。

## 文档列表

| 文件 | 内容 |
|---|---|
| [RESEARCH-STATUS.md](RESEARCH-STATUS.md) | 调查完成度与缺口看板 |
| [comparison.md](comparison.md) | **横表**：名词定义 · SKILL.md · 目录结构 |
| [agent-skills-open-standard.md](agent-skills-open-standard.md) | Agent Skills 开放标准 |
| [claude-code.md](claude-code.md) | Claude Code |
| [openai-codex.md](openai-codex.md) | OpenAI / Codex（含 `agents/openai.yaml`） |
| [openclaw.md](openclaw.md) | OpenClaw |
| [codebuddy.md](codebuddy.md) | CodeBuddy |
| [workbuddy.md](workbuddy.md) | WorkBuddy（本地 app 资产 + 专家包） |
| [qoder.md](qoder.md) | Qoder / QoderWork |
| [copilot-cli.md](copilot-cli.md) | GitHub Copilot CLI |

## 共同底座（摘要）

多数厂商对齐 [Agent Skills](https://agentskills.io)：

- Skill = 目录 + 必选 `SKILL.md`
- Frontmatter 至少 `name` + `description`
- 渐进披露：metadata → body → 按需资源
- 可选 `scripts/`、`references/`、`assets/`（名称略有差异）

## 创建能力形态（本轮本地路径补强后的摘要）

| 形态 | 代表 | 机制 |
|---|---|---|
| 工程脚手架脚本 | Codex、WorkBuddy | `init` / `validate` / `package` / `register` 脚本 |
| 对话式引导技能 | QoderWork CN | `create-skill` / `plugin-creator` / `create-command` |
| Slash 命令族 + 随包定义 | Claude Code、Copilot CLI | `/plugin`、`/agents`；Copilot 另有 `definitions/*.agent.yaml` |

## 与规范的关系

```text
research/   → 各平台「是什么」（证据）
SPEC.md     → 我们「规定做什么」（真源）
```

设计 portable skill 时以 `SPEC.md` 为准；需要核对某平台字段时再查本目录。

## 提取日期

- 主体公网文档提取：约 2026-07-16
- 本地创建路径 / 专家包 / Copilot CLI 补强：2026-07-17

数字限额与字段以各厂商最新文档或本地安装版本为准，引用前建议复核。
