# Skill 规范目录（skill-spec）

本目录只保留：

1. **一份规范长文**：[SPEC.md](SPEC.md) —— **0.4 正式版，自包含单文件**，作者和团队按适用条款执行，不依赖本仓库其他文件
2. **一份上手指南**：[GUIDE.md](GUIDE.md) —— SPEC 的入门伴侣，面向第一次写 skill 的业务作者，十分钟从模板到能用；条款以 SPEC 为准
3. **调研结果**：[research/](research/) —— 证据库，可选阅读

规范主线是：Skill 是什么 → 有哪些类型和设计选择 → 包、文件与章节长什么样 → 怎样写出标准格式 → 怎样验收。平台特点集中在第 9 章；协作、版本和材料边界放在后部。组织命名、私有目录与审批约定由采用方维护。

```text
docs/skill-spec/
  README.md           # 本说明
  SPEC.md             # 定义 → 分类选择 → 目录文件 → 主文件格式 → 示例与验收
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
| 理解 Skill 与类型、选择设计方式 | [SPEC.md](SPEC.md) 第 1～2 章 |
| 写主文件、辅助文件和目录结构 | [SPEC.md](SPEC.md) 第 3～6 章 |
| 看完整标准示例、检查是否合格 | [SPEC.md](SPEC.md) 第 7、10 章 |
| 多包组织、平台特点、版本协作 | [SPEC.md](SPEC.md) 第 8、9、11 章 |
| 查名词 / SKILL.md / 目录横表 | [research/comparison.md](research/comparison.md) |
| 查各平台差异与调研缺口 | [research/README.md](research/README.md) |
| 查还没查清什么 | [research/RESEARCH-STATUS.md](research/RESEARCH-STATUS.md) |

## 规范 30 秒摘要

```text
Skill = 一个目录 + 一个 SKILL.md 主文件 + 按需增加的辅助文件

文件形态：单文件 / 多文件资源包
任务路线：单路线 / 多路线（套件）
实现方式：指令执行 / 脚本辅助 / 外部工具集成
组织范围：单个 Skill / 多个独立 Skill / 可选 Router
这些维度可以组合；多路线不等于多文件，带脚本不等于独立 Skill

正文设计：流程型 / 操作集合型 / 规则评审型 / 产物模板型 / 路由型
按任务特点组织章节；多包平级组织，确有选择困难时再加 Router

三层加载：能力与适用事件写单行 description（L1），主工作流写正文（L2），
细节按需读（L3：references/, examples/, scripts/, assets/）
evals/ 为作者回归材料，不作为日常任务依赖；结构按需生长，不预建空目录

普通 skill 满足准确触发、主流程、完成/停止条件、按需资源、依赖副作用说明和
风险匹配验证即可停止扩展；不为形式补 manifest、脚本、评测、adapter 或部署证据
安装或变更已安装实例时检查重复发现；纯源码修订只检查当前包和声明的镜像

治理 metadata：version / updated 记录行为版本与日期；需要随文件明确责任时，
maintainer / updated_by 只记录当前人类负责人和当前行为版本修改人，不记录 AI
项目已有字段或版本契约时遵循项目契约；name、description 和调用控制计入行为版本

人类可读名称写 Markdown 标题；组织展示元信息只供人工阅读或自有索引
产品 UI 名和调用控制按目标平台适配；具体字段、版本差异与验证记录查 research/

references = 怎么做对   examples = 长什么样   evals = 测过了吗
skill-manifest.json = 可选且默认不建；治理信息需脱离 Git 随包携带时使用
大知识放包外，包内只写怎么查；Git 是真源，上传是发布
```

## 内容边界

| 落点 | 应放内容 |
|---|---|
| `SPEC.md` | 定义、类型与选择，包与文件格式，章节结构、写法、完整示例和验收；平台特点与治理单独成章 |
| `GUIDE.md` | 入门模板、操作路径和简短示例；引用 SPEC，不新增规范要求 |
| `research/` | 平台字段表、特定版本行为、源码观察、脚本与工具接口、证据和未验证项 |
| 采用方的 `AGENTS.md` / profile | 组织命名、私有目录、内部治理、权限与审批约定 |

## 相关仓内文档

- [skill-design.md](../skill-design.md) — 旧公开设计短文
- [skill-versioning.md](../skill-versioning.md) — 行为版本契约
- [agent-skill-map.md](../agent-skill-map.md) — Agent 与 skill 分工
