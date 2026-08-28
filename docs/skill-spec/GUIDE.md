# Agent Skill 上手指南

| 项 | 值 |
|---|---|
| 定位 | [SPEC.md](SPEC.md)（Agent Skill 开发规范）的入门伴侣：十分钟写出第一个能用的 skill |
| 读者 | 第一次写 skill 的人，不要求会写代码；工程与评审读者请直接读 SPEC |
| 效力 | 本文只讲路径与示例，条款以 SPEC 为准；两文冲突时以 SPEC 为准 |
| 分发 | 与 SPEC.md 同目录分发；单独转发本文亦可独立阅读 |

---

## 0. Skill 是什么（三句话）

1. Skill 是给 AI 助手（Claude Code、Codex、Copilot CLI、CodeBuddy、WorkBuddy、Qoder 等）预先写好的一份**工作说明书**：教它在某类任务上按你的流程做事。
2. 最小的 skill 就是**一个文件夹 + 一个 `SKILL.md` 文件**，纯文本，不用写代码。
3. AI 会参考文件开头的单行 `description` 判断这个 Skill 能处理什么事件或任务——描述是否准确，直接影响 Skill 是否被正确选择。

## 1. 第一步：抄模板

新建一个文件夹，起英文名（如 `weekly-report`），在里面新建 `SKILL.md`，把下面整段抄进去：

```markdown
---
name: weekly-report
description: 将一周内的工作记录归纳为结构化周报，适用于已有聊天记录、待办清单、commit 记录或进度笔记需要汇总成稿的任务。
---

# 周报生成

## 适用事件与输入
- 已有零散的一周工作记录，需要归类、压缩并整理为周报

## 工作流
1. 向用户要本周的工作记录（聊天记录、待办清单、commit 记录均可）
2. 按「本周完成 / 进行中 / 下周计划 / 风险与求助」四栏归类
3. 每条写成「动词开头 + 可量化结果」，删掉过程性流水账
4. 输出成 Markdown，请用户确认后再定稿

完成条件：
- [ ] 四栏齐全，无空栏（确无内容的栏写「无」）
- [ ] 每条不超过两行

## 异常与禁止
- 记录不足以成文时，先列出缺口问用户，禁止编造工作内容
- 禁止把敏感数据（客户名、金额）原样写入，除非用户明确要求
```

这已经是一个完整合格的 skill，可以直接停在这里。下面真正必改的是 `name`、`description` 和正文；metadata 只在协作治理需要时增加，平台展示名只在目标产品确有独立 UI 名需求时增加。

## 2. 第二步：改三组核心内容，按需补两组

### 2.1 `name`：给它起个英文名

规则一句话：**全小写英文，词间用连字符，文件夹名和 `name` 保持一致**。如 `weekly-report`、`prd-writer`、`meeting-notes`。

想叫中文名（如「周报生成」）怎么办：文件夹和 `name` 仍用英文，在 `description` 中用中文描述能力和适用事件。AI 选择 Skill 时主要参考 `description`，不是靠 `name` 猜任务，所以英文命名不影响中文环境使用。部分产品界面另有「展示名」字段可填中文，属产品自己的功能，填不填都不影响 Skill 本体。

### 2.2 `description`：描述能力和适用事件

这是全文件最重要的一段。口诀：**做什么 + 适用于什么事件、任务或输入状态**。

- 描述客观任务语义：处理对象、已有输入、目标动作和所处状态。不要猜用户会说哪些关键词、口令或固定句式。
- 整段必须写在 `description:` 所在的单个物理行；不要使用 `>`、`>-`、`|`、`|-` 等多行写法。
- 建议 100～200 字，核心能力和适用事件前置。
- 办公类 Skill（如 `office-*`，以及文档、表格、演示、PDF、周报、邮件、飞书流程）默认优先使用中文 `description`；只有目标用户明确以其他语言为主时才例外，产品名、API、配置键和代码标识符保留原文。这是本项目规范，不是各平台的语言硬限制。
- 默认不写「什么时候不用」；只有相邻 Skill 职责确实重叠、正向边界仍无法区分时，才补最小必要的排除说明。
- 开头两条 `---` 之间这块区域叫 frontmatter（元信息区）：冒号后面有空格，缩进用空格不用 Tab。

