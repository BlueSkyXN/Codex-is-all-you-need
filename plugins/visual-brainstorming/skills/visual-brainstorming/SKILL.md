---
name: visual-brainstorming
description: 两种模式。理解模式——把代码/文档里的真实结构提炼成架构图、关系图、流程图，帮助看懂一个项目而无需逐行读码，默认输出单文件 HTML 到 local/。决策模式——用本地浏览器并排展示并点选 2–4 个结构不同的 UI/架构/流程方案。仅在视觉化明显优于文字时使用；不用于普通问答、简单表格、代码轨迹或隐藏推理。
license: MIT. See LICENSE.txt.
metadata:
  short-description: 本地可视化：项目结构理解 + 方案比较选择
  version: "0.2"
  updated: "2026-07-29"
---

# Visual Brainstorming

把适合“看”的东西可视化：要么帮你**看懂一个项目的真实结构**，要么帮你**在几个候选方案里点选一个**。需求澄清、理由和最终结论留在对话或项目文档中。

**硬边界：** 页面是 Agent 生成的 HTML/CSS/SVG 外部产物，不是模型隐藏思维、Token 轨迹、注意力权重或内部状态。

概念参考 `obra/superpowers` 的 Visual Companion / Visual Brainstorming；本 Skill 为独立实现。出处见 `NOTICE.md` 与 `references/SOURCES.md`。

## 0. 先分流：理解模式 还是 决策模式

两种模式共用同一个本地 companion、同一套会话目录和浏览器交互，但目标和触发条件不同。

| | 理解模式（explore） | 决策模式（compare） |
|---|---|---|
| 用户要什么 | 帮我**看懂**这个项目/系统 | 帮我**在几个方案里选一个** |
| 典型触发 | “梳理这个项目”“架构图”“调用关系”“这个项目怎么跑的”“画个图帮我理解” | “帮我选”“哪个方案好”“对比一下这几个设计” |
| 输入 | 已有代码 + 文档（结构未知） | 2–4 个已想清的候选方案 |
| 默认产物 | 单文件 HTML 写到 `local/`，**默认不开浏览器** | 本地浏览器并排点选 |
| 是否需要提炼 | **必须先提炼（EXTRACTION.md）** | 不需要 |

**判断顺序：**

1. 用户想“看懂/梳理/理解”一个已存在的系统 → **理解模式**。
2. 用户面前摆着几个结构不同的候选，要你帮忙定一个 → **决策模式**。
3. 两者都不沾（普通问答、Markdown 表格足够、只需一张简单静态图、隐藏推理）→ 不要用本 Skill，用 Mermaid/ASCII/文字。

**理解模式专属规则：**

- **先提炼，后画图。** 生成任何 HTML 之前，必须先按 `references/EXTRACTION.md` 产出 `extraction.json`，把 `entities / edges / claims / paths` 核对清楚，尤其要区分“文档声称（claimed）”“代码坐实（verified）”“存在冲突（contradicted）”。**不允许凭印象直接画图。**
- **默认不开浏览器。** 提炼后用 `export` 把片段烘成自包含单文件 HTML 写到 `local/`（如 `local/<project>-architecture.html`），同时用 `--extraction` 把提炼 JSON 持久化到运行根的 `exports/<id>/`；产物内联了 frame CSS 和 explore helper，双击即可离线看。只有用户明确说“在浏览器里给我看”时，才走 `companion.py show` 打开本地页。

  ```bash
  python3 -I -S "$SKILL_DIR/scripts/companion.py" export \
    --source /tmp/arch.html \
    --output "$PROJECT_ROOT/local/<project>-architecture.html" \
    --project-dir "$PROJECT_ROOT" \
    --extraction /tmp/extraction.json
  ```
- **提炼遇到真实架构分叉时**，（例如“代码是单体，文档却说是三层”），把分叉整理成 2–3 个候选，**转入决策模式**让用户点选——这是两种模式的串联点。
- 渲染用 `assets/templates/explore-map.html`，节点用 `data-node`/`data-flows`/`data-evidence` 标注；交互由 `assets/explore-helper.js` 驱动（路径筛选、节点详情、证据边框、疑惑上报）。

下面第 1–6 节描述**决策模式**的完整流程。

## 运行要求与网络边界

- 需要 Python 3.9+，以及能够访问 Agent 主机本地 HTTP 服务的浏览器。
- 默认服务仅监听 `127.0.0.1`；正常工作流不得添加 `--allow-remote`。
- 只有用户明确要求、理解明文 HTTP 风险且目标位于受信任网络或安全隧道后时，才允许使用远程绑定。`--url-host` 必须是 Agent 主机实际持有的 literal loopback/private/link-local IP；不要把服务暴露到公网、不受信任局域网或另一台内网主机。
- 远程环境无法访问本地服务时，直接使用静态图、Mermaid、ASCII 或结构化文字降级，不把放宽监听地址当作默认修复。

## 默认读取预算

正常执行只读取：

1. 本文件；
2. 与当前模式匹配的**一个**模板：决策模式用 `assets/templates/choice-grid.html` 等，理解模式用 `assets/templates/explore-map.html`。

不要默认读取 `README.md`、实现脚本、全部示例或全部参考资料。理解模式画图前必须先读 `references/EXTRACTION.md`；只有定制视觉时读 `references/VISUAL_AUTHORING.md`；运行失败时读 `references/TROUBLESHOOTING.md`。

## 1. 判断是否启用

仅在以下三个条件全部成立时使用：

