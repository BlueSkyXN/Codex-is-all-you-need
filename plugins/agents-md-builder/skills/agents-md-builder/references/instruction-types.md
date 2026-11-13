# AGENTS.md 指令类型

这是一套用于编写和审查 AGENTS.md 的落点判断方法，不是新的文件类型，也不是
要求每个文件必须出现四个固定标题。先判断一句话属于哪种指令，再决定它是否应
放在 root router、Domain card 或 Guardrail card。

## Principle：原则

原则提供判断方向和取舍依据，适合处理无法穷举的情境。它应帮助 agent 回答
“为什么这样判断”，但不能伪装成无条件硬门禁。

检查问题：

- 这条原则是否真的改变决策，而不只是“遵循最佳实践”之类空话？
- 是否说明适用方向、重要取舍或 review question？
- 如果实际需要的是可验证的必须/禁止项，是否应该改写为 Rule？

## Rule：规则

规则表达明确的“必须”或“禁止”，需要同时说明适用范围、触发条件和验证方式。
可自动验证的 Rule 必须给出仓库中真实存在的命令；依赖上下文的建议不得写成
无条件 `MUST`。

推荐结构：

```text
Scope:
Trigger:
Required or prohibited behavior:
Validation:
```

“所有函数必须少于 20 行”通常是缺少适用条件的机械 Rule。除非仓库已有真实
门禁，应降级为带判断条件的 heuristic，或直接删除。

## Convention：约定

约定统一协作方式，例如命名、目录、命令入口、文件格式、ID 前缀或 commit/PR
格式。它减少无意义差异，但不应伪装成普遍正确性原则。

检查问题：

- 约定是否来自当前仓库的真实结构或工具？
- 适用范围是否明确？
- 更近的子目录是否存在不同约定？若有，以更近规则为准。

## Procedure：流程

流程描述有状态的操作步骤，必须有输入、顺序、输出、完成条件和停止条件。需要
网络、Docker、数据库、凭据、sudo、交互或外部服务时，必须标注 sandbox notes，
不得把依赖缺失后的失败当作默认完成路径。

推荐结构：

```text
Inputs and prerequisites:
Ordered steps:
Expected output or evidence:
Completion condition:
Stop or escalation condition:
Sandbox notes:
```

例如，需要数据库的 migration 命令应成为带前置依赖和停止条件的 Procedure，
而不是一句无条件全局 Rule。Procedure 也不应伪装成“始终如此”的全局原则。

## 放置与例外

- Root router 放跨目录通用的 Principle、Rule、Convention，以及指向局部
  Procedure 的导航；不要塞入单个服务的完整流程。
- Domain card 放本模块特有的不变量、接口/数据 Rule、局部 Convention 和验证
  Procedure。
- Guardrail card 放高风险触发条件、禁止项、前置检查、停止条件和补偿验证。
- 子目录不要重复上级 AGENTS.md 已有内容，只补充或收紧该子树特有约束。

任何例外都要写明原因、影响范围和补偿验证。例外不是删除规则，也不能用一句
“特殊情况除外”隐藏风险。

## 硬检查

- 可自动验证的 Rule 是否给出真实命令？
- 依赖上下文的建议是否被错误写成无条件 `MUST`？
- Procedure 是否具有输入、顺序、输出、完成和停止条件？
- Principle 是否被机械化为绝对禁令？
- Convention 是否与仓库事实一致，而非编造偏好？
- 例外是否说明原因、范围和补偿验证？
- 子目录是否重复上级规则？重复时保留更近的特有约束，删除复述。
