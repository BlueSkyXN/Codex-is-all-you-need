# Skill 平台调研（research）

本目录是 **调研证据**，不是 Skill 开发规范正文。  
规范请读上一级 **[../SPEC.md](../SPEC.md)**。

原路径 `docs/skill-platform-specs/` 已迁入 `docs/skill-spec/research/`。

## 文档列表

| 文件 | 内容 |
|---|---|
| [RESEARCH-STATUS.md](RESEARCH-STATUS.md) | 调查完成度与缺口看板 |
| [agent-skills-open-standard.md](agent-skills-open-standard.md) | Agent Skills 开放标准 |
| [claude-code.md](claude-code.md) | Claude Code |
| [openai-codex.md](openai-codex.md) | OpenAI / Codex（含 `agents/openai.yaml`） |
| [openclaw.md](openclaw.md) | OpenClaw |
| [codebuddy.md](codebuddy.md) | CodeBuddy |
| [qoder.md](qoder.md) | Qoder |

## 共同底座（摘要）

多数厂商对齐 [Agent Skills](https://agentskills.io)：

- Skill = 目录 + 必选 `SKILL.md`
- Frontmatter 至少 `name` + `description`
- 渐进披露：metadata → body → 按需资源
- 可选 `scripts/`、`references/`、`assets/`（名称略有差异）

## 与规范的关系

```text
research/   → 各平台「是什么」（证据）
SPEC.md     → 我们「规定做什么」（真源）
```

设计 portable skill 时以 `SPEC.md` 为准；需要核对某平台字段时再查本目录。

## 提取日期

约 2026-07-16。数字限额与字段以各厂商最新文档为准，引用前建议复核。
