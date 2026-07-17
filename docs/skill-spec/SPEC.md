# Skill 开发规范

| 项 | 值 |
|---|---|
| 文档 ID | `skill-spec` |
| 版本 | 0.1 |
| 日期 | 2026-07-17 |
| 权威范围 | 分档、单包结构、内容落点、SKILL.md 写法、多 skill 组织、合格判定 |
| 真源路径 | `docs/skill-spec/SPEC.md` |
| 适用对象 | 作者、评审、Agent |

本规范以两条基线校准，条款不超出它们的交集：

1. **实践基线**：本仓库 `plugins/*/skills/*` 与作者既有 skill 仓库的真实形态。
2. **平台基线**：Agent Skills 开放标准与各平台公开约束（证据见 [research/](research/README.md)）。

---

## 第 0 章　如何使用本文

### 0.1 人怎么读

| 你要做的事 | 读哪些章 |
|---|---|
| 新建一个 skill | 第 1、2、3、4 章 + 第 9 章清单 |
| 评审 PR | 第 8 章禁止项 + 第 9 章清单 |
| 组织多个 skill / 建 router | 第 5 章 |
| 定版本、跑门禁 | 第 7 章 |

### 0.2 Agent 怎么执行

```text
1. 只把「必须 / 禁止」当硬约束；「建议」默认照做
2. 顶层目录以第 3 章白名单为准，不发明未列出的顶层名
3. 结构按需生长：先判断现有材料够不够单文件，再决定建目录
4. 冲突时：更具体的条款 > 总述口号
5. 「说明 / 理由」小节不构成新目录或新例外的授权
```

### 0.3 用语强度

| 用语 | 含义 |
|---|---|
| **必须** / **禁止** | 违反即不合格 |
| **建议** | 默认照做；例外需能说明理由 |
| **可以** | 可选 |

### 0.4 不管什么

Agent / 专家角色设计（见 [agent-design.md](../agent-design.md)）、中央知识库选型与权限模型、各平台官方长文原文（见 [research/](research/README.md)）。

---

## 第 1 章　总则与分档

### 1.1 核心原则

1. **Skill 是可触发的工序单元**，不是长文百科，不是中央知识库。
2. **一个 skill = 一个目录 + 一个 `name` + 一个 `SKILL.md`**。
3. **Git 为协作真源，平台为发布渠道**：上传 / 市集上架是发布动作，不是多人共编方式。
4. **Portable 底座 = Agent Skills 开放标准**（`SKILL.md` + `name`/`description` + 渐进披露）；平台私有能力走 adapter，不污染最小结构。
5. **结构按需生长**：从单文件开始，材料出现了再建目录；**禁止**预建空目录。
6. **外部 skill 与中央知识只引用，不复制正文**。

### 1.2 四档与判定

分档描述「这个包现在长什么样」，不是升级路线图；一个 skill 可以永远停在最小档。

| 档 | 一句话判定 | 真实实例 |
|---|---|---|
| **最小** | 只需 `SKILL.md` 即可完整执行 | codex-next 的大部分叶子（`office-weekly-report`、`data-tabular-analysis`…） |
| **标准** | 单文件装不下，出现 `references/` 或 `scripts/`、`examples/` | `expression-fixer`、`dev-bugfix` |
| **集合** | 一个包内多条**同一意图族**的路线，配套文件成型 | `visual-brainstorming`、`hidden-watermark-risk-analysis`（外部仓） |
| **群** | 数十个独立 skill 的平级编队，可选 router 引导 | codex-next（57 叶 + `core-router` / `sdlc-router`） |

**集合档硬约束：**

- **必须**仍是一个包：一个 `name`、一个 `SKILL.md`；**禁止**包内嵌套子 `SKILL.md`。
- **必须**多条路线同属一个意图族（周报 + 修 bug + 画架构不能硬塞一包），且正文写清路线选择。

**群的量感（建议，非铁律）：**

- 参考线约 30 个独立可触发 skill，且入口多样到需要引导，才值得建 router；本仓库实例 codex-next 现有 57 叶配了两级 router。
- 规模在两位数早期时：靠 `description` 区分 + 文档级地图（README / docs）即可，**不要**急着建 router。
- **禁止**用同一 workflow 拆成 Phase 1…N 冒充多个独立 skill。

---

## 第 2 章　内容落点

先问一句：**这段材料执行时要不要被 agent 读？**

### 2.1 决策表

