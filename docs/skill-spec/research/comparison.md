# 跨平台对比：名词定义 · SKILL.md · 目录结构

Last updated: **2026-07-17**

本文是 **调研证据横表**，不是开发规范正文。规范真源见 [../SPEC.md](../SPEC.md)。  
证据来源：Agent Skills 开放标准 + 各平台 extract 文档 + 本机安装样本（2026-07-17）。

---

## 0. 怎么读

| 层 | 含义 | 写 portable skill 时 |
|---|---|---|
| **开放标准核心** | 各家都认的最小公约数 | **必须遵守** |
| **产品兼容扩展** | 某产品增强、通常可忽略/旁路 | 可选 adapter |
| **产品私有层** | 分发/专家包/角色套件，不是 skill 本体 | 不要写进 portable 核心 |

---

## 1. 名词定义（Terminology）

### 1.1 开放标准对 Skill 的定义

来源：[agentskills.io home](https://agentskills.io) + [specification](https://agentskills.io/specification)

> Agent Skills are a lightweight, open format for extending AI agent capabilities with specialized knowledge and workflows.

核心句：

- **Skill = 一个文件夹**，至少含 `SKILL.md`
- `SKILL.md` 至少含 metadata（`name` + `description`）+ instructions
- 可捆绑 scripts / references / templates / other resources
- 通过 **progressive disclosure** 加载，而非一次塞进上下文

开放标准 **不定义** 以下产品概念（留给各厂商）：

- Plugin / Marketplace / Expert / Team
- Agent / Subagent 编排
- 安装路径与冲突优先级

### 1.2 各平台「Skill 是什么」

| 平台 | 对 Skill 的产品表述 | 与开放标准关系 |
|---|---|---|
| **Agent Skills（标准）** | 可移植的能力/工作流文件夹 | 定义本身 |
| **Claude Code** | 带 `SKILL.md` 的目录，扩展 Claude 工具箱；可自动加载或 `/skill` 调用；slash command 已并入 skills 模型 | 兼容并 **大幅扩展** frontmatter 运行时字段 |
| **Codex** | 可复用工作流的 **authoring unit**；Plugin 是 **distribution unit** | 兼容；用 sidecar `agents/openai.yaml` 补 UI/策略 |
| **OpenClaw** | 教 agent 如何/何时用工具的 markdown 指令包 | 兼容；`metadata.openclaw` 做 gating |
| **CodeBuddy** | 领域专家工作流包；对比 slash command 更偏自动触发与工具白名单 | 高度 Claude-like |
| **WorkBuddy** | 与 CodeBuddy/标准同形的能力包；另有 **专家包** 作为上架角色层 | Skill 层兼容；Expert 层是私有包装 |
| **Qoder / QoderWork** | 可复用领域能力；QoderWork 中 Skill=单工具，Plugin=角色工具箱 | Skill 层兼容；Plugin 是角色套件 |
| **Copilot CLI** | Agent Skills 形目录；与 user agents / plugins 并列 | Skill 层兼容；Agent 有独立 md/yaml 格式 |

### 1.3 相邻概念对照（极易混）

| 概念 | 开放标准？ | 谁在用 | 定义（调研共识） | 与 Skill 关系 |
|---|---|---|---|---|
| **Skill** | ✅ | 全员 | 可触发的工序/能力包：`dir + SKILL.md` | 本体 |
| **Plugin** | ❌ | Codex / Claude / Copilot / WorkBuddy / QoderWork | **分发与装配单元**，可装多个 skills（及 MCP/hooks/commands） | 包 Skill，不是 Skill |
| **Agent / Subagent** | ❌ | Claude / Codex / Copilot / WorkBuddy | 独立角色或子代理配置（md / toml / yaml） | 可引用 Skill；WorkBuddy 禁止 agent MD 写 tools |
| **Expert（专家包）** | ❌ | WorkBuddy | 可上架的 Agent 型或 Team 型角色包（`.codebuddy-plugin`） | 可内嵌 agents + skills |
| **Team** | ❌ | WorkBuddy / Claude teams | 多角色协作（lead + members） | 编排层，不是 skill |
| **Command / Slash** | ❌ | 多数产品 | 用户显式 `/name` 入口 | Claude 中与 skill 合流；Qoder 中常分目录 `commands/` |
| **Connector / MCP** | ❌ | QoderWork / 多数插件生态 | 外部工具桥 | Plugin 可附带；Skill 可依赖 |
| **Suite** | ❌ | Codex 本地生态 | 编排用 agent 套件（本机 `suites/all/agents`） | 非 skill 包标准 |

### 1.4 一句话心智模型

```text
Skill     = 可触发的工序说明书（+可选脚本/资料）
Plugin    = 怎么打包分发（可含多个 Skill）
Agent     = 谁来干 / 以什么角色干
Expert    = WorkBuddy 把 Agent/Team 产品化上架的壳
Command   = 用户怎么点名调用（常与 Skill 重叠）
```

### 1.5 命名冲突提醒

| 词 | 在 A 平台 | 在 B 平台 | 风险 |
|---|---|---|---|
| **Agent** | Claude/Copilot：subagent 定义 | WorkBuddy：专家类型之一 | 不要把 agent md 当成 skill |
| **Plugin** | Codex：skills 分发容器 | QoderWork：角色工具箱 | 同名不同粒度 |
| **name** | 开放标准：目录名 + kebab-case id | QoderWork UI skill：可为中文展示名 | 可移植包禁止依赖中文 name |
| **description** | 发现/触发元数据（L1） | 有人误写进正文「何时使用」 | 正文 When-to-use **不参与**多数产品的自动发现 |

---

## 2. `SKILL.md` 主文件标准

### 2.1 开放标准硬规则（可移植底线）

`SKILL.md` = **YAML frontmatter + Markdown body**。

| 字段 | 必须？ | 约束 |
|---|---|---|
| `name` | **是** | ≤64；仅 `a-z` `0-9` `-`；不以 `-` 开头/结尾；无连续 `--`；**必须等于父目录名** |
| `description` | **是** | ≤1024；非空；写清 **做什么 + 何时用**；含触发关键词 |
| `license` | 否 | 许可证名或捆绑许可证文件引用 |
| `compatibility` | 否 | ≤500；环境/产品/依赖要求 |
| `metadata` | 否 | `string → string` 映射；键名应尽量唯一 |
| `allowed-tools` | 否 | 空格分隔工具列表；**实验性**，支持度不一 |

正文：

- **无固定 schema**
- 建议：步骤、输入输出样例、边界情况
- 激活后 **整文件加载** → 长文应拆到引用文件
- 建议整文件 **&lt; 500 行**；指令层 **&lt; 5000 tokens**

校验参考：

```bash
skills-ref validate ./my-skill
```

### 2.2 渐进披露（所有兼容客户端应支持的加载语义）

| 阶段 | 加载内容 | 预算特征 |
|---|---|---|
| Discovery | 仅 `name` + `description` | ~100 tokens / skill 量级 |
| Activation | 完整 `SKILL.md` | 建议 &lt; 5000 tokens |
| Execution | `scripts/` `references/` `assets/` 等按需 | 按需，可不进上下文（脚本可直接执行） |

### 2.3 Frontmatter 字段矩阵（核心 + 扩展）

图例：`R`=产品侧必填或强烈当必填；`O`=可选；`—`=未见/不适用；`X`=产品明确禁止或冲突。

#### A. 开放标准核心

| 字段 | 标准 | Claude | Codex | OpenClaw | CodeBuddy | WorkBuddy | Qoder | Copilot |
|---|---|---|---|---|---|---|---|---|
| `name` | R | O* | R | R | O* | R | R | R |
| `description` | R | 推荐* | R | R | 推荐* | R | R | R |
| `license` | O | O | O | O | O | O | O | O |
| `compatibility` | O | O | O | O | O | O | O | O |
| `metadata` | O | O | O | O（含 vendor ns） | O | O | O | O |
| `allowed-tools` | O 实验 | O | O | O | O | O | — | O |

\*Claude/CodeBuddy 产品文档常把 `name`/`description` 写成可省略并回退目录名/首段，但 **可移植包仍应按标准必填**。

#### B. 调用控制类（多为 Claude 家族）

| 字段 | Claude | CodeBuddy | OpenClaw | Copilot | Codex | WorkBuddy | Qoder |
|---|---|---|---|---|---|---|---|
| `disable-model-invocation` | O | O | O | — | —（见 sidecar policy） | — | — |
| `user-invocable` | O | O | O | O（样本） | — | — | — |
| `argument-hint` | O | — | — | — | — | — | O（QoderWork 样本） |
| `arguments` | O | — | — | — | — | — | — |
| `paths` | O | — | — | — | — | — | — |
| `command-dispatch` / `command-tool` | — | — | O | — | — | — | — |

Codex 对等能力不在 frontmatter，而在：

```yaml
# agents/openai.yaml
policy:
  allow_implicit_invocation: true|false
```

#### C. 运行时/模型/工具类

| 字段 | Claude | CodeBuddy | Copilot skill | Copilot **agent** | WorkBuddy skill | WorkBuddy **agent MD** | QoderWork |
|---|---|---|---|---|---|---|---|
| `model` | O | O（fork） | — | O | — | — | — |
| `effort` | O | — | — | — | — | — | — |
| `context: fork` | O | O | — | — | — | — | — |
| `agent` | O | O | — | — | — | — | — |
| `hooks` | O | O（fork+trust） | — | — | — | — | — |
| `allowed-tools` / `tools` | O | O | O | **O（tools）** | O | **X 禁止 tools** | — |
| `disallowed-tools` | O | — | — | — | — | — | — |
| `shell` | O | — | — | — | — | — | — |

#### D. 产品私有 / UI / 生命周期

| 字段 | 谁 | 作用 | 可移植？ |
|---|---|---|---|
| `agent_created: true` | WorkBuddy | 允许 `skill_manage` 后续改删 | ❌ 私有 |
| `disable` | WorkBuddy 内置样本 | 启用开关 | ❌ |
| `version`（顶层） | QoderWork creators | 技能自身版本 | ⚠️ 标准推荐放 `metadata.version` |
| `description_zh` / `name_en` / `description_en` | QoderWork | 双语 | ❌ UI adapter |
| `displayName` | QoderWork 部分 skill | UI 名 | ❌ |
| `metadata.openclaw.*` | OpenClaw | OS/bin/env gating、install、emoji… | ❌ vendor ns（可共存） |
| `metadata.short-description` 等 | Codex 样本 | 短描述 | ⚠️ 用唯一键 |

### 2.4 真实 frontmatter 样本（本机）

**开放标准 / Codex 最小可移植：**

```yaml
---
name: skill-creator
description: Guide for creating effective skills. This skill should be used when...
metadata:
  short-description: Create or update a skill
---
```

**WorkBuddy 用户 skill：**

```yaml
---
name: feishu-spreadsheet-sheet-float-image
description: This skill should be used when the task involves ...
agent_created: true
---
```

**QoderWork 角色插件内 skill（中文 name，不可作为 portable 核心）：**

```yaml
---
name: PRD生成
description: >
  输入功能需求描述，生成结构化PRD文档...
argument-hint: "输入功能需求描述，如：..."
name_en: "prd-generation"
description_en: >
  Enter a feature description...
---
```

**Copilot / Claude 风格最小 skill：**

```yaml
---
name: pua
description: "Use when any task has failed 2+ times..."
---
```

### 2.5 正文（Body）标准共识

| 维度 | 共识 | 分歧 |
|---|---|---|
| 格式 | Markdown，无强制章节名 | 各 creator 推荐章节不同 |
| 语气 | 对 agent 的祈使/流程说明 | 有的样本写成「你是…」角色口吻 |
| 触发信息 | **必须在 description** | 正文再写 When to Use 仅作人类/执行补充，不替代 L1 |
| 长度 | 宜短；细节外置 | 500 行 / 5k tokens 是建议不是解析硬限 |
| 引用 | 相对路径；宜一层深 | 目录名 `references` vs `REFERENCE.md` vs `examples/` 不统一 |

推荐的可移植正文骨架（调研归纳，非标准强制）：

```markdown
# <Title>

## Overview
一句话能力边界

## When to use / When not to use
执行期补充（发现仍靠 description）

## Workflow
有序步骤

## Resources
- scripts/...
- references/...

## Output
交付物形状 / 验收点
```

### 2.6 `name` 规则冲突表（高价值）

| 规则 | 开放标准 | Claude 产品 | QoderWork UI 插件 | 可移植策略 |
|---|---|---|---|---|
| 字符集 | 小写 kebab | 更松；命令名常取 **目录名** | 允许 **中文 name** | 只用 `[a-z0-9-]` |
| 与目录名 | **必须一致** | 目录名决定 `/` 命令（多数情况） | 目录也用中文 | 目录名 = name = kebab |
| 大小写 | 禁止大写 | 较宽容 | 中文无此问题 | 全小写 |
| 显示名 | 无独立字段 | 列表可用 name/目录 | `displayName` / 中文 name | UI 名放产品层，不占 `name` |

---

## 3. 目录结构标准

### 3.1 开放标准 skill 包（唯一跨平台目录契约）

```text
skill-name/                 # 目录名 = frontmatter name
├── SKILL.md                # 必须：metadata + instructions
├── scripts/                # 可选：可执行代码
├── references/             # 可选：按需文档
├── assets/                 # 可选：模板/图片/静态资源
└── ...                     # 允许其他文件/目录
```

标准要点：

1. **唯一硬必须文件**：`SKILL.md`
2. `scripts/` `references/` `assets/` 是 **约定俗成的可选目录**，不是强制白名单
3. 允许额外目录（`...`）——产品扩展靠这个口子
4. 引用用 skill 根相对路径；**避免深层引用链**

### 3.2 可选目录职责对照

| 目录/文件 | 开放标准职责 | 典型内容 | 加载语义 |
|---|---|---|---|
| `SKILL.md` | 入口元数据 + 主指令 | frontmatter + workflow | Activation 整读 |
| `scripts/` | 可执行帮助程序 | py/sh/js | 执行，不必全文进上下文 |
| `references/` | 按需文档 | API、schema、政策 | 需要时读 |
| `assets/` | 输出用静态资源 | 模板、图标、样例文件 | 复制/引用，通常不进 prompt |
| `agents/` | **非标准**；Codex 约定 | `openai.yaml` | harness 读，不替代 SKILL.md |
| `examples/` / `EXAMPLES.md` | 常见实践 | 输入输出样例 | 按需 |
| `evals/` | Claude skill-creator 实践 | 回归集 | 运行时通常不读 |
| `templates/` | Qoder 文档示例命名 | 模板 | 约等于 assets/examples |

### 3.3 各平台 skill 目录「标准形」

| 平台 | 规范/文档推荐形 | 本机常见形 | 相对标准的增量 |
|---|---|---|---|
| **开放标准** | `SKILL.md` + scripts/references/assets | — | 基线 |
| **Codex** | 同上 + **`agents/openai.yaml`** | system skill-creator 含 agents/scripts/references/assets | sidecar |
| **Claude** | `SKILL.md` + 任意辅助文件；示例含 `examples/` `scripts/` 与平级 `reference.md` | 用户 skill 常极简仅 SKILL.md；插件另有 agents/commands | 结构更自由；eval 实践 |
| **OpenClaw** | 标准 skill 目录；可用 `{baseDir}` | 随 ClawHub 可有 `.clawhub/` 元数据 | gating 元数据在 frontmatter |
| **CodeBuddy** | Claude-like；`${CODEBUDDY_SKILL_DIR}` | 同 Claude 家族 | 占位符 |
| **WorkBuddy** | creator 明示 scripts/references/assets | 用户 skill：`SKILL.md`+`references/` | + `agent_created`；打包 zip |
| **Qoder 文档** | `SKILL.md` + REFERENCE.md/EXAMPLES.md/scripts/templates | — | 平级大写 md 文件名 |
| **QoderWork** | creator：`reference.md` `examples.md` `scripts/` | 用户/插件 skill 常仅 `SKILL.md` | 中文目录名 |
| **Copilot CLI** | Agent Skills 形 | 用户 skill 常仅 `SKILL.md` | agent 不在 skill 目录内 |

### 3.4 分发层目录（不是 skill 标准，但常被误当成 skill 标准）

```text
# Codex skill-only plugin
my-plugin/
├── .codex-plugin/plugin.json
└── skills/
    └── hello/
        └── SKILL.md

# Claude plugin（示意）
my-plugin/
├── .claude-plugin/plugin.json
├── skills/...
├── commands/...
└── agents/...

# WorkBuddy expert
my-expert/
├── .codebuddy-plugin/plugin.json
├── agents/*.md
├── skills/...
└── avatars/...

# QoderWork role plugin
产品管理/
├── .qoder-plugin/plugin.json
├── .mcp.json
├── skills/PRD生成/SKILL.md
├── README.md
└── CONNECTORS.md

# Copilot plugin（样本）
plugin-root/
├── plugin.json
├── hooks.json
├── commands/
└── scripts/
```

**写作规则：**

- 讨论「skill 目录标准」时，只比到 `skill-name/SKILL.md(+resources)`
- Plugin/Expert 清单目录名（`.xxx-plugin`）属于 **分发适配**，不得上升为 portable skill 必选结构

### 3.5 发现根目录（安装位置 ≠ 包内结构）

包内结构跨平台高度同构；**发现根**完全产品化：

| 平台 | 用户 skill 根（常见） | 项目 skill 根（常见） |
|---|---|---|
| 开放标准 | 不规定 | 不规定 |
| Claude | `~/.claude/skills/` | `.claude/skills/` |
| Codex | `$HOME/.agents/skills` 等 | `$CWD|.REPO/.agents/skills` |
| OpenClaw | `~/.agents/skills`, `~/.openclaw/skills` | `<ws>/skills`, `<ws>/.agents/skills` |
| CodeBuddy | `~/.codebuddy/skills/` | `.codebuddy/skills/` |
| WorkBuddy | `~/.workbuddy/skills/`（活体） | `.workbuddy/skills/` |
| Qoder 文档 | `~/.qoder/skills/` | `.qoder/skills/` |
| QoderWork CN | `~/.qoderworkcn/skills/` | （以产品为准） |
| Copilot CLI | `~/.copilot/skills/` | 另有多根互通（`.agents`/`.claude`/`.github`，优先级待测） |

### 3.6 「标准目录」vs「允许额外目录」

| 立场 | 谁 | 含义 |
|---|---|---|
| 标准推荐三件套 | Agent Skills | scripts / references / assets |
| 明确允许 `...` | Agent Skills | 额外目录合法 |
| 产品强推 sidecar | Codex | `agents/openai.yaml` |
| 产品示例用平级 md | Claude / Qoder | `reference.md` `EXAMPLES.md` 亦可 |
| 业务上架包 | WorkBuddy / QoderWork | expert/plugin 另有强制清单与展示字段 |

对 portable 作者的可操作结论：

1. **最小合法包**：`skill-name/SKILL.md`（仅 name+description 亦可）  
2. **标准包**：再加真正用到的 `scripts/` `references/` `assets/`  
3. **按需生长**：无材料不建空目录  
4. **产品目录**（`agents/`、中文 skill 名、plugin 壳）放适配层，不污染核心

---

## 4. 三层对照总表（一张图记住）

| 维度 | 可移植核心（所有人） | 常见兼容扩展 | 明确私有、勿当核心 |
|---|---|---|---|
| **名词** | Skill = dir + SKILL.md | Plugin 作分发；Agent 作角色 | Expert/Team 上架壳；Suite |
| **SKILL.md** | YAML + MD；`name`+`description` 必填与限额 | Claude 调用控制字段；`metadata.*` | 中文 `name`；`agent_created`；顶层随意字段 |
| **目录** | `SKILL.md`；可选 scripts/references/assets | `agents/openai.yaml`；examples/evals | `.xxx-plugin/`；avatars；中文目录 |

---

## 5. 对规范设计的直接含义（供 SPEC 校准，非 SPEC 正文）

1. **名词**：SPEC 应只把 Skill 定义成工序单元；Plugin/Agent/Expert 最多作为边界说明，不并进 skill 分类。  
2. **SKILL.md**：可移植必须集 = 开放标准六字段模型（2 必填 + 4 可选）；其余一律「平台扩展」。  
3. **目录**：标准推荐 scripts/references/assets；允许有独立职责的新目录；禁止把分发壳目录写成 skill 必选。  
4. **冲突处理**：`name` 字符集与「目录名一致」以开放标准为准；QoderWork 中文 UI 名视为产品例外。  
5. **仍待 runtime 验证**：未知 frontmatter 忽略还是拒绝；Copilot 多根发现优先级；Qoder 重名优先级。

---

## 6. 证据索引

| 主题 | 文档 |
|---|---|
| 开放标准 | [agent-skills-open-standard.md](agent-skills-open-standard.md) |
| Claude | [claude-code.md](claude-code.md) |
| Codex | [openai-codex.md](openai-codex.md) |
| OpenClaw | [openclaw.md](openclaw.md) |
| CodeBuddy | [codebuddy.md](codebuddy.md) |
| WorkBuddy | [workbuddy.md](workbuddy.md) |
| Qoder/QoderWork | [qoder.md](qoder.md) |
| Copilot CLI | [copilot-cli.md](copilot-cli.md) |
| 缺口看板 | [RESEARCH-STATUS.md](RESEARCH-STATUS.md) |

公网真源：

- https://agentskills.io/home.md  
- https://agentskills.io/specification  
