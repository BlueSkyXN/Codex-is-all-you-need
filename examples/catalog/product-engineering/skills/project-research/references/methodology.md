# Project Research Methodology

This document carries the conceptual depth of the skill. The `SKILL.md` is the operational contract; this file is the why. Load it on first use, when the user asks about maturity or status tags, or when a research output is being challenged for honesty or rigor.

## 1. Two passes, not one

Research and evaluation must be physically separated.

- **Research pass** describes what is. It produces a research pack — positioning, capabilities, evidence, blockers, maturity. It produces no scores, no weights, no percentages, no "done / not done" verdicts.
- **Evaluation pass** assigns weights, judges progress, scores delivery, and prepares performance or reporting narrative. It runs on top of an accepted research pack.

Why this matters: when scoring lives in the same workflow as research, the model starts shaping the evidence to justify a score. The research pack becomes self-fulfilling. Keeping them apart preserves the research pack as something a human or a downstream skill can trust, including disagreeing with later.

If a user asks for completion rate, weight, or score inside this skill, refuse the framing and direct them to run the evaluation step separately on top of the produced pack.

## 2. M0-M9 delivery maturity model

Maturity levels describe how far a capability has progressed toward being deliverable. Levels are inclusive (M5 implies M4). A capability that has run but never been tested is M5, not M7. A capability that has been tested but not deployed is M7, not M8.

| Level | Name | Recognition criterion |
|---|---|---|
| M0 | Idea | Goal or verbal request only; no artifact. |
| M1 | Scoped | In-scope and out-of-scope are written down. |
| M2 | Specified | Function spec, IO contract, and acceptance criteria exist. |
| M3 | Designed | Architecture, modules, interfaces, data model, and state design exist. |
| M4 | Implemented | Pages, endpoints, scripts, configs, or models exist as code. |
| M5 | Runnable | Runs in a local or experimental environment end-to-end. |
| M6 | Integrated | Multiple modules or external services interoperate as intended. |
| M7 | Tested | Test cases exist, have been executed, and the defect list is tracked. |
| M8 | Pilotable | Used in a real or near-real scenario with real data or real users. |
| M9 | Deliverable | Accepted, reusable, operable, with handoff materials in place. |

Inferred maturity is not allowed without evidence. If only some sub-modules of a capability reach M5 and others stop at M4, record the capability as M4 with a note that some parts reach M5; do not average.

## 3. Status tags

Status tags describe the state of a capability or function point along orthogonal axes. Multiple tags per item are allowed and expected — a capability can be `implemented` + `runnable` + `blocked` + `changed` at the same time.

| Tag | Meaning |
|---|---|
| `planned` | In the project's stated scope but no spec or code yet. |
| `specified` | Has a function spec or written behavior contract. |
| `designed` | Has architecture, interface, or data design committed. |
| `implemented` | Code exists for the capability. |
| `runnable` | Starts and produces output in a non-production environment. |
| `integrated` | Connected to its peer modules or external services. |
| `tested` | Test cases written and executed at least once. |
| `demoable` | Can be shown end-to-end with sample inputs. |
| `deployed` | Reachable on a real environment (staging or prod). |
| `operable` | Has logs, health checks, and a documented recovery path. |
| `blocked` | A specific blocker prevents progress; must link to a blocker entry. |
| `changed` | The target or scope shifted after implementation started; must link to a `target-shift-log` entry. |
| `deprecated` | No longer in scope; code may still exist but should not be invested in. |

Status tags are preferred over completion percentages because they describe orthogonal dimensions a real project actually has, instead of collapsing them into a single fictional number.

## 4. Evidence strength levels

Evidence strength controls how much confidence to put behind a claim. Always record both the type and the path that supports it.

| Level | Source | Confidence |
|---|---|---|
| Plan | Stated in roadmap, PRD, or planning doc only. | Low |
| Doc | Described in README, design doc, or spec. | Medium |
| Code | Code exists for the behavior. | Medium-high |
| Runnable | Demonstrated start-up, request-response, or sample output. | High |
| Integrated | Multi-module or external-service interaction observed. | High |
| Tested | Test cases run with passing results recorded. | Very high |
| Deployed | Reachable on a real environment with proof of access. | Very high |
| Audited | Accepted by review, audit, or pilot sign-off. | Highest |

