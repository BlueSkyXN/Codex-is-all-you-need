---
name: agents-md-builder
description: "为仓库或工作区设计、新建、审计或重构 AGENTS.md 分层：根路由、子目录卡片、命令与验证，以及 Codex 和 Claude Code 的指令共存。用于“写 AGENTS.md”“AGENTS 分层”“整理仓库指令”“CLAUDE.md 和 AGENTS.md 怎么共存”“按加载模型重构”等请求。只问概念或仅审查规则措辞时不用。"
metadata:
  version: "0.1"
  updated: "2026-11-13"
---

# AGENTS.md 分层构建

## 何时用这个 skill

- 仓库还没有 AGENTS.md，要从零设计一套
- 已有指令文件不符合所用客户端的实际加载方式，要按加载模型重构
- 团队同时用多个客户端（如 Codex 和 Claude Code），要让同一套规则在各客户端都生效
- 审计现有分层：覆盖度、路由是否失效、哪个客户端读得到哪份文件
- 多仓库工作区的上级 AGENTS.md：先按 `references/loading-model.md` 的“仓库外的层级”说明哪些客户端读得到

本 skill 决定文件放在哪、谁在什么时候读到、根文件怎么路由。仅审查已有规则的措辞时，直接按该请求处理。只问“AGENTS.md 是什么”时直接回答，不走分层构建流程。

## 核心世界观（开始前必读）

1. **根 AGENTS.md 是共享原件，也是启动期 router。** 设计目标是让各客户端读到这份原件；实际加载取决于项目边界、override、预算和客户端设置。其他客户端先按 `references/loading-model.md` 的核对清单确认。
2. **子目录卡片的加载时机因客户端而异。** Codex 启动时只读项目根到启动目录这条路径上的文件；Claude Code 直接启用 AGENTS.md 时，会在读取子目录文件时加载相应卡片。通过 CLAUDE.md 导入根文件只保证该导入生效，其他卡片仍要按实际加载方式核对。根文件要给出目录地图和按需读取协议。
3. **客户端专属文件会改变谁读到什么。** 启动目录及其上级有 `CLAUDE.md`、`.claude/CLAUDE.md` 或 `CLAUDE.local.md` 时，Claude Code 默认只读这些文件，不读 AGENTS.md；`AGENTS.override.md` 只有 Codex 读，会替换同目录的 AGENTS.md。设计前先盘点这些文件。
4. **仓库根以上的目录，两个客户端读法不同。** Claude Code 会一直读到文件系统根；Codex 从项目根（通常是 Git 根）开始，另外只读 Codex home 里的全局文件。要两边都生效的规则，放进仓库根 AGENTS.md。

完整加载模型、字节预算、共存做法、override 处理和其他客户端核对清单：见 `references/loading-model.md`。

## 三类文件判定

只用三种，不要再细分。只导入 AGENTS.md 的客户端专属文件（如 `CLAUDE.md`）不承载共享规则，按 Step 5 处理。

| 目录类型 | 选哪个模板 | 是否必须创建 |
|---|---|---|
| 仓库根 | Root router | 是 |
| 应用、服务、共享库、有独立职责边界的业务模块 | Domain card | 有边界风险/不变量/专属验证时才创建 |
| infra / migrations / auth / payments / secrets / generated / vendor 等高风险或只读 | Guardrail card | 该目录存在且会被手动改时通常创建 |
| 纯组织层级目录、无独立规则、无专属验证 | 不创建 | 否 |

判定原则：**只在有实际价值时创建**。不要为了覆盖率给纯组织目录建空 AGENTS.md。

三类模板的完整结构和示例：见 `references/card-templates.md`。

## 六步流程

### Step 1：只读探索（≤30 次 tool 调用）

识别七件事：技术栈、目录职责、现有指令文件、团队使用的客户端、命令（test/lint/build/codegen/migration）、高风险目录、生成/只读目录。

- **现有指令文件**要盘全：任意层级的 `AGENTS.md`、`.claude/AGENTS.md`、`AGENTS.override.md`、`CLAUDE.md`、`.claude/CLAUDE.md`、`CLAUDE.local.md`、`.claude/rules/`，仓库外上级目录里的指令文件，以及其他客户端的规则文件。区分用户全局文件和会改变项目加载选择的上级文件。
- **客户端**从这些文件、`.codex/`、`.claude/` 等配置目录和 README / CONTRIBUTING 判断。看不出来时，按 Codex 和 Claude Code 都在用来设计，并在 Step 2 写明这个假设。

