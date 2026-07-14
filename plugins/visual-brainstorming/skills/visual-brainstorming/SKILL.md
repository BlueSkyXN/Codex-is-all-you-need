---
name: visual-brainstorming
description: 用本地浏览器并排展示并点选 2–4 个结构不同的 UI/mockup、布局、架构/数据流、流程/状态或模型路由方案。仅当存在明确待决策变量，且视觉比较明显优于文字时使用；不要用于普通问答、简单表格、代码轨迹、单张简单图或隐藏推理。
license: MIT. See LICENSE.txt.
metadata:
  short-description: 本地浏览器可视化方案比较与选择
  version: "0.1"
  updated: "2026-07-14"
---

# Visual Brainstorming

把适合“看”的设计决策放进本地浏览器；把需求澄清、理由和最终结论留在对话或项目文档中。

**硬边界：** 页面是 Agent 生成的 HTML/CSS/SVG 外部产物，不是模型隐藏思维、Token 轨迹、注意力权重或内部状态。

概念参考 `obra/superpowers` 的 Visual Companion / Visual Brainstorming；本 Skill 为独立实现。出处见 `NOTICE.md` 与 `references/SOURCES.md`。

## 运行要求与网络边界

- 需要 Python 3.9+，以及能够访问 Agent 主机本地 HTTP 服务的浏览器。
- 默认服务仅监听 `127.0.0.1`；正常工作流不得添加 `--allow-remote`。
- 只有用户明确要求、理解明文 HTTP 风险且目标位于受信任网络或安全隧道后时，才允许使用远程绑定。`--url-host` 必须是 Agent 主机实际持有的 literal loopback/private/link-local IP；不要把服务暴露到公网、不受信任局域网或另一台内网主机。
- 远程环境无法访问本地服务时，直接使用静态图、Mermaid、ASCII 或结构化文字降级，不把放宽监听地址当作默认修复。

## 默认读取预算

正常执行只读取：

1. 本文件；
2. 与当前任务最接近的**一个** `assets/templates/*.html`。

不要默认读取 `README.md`、实现脚本、全部示例或全部参考资料。只有定制视觉时读 `references/VISUAL_AUTHORING.md`；运行失败时读 `references/TROUBLESHOOTING.md`。

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