Lower-level evidence does not invalidate a claim, but it must be honestly labeled. Never round up.

## 5. Vibe-coding adaptations

AI-assisted or "vibe-coded" projects have a different shape from waterfall projects. The methodology accommodates this without inventing a separate framework.

### 5.1 Code can precede spec

It is normal for a function point to reach `implemented` or `runnable` before any spec is written. Do not mark such items as "missing spec" failures. Instead, record them as `implemented` + (no `specified` tag), and add them to `next-actions.md` under "specs to backfill".

### 5.2 Target shifts are first-class

Targets often change mid-stream. Capture each shift as an entry in `target-shift-log.md`:

```
Old goal:
Trigger / reason:
New goal:
Affected components:
Reusable artifacts:
Refactor required:
Current status:
```

Tag any affected capability `changed`. Do not silently rewrite the original goal — both old and new must remain visible so a reader can see the path.

### 5.3 Exploration assets are real work

Prompts, workflow drafts, agent configs, failed experiments, model comparisons, and refactor records are part of the engineering output, not noise. List them in the capability map under an `exploration` domain with their own evidence.

### 5.4 Blockers and demo chains are deliverables

Two artifacts that traditional methods underweight:

- **Blocker list** is a first-class output, not a footnote. The shape of the blocker list often predicts whether a capability will land.
- **Demo chain** is the path a human can use to show the capability working: input sample, expected output, fallback for failures. Track demo chains explicitly for capabilities tagged `demoable`.

### 5.5 Deployment and operations are inside the capability map

Startup, environment variables, dependency management, health checks, log access, recovery paths, and handoff documentation are capabilities, not chores. Map them as the `deployment` and `operations` capability domains with their own L3 function points.

## 6. Anti-fabrication rules

The single largest failure mode of an LLM doing project research is to invent capabilities, function points, or evidence that sound plausible but do not exist. These rules exist to make that failure mode visible.

### 6.1 Every claim cites a path

- Capability claims cite a directory or set of files.
- Function point claims cite a file path and, where applicable, a line number.
- Evidence map entries are invalid without a path.
- If a claim cannot be backed by a path, it is not a claim — it is an inference (see 6.2) or it is removed.

### 6.2 Inferred items are tagged

- Inferred goals, capabilities, or function points are tagged `[INFERRED]` with the inference source: "inferred from presence of `auth/` directory and JWT helpers".
- Inferred items are kept separate from evidenced items in tables and lists, never blended.
- An inferred item being repeated across many runs does not promote it to evidenced.

### 6.3 Unknowns are explicit

- Items that look like they should exist but do not are tagged `[UNKNOWN]` with the resolution path: "[UNKNOWN] no test directory found — confirm whether tests live elsewhere or are absent".
- Do not silently omit unknowns to make a report look clean. A clean report with hidden unknowns is worse than a transparent report with marked gaps.

### 6.4 No reasoning by analogy

- Do not write "this is similar to project X so it probably also does Y". The research pack records what the target project actually has, not what its peers have.
- Do not borrow function points from one capability domain to fill out another that looks thin.

### 6.5 Incremental runs are honest about drift

- When an incremental run finds that an old claim no longer holds, remove the claim and add a `[REMOVED]` line to `target-shift-log.md` with the date and reason.
- Do not preserve a stale claim because the previous run wrote it.

## 7. Output language convention

- The research pack uses the same primary language as the target project's documentation. An English-first repo gets English outputs; a Chinese-first repo gets Chinese outputs.
- Code paths, identifiers, and command names stay in their original form regardless of language.
- The `methodology.md` and the template stubs in this skill are written in English so they are stable across projects, but they are reference material; the outputs they produce follow the target project's convention.

## 8. Breakdown structures: capability, product, work, and what stays out

The research pack uses three breakdown structures in parallel, kept as separate documents so each view stays clean:

