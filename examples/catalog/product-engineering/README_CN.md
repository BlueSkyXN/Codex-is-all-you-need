# Product Engineering Catalog

中文 | [English](README.md)

用于开发前产品工程工作的 agents 和 skills：现有项目能力地图、需求澄清、范围锁定、功能行为规格、技术桥接草案、交付计划、准备度审查，以及 change-spec 交接。

这个 catalog 和 `dev` 分开。它负责把需求和规划产物整理到可交给开发的程度，但不负责 repo-aware 的代码实现、测试、PR review、安全 review 或 release check。

## 内容

```text
agents/   7 个 product-engineering agents
skills/   7 个公开 skills
```

## Agent 角色

- `product_engineering_project_researcher`：读取现有代码库，输出轻量项目功能能力地图（项目定位、一级能力域、二级功能组或模块、三级功能点、证据路径、当前状态、缺口和可用于汇报的中文表达）。
- `product_engineering_requirements_lead`：把产品意图和输入材料整理成 PRD、scope lock 和 spec handoff。
- `product_engineering_functional_specifier`：把已确认的 PRD 范围转成行为、状态、字段、权限、UI state 和验收标准规格。
- `product_engineering_technical_bridge`：输出工程桥接草案，但不替代最终架构决策角色。
- `product_engineering_delivery_planner`：把已批准规格拆成实施任务、依赖顺序、验证要求和 agent handoff。
- `product_engineering_readiness_reviewer`：在进入下一阶段前审查 PRD、spec、tech bridge、task plan 或 change-spec 产物。
- `product_engineering_change_adapter`：把已批准规划产物转换成 repository change-spec 或 OpenSpec-style assets。

## Skills

- `project-research`：在 PRD、规划或汇报之前读取现有代码库，产出轻量项目功能能力地图：`项目能力摘要.md`、`项目功能能力地图.md` 和 `项目能力表.csv`。默认使用简体中文文件名、中文章节、中文表头和中文状态；默认不产出工作分解、产品结构拆解、成熟度、卡点长分析、规格或任务类重型产物。
- `prd-workflow`：从 idea 到 PRD、scope lock、detailed PRD 和 spec handoff。
- `functional-spec`：从 PRD 输出行为规格：流程、状态、字段、权限、UI states、错误和 AC。
- `technical-spec-bridge`：输出工程桥接产物：架构简报、API/data draft、NFR、测试草案和开放问题。
- `delivery-task-planning`：输出 implementation plan、task breakdown、dependency graph、test tasks 和 agent handoff。
- `readiness-review`：审查 PRD、functional spec、technical bridge、task plan 或 change-spec 是否能进入下一阶段。
- `change-spec-adapter`：把已批准产物转换成 proposal、design、tasks 和 behavior delta 文档。

## 使用说明

当任务处在“产品意图”和“开发实现”之间时使用这个 catalog。交接点应该是清楚的 `agent-handoff.md`、`task-breakdown.md`、`review-report.md` 或等价 change-spec 产物。

如果项目已经存在但还不清楚它到底是什么，先用 `project-research`。它输出的能力地图会交给 `prd-workflow`（选择范围）、`functional-spec`（把选中的功能点提升为正式规格）、`delivery-task-planning`（把选中的缺口展开为工作）以及汇报类流程（表达已形成能力，但不虚构进度分数）。

进入需要代码库映射、API 兼容性审查、架构审查、实现、测试、PR review、安全 review、性能诊断或发布验证的阶段后，再使用 `dev`。

## 维护说明

保持这个 group 专注于工程管理和规划。不要加入代码编辑 workflow、真实内部模板、私有 roadmap 细节、客户名或机器路径。技术决策如果没有 repo evidence 和 implementation owner 确认，应标记为 draft。