| 你手里的材料 | 落点 |
|---|---|
| 触发条件、主工作流、完成条件、硬禁令 | `SKILL.md` 正文 |
| 执行时按需查的规则、协议、契约、排查手册 | `references/`（短则直接并入正文） |
| 输入输出样张、正反例、长支路演示 | `examples/` |
| 触发 / 质量回归材料（运行时默认不读） | `evals/` |
| 一跑就稳的命令与脚本 | `scripts/` |
| 输出模板、图标、静态资源 | `assets/` |
| 大体量 / 多包共享 / 有权限边界的语料 | **包外**（KB、MCP、独立仓库）；包内只写怎么查 |
| 外部 skill 的工序 | **包外引用**：`SKILL.md` 写清何时用、怎么调 |

### 2.2 三个资料目录的分工

```text
references = 怎么做对（执行说明，默认平铺）
examples   = 长什么样 / 这种情形怎么走（示范）
evals      = 测过了吗（回归；默认运行时不读）
```

同一事实**只留一份真源**：铁律写在 `SKILL.md` / `references`，examples 只做示范，evals 只写可观察断言。三者都可以没有。

### 2.3 中央知识与外部 skill（包外原则)

任一命中即放包外：体积大（数千 token 以上）、更新节奏独立于 skill 流程、被多个 skill 共享、有权限或密级差异。

- 包内**可以**写「怎么查」：用哪个服务 / 命令、典型 query、结果怎么用——直接写进 `SKILL.md` 或 `references/` 的一个文件，不需要专用配置格式。
- **禁止**把中央知识正文拷进包内，**禁止**建立包内快照目录当第二真源（真源漂移的根源）。
- 外部 skill（如 lark-cli 舰队）：稳定名称引用 + 写清前置条件与失败降级；**禁止**复制对方正文。

---

## 第 3 章　单包目录结构

### 3.1 顶层白名单

```text
<skill-id>/                  # 必须：目录名 = name，kebab-case
├── SKILL.md                 # 必须：唯一入口
├── references/              # 可选：按需读的执行说明，默认平铺
├── examples/                # 可选：样张与长支路演示
├── scripts/                 # 可选：可执行辅助
├── assets/                  # 可选：模板与静态资源（可有 templates/ 等子目录）
├── evals/                   # 可选：回归材料，默认运行时不读
├── agents/
│   └── openai.yaml          # 可选：Codex 平台 adapter
└── README.md / LICENSE* / NOTICE*   # 可选：分发说明文件，不承载工序
```

**禁止的结构：**

- 包内第二个 `SKILL.md`（含 `subskills/**/SKILL.md` 嵌套）。
- 白名单之外发明顶层目录（分发说明文件除外）。
- 包内版本目录（`v2/`、`v3/`）：大版本换代要么按第 7 章版本契约升主版本，要么开平级新包（如 `lobster-daily-report-v2`，既有实践）。

**遗留形态**：历史包把说明 md 平铺在包根（早期个人仓库常见）不判不合格，但新建包不采用；迁移或大改时收进 `references/`。收编外部第三方包时同理：白名单外的既有顶层目录先不判不合格，随大改收敛到白名单。

### 3.2 生长谱系（真实实例）

```text
office-weekly-report/          SKILL.md                              ← 最小
expression-fixer/              + references/
dev-bugfix/                    + references/ + scripts/
hidden-watermark-risk-…/       + assets/ + evals/ + README.md
visual-brainstorming/          + agents/ + examples/ + LICENSE/NOTICE  ← 全形态
```

每一步都由真实材料驱动；没有材料就停在上一步。除 `hidden-watermark-risk-analysis` 位于作者外部 skill 仓库外，其余实例均可在本仓库 `plugins/` 下核验。

### 3.3 命名

**必须：**

- 目录名 = `name`，匹配 `^[a-z0-9]+(?:-[a-z0-9]+)*$`。
- 入口文件名固定 `SKILL.md`。

**建议：**

- 群内用前缀分域：`core-` / `sdlc-` / `dev-` / `data-` / `office-` / `research-`（既有实践，兼容各家扁平发现模型）。
- `references/` 语义名平铺（`output-contract.md`、`troubleshooting.md`）；同主题文件很多时最多一层子目录。
- `examples/` 语义名；正反例用 good / bad 标注，前后缀均可（既有实践：`weekly-report-good.md`、`failure-cases.md`）；演示序列可用 `NN-<slug>.*`；不用日期当文件名（样张是稳定资产，不是日志）。
- `scripts/` 动宾式（`diagnose_image_watermark.py`）；公共模块名不限（`audit_common.py`）。

### 3.4 发货与提交

| 内容 | 处置 |
|---|---|
| `SKILL.md`、`references`、`examples`、`scripts`、`assets`、`agents/`、分发说明文件 | 随包发布 |
| `evals/` | 建议随包（便于消费方回归；非运行时依赖） |
| `__pycache__/`、`.DS_Store` 等生成物与系统垃圾 | **禁止**提交 |
| 密钥、内网路径、真实客户数据 | **禁止**出现在包内任何文件 |

