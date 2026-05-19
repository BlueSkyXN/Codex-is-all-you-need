---
name: project-research
description: "Use before PRD, planning, or progress reporting to turn an existing codebase into a trackable project structure: capability tree / CBS, function points, spec candidates, product structure, WBS, evidence map, blockers, maturity, Markdown summaries, and CSV tables. Not for scoring, completion-rate reporting, resource estimation, or implementation."
---

# Project Research

## Purpose

Turn an existing codebase, configuration, and docs into a trackable project structure that downstream skills (`prd-workflow`, `functional-spec`, `delivery-task-planning`) and humans can use for planning, management, and progress reporting.

The core deliverable is not a long narrative. It is a linked structure:

- Capability Breakdown Structure (`capability-map.md`): capability domains, function points, and spec candidates.
- Product Breakdown Structure (`product-structure.md`): shipped modules, components, integrations, and runtime artifacts.
- Work Breakdown Structure (`work-breakdown.md`): management-level work packages that move capabilities forward.
- Tracking matrix (`tracking-matrix.md`): the management index linking capability, function point, spec candidate, product module, work package, evidence, maturity, blocker, and next action.
- CSV tables (`tables/*.csv`): the manageable data layer for importing into spreadsheets, Notion, Airtable, BI tools, or later reporting automation.

Markdown files explain the project. CSV files carry the durable tracking rows. Keep both in sync.

## Boundary

Project research answers what the project is, what it already does, which function points and capability domains exist, which specs are missing, where the end-to-end chain breaks, what blockers stand in the way, and how capabilities can be tracked over time.

It can record status tags, maturity levels, blockers, and management work packages. It does not assign weights, completion percentages, performance scores, resource estimates, dates, owners, or status-report narrative. Evaluation, scheduling, and reporting are downstream activities that run on top of the accepted tracking structure.

In this skill, **CBS means Capability Breakdown Structure**, not Cost Breakdown Structure. Cost breakdown, resource planning, schedule estimation, and staffing are out of scope.

## Safety

- Default to read-only scanning. Run only non-destructive commands needed to verify runnable/test/deployment evidence.
- Do not delete files, rewrite config, run migrations, reset Git state, clear databases, or deploy unless the user explicitly asks outside this research pass.
- Do not copy raw secrets, tokens, credentials, private URLs, or personal data into outputs. Record variable names and redacted examples only.
- If commands are run, record the command and result in the relevant evidence row or Markdown section.

## Output Language

- Write human-facing outputs in Simplified Chinese by default: Markdown titles, prose, table descriptions, notes, blocker descriptions, maturity reasons, and next actions.
- Keep file names, CSV column names, IDs, code paths, commands, package names, API names, config keys, and code identifiers in their original form.
- CSV files use stable English `snake_case` headers for import compatibility; cell content should be Simplified Chinese unless it is an ID, path, command, code identifier, or exact source reference.
- The English templates in `references/` are structural guides. Do not copy their English headings verbatim into final artifacts; localize generated section titles and explanatory text to Simplified Chinese.

## Tiers

Choose one tier per run. Default is `standard`.

- `quick` — positioning, capability map, blocker list, and tracking matrix. Use when scoping a discussion or first-touch onboarding.
- `standard` — Full capability map, product structure, WBS, tracking matrix, evidence map, end-to-end flow, maturity, blockers, and next actions. Use as the durable tracking baseline for most projects.
- `deep` — Adds per-function spec cards, deployment/ops review, and target-shift log. Use before serious PRD work on a critical capability, or when handing the project to a new owner.

Tier is selected by the user or inferred from the request. Do not silently upgrade or downgrade.

## Workflow

1. Confirm target project root (default to current working directory) and tier.
2. Confirm output directory (default `./local/research/`; create if missing).
3. If `snapshot.json` already exists in the output dir, run in incremental mode: re-scan, diff against the snapshot, and update only what changed. Record any goal changes in `target-shift-log.md` instead of overwriting prior entries.
4. Scan project structure: entry points, languages and frameworks, dependency manifests, routes, models, components, scripts, deployment configs, tests, docs, examples, env templates, and CI files.
5. Reconstruct project positioning using only signals present in the repo. Separate explicit goals (named in README/docs) from implicit goals (inferred from code structure). Mark every inferred item as `[INFERRED]` with the inference source.
6. Build three breakdown views in sequence; do not collapse them into one view (see `references/methodology.md` §8 for the reasoning):
   - **Capability tree / CBS (`capability-map.md`)**: business-behavior view. L0 project goal → L1 capability domain → L2 capability module → L3 function point → optional L4 spec candidate.
   - **Product structure / PBS (`product-structure.md`)**: deliverable view. Subsystems, modules, components, integrations, and runtime artifacts. Use what the repository actually ships, not idealized architecture.
   - **Work Breakdown Structure / WBS (`work-breakdown.md`)**: management work packages that move capabilities or function points forward. Record tracking status and management-unit fit; do not estimate person-weeks, schedules, cost, or staffing.
