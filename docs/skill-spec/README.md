# Skill 规范目录（skill-spec）

本目录只保留：

1. **一份规范长文**：[SPEC.md](SPEC.md) —— **自包含单文件**，可直接分发给任何人 / 任何团队执行，不依赖本仓库其他文件
2. **调研结果**：[research/](research/) —— 证据库，可选阅读

```text
docs/skill-spec/
  README.md           # 本说明
  SPEC.md             # 规范唯一长文（最小/标准/集合/群 + 目录 + 清单）
  research/           # 各平台 Skill 规范调研（证据，非规范正文）
    README.md
    RESEARCH-STATUS.md
    agent-skills-open-standard.md
    claude-code.md
    openai-codex.md
    openclaw.md
    codebuddy.md
    qoder.md
```

## 怎么用

| 目的 | 打开 |
|---|---|
| 写/审 skill、定目录与分档 | [SPEC.md](SPEC.md) |
| 查五家平台差异与调研缺口 | [research/README.md](research/README.md) |
| 查还没查清什么 | [research/RESEARCH-STATUS.md](research/RESEARCH-STATUS.md) |

## 规范 30 秒摘要

```text
最小 / 标准 / 集合 = 一个目录、一个 name、一个 SKILL.md
群 = 数十个独立 skill 的平级编队 + 可选 router（量感参考 ~30）

单包顶层白名单：
  SKILL.md + 按需 references/, examples/, scripts/,
  assets/, evals/, agents/
（另可有 README/LICENSE 等分发文件；结构按需生长，不预建空目录）

references = 怎么做对（执行说明；默认平铺语义名）
examples   = 长什么样 / 这种情形怎么走
evals      = 触发/质量回归（默认运行时不读；形态自由）
大知识放包外，包内只写怎么查；Git 是真源，上传是发布
```

## 相关仓内文档

- [skill-design.md](../skill-design.md) — 旧公开设计短文  
- [skill-versioning.md](../skill-versioning.md) — 行为版本契约  
- [agent-skill-map.md](../agent-skill-map.md) — Agent 与 skill 分工  
