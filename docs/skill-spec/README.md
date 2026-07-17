# Skill 规范目录（skill-spec）

本目录只保留：

1. **一份规范长文**：[SPEC.md](SPEC.md) —— **自包含单文件**，可直接分发给任何人 / 任何团队执行，不依赖本仓库其他文件
2. **调研结果**：[research/](research/) —— 证据库，可选阅读

```text
docs/skill-spec/
  README.md           # 本说明
  SPEC.md             # 规范唯一长文（单文件/标准/套件/群 + 目录 + 清单）
  research/           # 各平台 Skill 规范调研（证据，非规范正文）
    README.md
    RESEARCH-STATUS.md
    comparison.md     # 名词 / SKILL.md / 目录结构横表
    agent-skills-open-standard.md
    claude-code.md
    openai-codex.md
    openclaw.md
    codebuddy.md
    workbuddy.md
    qoder.md
    copilot-cli.md
```

## 怎么用

| 目的 | 打开 |
|---|---|
| 写/审 skill、定目录与形态 | [SPEC.md](SPEC.md) |
| 查名词 / SKILL.md / 目录横表 | [research/comparison.md](research/comparison.md) |
| 查各平台差异与调研缺口 | [research/README.md](research/README.md) |
| 查还没查清什么 | [research/RESEARCH-STATUS.md](research/RESEARCH-STATUS.md) |

## 规范 30 秒摘要

```text
单文件 / 标准 / 套件 = 一个目录、一个 name、一个 SKILL.md
群 = 数十个独立 skill 的平级组织 + 可选 router（参考线约 30）

三层加载：触发写 description（L1），主工作流写正文（L2），
细节按需读（L3：references/, examples/, scripts/, assets/）
evals/ 为回归材料，运行时不读；结构按需生长，不预建空目录

references = 怎么做对   examples = 长什么样   evals = 测过了吗
大知识放包外，包内只写怎么查；Git 是真源，上传是发布
```

## 相关仓内文档

- [skill-design.md](../skill-design.md) — 旧公开设计短文  
- [skill-versioning.md](../skill-versioning.md) — 行为版本契约  
- [agent-skill-map.md](../agent-skill-map.md) — Agent 与 skill 分工  