平台打包注意：ClawHub 仅接受文本文件、单包上限 50MB；WorkBuddy 类工作台暂无稳定公开打包规范，以导出包实测为准；真源始终在 Git，打包由脚本完成。

---

## 第 4 章　`SKILL.md` 写法

### 4.1 Frontmatter

**必须**（`scripts/check_skill_metadata.py` 门禁校验）：

```yaml
---
name: <与目录名一致>
description: >-
  <做什么>。当 <用户真实说法的触发场景> 时使用。
metadata:
  version: "0.1"          # 两段式字符串，契约见 docs/skill-versioning.md
  updated: "YYYY-MM-DD"
---
```

| 字段 | 要求 |
|---|---|
| `name` | 必须；与目录名一致 |
| `description` | 必须；含**做什么 + 何时用**；触发信息必须写在这里，不能只写正文（发现层只读 metadata）。**建议**补「何时不用」，尤其曾误触发时。长度建议一两百字，portable 硬上限 1024 字符 |
| `metadata.version` | 必须（本仓库公开 skill 治理）；行为版本字符串 |
| `metadata.updated` | 必须；`YYYY-MM-DD` |

**可以**（既有实践）：`license`、`compatibility`、`metadata.short-description`、`metadata.domain` 等自由字段。开放标准要求解析器忽略未知字段；但跨运行时全矩阵尚未实测，混投新平台前先冒烟。

**平台扩展落点**（按需，互不污染）：

| 平台 | 扩展方式 |
|---|---|
| Codex | sidecar `agents/openai.yaml`（顶层键 `interface` / `policy` / `dependencies`） |
| Claude Code / CodeBuddy | frontmatter 运行时字段（`allowed-tools` 等），仅面向该平台时写 |
| OpenClaw | `metadata.openclaw` 命名空间 |

### 4.2 正文

**必须**只有四条：

1. 主工作流写在正文（触发后正文是唯一保证加载的内容，**禁止**正文只剩链接壳）。
2. 关键路线有**可观察完成条件**（命令、产物、检查项）。
3. 集合档写清路线选择。
4. 相对链接全部可达；**禁止**为了好看预链不存在的文件。

**建议骨架**（非强制；既有 skill 各有自己的结构，如「使用场景」「检测框架」）：

```markdown
# <标题>
## 适用 / 不适用
## 前置检查
## 工作流          # 每条路线附完成条件
## 输出与完成条件
## 异常与 Do not
## 参考            # 只链真实存在的文件与外部 skill
```

---

## 第 5 章　多 skill 组织

### 5.1 布局

```text
skills/（或 plugins/<id>/skills/）
  core-router/        # 可选引导包，本身也是一个合法单包
  <domain>-router/    # 可选
  leaf-a/             # 每个叶子独立遵守第 3～4 章
  leaf-b/
  …
```

平级目录 + 前缀分域；文档地图放 docs / README，不占运行时。

### 5.2 Router 职责边界

- **只选路**：意图识别 → Route 表 → 交给叶子执行。
- **禁止**复制叶子正文；**禁止**用户要结果时只指路不执行。
- Route 表建议含：条件、目标 skill、原因；外部前置（如 lark 登录）单独列。

### 5.3 群内调用协议

```markdown
当 <条件>：使用 `<skill-name>`
- 传入：…
- 期望返回：…
- 返回后本 skill 继续：…
```

---

## 第 6 章　评测 evals

- 只回答两件事：**该不该触发**（trigger）、**结果过不过**（quality）。
- 默认运行时不读；读者是作者与 CI。
- **形态自由**：json / yaml / md 皆可（既有实践：`evals/trigger_queries.json`）。建议至少覆盖「应触发 / 不应触发」两类样本；质量断言写可观察要点与禁令，不复制整本手册。
- 有回归需求再建（description 大改过、曾误触 / 漏触、完成条件变更）；**禁止**预建空 `evals/`，**禁止**把日常操作步骤写进 evals 代替正文。

---

## 第 7 章　版本与协作

### 7.1 版本

契约全文见 [skill-versioning.md](../skill-versioning.md)，要点：

- 首个实质状态 `"0.1"`；兼容变化升次段（`0.9 -> 0.10`）；破坏调用名 / IO 契约 / 脚本 CLI / 默认主路径升主段。
- `updated` 取最后实质变更的 Git committer date。
- Plugin 包 SemVer（`.codex-plugin/plugin.json`）与 skill 行为版本**分开**管理。

门禁命令：

```bash
python3 scripts/check_skill_metadata.py check --base-ref origin/main
```

### 7.2 协作流程