Git 操作只允许只读命令：`git status`、`git diff`、`git ls-files`、`git rev-parse`、`git log`。
普通仓库探索允许使用只读文件命令，如 `pwd`、`find`、`rg`、`sed`、`cat`、`head`、`wc`。

完整探索清单（必查项 / 推荐命令 / 忽略目录 / 预算控制）：见 `references/output-format.md` 的探索清单段。

### Step 2：输出放置策略（到对话，不落盘）

在对话里输出一份简短策略，不要创建 `AGENTS_PLAN.md` 或类似计划文件。

必须包含：
- 仓库类型 + 主要技术栈
- 团队使用的客户端，以及判断依据或假设
- 已有指令文件清单（含 `AGENTS.override.md` 和客户端专属文件）
- 要新增或更新的文件路径清单
- 每个文件的类型（Root router / Domain card / Guardrail card / 客户端专属文件）
- 每个文件主要承载哪些指令类型（Principle / Rule / Convention / Procedure）及原因
- 加载对照表：每个客户端从仓库根启动、从常用子目录启动时分别读到哪些文件
- 不创建 AGENTS.md 的目录及原因
- 不确定的命令或假设

输出后**直接进入 Step 3**，不等用户确认。除非命中下方"暂停条件"。

### Step 3：写根 AGENTS.md

必须包含：仓库目的、Agent 启动行为（所用客户端各自怎么加载本仓库的指令）、目录地图（含 Local AGENTS.md 列和 Read when 列）、按需 cat 协议、关键命令复述、全局规则、Do not、Validation 标准。

按 `references/instruction-types.md` 区分 Principle、Rule、Convention、Procedure：
根文件只保留跨目录判断、可验证规则、全局约定和必要的流程入口，不把局部操作
流程伪装成全局原则。

目标长度 **8–16 KiB**，硬上限 **25 KiB**。Codex 默认只加载路径上合计 32 KiB 的 AGENTS.md，达到上限后不再加入后面的文件；Claude Code 文档建议每个文件不超过 200 行。

完整模板和必含元素：见 `references/card-templates.md` 的 Root router 段。

### Step 4：写必要的子目录 AGENTS.md

Domain card 或 Guardrail card，单文件 **0.5–2 KiB**。

只在"三类文件判定"通过时写。无独立价值的目录不写。

用四类指令决定内容落点：Domain card 只写本模块特有 Principle/Rule/Convention/
Procedure；Guardrail card 优先写有触发条件和验证方式的 Rule，以及有完成/停止
条件的 Procedure。不要重复上级规则：Claude Code 会把根文件和读到的卡片一起放进上下文，重复内容占两份。

完整模板见 `references/card-templates.md` 的对应段。

### Step 5：处理客户端专属文件

AGENTS.md 是共享规则的唯一原件，客户端专属文件只放导入和该客户端独有的内容。按 Step 2 的加载对照表，逐项对照 `references/loading-model.md` 第 4 节处理：

- **当前会话能直接加载 AGENTS.md，且仓库没有 CLAUDE.md 系列文件**：不新建桥接文件。先检查上级目录和客户端设置，不能只看仓库内。
- **仓库内已有 `CLAUDE.md` 或 `.claude/CLAUDE.md`**：把共享规则收进相应 AGENTS.md，再从原文件导入并保留专属内容；大量删改前按暂停条件处理。导入路径以导入文件所在目录为基准。
- **仓库内没有入口，但上级 CLAUDE.md 系列文件阻断直接加载，或目标会话不支持直接加载 AGENTS.md**：在本仓库根添加只含 `@AGENTS.md` 的 `CLAUDE.md`。上级文件保持原样；子目录卡片继续通过根路由按需读取。

`CLAUDE.local.md` 是个人文件，不改，只提示其对加载的影响及用户可选的导入或设置方案。若设置禁用了项目指令（如 `managed-only`），在汇报中说明需要用户调整配置，添加桥接文件不能解决。其他客户端先按 `references/loading-model.md` 第 6 节核对。模板见 `references/card-templates.md`。

### Step 6：自检与最终汇报

