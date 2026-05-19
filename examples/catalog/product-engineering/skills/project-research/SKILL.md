---
name: project-research
description: "Use before PRD, planning, or progress reporting to read an existing codebase and produce a lightweight Project Capability Map: project positioning, L1 capability domains, L2 function groups/modules, L3 function points, evidence paths, simple status, and next-step notes. Not for WBS, PBS, maturity scoring, blocker analysis, task planning, schedule/resource estimates, or implementation."
---

# Project Capability Map

## Purpose

Read an existing codebase, configuration, and docs, then produce a lightweight project capability map that can support management tracking, progress reporting, PRD scoping, and performance-material preparation.

The core output is one evidence-backed table:

```text
L0 project goal
-> L1 capability domain
-> L2 function group / module
-> L3 function point
-> evidence path
-> current status
-> next step
```

This skill keeps the legacy runtime name `project-research`, but its default behavior is now **Project Capability Map**, not a full research pack.

## Boundary

This skill answers:

- What is this project for?
- Which capability domains does it expose?
- Which function groups or modules exist under each domain?
- Which observable function points can be found?
- Which files, docs, configs, tests, or commands support each function point?
- What is the current simple status of each function point?
- What is the most useful next step for each L2 module?

This skill does **not** produce by default:

- Product Breakdown Structure / PBS.
- Work Breakdown Structure / WBS.
- Tracking matrix.
- Full blocker list.
- Delivery maturity or M0-M9 levels.
- Function spec cards.
- Deployment/ops review.
- Target-shift log.
- Snapshot/incremental state.
- Large `tables/` data layer.
- Completion percentages, weights, scores, resource estimates, schedules, owners, staffing, or performance judgments.

If the user asks for task planning, hand off to `delivery-task-planning`. If the user asks for formal behavior specs, hand off to `functional-spec`. If the user asks for scoring, reporting language, or performance evaluation, treat that as a downstream pass on top of the capability map.

## Safety

- Default to read-only scanning.
- Run only non-destructive commands needed to verify evidence, such as listing files, reading docs, inspecting manifests, or running clearly safe smoke/test commands.
- Do not delete files, rewrite config, run migrations, reset Git state, clear databases, or deploy unless the user explicitly asks outside this skill run.
- Do not copy raw secrets, tokens, credentials, private URLs, or personal data into outputs. Record variable names and redacted examples only.
- If commands are run for evidence, record the command and result briefly in the relevant evidence or notes field.

## Output Language

- Write human-facing outputs in Simplified Chinese by default.
- Keep file names, CSV column names, IDs, code paths, commands, package names, API names, config keys, and code identifiers in their original form.
- CSV uses stable English `snake_case` headers for import compatibility; cell content should be Simplified Chinese unless it is an ID, path, command, code identifier, config key, or exact source reference.

## Status Labels

Use exactly one primary status per L3 function point:

| Status | Meaning |
|---|---|
| `已规划` | Goal or plan exists, but no concrete design or code evidence was found. |
| `已设计` | Architecture, interface, schema, prompt, route, or template exists, but implementation is incomplete or not found. |
| `已开发` | Code or configuration exists for the function point. |
| `可运行` | The function point can start, execute, or produce observable output in the current or documented environment. |
| `待验证` | Evidence suggests implementation exists, but integration, tests, stability, or real usage still needs confirmation. |
| `已废弃/重构` | Evidence shows the function point is deprecated, replaced, or no longer the intended path. |
| `未发现证据` | The function point is expected or mentioned, but no supporting evidence was found. |

Do not use M0-M9 maturity levels in this skill.

## Workflow

1. Confirm the target project root. Default to the current working directory.
2. Confirm output directory. Default to `./local/capability-map/` unless the user provides a path.
3. Scan only enough repository evidence to build the map: README/docs, manifests, entry points, routes, APIs, models, services, UI components, prompts/workflows, config, tests, examples, deployment files, and recent generated artifacts when relevant.
4. Write a one-sentence L0 project goal. Prefer explicit repo docs; mark inferred goals as `[INFERRED]` with the source.
5. Identify L1 capability domains by business behavior, not by mechanically copying frontend/backend folders. Keep L1 to 3-8 domains when the repo supports that range.
6. Under each L1, identify L2 function groups/modules. Keep each L1 to 3-8 L2 modules when evidence supports that range.
7. Under each L2, identify L3 function points. Keep each L2 to 2-8 L3 function points. L3 must be observable behavior, not an abstract concept.
8. Attach evidence for every L3 function point:
   - Use concrete paths and line numbers when practical.
   - Mark unsupported but plausible items as `[INFERRED]` with the inference source.
   - Mark missing evidence as `[UNKNOWN]` or status `未发现证据`.
9. Assign one primary status from the allowed status labels.
10. Give one concise next-step note per L2 module. Repeat that note across rows only when using a flat CSV table.
11. Write exactly the default outputs unless the user explicitly asks for more:
    - `project-summary.md`
    - `capability-map.md`
    - `capability-table.csv`
12. Print a short delivery summary: output paths, L1 count, L2 count, L3 count, key evidence gaps, and three report-ready sentences.

## Outputs

Default outputs:

- `project-summary.md` — project goal, core capability domains, formed capabilities, major gaps, and report-ready one-liner.
- `capability-map.md` — readable L1/L2/L3 capability map table, L1 summaries, gap summary, and three report-ready sentences.
- `capability-table.csv` — importable flat table with stable columns:

```csv
l1_domain,l2_module,l3_function,function_desc,evidence,current_status,next_step,notes
```

The CSV is the management-friendly data layer. Do not create many CSV files by default.

## References / Load When

- `references/methodology.md` — load when the user asks about the design rationale or when checking whether an output is too heavy.
- `references/project-summary-template.md` — load when writing `project-summary.md`.
- `references/capability-map-template.md` — load when writing `capability-map.md`.
- `references/csv-output-schema.md` — load when writing `capability-table.csv`.

## Validation

- Output language is Simplified Chinese by default.
- The output contains L0 project goal plus L1/L2/L3 capability rows.
- L1 is capability/domain shaped; L2 is function-group/module shaped; L3 is observable function-point shaped.
- L3 rows cite concrete evidence paths whenever available.
- Claims without direct evidence are marked `[INFERRED]` or `[UNKNOWN]`; they are not written as facts.
- Every L3 row uses one of the allowed Chinese status labels.
- Default output is limited to `project-summary.md`, `capability-map.md`, and `capability-table.csv`.
- No WBS, PBS, tracking matrix, maturity model, blocker analysis, spec cards, snapshot, task cards, or large `tables/` layer appears unless the user explicitly asks for that separate downstream work.
- No completion percentage, score, weight, schedule, cost, resource estimate, staffing plan, owner assignment, or performance judgment appears.
- Secrets and personal data are redacted.
