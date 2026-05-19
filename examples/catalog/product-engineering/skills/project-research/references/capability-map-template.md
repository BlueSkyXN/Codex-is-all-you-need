# Capability Map: {project name}

## L0 — Project goal
{One sentence; copy from `project-overview.md`.}

## Capability Breakdown Structure (CBS)

For each business-behavior capability domain, fill the L1-L4 block below. In this skill, CBS means Capability Breakdown Structure. Decompose by behavior first, then map to engineering layers in §Engineering mapping.

CSV companion: write the same hierarchy to `tables/capability_tree.csv`, and write the L3 function-point inventory to `tables/function_inventory.csv`.

### {L1 capability name}

**Purpose:** {what this capability lets the user/system do}
**Status tags:** {planned, specified, implemented, runnable, integrated, tested, blocked, changed, ...}
**Maturity (M0-M9):** M{n} — {evidence summary, see `delivery-maturity.md`}

#### L2 — Capability modules
| Module | Path | Role |
|---|---|---|
| ... | `src/...` | ... |

#### L3 — Function points
| ID | Function point | Path:line | Status tags |
|---|---|---|---|
| FP-{capability}-001 | ... | `src/file.py:120` | implemented, runnable |
| FP-{capability}-002 | ... | `[UNKNOWN]` — referenced in README but no code found | planned |

#### L4 — Spec candidates
Lightweight spec stubs for function points that need later promotion into `functional-spec`. These are not approved specs yet.

| Spec candidate ID | Function point | Actor / trigger | Input | Output | Acceptance signal | Open question |
|---|---|---|---|---|---|---|
| SPEC-{capability}-001 | FP-{capability}-001 | ... | ... | ... | ... | ... |

(Repeat L1 block per capability domain.)

## Engineering mapping
Map each L1 capability to engineering layers (frontend / backend / data / AI / deploy / ops). This is a secondary view; the L1 list above is the primary decomposition.

| L1 capability | Frontend | Backend | Data | AI/ML | Deploy/Ops |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

## Cross-view alignment
Short navigation table linking this view to `product-structure.md`, `work-breakdown.md`, and `tracking-matrix.md`. Navigation only — do not duplicate detail.

| L1 capability | Primary product modules (→ `product-structure.md`) | Key function points | Spec candidates | Work items (→ `work-breakdown.md`) | Tracking row |
|---|---|---|---|---|---|
| ... | `subsystem-a`, `subsystem-b` | FP-{...}-001, FP-{...}-003 | SPEC-{...}-001 | WP-{...}-002, WP-{...}-005 | TRK-{...}-001 |