| View | File | Question it answers | Granularity |
|---|---|---|---|
| Capability tree | `capability-map.md` | What capabilities does the system have or need? | L1 domain → L3 function point |
| Product structure (PBS) | `product-structure.md` | What does the system actually ship — subsystems, modules, components, runtime artifacts? | Subsystem → module → component |
| Work breakdown (WBS-lite) | `work-breakdown.md` | What work would move each capability to its next maturity level? | Work package (1-3 person-weeks); deep tier may drill to task cards |

### 8.1 Why three views, not one

A single fused table looks compact but quietly distorts each view:

- Capabilities are business-shaped (what the system does for a user). They do not map 1:1 to modules — one capability often spans many modules; one module often supports many capabilities.
- Product structure is engineering-shaped (what the codebase actually ships). It reveals integrations, shared infrastructure, and runtime artifacts that the capability view hides.
- Work items are time-shaped (effort to move forward). They cross both capabilities and modules and have their own dependency graph.

Forcing all three into one row encourages the model to drop whichever view does not fit the row, which is the most common way capability/product confusion enters a research pack.

### 8.2 Keeping the three views aligned

Independence does not mean disconnection. The end of `capability-map.md` carries a short **Cross-view alignment** table:

| Capability (L1) | Primary product modules | Key function points | Open work items |
|---|---|---|---|
| ... | (refs into `product-structure.md`) | (refs into `capability-map.md` body) | (refs into `work-breakdown.md`) |

This is the only cross-reference. It is intentionally short — the goal is navigation, not duplication. If a reader needs more, they jump to the target document.

### 8.3 WBS granularity rule

Research-pass WBS is deliberately lighter than project-management WBS:

- **Default (standard tier)**: work-package granularity, 1-3 person-weeks per item. Each package names the capability and maturity transition it serves (for example, "move task-management capability from M5 to M6"), plus a one-line scope description and any blockers it depends on.
- **Drill-down (deep tier)**: the most critical packages — typically the top 3-5 that gate the end-to-end chain — are decomposed into task cards (hours to a few days). Other packages remain at package granularity.
- **Out of scope**: full project-wide task decomposition, dependency graphs across all tasks, sequencing, and per-task validation expectations. Those are produced by `delivery-task-planning` after the research pack is accepted.

If a reader needs full WBS, the research pack tells them where to go (`delivery-task-planning`) rather than expanding inside this skill.

### 8.4 What stays out of this skill

The breakdown-structure family includes more than these three. The ones we deliberately do not produce in a research pass:

- **CBS (Cost Breakdown)** — cost is an evaluation/budgeting activity. Mixing it into research distorts the evidence (people start sizing the research to justify a budget). It belongs downstream, on top of an accepted pack.
- **OBS (Organization Breakdown)** — ownership and RACI live with the team and change faster than the research pack should. Capture owners only where they are evidenced (commit history, CODEOWNERS), not as a separate breakdown.
- **RBS (Risk Breakdown)** — research surfaces blockers and unknowns, which are concrete and code-grounded. Treating risk as a separate hierarchy invites speculation. Open risks are recorded inside `blocker-list.md` and `next-actions.md`, not as a parallel tree.
- **BOM (Bill of Materials)** — meaningful for hardware/manufacturing; not applicable to software research.

These are valid management tools, but they belong to other skills or other phases. Keeping them out of the research pass preserves its evidence discipline.

## 9. Interaction with downstream skills

The research pack is designed to feed:

- `prd-workflow` — uses `project-overview.md`, `capability-map.md`, and `next-actions.md` to scope a new PRD on top of an existing system.
- `functional-spec` — uses `function-spec-cards/` (deep tier) as starting drafts; cards are not yet PRD-approved specs and must be reviewed before promotion.
- `delivery-task-planning` — uses `blocker-list.md` and `next-actions.md` to size near-term work.
- `readiness-review` — uses `evidence-map.md` and `delivery-maturity.md` to judge whether a capability is ready to move to the next gate.
- Office and reporting skills (e.g., `project-progress-report`) — reuse the research pack as raw material; they apply their own evaluation pass and do not assume completion language already exists in the pack.

When invoked back-to-back with one of these skills, the research pass still runs to completion first. The downstream skill consumes the artifacts as a separate step.
