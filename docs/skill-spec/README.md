# Skill 规范目录（skill-spec）

本目录只保留：

1. **一份规范长文**：[SPEC.md](SPEC.md) —— **自包含单文件**，可直接分发给任何人 / 任何团队执行，不依赖本仓库其他文件
2. **一份上手指南**：[GUIDE.md](GUIDE.md) —— SPEC 的入门伴侣，面向第一次写 skill 的业务作者，十分钟从模板到能用；条款以 SPEC 为准
3. **调研结果**：[research/](research/) —— 证据库，可选阅读

规范只维护可移植底座、通用工程默认和平台适配边界。组织命名、责任、源码目录、审批与分发规则应放在各自仓库的增量 profile 中，不复制或改写成新的“通用标准”。

```text
docs/skill-spec/
  README.md           # 本说明
  SPEC.md             # 规范唯一长文（单文件/标准/套件/群 + 目录 + 清单）
  GUIDE.md            # 上手指南（抄模板 → 改三处 → 放哪里 → 触发调不准怎么办）
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
| 第一次写 skill、十分钟上手 | [GUIDE.md](GUIDE.md) |
| 写/审 skill、定目录与形态 | [SPEC.md](SPEC.md) |
| 查名词 / SKILL.md / 目录横表 | [research/comparison.md](research/comparison.md) |
| 查各平台差异与调研缺口 | [research/README.md](research/README.md) |
| 查还没查清什么 | [research/RESEARCH-STATUS.md](research/RESEARCH-STATUS.md) |

## 规范 30 秒摘要

```text
单文件 / 标准 / 套件 = 一个目录、一个 name、一个 SKILL.md
群 = 数十个独立 skill 的平级组织 + 可选 router（参考线约 30）

三层加载：能力与适用事件写单行 description（L1），主工作流写正文（L2），
细节按需读（L3：references/, examples/, scripts/, assets/）
evals/ 为回归材料，运行时不读；结构按需生长，不预建空目录

普通 skill 满足准确触发、主流程、完成/停止条件、按需资源、依赖副作用说明和
风险匹配验证即可停止扩展；不为形式补 manifest、脚本、评测、adapter 或部署证据

治理 metadata：version / updated 记录行为版本与日期；需要随文件明确责任时，
maintainer / updated_by 只记录当前人类负责人和当前行为版本修改人，不记录 AI

展示名按平台适配：Codex 用 agents/openai.yaml.interface.display_name；Claude Code
复用 name；WorkBuddy 5.3.5 的 bundled scanner 不读取 SKILL.md 顶层
display_name / display-name，因此不要把它当成当前通用适配字段

references = 怎么做对   examples = 长什么样   evals = 测过了吗
skill-manifest.json = 可选且默认不建；治理信息需脱离 Git 随包携带时使用
大知识放包外，包内只写怎么查；Git 是真源，上传是发布
```

## 相关仓内文档

- [skill-design.md](../skill-design.md) — 旧公开设计短文
- [skill-versioning.md](../skill-versioning.md) — 行为版本契约
- [agent-skill-map.md](../agent-skill-map.md) — Agent 与 skill 分工