### 2.3 `metadata`：记录版本和人类责任

这是协作和分发时才需要的治理信息，不是最小 Skill 的必填内容。

- 新建 Skill 的首个实质状态写 `version: "0.1"`；处于初始开发的 `0.x` Skill 下一次实质状态递增次段，例如 `0.1 -> 0.2`，即使调整调用名也不自动跳到 `1.0`。`1.0` 只在负责人明确声明首个稳定公开契约时使用；已有 Skill 不得因为复制模板而改回 `0.1`。
- `updated` 写当前行为版本最终形成的日期，格式为 `YYYY-MM-DD`；同一未发布修改批次内不要每改一次就重写日期。
- `maintainer` 写当前人类负责人或稳定团队；`updated_by` 写形成当前行为版本并对结果负责的人类修改人。
- 多人使用英文逗号加一个空格分隔，例如 `"Alice, Bob"`。
- 不记录 AI、formatter、CI 或自动镜像；AI 参与修改时，记录提出、审阅并接受该版本的人类负责人和修改人。
- 不设置 `author`；原始作者和历史贡献者由 Git history / PR 保存。

个人自用且不需要随文件记录维护责任时，可以只保留 `name`、`description`，省略整个 `metadata`。多人协作或公开发布时必须维护 `version` / `updated`；`maintainer` / `updated_by` 用于需要随文件明确责任的场景。

### 2.4 平台展示名：默认不加，按目标产品落位

展示名不是可移植 frontmatter 字段，不能为了“兼容更多平台”同时堆进 `SKILL.md`：

- OpenAI Codex / ChatGPT：写在 `agents/openai.yaml` 的 `interface.display_name`；创建该 sidecar 时同时填写非空 `interface.short_description`。
- Claude Code：当前 Skill frontmatter 没有独立 display-name 字段；`name` 本身用于列表展示。为保持可移植性，仍让目录名与 `name` 一致，不拿它做本地化文案。
- WorkBuddy：只有明确面向 WorkBuddy 且需要单独 UI 名时，才在 `SKILL.md` 顶层写 `display_name: "展示名"`。它不影响触发，不能替代 `name` / `description`；默认省略，不写 `display-name` 或 camelCase `displayName`。

### 2.5 正文：把你的做法写成步骤

正文是 skill 被唤起后 AI 实际照着做的部分：

- 按「适用事件与输入 / 工作流 / 完成条件 / 禁止」四段写，工作流用有序步骤。
- **完成条件要可检查**：「四栏齐全」「每条不超过两行」是可检查的；「质量要高」不是。
- 你平时怎么给新同事交接这件事，就怎么写。

## 3. 第三步：放哪里

写好的文件夹整个放进所用工具的 skill 目录（「用户级」对你所有项目生效；「项目级」只对当前项目生效）：

| 工具 | 用户级 | 项目级 |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `<项目>/.claude/skills/` |
| Codex CLI | `~/.agents/skills/` | `<项目>/.agents/skills/` |
| Copilot CLI | `~/.copilot/skills/` | 见产品文档（多根互通） |
| CodeBuddy | `~/.codebuddy/skills/` | `<项目>/.codebuddy/skills/` |
| WorkBuddy | `~/.workbuddy/skills/` | `<项目>/.workbuddy/skills/` |
| Qoder | `~/.qoder/skills/` | `<项目>/.qoder/skills/` |

说明：`~` 指你的用户主目录；路径以各产品最新文档为准。在产品界面里直接新建 skill 的（QoderWork 等），界面上的「名称 / 描述 / 内容」就分别对应 `name` / `description` / 正文，本指南的写法建议同样适用。

放好后重启或新开一个会话，提交一个符合 `description` 所述事件、输入状态和任务目标的代表性任务，观察它是否选择正确的 Skill。

## 4. Skill 选择不准怎么办

只有两种病，各有一条修法：

| 症状 | 修法 |
|---|---|
| 应选择但未选择 | 补齐缺失的事件、输入状态、处理对象或目标动作，不堆砌用户话术 |
| 不应选择却选择 | 收窄正向任务边界；只有仍与相邻 Skill 冲突时才补最小排除说明 |

改完重开会话再试。每次只改 `description`，不用动正文。

## 5. 什么时候需要建文件夹结构（多数人不需要）

