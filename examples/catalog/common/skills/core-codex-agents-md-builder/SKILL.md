---
name: core-codex-agents-md-builder
description: 为 Codex 仓库设计、审计或重构 AGENTS.md 层级；用于写/改/审计 AGENTS.md，不用于 CLAUDE.md 或 Cursor 规则。
metadata:
  version: "0.3"
  updated: "2026-06-12"
---

# Codex AGENTS.md 设计技能

## 何时用这个 skill

- 仓库还没有 AGENTS.md，要从零设计一套
- 已有 AGENTS.md 但不符合 Codex 实际加载模型，要按根启动 workflow 重构
- 需要审计现有 AGENTS.md 的覆盖度、冲突点、过时项

不适用：CLAUDE.md / Cursor 规则 / 其他格式；仅询问"AGENTS.md 是什么"的解释类问题。

## 核心世界观（开始前必读）

四件事讲清整个任务的前提：

1. Codex 从仓库根目录启动时，repo-local 启动上下文通常只包含根 AGENTS.md。
2. 子目录 AGENTS.md 对该子树仍有效；但从根启动时，它通常需要由**根 AGENTS.md 的按需 cat 协议**指引才会被消费。
3. 所以根 AGENTS.md 是**启动期 router**，子目录 AGENTS.md 是**按需 navigation card**。
4. 如果目标目录已有 `AGENTS.override.md`，同目录普通 `AGENTS.md` 会被替换，必须先暂停确认。

完整加载模型、字节预算、override.md 处理、沙箱限制：见 `references/loading-model.md`。

## 三类文件判定

只用三种，不要再细分。

| 目录类型 | 选哪个模板 | 是否必须创建 |
|---|---|---|
| 仓库根 | Root router | 是 |
| 应用、服务、共享库、有独立职责边界的业务模块 | Domain card | 有边界风险/不变量/专属验证时才创建 |
| infra / migrations / auth / payments / secrets / generated / vendor 等高风险或只读 | Guardrail card | 该目录存在且会被手动改时通常创建 |
| 纯组织层级目录、无独立规则、无专属验证 | 不创建 | 否 |

判定原则：**只在有实际价值时创建**。不要为了覆盖率给纯组织目录建空 AGENTS.md。

三类模板的完整结构和示例：见 `references/card-templates.md`。

## 五步流程

### Step 1：只读探索（≤30 次 tool 调用）

识别六件事：技术栈、目录职责、已有 AGENTS.md/override.md、命令（test/lint/build/codegen/migration）、高风险目录、生成/只读目录。

Git 操作只允许只读命令：`git status`、`git diff`、`git ls-files`、`git rev-parse`、`git log`。
普通仓库探索允许使用只读文件命令，如 `pwd`、`find`、`rg`、`sed`、`cat`、`head`、`wc`。

完整探索清单（必查项 / 推荐命令 / 忽略目录 / 预算控制）：见 `references/output-format.md` 的探索清单段。

### Step 2：输出放置策略（到对话，不落盘）

在对话里输出一份简短策略，不要创建 `AGENTS_PLAN.md` 或类似计划文件。

必须包含：
- 仓库类型 + 主要技术栈
- 已有的 AGENTS.md / AGENTS.override.md 清单
- 要新增或更新的 AGENTS.md 路径清单
- 每个文件的类型（Root router / Domain card / Guardrail card）
- 不创建 AGENTS.md 的目录及原因
- 不确定的命令或假设

输出后**直接进入 Step 3**，不等用户确认。除非命中下方"暂停条件"。

### Step 3：写根 AGENTS.md

必须包含：仓库目的、Codex 启动行为、目录地图（含 Local AGENTS.md 列和 Read when 列）、按需 cat 协议、关键命令复述、全局规则、Do not、Validation 标准。

目标长度 **8–16 KiB**，硬上限 **25 KiB**。

完整模板和必含元素：见 `references/card-templates.md` 的 Root router 段。

### Step 4：写必要的子目录 AGENTS.md

Domain card 或 Guardrail card，单文件 **0.5–2 KiB**。

只在第 3 节"判定"通过时写。无独立价值的目录不写。

完整模板见 `references/card-templates.md` 的对应段。

### Step 5：自检与最终汇报

自检清单和中文最终汇报格式：见 `references/output-format.md` 的自检 + 汇报段。

## 硬约束

- **只创建或更新 AGENTS.md**。不修改源码、测试、README、lock 文件、build/CI/deployment 配置、generated、vendor、docs。
- **不创建 AGENTS.override.md**。如果目标目录已有同目录 `AGENTS.override.md`，或判断需要创建 / 修改 override，停下来询问用户。
- **Git 操作只读**：禁止 `git add` / `git commit` / `git reset` / `git checkout` / `git clean` / `git stash`。只用 `git status` / `git diff` / `git ls-files` / `git rev-parse` / `git log`。
- **命令必须来自仓库实际配置**：从 `package.json` scripts、`Makefile`、`pyproject.toml`、CI 配置、官方文档中确认存在。**不编造**。不确定就写"不确定"并指回根命令。
- **Validation 命令优先选默认沙箱可运行**（无网络、非交互、非 sudo、不依赖外部服务）。需要网络/Docker/数据库/凭据/sudo 的命令**必须显式标注**。
- **不重复上级 AGENTS.md 已覆盖的规则**。
- **不写空话**："遵循最佳实践""写高质量代码"——除非后面跟具体标准。
- **不复制 README 大段**，不泄露 secret / token / PII。
- **不创建空文件**。

## 暂停条件（命中则停下问用户）

- 已有 AGENTS.md 看起来人工精心维护，新策略要删大量内容
- 现有 AGENTS.md 与新规则严重冲突，无法安全判断
- 目标目录已有 `AGENTS.override.md`，会屏蔽同目录普通 `AGENTS.md`
- 需要创建或修改 `AGENTS.override.md`
- 需要修改 AGENTS.md 之外的文件

其他情况一律继续执行，不要反复请示。

## 冲突优先级

- 根 AGENTS.md 与子目录 AGENTS.md 冲突 → **子目录优先**（更接近适用范围）
- 同目录 AGENTS.override.md 与 AGENTS.md 冲突 → **override 生效**；不要写一个会被忽略的普通 AGENTS.md
- 新 Codex 加载模型与已有 AGENTS.md 内容冲突 → **新模型优先**
- 删除/压缩/改写已有重要内容 → 必须在最终汇报中列出摘要并说明理由

## 语言

- AGENTS.md 文件本体：优先沿用仓库现有文档主语言（英文文档→英文 AGENTS.md，中文文档→中文 AGENTS.md，无法判断→英文）
- 对用户的最终汇报：始终用中文

## references 索引

| 文件 | 何时读 |
|---|---|
| `references/loading-model.md` | 开始前必读：Codex 加载模型、字节预算、override.md 处理、沙箱限制、与 README 的关系 |
| `references/card-templates.md` | Step 3、4 写文件时：三类卡片完整模板、必含元素、禁止事项、最短形式示例 |
| `references/output-format.md` | Step 1 探索时 + Step 5 汇报时：探索清单、推荐命令、忽略目录、自检项、中文最终汇报格式 |

按需读取，不要一次性全读。SKILL.md 本身的判断和约束足够覆盖大多数决策；只在写具体内容、收尾汇报、或对加载模型有疑问时才打开对应 references。
