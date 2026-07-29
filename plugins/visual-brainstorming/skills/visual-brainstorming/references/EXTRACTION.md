# 结构提炼契约（理解模式）

理解模式的目标不是"画一张好看的图"，而是**先搞清结构，再把结构画对**。画图之前必须先产出一份结构提炼（extraction），否则不允许进入渲染阶段。这份契约规定提炼的字段、证据规则和落盘位置。

## 为什么先提炼、后画图

凭印象直接画图，最容易犯的错是把"文档声称的架构"画成"代码实际的架构"。提炼阶段强制把两者分开核对，让图上的每个框、每条线都能追溯到证据——这正是理解一个陌生项目时最值钱、也最容易被跳过的一步。

## 产出物：`extraction.json`

在生成任何 HTML 之前，先把提炼结果写成一份 JSON。字段：

```json
{
  "version": "1",
  "project": "项目名",
  "summary": "一句话说明这个系统是干什么的",
  "entities": [
    {
      "id": "feishu-app",
      "name": "FeishuApp",
      "kind": "service",
      "responsibility": "飞书身份、凭据、WS/HTTP 接入与限流",
      "evidence": "verified",
      "source": "src/app.ts:40"
    }
  ],
  "edges": [
    {
      "from": "feishu-app",
      "to": "agent-def",
      "label": "路由",
      "paths": ["message"]
    }
  ],
  "claims": [
    {
      "statement": "多 App × 多 Agent × 多会话",
      "evidence": ["docs/design.md:8"],
      "status": "claimed"
    },
    {
      "statement": "WorkspaceGuard 已做文件隔离",
      "evidence": ["src/guard.ts:55", "tests/guard.test.ts"],
      "status": "verified"
    },
    {
      "statement": "统一走模型网关",
      "evidence": ["docs/design.md:8", "src/agent.ts:77"],
      "status": "contradicted"
    }
  ],
  "paths": [
    { "id": "message", "name": "消息路径", "stages": ["入口", "Binding", "Agent", "模型"] }
  ]
}
```

### 字段说明

- `entities[]`：结构节点。`id` 用稳定 kebab-case；`kind` 表示类别（service / store / gateway / tool / external …）；`responsibility` 一句话职责。
- `edges[]`：节点间的真实调用边。`paths` 标这条边属于哪些调用路径，供路径筛选用。
- `claims[]`：**核心**。把"系统宣称具有的属性"逐条列出，并标注证据状态。
- `paths[]`：有代表性的调用路径（消息 / 模型 / 工具 / 运维…），是图上路径筛选的依据。

## 证据状态（三态）

每个 `entity` 和每条 `claim` 必须标一个状态，不许省略：

| 状态 | 含义 | 图上的表现 |
|---|---|---|
| `verified` | 文档与源码一致，已被代码/测试坐实 | 实线边框 |
| `claimed` | 只在文档/README/注释里出现，代码未坐实 | 虚线边框 |
| `contradicted` | 文档与代码不一致，存在冲突 | 红色/加粗边框 |

**核对纪律：**

- 只用"读文档"得出的结论，最高只能标 `claimed`；必须找到对应源码或测试才能升 `verified`。
- 文档说法与代码实现冲突时，标 `contradicted`，并把两边出处都写进 `evidence`。
- 找不到任何出处、只是推测的，**不要画进图里**，在聊天中说明是推测。

## 落盘位置

提炼是"过程证据"，不是交付物。理解模式默认走 `export`（无会话），用 `--extraction` 把它持久化到根运行目录的独立导出区：

```text
<项目>/.visual-brainstorming/exports/<id>/extraction.json
```

`exports/<id>/` 与 `sessions/<id>/` 分离，不需要起服务，也不进 `local/`。最终给你看的架构图 HTML 由 `export` 烘成自包含单文件，单独放在 `local/`（如 `local/<project>-architecture.html`），与这份过程证据分开。

```bash
python3 -I -S "$SKILL_DIR/scripts/companion.py" export \
  --source /tmp/arch.html \
  --output "$PROJECT_ROOT/local/<project>-architecture.html" \
  --project-dir "$PROJECT_ROOT" \
  --extraction /tmp/extraction.json
```

`--extraction` 只接受合法 UTF-8 JSON（`.json` 后缀，≤100 KiB），落盘为 `0600`。

## 与渲染的衔接

提炼完成后，把 `entities` / `edges` / `paths` 映射到 `assets/templates/explore-map.html` 的契约：

- `entity.id` → `data-node`；`entity.name` → `data-label`；`entity.evidence` → `data-evidence`；`entity.source` → `data-source`。
- `edge.paths` → 连线元素的 `data-flows`。
- `paths[].id` → 路径筛选按钮的 `data-vb-path`；`paths[].name` → 按钮文字。
- `claims` 里 `contradicted` 的项，必须在图旁用文字单独列出，不能只靠边框颜色。