单个 `SKILL.md` 能容纳的，就不要建目录。只有材料真实多起来时才加：

- 执行细则长了 → 拆到 `references/` 目录，正文留一句「详见 references/xxx.md」
- 想给 AI 看输出样例 → 放 `examples/`
- 有固定要跑的脚本 → 放 `scripts/`

先建空目录等着装东西是被规范明确禁止的。详细规则见 SPEC 第 4～5 章。

## 6. 想分享给团队或网上发布时

个人自用到此为止。要多人协作或分发时再补三件事：

1. frontmatter 里维护 `metadata.version`（一个未发布修改批次最终形成新的实质状态时只升一次）和 `metadata.updated`（该批次最终状态日期）；需要随文件明确责任时，再维护 `metadata.maintainer` 与 `metadata.updated_by`。规则见 SPEC 第 6、9 章。
2. 先区分内部私有协作与公开 / 可外发分发：任何包都不得含密钥、凭据或客户原始报告；公开边界不得含内网地址或可识别个人 / 客户数据。内部私有案例只有逐项满足 SPEC 4.3 的明确授权、写入前风险提醒、人工持久化决定、最小必要、受限分发和对外脱敏条件时才可纳入；仅本次使用授权不等于允许写进 Skill（SPEC 5.4）。
3. 用 SPEC 第 11 章的清单自查一遍。

默认不要创建 `skill-manifest.json`。只有 Skill 脱离 Git 分发后仍必须随包携带维护人和简短 changelog 时，才按下面的轻量格式增加：

```json
{
  "maintainer": "Alice",
  "changelog": [
    {
      "version": "0.1",
      "date": "2026-07-28",
      "updated_by": "Alice",
      "changes": "建立首个可执行版本。"
    }
  ]
}
```

manifest 中的 `maintainer` 和最新一项 `updated_by` 必须与 `SKILL.md` 的同名 metadata 一致。多人时用英文逗号加一个空格分隔，只记录负责人和人类修改人，不记录 AI。`changes` 保持单行简短；完整修改过程查 Git 和 PR。公开发布或多人协作本身不要求创建这个文件。

## FAQ

- **必须懂 Git 吗？** 个人自用不必须。团队协作或公开发布时，规范要求以 Git 仓库为唯一真源（SPEC 2.3、第 9 章）。
- **一个 skill 能干几件事吗？** 同一类事的几条路线可以（如「PDF 提取 / 填表 / 合并」），互不相干的事（如「写周报」和「初始化数据库」）必须拆成两个 skill（SPEC 3.2）。
- **`version` 和 `updated` 不写行吗？** 个人自用可不写；分发时必须写（SPEC 6.1）。
- **为什么不写 `author`？** Git history / PR 已经保存原始作者和历次贡献者；`maintainer` 表示当前负责人，`updated_by` 表示形成当前行为版本的人类修改人，三者不应混用。
- **不同平台怎么写展示名？** Codex 用 `agents/openai.yaml.interface.display_name`；WorkBuddy 才在 `SKILL.md` 顶层写可选 `display_name`；Claude Code 没有独立字段。纯展示名变化不升级行为版本。
- **短时间连续修改要每次升版吗？** 不要。同一未发布任务、同一 PR 或同一轮 review 中的连续修订合并成一个版本，只在最终形成新的实质状态时升一次。初始开发阶段统一递增 `0.x` 次段（如 `0.1 -> 0.2`）；`1.0` 是负责人明确声明的首个稳定公开契约，不由一次不兼容修改自动触发。进入稳定阶段后，兼容变化升次段，破坏公开契约才升主段。前一版本已发布或成为正式基线后，新的实质变化才开始下一次升版。
- **`skill-manifest.json` 必须有吗？** 不必须，默认不要创建。只有维护人与简短 changelog 确需脱离 Git 随包携带时才添加，而且不放运行时规则。
- **怎么禁止模型自动调用？** 默认不写任何字段；只有目标平台支持且 Skill 必须由用户显式调用时，才写 `disable-model-invocation: true`。Codex 使用 `agents/openai.yaml` 中的 `policy.allow_implicit_invocation: false`。
- **别人的 skill 能直接装吗？** 装之前通读它的 `SKILL.md` 和脚本——skill 既是提示词也是可执行代码，按不可信代码对待（SPEC 5.4）。
