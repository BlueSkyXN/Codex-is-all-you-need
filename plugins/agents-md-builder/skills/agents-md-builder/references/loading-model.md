# 加载模型详解

SKILL.md 的核心世界观四条讲清了"是什么"。本文件讲各客户端的具体加载规则、由此带来的设计约束和边界条件。

适用基线：Codex CLI 0.167.1、Claude Code 2.1.322。Claude Code 部分按 2026-11-13 的官方文档复核；目标客户端的实际加载结果仍需用本文件的复核方法确认。客户端版本或设置变化时，重新核对相应规则。

官方来源：[Codex AGENTS.md 指南](https://developers.openai.com/codex/guides/agents-md/)；[Claude Code 指令加载与导入](https://code.claude.com/docs/en/memory#agents-md)。

## 1. 设计假设

按团队所用客户端里最严格的加载方式设计：

- 根 AGENTS.md 承载启动路由；先确认它直接加载或被客户端入口导入
- 子目录卡片可能不会自动加载，要靠根文件的目录地图和按需 cat 协议才会被读到
- 不同客户端读到的文件可能不同，用 Step 2 的加载对照表逐个核对

从子目录启动时，Codex 会按路径链加载卡片；Claude Code 直接启用 AGENTS.md 时，可在读取子目录文件时加载卡片。使用 CLAUDE.md 导入时，逐个确认导入覆盖了哪些文件，其余卡片由根 AGENTS.md 的按需读取指引覆盖。

## 2. Codex

**全局**：Codex home（默认 `~/.codex`，可用 `CODEX_HOME` 改）里有 `AGENTS.override.md` 就读它，否则读 `AGENTS.md`；只用第一个非空文件。

**项目**：

- 从项目根（通常是 Git 根）往下走到当前工作目录；找不到项目根时只看当前目录
- 每个目录最多取一个文件，依次找 `AGENTS.override.md`、`AGENTS.md`、`project_doc_fallback_filenames` 里列的文件名；不在列表里的文件名（如 `CLAUDE.md`）不参与
- 从根往下拼接，越靠近当前目录越靠后，冲突时越近越优先
- 到当前目录为止，更深的子目录不加载
- 每次启动构建一次（TUI 通常是每个会话一次），改了文件要新开会话才生效

**仓库外的上级目录**：默认 Git 项目边界下，不在项目指令加载路径上。若目标环境改变了项目根识别方式，先确认实际项目根。

**复核**：查 `$CODEX_HOME/sessions` 下最新会话记录里注入的 `# AGENTS.md instructions for <目录>` 段，看包含了哪些文件。

子目录 AGENTS.md 被消费的三种路径：

1. Codex 从该子目录或其后代目录启动（少见）
2. 根 AGENTS.md 明确指引 agent："修改 `services/payments/` 前，先 cat `services/payments/AGENTS.md`"
3. 用户在会话中显式要求读取该文件

## 3. Claude Code

以下默认行为以 Project instructions 为 `claude-md-or-agents-md` 为前提；先核对目标会话的实际设置。

**什么时候读 AGENTS.md**（v2.1.277 起）：默认设置下，启动目录及其上级都没有 `CLAUDE.md`、`.claude/CLAUDE.md`、`CLAUDE.local.md` 时才读 AGENTS.md；有其中任何一个，就只读 CLAUDE.md 系列。`~/.claude/CLAUDE.md`、组织下发的 managed `CLAUDE.md` 和 `.claude/rules/` 不影响这个判断，会和 AGENTS.md 一起加载。

**读哪些**：

- 启动时：启动目录及所有上级目录（一直到文件系统根）里的 `AGENTS.md` 和 `.claude/AGENTS.md`
- 工作中：用 Read 打开某个子目录的文件时，加载该子目录的 `AGENTS.md`，前提是那里没有自己的 CLAUDE.md 系列文件
- 不读：`AGENTS.override.md`、`AGENTS.local.md`、`.agents/` 目录下的任何文件

**怎么合并**：所有文件拼接进上下文，不互相覆盖；从文件系统根往下排列，越靠近启动目录越靠后。两条指令矛盾时，Claude 可能任选一条。

**导入**：文件里的 `@path` 会展开，相对路径以导入它的文件为准，最多嵌套 4 层；行内代码和代码块里的 `@path` 不展开。导入不减少上下文占用。

**长度**：官方建议每个 CLAUDE.md 不超过 200 行；AGENTS.md 按同样标准控制。

**设置**：`/config` 里的 Project instructions 默认是 `claude-md-or-agents-md`；改成 `claude-md-and-agents-md` 后两种都读（每个目录先 CLAUDE.md 后 AGENTS.md，已经读过的 AGENTS.md 不重复读）。这个设置只在用户级 `~/.claude/settings.json`、`--settings` 文件或 managed 设置里生效，写进项目设置无效。

**读不了 AGENTS.md 的会话**：读取 AGENTS.md 的内置插件被禁用；从 2.1.276 及更早版本升级后的第一个会话；2.1.281 之前的部分会话（如 Amazon Bedrock、关闭遥测）。这些会话要靠 `CLAUDE.md` 里的 `@AGENTS.md` 导入。

**复核**：会话里运行 `/memory` 看文件列表；交互会话启动时会显示 `no CLAUDE.md found; AGENTS.md loaded: <路径>` 这样的提示。

## 4. 共存：Codex 和 Claude Code 共用一套规则

AGENTS.md 作为共享规则的唯一原件，客户端专属文件只放导入和专属内容。先核对上级目录、客户端版本和 Project instructions 设置，再决定是否需要桥接文件。导入根文件不会自动导入其他子目录卡片，仍保留根路由的按需读取协议。

| 情况 | 做法 |
|---|---|
| 只有 AGENTS.md，且当前会话能直接加载它 | 不建 CLAUDE.md |
| 团队有不支持直接加载 AGENTS.md 的 Claude Code 会话 | 本仓库根建 `CLAUDE.md`，首行 `@AGENTS.md` |
| 仓库内已有 `CLAUDE.md` 或 `.claude/CLAUDE.md` | 共享内容收进对应 AGENTS.md，原入口按相对路径导入，再保留 Claude Code 专属内容；根 `.claude/CLAUDE.md` 应从上一级目录导入共享原件 |
| 只有上级目录的 CLAUDE.md 系列文件阻断直接加载 | 保留上级文件，在本仓库根新建 `CLAUDE.md`，内容为 `@AGENTS.md` |
| Project instructions 为 `claude-md` | 使用已有 CLAUDE.md 入口导入，缺少入口时在本仓库根创建 |
| Project instructions 为 `managed-only` | 项目入口不生效；汇报需要用户调整配置，不自动修改设置 |
| 子目录同时有 `CLAUDE.md` 和 `AGENTS.md` | Claude Code 读 CLAUDE.md，Codex 读 AGENTS.md；在该子目录的 CLAUDE.md 里同样导入 |
| 目录里有 `AGENTS.override.md` | Codex 读 override，Claude Code 读普通 AGENTS.md；暂停，让用户决定 override 策略 |
| 个人的 `CLAUDE.local.md` | 不改。默认设置下它会阻断直接加载；提示用户按该文件位置导入目标 AGENTS.md，或把 Project instructions 设为 `claude-md-and-agents-md` |
| `CLAUDE.md` 是指向 AGENTS.md 的软链接 | 能用，内容只读一次；有 Windows 协作者时改用导入（建软链接需要权限，Git 可能把它检出成一行文本） |
| `CLAUDE.md` 里只用文字写"请阅读 AGENTS.md" | 改成 `@AGENTS.md` 导入；文字提示要等 Claude 自己决定去打开 |
| 两边都要看到的内容 | 直接写进 AGENTS.md；`@path` 只有 Claude Code 展开，Codex 的加载规则里没有导入 |
| Codex 需要读 CLAUDE.md | 一般不需要。确有需要时由用户在 `~/.codex/config.toml` 的 `project_doc_fallback_filenames` 里加上它，且只在同目录没有 AGENTS.md 时生效 |

## 5. 仓库外的层级

- **用户全局文件**：Codex 读 Codex home 里的 `AGENTS.md`（或 override），Claude Code 读 `~/.claude/CLAUDE.md`，两份互不相通。内容要一致时由用户自己同步；本 skill 默认不改全局文件。
- **多仓库工作区的上级 AGENTS.md**（如 `<workspace>/AGENTS.md`，下面放着多个 Git 仓库）：Claude Code 直接启用 AGENTS.md 时会向上加载它，使用 CLAUDE.md 入口时要检查导入。Codex 按实际项目根划定路径；默认 Git 项目边界下，工作区文件不在子仓库会话的加载路径中。从非 Git 工作区目录本身启动时，Codex 会读取当前目录。必须对 Codex 子仓库会话生效的规则放进各仓库根文件或 Codex 全局文件。

## 6. 其他客户端：写进策略前先核对

Copilot、Cursor、Qoder 等客户端是否读 AGENTS.md、怎么读，以各自官方文档为准。写进策略前回答五个问题：

1. 读不读 AGENTS.md？用什么文件名，能否配置备用文件名？
2. 从哪些目录读：只读仓库根、读项目根到启动目录的路径，还是也读上级目录？
3. 子目录的文件什么时候加载？
4. 有没有大小上限，超出后怎么处理？
5. 和它自己的规则文件同时存在时读哪个、按什么顺序？

答不出来的写进 Step 2 的"不确定的命令或假设"，不要按 Codex 或 Claude Code 的行为类推。

## 7. 字节预算

Codex 用 `project_doc_max_bytes` 控制项目指令读取预算，默认 **32 KiB**：路径上的 AGENTS.md 合计达到上限后，不再加入后面的文件；空文件跳过。

注意：

- 这个预算**只对自动加载的项目指令生效**——也就是项目根到当前目录路径上的 AGENTS.md
- 子目录卡片如果是按需 cat，**不进入这个预算**，但 cat 进上下文后仍占用对话 token
- Claude Code 对启动指令给出长度建议；按需加载的子目录 CLAUDE.md、其导入文件和 rules 另有单文件字符限制，超限时只加载开头。具体限制随客户端和上下文窗口变化，见[官方大小限制说明](https://code.claude.com/docs/en/memory#claude-ignores-the-end-of-my-subdirectory-claude-md)。不要把建议的 200 行当成硬上限，也不要假设按需文件可以无限长

实际取值建议（按 UTF-8 文件字节估算，**不**按 token / 段落 / 行数）：

| 文件 | 目标 | 硬上限 |
|---|---|---|
| 根 AGENTS.md | 8–16 KiB | 25 KiB |
| 子目录 Domain card | 0.5–2 KiB | 4 KiB |
| 子目录 Guardrail card | 0.5–2 KiB | 4 KiB |
| 生成 / 只读目录卡片 | < 0.5 KiB | 1 KiB |

超过硬上限要么拆 references 子文件（仓库内可以用 Markdown 链接），要么裁掉重复 / 空泛内容。客户端专属文件只含导入和专属内容，通常不到 1 KiB。

## 8. 执行环境与命令约束

Agent 常在受限环境里运行：可能没有网络、不能等用户输入、没有 sudo 和凭据、只能写工作区。Codex 的沙箱和 Claude Code 的权限设置都可能带来这些限制。

**Validation 命令落入 AGENTS.md 时必须区分两类**：

| 类别 | 处理方式 |
|---|---|
| 受限环境也能运行（单元测试、lint、typecheck、纯文件操作） | 直接列出，不加额外标注 |
| 需要网络 / Docker / 数据库 / 外部服务 / 凭据 / sudo / 交互 | **显式标注限制**，并明确"在受限环境下跳过或改用 X" |

**不要把需要外部依赖的命令当作默认验证步骤**。如果 e2e 测试需要数据库，那它就不是"完成验证"的默认动作，而是"需要数据库可用时再跑"的可选验证。

## 9. AGENTS.override.md

override.md 只有 Codex 读，用于**屏蔽**同目录的 AGENTS.md（不是"补充"，是"替换"）。Claude Code 不读它，仍读同目录的普通 AGENTS.md，所以目录里一旦有 override，两个客户端看到的规则就不一样。

如果目标目录已经存在 `AGENTS.override.md`，继续创建或更新同目录普通 `AGENTS.md` 对 Codex 通常没有效果。此时必须暂停并问用户是维护 override，还是移除 / 改造现有 override 策略。

默认**不创建**。只有以下情况才考虑：

- 仓库已有 AGENTS.md 由其他系统/团队维护，本 skill 不能直接改它
- 需要在临时分支/特定场景下覆盖整套规则
- 用户明确要求

其他情况一律继续用 AGENTS.md 增量维护。

如果本 skill 判断需要创建或修改 override.md，**必须停下来询问用户**，不要自动创建或改写。

## 10. 与 README / CONTRIBUTING 的关系

AGENTS.md 是**给 agent 看的项目指令**，不是用户文档。两者面向不同读者：

| 维度 | AGENTS.md | README |
|---|---|---|
| 读者 | Agent | 人类开发者 |
| 触发 | 启动时自动加载 | 人主动打开 |
| 重点 | 命令、约束、目录地图、按需 cat 协议 | 项目介绍、安装、用法、贡献 |

**关键命令必须复述进 AGENTS.md**，不能只写 "see README"。原因：

- Agent 不一定会主动去读 README 推断命令
- 依赖 README 等于丢失启动上下文
- 写 "see README" 等于强制 agent 额外开一次工具调用，且读到的内容可能与 README 当前状态不匹配

可以的写法：

- AGENTS.md 列出命令和最小说明
- 详细解释、背景、设计动机放 README

## 11. 冲突优先级

按顺序处理：

1. **根 AGENTS.md 与子目录 AGENTS.md 冲突** → 子目录优先（更接近适用范围），并在子目录卡片里写明替换了根文件的哪条规则
2. **客户端当前的加载方式与已有 AGENTS.md 内容冲突** → 以核实过的当前加载方式为准
3. **删除 / 压缩 / 改写已有人工维护内容** → 必须在最终汇报中列摘要并说明理由
4. **冲突无法安全判断** → 暂停并请求用户确认，不要静默删除

不要假装看不到冲突。看似人工维护的重要规则被删时，**显式说出来**比偷偷删更安全——用户可以选择恢复。
