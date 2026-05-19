# Project Capability Map Methodology

This skill is intentionally lightweight. Its job is not to create a formal research pack. Its job is to help a local AI quickly read a codebase and turn it into a capability/function-point map that a human can use for management tracking, progress reporting, PRD scoping, or performance-material preparation.

## 1. Default output is one map, not many artifacts

The default shape is:

```text
Project goal
-> capability domain
-> function group / module
-> function point
-> evidence
-> status
-> next step
```

The map should answer the management question:

```text
这个项目做了什么？有哪些能力域？每个能力域下面有哪些模块？每个模块已经形成哪些功能点？
```

Do not expand into PBS, WBS, tracking matrices, maturity reports, blocker reports, spec cards, deployment reviews, target-shift logs, or many CSV files unless the user explicitly asks for a separate downstream activity.

## 2. Layer definitions

| Layer | Meaning | Example |
|---|---|---|
| L0 | Project goal | `面向跨境电商质量分析的 AI 工作台` |
| L1 | Capability domain / subsystem | `AI工作流/智能中台能力域` |
| L2 | Function group / module | `Dify封装` |
| L3 | Observable function point | `工作流调用` |

L4 task/spec expansion is deliberately out of scope for the default run. Use `functional-spec` for formal behavior specs and `delivery-task-planning` for implementation task planning.

## 3. Business-first decomposition

Decompose by business capability first. Do not mechanically split by repository folders such as `frontend`, `backend`, `scripts`, or `infra`.

Engineering layers are still useful evidence, but they are secondary. A function point may be supported by frontend, backend, data, AI, and deployment files at the same time.

Typical L1 domains for AI/platform projects can include:

- `前端工作台能力域`
- `后端控制面能力域`
- `AI工作流/智能中台能力域`
- `文件/OSS服务能力域`
- `数据中台/AI+BI能力域`
- `业务智能体能力域`

These are examples, not mandatory rows. Only include a domain when the target project has evidence or a clearly marked inference.

## 4. Function point rules

An L3 function point must be observable behavior. Good examples:

- `工作流调用`
- `参数传递`
- `任务状态查询`
- `文件上传`
- `人工复核`
- `调用日志记录`

Weak examples that should be rewritten:

- `平台能力`
- `后端逻辑`
- `AI模块`
- `数据支持`
- `系统建设`

## 5. Evidence rules

Every L3 row should cite evidence when possible:

- Code path: `src/services/workflow.py`
- UI path: `src/pages/tasks/index.tsx`
- API path: `apps/api/routes/task.py`
- Config path: `docker-compose.yml`
- Prompt/workflow path: `prompts/monthly-report.md`
- Test path: `tests/test_task_api.py`
- Doc path: `README.md`

When direct evidence is missing:

- Use `[INFERRED]` for items inferred from names, routes, config, or docs.
- Use `[UNKNOWN]` when the item is expected or mentioned but evidence was not found.
- Do not borrow capability rows from peer projects to make the map look complete.

## 6. Status is simple

Use one primary status per L3 function point:

- `已规划`
- `已设计`
- `已开发`
- `可运行`
- `待验证`
- `已废弃/重构`
- `未发现证据`

Do not use M0-M9, weighted progress, completion percentage, or status-report language in this skill.

## 7. Output language convention

Generated artifacts should be in Simplified Chinese by default. Keep code paths, command names, file names, package names, API names, config keys, IDs, and CSV headers in their original form.

The CSV header is intentionally stable and English:

```csv
l1_domain,l2_module,l3_function,function_desc,evidence,current_status,next_step,notes
```

CSV cell content should be Chinese unless the value is a path, command, identifier, or exact source reference.

## 8. Downstream handoff

This capability map can feed other work:

- `prd-workflow`: use the L1/L2/L3 map to decide PRD scope.
- `functional-spec`: promote selected L3 function points into formal behavior specs.
- `delivery-task-planning`: expand selected gaps into implementation tasks and dependency order.
- reporting/office workflows: reuse the capability map as raw material for progress or performance expression.

The downstream step should add evaluation, priority, schedule, ownership, or reporting language. This skill should not preempt those decisions.