自检清单和中文最终汇报格式：见 `references/output-format.md` 的自检 + 汇报段。

同时检查：

- Principle、Rule、Convention、Procedure 没有混写成含义不清的口号
- Rule 有范围、触发条件和真实验证方式
- Procedure 有输入、顺序、输出、完成和停止条件
- Principle 没有被机械化为无适用条件的绝对禁令
- 按 Step 2 的加载对照表，逐个客户端完成 `references/output-format.md` 的“客户端加载”核对项；汇报里附上运行时复核方法

## 硬约束

- **只创建或更新指令文件**：AGENTS.md，以及 Step 5 确定要改的客户端专属文件（如 `CLAUDE.md`）。不修改源码、测试、README、lock 文件、build/CI/deployment 配置、generated、vendor、docs，也不改客户端配置（如 `~/.codex/config.toml`、`~/.claude/settings.json`）；需要改配置时写进汇报，由用户决定。
- **不创建 AGENTS.override.md**。如果目标目录已有同目录 `AGENTS.override.md`，或判断需要创建 / 修改 override，停下来询问用户。
- **Git 操作只读**：禁止 `git add` / `git commit` / `git reset` / `git checkout` / `git clean` / `git stash`。只用 `git status` / `git diff` / `git ls-files` / `git rev-parse` / `git log`。
- **命令必须来自仓库实际配置**：从 `package.json` scripts、`Makefile`、`pyproject.toml`、CI 配置、官方文档中确认存在。**不编造**。不确定就写"不确定"并指回根命令。
- **Validation 命令优先选受限环境能运行的**（无网络、非交互、非 sudo、不依赖外部服务）。需要网络/Docker/数据库/凭据/sudo 的命令**必须显式标注**。
- **不重复上级指令文件已覆盖的规则**。
- **不写空话**："遵循最佳实践""写高质量代码"——除非后面跟具体标准。
- **不复制 README 大段**，不泄露 secret / token / PII。
- **不创建空文件**。

## 暂停条件（命中则停下问用户）

- 已有指令文件看起来人工精心维护，新策略要删大量内容
- 现有指令文件与新规则严重冲突，无法安全判断
- 已有 `CLAUDE.md` 或其他客户端规则文件内容较多，需要决定以哪份为原件、怎么合并
- 目标目录已有 `AGENTS.override.md`：Codex 读它，Claude Code 读同目录的普通 `AGENTS.md`，两边会分叉
- 需要创建或修改 `AGENTS.override.md`
- 需要修改指令文件之外的文件，或修改客户端配置

其他情况一律继续执行，不要反复请示。

## 冲突优先级

- 根与子目录指令冲突 → **子目录优先**（更接近适用范围）。在子目录卡片里写明它替换了根文件的哪条规则：Claude Code 只按顺序拼接文件，两条矛盾时可能任选一条
- 同目录 `AGENTS.override.md` 与 `AGENTS.md` 冲突 → Codex 中 **override 生效**；不要写一个会被 Codex 忽略的普通 AGENTS.md
- 客户端当前的加载方式与已有文件里的描述冲突 → **以核实过的当前加载方式为准**
- 删除/压缩/改写已有重要内容 → 必须在最终汇报中列出摘要并说明理由

## 语言

- 指令文件本体：优先沿用仓库现有文档主语言（英文文档→英文 AGENTS.md，中文文档→中文 AGENTS.md，无法判断→英文）
- 对用户的最终汇报：始终用中文

## references 索引

| 文件 | 何时读 |
|---|---|
| `references/loading-model.md` | 开始前必读：Codex 与 Claude Code 的加载规则、共存做法、仓库外层级、其他客户端核对清单、字节预算、执行环境限制、override、与 README 的关系 |
| `references/card-templates.md` | Step 3–5 写文件时：三类卡片和客户端专属文件的模板、必含元素、禁止事项、最短形式示例 |
| `references/output-format.md` | Step 1 探索时 + Step 6 汇报时：探索清单、推荐命令、忽略目录、自检项、中文最终汇报格式 |
| `references/instruction-types.md` | Step 2–6：判断 Principle、Rule、Convention、Procedure 的落点和硬检查 |

按需读取，不要一次性全读。SKILL.md 本身的判断和约束足够覆盖大多数决策；只在写具体内容、收尾汇报、或对加载模型有疑问时才打开对应 references。