1. 决策依赖布局、空间、层级、流程、状态、数据流、视觉密度或交互路径；
2. 存在 2–4 个结构上真实不同、值得比较的候选方案；
3. 并排看图会明显降低纯文字描述的歧义。

不要用于：普通文字澄清、Markdown 表格足够的参数比较、代码或日志轨迹、只需一张简单图、没有明确待决策变量、隐藏推理请求，或用户已拒绝本次浏览器展示。

单张简单图优先使用 Mermaid、ASCII 或聊天内静态图。

## 2. 处理同意

- 用户已明确要求“在网页或浏览器中展示、做 mockup、画图让我点选”，视为已同意。
- 隐式触发时，只在首次打开本地页面前询问一次：

> 这一项更适合并排看图。我可以打开一个仅本机可访问的页面，展示方案并记录你的点击；也可以继续只用聊天。是否启用？

用户拒绝后继续在聊天中完成，不再次推销。

## 3. 确定路径

- `SKILL_DIR`：本 `SKILL.md` 所在目录；不要假设它等于插件根目录。
- `PROJECT_ROOT`：优先使用宿主或用户给定的项目根目录；否则使用 Git 根目录；再否则使用当前可写目录。

会话数据写入 `PROJECT_ROOT/.visual-brainstorming/`；运行时会在其中自动写入 deny-all `.gitignore`。

## 4. 快路径：一屏、一文件、一条命令

### 4.1 先定义本屏

写清：

- 本屏只决定什么；
- 哪些变量固定；
- 唯一允许变化的主变量；
- 用户应观察的 1–3 个差异；
- 数据是事实、估算还是示意。

默认给 2–3 个方案；只有第四个方案具有独立逻辑时才增加到 4 个。

### 4.2 只复制一个模板

按任务选择：

- 通用方案：`assets/templates/choice-grid.html`
- UI/导航：`assets/templates/ui-compare.html`
- 架构/数据流：`assets/templates/architecture-compare.html`
- 流程/状态：`assets/templates/process-compare.html`

生成 UTF-8 HTML **片段**，默认使用内置 CSS 类，不写自定义 JavaScript。每个可选元素必须包含：

```html
<article data-choice="stable-id" data-label="方案名称">…</article>
```

页面要求：

- 一屏只比较一个主变量，其他条件保持一致；
- 方案差异必须体现在结构、路径、层级或空间关系上，而不是只换颜色；
- 同一比较尺度；写明适用条件和主要代价；
- 非实测数字明确标为“示意”或“估算”；
- 360px 与桌面宽度均可读；
- 不依赖 CDN、远程字体或在线图片；
- 目标文件尽量控制在 120 KB 内。

### 4.3 启动、发布并打开

把片段写到一个可写的临时文件，然后只运行一条命令：

```bash
python3 -I -S "$SKILL_DIR/scripts/companion.py" show \
  --project-dir "$PROJECT_ROOT" \
  --source "/absolute/path/to/draft.html" \
  --name "decision-name" \
  --open
```

`show` 会复用或启动服务、原子发布页面，并在发布完成后请求打开浏览器。不要再额外执行 `start` 和 `status`，除非排查故障。

首次 URL 的 fragment 含随机会话密钥；应使用 `show` 返回的完整 URL，不要公开到外网。页面加载后会把密钥保存在当前 origin/tab 的 `sessionStorage` 并清理地址栏；Cookie 不作为会话凭据。

### 4.4 把控制权交给用户

发布后只说明：

- 本屏解决什么；
- 建议观察什么；
- 可以点击方案，也可以直接在聊天中回答。

然后结束当前轮次，不继续堆叠新问题。

## 5. 下一轮读取选择

读取最近事件：

```bash
python3 -I -S "$SKILL_DIR/scripts/companion.py" events \
  --project-dir "$PROJECT_ROOT" --tail 20
```

处理规则：

- 采用最近一次有效 `choice`，并同时考虑其后的 `note`；
- 聊天中的明确修正优先于浏览器旧事件；
- 没有事件时允许用户直接在聊天中选择；
- 下一屏只处理尚未确定的新变量，不重新发散已解决的问题。

## 6. 结束与降级

视觉探索结束后，把确认方向、放弃方案、理由和未验证假设写回项目设计文档或实现计划，然后停止服务：

```bash
python3 -I -S "$SKILL_DIR/scripts/companion.py" stop \
  --project-dir "$PROJECT_ROOT"
```

本地 URL 不可达时，不声称页面已打开。保留 HTML，并改用静态图、Mermaid、ASCII 或结构化文字继续，不让浏览器能力阻塞任务。

建议项目忽略：

```gitignore
.visual-brainstorming/
```

历史 session 会保留用于审计。只有用户要求清理时才先运行 dry-run：

```bash
python3 -I -S "$SKILL_DIR/scripts/companion.py" prune \
  --project-dir "$PROJECT_ROOT"
```

dry-run 会返回绑定精确候选列表的 `plan`。检查列表后，只有用户明确同意这些候选时，才用相同参数执行 `--apply --plan "<dry-run-plan>"`；若 plan 失效则重新预览，不得绕过。不得清理当前或仍在运行的 session。

## 按需资料

- 页面编写与质量规则：`references/VISUAL_AUTHORING.md`
- 标准会话与高级命令：`references/WORKFLOW.md`、`references/PROTOCOL.md`
- 运行故障：`references/TROUBLESHOOTING.md`
- 搬入现有插件与裁剪：`references/ADAPTATION.md`
- 背景、评估、学习与来源：`references/BACKGROUND.md`、`references/EVALUATION.md`、`references/LEARNING_GUIDE.md`、`NOTICE.md`