| 变更 | 流程 |
|---|---|
| `SKILL.md` / `references` / `scripts`（行为面） | PR + 评审 |
| `examples` 新增样张 | 轻量评审 |
| `evals` | 与对应行为变更同一 PR |
| 发布到平台 | 构建产物上传；真源在 Git |

catalog 镜像（如 `examples/catalog` 与 codex-next 包副本）**必须**逐字节一致，由门禁校验。

---

## 第 8 章　禁止清单（总表）

```text
1.  包内第二个 SKILL.md；subskills 嵌套
2.  白名单外发明顶层目录（分发说明文件除外）
3.  预建空目录
4.  SKILL.md 断链；预链不存在的路径
5.  触发条件只写正文、不进 description
6.  正文空心化：主工作流不在 SKILL.md
7.  复制外部 skill 或中央知识正文进包；包内快照第二真源
8.  Router 复制叶子全文；用户要结果时只指路不执行
9.  集合包塞入不同意图族的多条工作流；Phase 拆包凑数
10. evals 当运行时主手册；铁律只写在 examples
11. 提交生成物、系统垃圾、密钥或真实敏感数据
```

---

## 第 9 章　合格清单

### 9.1 所有单包

- [ ] 目录名 = `name` = kebab-case；有且仅有一个 `SKILL.md`
- [ ] 顶层 ⊆ 第 3.1 白名单（分发说明文件除外）
- [ ] `description` 含做什么 + 何时用（触发在 metadata 层）
- [ ] `metadata.version` / `metadata.updated` 合法，门禁通过
- [ ] 主工作流在正文且有可观察完成条件
- [ ] 无断链；无空目录；无生成物 / 敏感数据
- [ ] 外部依赖与中央知识只引用不复制

### 9.2 集合追加

- [ ] 多路线同一意图族，正文有路线选择
- [ ] 无嵌套子 skill

### 9.3 群追加

- [ ] 叶子平级、各自独立合格；router（若有）只选路
- [ ] 规模未到量感线时未建 router

---

## 第 10 章　模板

### 10.1 最小

```markdown
---
name: example-minimal
description: >-
  示例最小 skill。当用户说「跑最小示例」时使用。日常闲聊不使用。
metadata:
  version: "0.1"
  updated: "2026-07-17"
---

# Example Minimal

## 适用 / 不适用
- 适用：…
- 不适用：…

## 工作流
1. …
完成条件：
- [ ] …

## 异常与 Do not
- 禁止 …
```

### 10.2 标准

```text
example-standard/
  SKILL.md                  # 正文链到下面的真实文件
  references/
    output-contract.md
  examples/
    report-good.md          # 可选
    report-bad.md           # 可选
```

### 10.3 集合

```text
example-suite/
  SKILL.md                  # 2～3 条同意图族路线 + 路线选择
  references/
    ops-protocol.md
    troubleshooting.md
  examples/
    scenario-screenshot-only.md
  scripts/
    validate_output.py
  agents/
    openai.yaml             # 面向 Codex 发布时
```

### 10.4 Router 要点

```markdown
## 工作流
1. 识别意图 → 查 Route 表 → 处理外部前置 → 执行选中 skill → 汇总
（用户要结果时不得停在指路）

## Route 表
| 条件 | skill | 原因 |
|---|---|---|
| … | `leaf-a` | … |
```

---

## 第 11 章　相关文档

| 文档 | 关系 |
|---|---|
| `docs/skill-spec/SPEC.md` | **本文，规范权威主文** |
| [research/](research/README.md) | 平台调研证据与缺口看板，非规范正文 |
| [skill-versioning.md](../skill-versioning.md) | 版本契约与门禁细节 |
| [skill-design.md](../skill-design.md) | 公开安全的写法导读（短文） |
| [agent-skill-map.md](../agent-skill-map.md) | Agent 与 skill 分工 |

---

## 第 12 章　修订记录

| 版本 | 日期 | 说明 |
|---|---|---|
| 0.1 | 2026-07-17 | 首版（未正式发布）。由 2026-07-16 内部草稿按实践与平台双基线收敛而来：删无实践支撑的发明（`knowledge.map.yaml`、包内快照约定、evals 字段规范、「算子」术语）；evals 形态自由化、examples 命名放开；群 30 由硬门槛改量感参考；正文必须项收敛为四条，禁止清单并为 11 条。每条「必须/禁止」均可追溯到开放标准、平台硬限、本仓治理或两仓实践共识 |

---

## 附录 A　一句话备忘

```text
最小 = 单文件工序；标准 = +基础配套；集合 = 一包多路线；群 = 数十包编队
结构按需生长，没有材料不建目录
references = 怎么做对   examples = 长什么样   evals = 测过了吗（运行时不读）
触发写 description，工序写正文，大知识放包外
Git 是真源，上传是发布
```
