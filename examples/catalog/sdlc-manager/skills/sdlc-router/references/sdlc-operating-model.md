# SDLC ADS Operating Model

This file is the single source of truth for SDLC/ADS lanes, `local/sdlc` layout, lightweight IDs, status words, and minimal templates. If older SDLC skills conflict with this file, this file wins for routing and material weight decisions.

## 1. Four Zones

- 孵化区：想法、讨论、BRD/URS/PRD 式思考。默认可弃，不进 traceability。
- 气闸：需求包或范围决策表。`REQ` 从这里开始。
- 交付区：本次规格、handoff、dev、验证。
- 资产区：跨交付继续有效的 `_资产.md`、`架构.md`、`领域.md`。

## 2. Lanes

- 快线：bugfix、小修、小配置、小文案、明确 issue。
- 增补：清楚的新功能、小模块或局部行为变化。
- 重构：外部行为基本不变，内部结构、依赖、模块边界或实现方式调整。
- 重建：旧系统重做、替换、迁移或能力重新映射。
- 从头：greenfield 项目或全新子系统。

Modifiers:

- 规则变更：权限、计费、数据口径、状态机、合规、隐私、业务语义或领域归属变化。
- 发布：release、rollback、上线证据、发布风险或支持成本变化。

## 3. ADS Quick Judgment

- A / Architecture：架构、模块、运行边界、依赖方向、部署或迁移路径是否变化。
- D / Domain：领域归属、业务规则、数据归属、权限、口径或禁止依赖是否变化。
- S / Specification：范围、非范围、验收和验证方式是否清楚。

ADS 是判断框架，不是每次都要写三份文档。

## 4. Progressive `local/sdlc`

```text
local/sdlc/
  _资产.md
  架构.md
  领域.md
  <slug>/
    00-状态.md
    01-外部讨论.md
    10-需求包.md
    20-规格.md
    30-handoff.md
    40-验证记录.md
```

Use progressively:

- 快线可以 0 files。
- 跨会话、跨 agent、风险升级或后续接力时，写交付卡或 `00-状态.md`。
- 外部 Web / GPT / 其他 AI 讨论较长时，写 `01-外部讨论.md`；短输入只归纳到 `00-状态.md`。
- 长期决策、架构约束、领域归属或验证底线变化时，才更新 `_资产.md`、`架构.md`、`领域.md`。

## 5. ID Contract

- `REQ-001`: requirement from a requirements package or scope decision table.
- `DEC-001`: durable decision.
- `ARCH-001`: architecture constraint.
- `DOM-001`: domain, ownership, data, or dependency constraint.
- `TASK-001`: handoff task.
- `VAL-001`: validation item.
- `Q-001`: open question or blocker.
- `ITEM-001`: midstream intake item.

Default links:

```text
REQ -> TASK -> VAL
ARCH / DOM / DEC -> TASK
ITEM -> TASK / VAL / Q
```

## 6. Delivery Card

Use in conversation, `00-状态.md`, or `30-handoff.md` depending on persistence need.

```markdown
# 交付卡：<slug>

## 1. 判断

- 车道：
- Dev path：direct-read / direct-dev / handoff-lite / handoff-full / blocked
- 证据：[用户确认] / [代码证据] / [local材料] / [推断] / [未确认]

## 2. ADS

- A 架构影响：
- D 领域影响：
- S 规格清晰度：

## 3. 范围

- 本次做：
- 本次不做：

## 4. 执行

- TASK-001：

## 5. 验证

- VAL-001：

## 6. 中途接入

- ITEM-001：
  - 类型：同范围补充 / 旁路小修 / 冲突变更 / 紧急修复
  - 处理：并入 TASK-001 / 新增 TASK-002 / direct-dev / blocked
  - 验证：VAL-001
  - 状态：pending / done / blocked

## 7. 未决

- Q-001：
```

If there is no midstream intake, omit section 6.

## 7. External Discussion Intake

Use this when a plan comes from Web, GPT5.5Pro, another AI, a pasted chat, a meeting note, or an external research session.

Rules:

- External discussion is reference input, not executable truth.
- Keep source labels: `[用户确认]`, `[外部建议]`, `[代码证据]`, `[local材料]`, `[推断]`, `[未验证]`.
- Execute only the parts converted into `REQ`, `TASK`, and `VAL`.
- Do not require external material to match this template; normalize it after import.

Short input can be summarized in `00-状态.md`. Long input uses:

```markdown
# 外部讨论：<slug>

## 1. 来源

- Source：
- Date：
- Tool / channel：
- Original context：

## 2. 可采纳要点

- [外部建议]：
- [用户确认]：

## 3. 未验证假设

- Q-001：

## 4. 需要代码或 local 证据核查

- CHECK-001：

## 5. 转换结果

- REQ-001：
- TASK-001：
- VAL-001：

## 6. 不进入本次交付

-
```

## 8. `00-状态.md`

```markdown
# 状态：<slug>

- 车道：
- 修饰：
- 阶段：intake / scoped / spec-ready / handoff-ready / dev / validation / closed
- Dev path：direct-dev / handoff-lite / handoff-full / blocked

## 产物

- 10-需求包.md：none / draft / baseline
- 01-外部讨论.md：none / reference
- 20-规格.md：none / draft / baseline
- 30-handoff.md：none / ready
- 40-验证记录.md：none / partial / complete

## 决策

- DEC-001：

## 约束引用

- ARCH-001：
- DOM-001：

## 中途接入

| ITEM | 类型 | 处理 | 关联 TASK/VAL/Q | 状态 |
|---|---|---|---|---|
| ITEM-001 | 同范围补充 | 并入 TASK-001 | VAL-001 | done |

## 未决

- Q-001：

## 下一步

-
```

## 9. Handoff Lite

```markdown
# Handoff Lite：<slug>

## 1. 来源与目标

- Source：
- Goal：
- Must not：

## 2. 任务

| TASK | Source / REQ | Change | Area | Constraints |
|---|---|---|---|---|

## 3. 验证

- VAL-001：
- Smallest check：
- Done：
```

## 10. Scope Decision Table

Use for rebuilds and replacement work. Do not write all future specs at once.

```markdown
# 范围决策表：<slug>

| 能力项 | 旧系统证据 | 决策 | 新 REQ | 验证方式 | 备注 |
|---|---|---|---|---|---|
| 登录 | old/auth | 保留 | REQ-001 | 老行为对照 + 新测试 | |
| 导出 | old/export | 改造 | REQ-002 | 新格式验收 | |
| 旧后台 | old/admin | 舍弃 | - | - | 被新后台替代 |
| 推送 | old/notify | 存疑 | Q-001 | 待确认 | |
```

## 11. Midstream Intake Questions

When new information appears during implementation, ask:

1. Is it required for the current task?
2. Does it change current scope?
3. Does it change Architecture, Domain, or business rules?
4. Does it change validation?
5. Can it be independently validated?

Escalate only when scope, Architecture, Domain, business semantics, release risk, or validation baseline changes.
