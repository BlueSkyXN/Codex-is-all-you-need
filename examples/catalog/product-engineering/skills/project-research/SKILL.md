---
name: project-research
description: "Use to research an existing codebase end-to-end before PRD or planning: project positioning, capability map, function inventory, evidence map, end-to-end flow, deployment readiness, blockers, and delivery maturity. Produces an evidence-grounded research pack consumable by prd-workflow and downstream skills, or by humans writing project reports, product intros, and technical proposals. Not for performance scoring, completion-rate reporting, status updates, or implementation."
---

# Project Research

## Purpose

Turn an existing codebase, configuration, and docs into an evidence-grounded research pack that downstream skills (`prd-workflow`, `functional-spec`, `delivery-task-planning`) can build on, and that humans can reuse for project reports, product introductions, technical proposals, or planning discussions.

## Boundary

Project research answers what the project is, what it already does, what is missing, where the end-to-end chain breaks, what blockers stand in the way, and how mature each capability is. It does not assign weights, completion percentages, performance scores, or status-report language. Evaluation, scoring, and reporting are downstream activities that must run on top of an accepted research pack, never inside the same pass.

## Tiers

Choose one tier per run. Default is `standard`.

- `quick` — 1-page positioning + blocker list. Use when scoping a discussion or first-touch onboarding.
- `standard` — Full capability map, evidence map, end-to-end flow, maturity, blockers, and next actions. Use as the durable research baseline for most projects.
- `deep` — Adds per-function spec cards, deployment/ops review, and target-shift log. Use before serious PRD work on a critical capability, or when handing the project to a new owner.

Tier is selected by the user or inferred from the request. Do not silently upgrade or downgrade.

## Workflow

1. Confirm target project root (default to current working directory) and tier.
2. Confirm output directory (default `./local/research/`; create if missing).
3. If `snapshot.json` already exists in the output dir, run in incremental mode: re-scan, diff against the snapshot, and update only what changed. Record any goal changes in `target-shift-log.md` instead of overwriting prior entries.
4. Scan project structure: entry points, languages and frameworks, dependency manifests, routes, models, components, scripts, deployment configs, tests, docs, examples, env templates, and CI files.
5. Reconstruct project positioning using only signals present in the repo. Separate explicit goals (named in README/docs) from implicit goals (inferred from code structure). Mark every inferred item as `[INFERRED]` with the inference source.
6. Build three breakdown views in sequence; do not collapse them into one view (see `references/methodology.md` §9 for the reasoning):
   - **Capability tree (`capability-map.md`)**: business-behavior view. L0 project goal → L1 capability domain → L2 module → L3 function point. End with a "Cross-view alignment" table mapping each L1 capability to its product modules and key work items.
   - **Product structure (`product-structure.md`)**: deliverable view, akin to a Product Breakdown Structure (PBS). Subsystems, modules, components, integrations, and runtime artifacts. Use what the repository actually ships, not idealized architecture.
   - **Work breakdown (`work-breakdown.md`)**: a lite WBS limited to "what work would move each capability to its next maturity level". Default granularity is **work package (1-3 person-weeks)**. In `deep` tier, drill the most critical packages down to task-card level. Full project-wide WBS belongs to `delivery-task-planning`, not here.
7. Build the evidence map: for each function point, attach code path, evidence type, evidence strength, and confidence.
8. Trace the end-to-end main flow from external input to archived output and audit log. Mark where humans are required and where AI/ML is involved.
9. Catalog blockers as first-class artifacts (need / spec / code / data / AI-output / deployment / test / ops / dependency types). Each blocker records symptom, hypothesis, attempted fixes, next step, and whether it blocks end-to-end delivery.
10. Assign a delivery maturity level per capability domain using the M0-M9 scale, with traced evidence. Apply status tags (`planned`, `specified`, `designed`, `implemented`, `runnable`, `integrated`, `tested`, `demoable`, `deployed`, `operable`, `blocked`, `changed`, `deprecated`); multiple tags per capability are allowed and expected.
11. For `deep` tier only: produce a function spec card per critical function point, a deployment/ops review, and drill the most critical work packages in `work-breakdown.md` to task-card level.
12. Write `next-actions.md` with short-term loop-closing items, mid-term build items, long-term optimization items, and items that need human or owner confirmation. Next actions are summary-level; the detailed work decomposition lives in `work-breakdown.md`.
13. Update `snapshot.json` with the current scan state for the next incremental run.
14. Print a delivery summary: tier, output paths, capability count, evidence coverage ratio, top three blockers, and the single most useful next action.

## Outputs

Written under the chosen output directory (default `./local/research/`).

Quick tier:

- `project-overview.md`
- `blocker-list.md`
- `snapshot.json`

Standard tier (adds):

- `capability-map.md` — capability tree + cross-view alignment table
- `product-structure.md` — PBS view of shipped deliverables
- `work-breakdown.md` — lite WBS at work-package granularity
- `evidence-map.md`
- `e2e-flow.md`
- `delivery-maturity.md`
- `next-actions.md`

Deep tier (adds):

- `function-spec-cards/<id>.md` (one per critical function point)
- `deployment-ops-review.md`
- `target-shift-log.md` (also created in incremental runs whenever goals shift)

## References / Load When

- `references/methodology.md` — load on first use, or when the user asks about maturity, status tags, evidence strength, vibe-coding adaptation, or anti-fabrication rules.
- `references/project-overview-template.md` — load when writing `project-overview.md`.
- `references/capability-map-template.md` — load when writing `capability-map.md`.
- `references/product-structure-template.md` — load when writing `product-structure.md`.
- `references/work-breakdown-template.md` — load when writing `work-breakdown.md`.
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
- No completion percentage, weight, score, or "X% done" appears in any output. The research pass is not the evaluation pass.
- Blockers are written as symptom + hypothesis + next-step triples, not as complaints.
- The capability map is organized by business behavior, with engineering layers (frontend/backend/data/AI/deploy) as a secondary mapping.
- The three breakdown views (capability / product / work) are produced separately and stay aligned via the cross-view table at the end of `capability-map.md`. They are not merged into one document.
- `work-breakdown.md` stays at work-package granularity (1-3 person-weeks) in standard tier; drill-down to task-card level happens only in deep tier and only for the most critical packages. Full project-wide task decomposition is left to `delivery-task-planning`.
- Cost, organization, and risk breakdown structures (CBS / OBS / RBS) are deliberately out of scope for this skill — they belong to budgeting, staffing, and risk management activities downstream.
- Incremental runs append to `target-shift-log.md` instead of overwriting; prior entries are preserved.
- Output language matches the codebase's primary documentation language (English-first repos get English outputs; Chinese-first repos get Chinese outputs).
- The delivery summary at the end of the run is short and does not duplicate the artifacts.