7. Write the CSV data layer under `tables/` using `references/csv-output-schema.md`. At minimum, export capability, function-point, product-structure, WBS, evidence, blocker, maturity, and tracking-matrix rows for the selected tier.
8. Build the evidence map: for each function point, attach code path, evidence type, evidence strength, and confidence.
9. Trace the end-to-end main flow from external input to archived output and audit log. Mark where humans are required and where AI/ML is involved.
10. Catalog blockers as first-class artifacts (need / spec / code / data / AI-output / deployment / test / ops / dependency types). Each blocker records symptom, hypothesis, attempted fixes, next step, and whether it blocks end-to-end delivery.
11. Assign a delivery maturity level per capability domain using the M0-M9 scale, with traced evidence. Apply status tags (`planned`, `specified`, `designed`, `implemented`, `runnable`, `integrated`, `tested`, `demoable`, `deployed`, `operable`, `blocked`, `changed`, `deprecated`); multiple tags per capability are allowed and expected.
12. Write `tracking-matrix.md` and `tables/tracking_matrix.csv` as the main management index linking capabilities, function points, spec candidates, product modules, work packages, evidence, maturity, blockers, and next actions.
13. For `deep` tier only: produce a function spec card per critical function point, a deployment/ops review, and drill the most critical work packages in `work-breakdown.md` to task-card level.
14. Write `next-actions.md` with short-term loop-closing items, mid-term build items, long-term optimization items, and items that need human or owner confirmation. Next actions are summary-level; the detailed work decomposition lives in `work-breakdown.md`.
15. Update `snapshot.json` with the current scan state for the next incremental run.
16. Print a delivery summary: tier, output paths, capability count, function-point count, evidence counts, top three blockers, and the single most useful next action.

## Outputs

Written under the chosen output directory (default `./local/research/`).

Quick tier:

- `project-overview.md`
- `capability-map.md`
- `blocker-list.md`
- `tracking-matrix.md`
- `tables/capability_tree.csv`
- `tables/function_inventory.csv`
- `tables/blockers.csv`
- `tables/tracking_matrix.csv`
- `snapshot.json`

Standard tier (adds):

- `capability-map.md` — capability tree / CBS + navigation links into the tracking matrix
- `product-structure.md` — PBS view of shipped deliverables
- `work-breakdown.md` — WBS at management work-package granularity
- `tracking-matrix.md` — management index linking capability/function/spec/work/evidence/status
- `tables/capability_tree.csv` — L0-L4 capability hierarchy as rows
- `tables/function_inventory.csv` — function points, spec candidates, status tags, and evidence refs
- `tables/product_structure.csv` — PBS hierarchy as rows
- `tables/wbs.csv` — WBS work packages as rows
- `tables/evidence_map.csv`
- `tables/blockers.csv`
- `tables/maturity.csv`
- `tables/tracking_matrix.csv`
- `evidence-map.md`
- `e2e-flow.md`
- `delivery-maturity.md`
- `next-actions.md`

Deep tier (adds):

- `function-spec-cards/<id>.md` (one per critical function point)
- `deployment-ops-review.md`
- `target-shift-log.md` (also created in incremental runs whenever goals shift)
- `tables/spec_candidates.csv`
- `tables/task_cards.csv` (only for drilled-down WBS packages)

## References / Load When

- `references/methodology.md` — load on first use, or when the user asks about maturity, status tags, evidence strength, vibe-coding adaptation, or anti-fabrication rules.
- `references/project-overview-template.md` — load when writing `project-overview.md`.
- `references/capability-map-template.md` — load when writing `capability-map.md`.
- `references/product-structure-template.md` — load when writing `product-structure.md`.
- `references/work-breakdown-template.md` — load when writing `work-breakdown.md`.
- `references/tracking-matrix-template.md` — load when writing `tracking-matrix.md`.
- `references/csv-output-schema.md` — load when writing `tables/*.csv`.
- `references/evidence-map-template.md` — load when writing `evidence-map.md`.
- `references/function-spec-card-template.md` — load when writing each card in `function-spec-cards/`.
- `references/blocker-list-template.md` — load when writing `blocker-list.md`.
- `references/delivery-maturity-template.md` — load when writing `delivery-maturity.md`.
- `references/e2e-flow-template.md` — load when writing `e2e-flow.md`.
- `references/deployment-ops-template.md` — load when writing `deployment-ops-review.md`.
- `references/next-actions-template.md` — load when writing `next-actions.md`.
- `references/target-shift-log-template.md` — load when writing or appending `target-shift-log.md`.
- `references/snapshot-schema.md` — load when writing or reading `snapshot.json`.

## Validation

- Every capability, function point, and maturity claim cites a concrete path (and line number when applicable).
- Items without direct evidence are marked `[INFERRED]` with the inference source, or `[UNKNOWN]` with what would resolve them.
- No completion percentage, weight, score, "X% done", resource estimate, cost estimate, schedule commitment, or staffing plan appears in any output. The research pass is not the evaluation pass.
- Blockers are written as symptom + hypothesis + next-step triples, not as complaints.
- The capability map is organized by business behavior, with engineering layers (frontend/backend/data/AI/deploy) as a secondary mapping. It explicitly separates function points from spec candidates.
- The three breakdown views (capability / product / work) are produced separately and stay aligned through `tracking-matrix.md`. They are not merged into one master table.
- `work-breakdown.md` stays at management work-package granularity in standard tier; drill-down to task-card level happens only in deep tier and only for the most critical packages. Full project-wide task decomposition is left to `delivery-task-planning`.
- `tracking-matrix.md` has one row per tracked function point or work package and is usable as the later progress-management entrypoint.
- CSV files under `tables/` use stable IDs, `parent_id` for hierarchy expansion, and cross-file references instead of duplicated prose. `tables/tracking_matrix.csv` is the primary importable management table.
- Outputs redact secret values and personal data. Use `API_KEY=<redacted>` style examples when config evidence matters.
- Cost Breakdown, Organization Breakdown, Risk Breakdown, resource planning, and scheduling are deliberately out of scope. Capability Breakdown is in scope.
- Incremental runs append to `target-shift-log.md` instead of overwriting; prior entries are preserved.
- Output language is Simplified Chinese by default. Keep file names, IDs, code identifiers, paths, commands, API names, config keys, and CSV headers in their original form for traceability and import stability.
- The delivery summary at the end of the run is short and does not duplicate the artifacts.
