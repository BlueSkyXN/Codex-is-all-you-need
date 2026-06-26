---
name: infoops
description: "Use for maintaining a workspace/infoops operating system: signal collection and classification, thread management, source profiles, and PULSE dashboard refresh. Triggers when working with the workspace/infoops directory, refreshing PULSE, managing threads, or tracking source profiles."
---

# InfoOps — 信息运营系统

## 核心定位

从飞书等工作平台的海量信息流中，持续采集、结构化、分类信号，构建可操作的工作态势认知，反向驱动行动决策。

```
采集（IM / 云空间 / 日历 ...）
  → 分类（Surge / Active / Ongoing / Emerging / Cooling）
  → 感知（PULSE 态势面板）
  → 行动（辅助 / 引导 / 指挥）
  → 反馈 → 回到采集
```

不是存档系统。不是通讯录。不是笔记本。

---

## 平台兼容

- **Codex**：通过 `.codex-plugin/plugin.json` 作为 marketplace plugin 安装。
- **Claude Code / Copilot**：通过 `.claude-plugin/plugin.json` 安装（Copilot 复用 `.claude-plugin/` 路径）。
- **OpenClaw bundle**：可通过 `plugins/infoops/` 作为 Codex-compatible bundle 加载。
- **OpenClaw standalone skill**：也可直接使用 `plugins/infoops/skills/infoops/`；本目录不依赖 Codex-only manifest 字段。
- **运行态边界**：`workspace/infoops/` 是调用时创建/维护的用户工作区，不随插件预置。

---

## 操作铁律

1. **飞书侧只读**：只通过 lark-cli 读取数据（拉消息、查成员、查文档元信息），不发消息、不建群、不改文档、不删文件
2. **本地侧写入**：所有写入操作只发生在 `workspace/infoops/` 目录内
3. **前置依赖**：
   - 已安装 `lark-cli`（`command -v lark-cli` 验证）
   - 已配置飞书应用凭据（`lark-cli auth` 已登录）
   - 操作飞书前先读 `lark-cli skills read lark-shared` 了解认证和安全规则
4. **采集优先级**：
   - 群：7天内**我有发言**的群优先
   - 单聊：30天内**我有发言**的人优先
   - 人：从群消息 + 单聊跨源综合捕捉
5. **写入前自检**：写入任何 InfoOps 文件前，对照 `references/format-spec.md` 末尾的自检清单

---

## Reference 文件导航

| 文件 | 何时读 | 内容 |
|------|--------|------|
| `references/taxonomy.md` | 新建文件、分类对象、判断排除 | 数据源分类法、排除规则、标签体系、升格规则、ID-MAP 分区 |
| `references/signal-model.md` | 刷新 PULSE、判断信号、关联分析 | 五种信号节奏定义、判定阈值、节奏流转、跨源关联 |
| `references/format-spec.md` | 写入任何 InfoOps 文件 | 所有文件类型的格式约束、书写边界、自检清单 |
| `references/templates.md` | 创建新文件 | 所有文件类型的标准模板 |
| `references/feishu-guide.md` | 从飞书采集数据 | lark-cli 引导、采集策略、cron 配置、初始化流程 |
| `references/ops-protocol.md` | 执行任何 InfoOps 操作 | 操作步骤序列：PULSE 刷新、线程管理、采集流程 |

操作前至少读 SKILL.md + 当次操作相关的 reference。

---

## 运行态目录结构

```
workspace/infoops/
├── MISSION.md          系统总纲
├── PULSE.md            态势面板（Agent 定期刷新）
├── ID-MAP.md           纯 ID 字典
├── _RULES.md           操作规则速查
├── threads/            事务线程（active/ + closed/）
├── sources/            信息源画像
│   ├── groups/         IM 群组（internal/ + external/）
│   ├── people/         人物档案（跨源）
│   └── space/          云空间追踪（docs/ sheets/ bitables/ pdfs/）
└── archive/            统一归档
```

完整子目录结构、升格/降格规则和云空间 L0-L4 追踪层级见 `references/taxonomy.md`。

文件格式、标签规范和 ID-MAP 分区规范见 `references/format-spec.md`。
