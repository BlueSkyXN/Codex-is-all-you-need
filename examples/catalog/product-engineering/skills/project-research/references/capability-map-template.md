# Capability Map: {project name}

## L0 — Project goal
{One sentence; copy from `project-overview.md`.}

## L1 — Capability domains

For each business-behavior capability domain, fill the L1-L3 block below. Decompose by behavior first, then map to engineering layers in §Engineering mapping.

### {L1 capability name}

**Purpose:** {what this capability lets the user/system do}
**Status tags:** {planned, specified, implemented, runnable, integrated, tested, blocked, changed, ...}
**Maturity (M0-M9):** M{n} — {evidence summary, see `delivery-maturity.md`}

#### L2 — Modules under this capability
| Module | Path | Role |
|---|---|---|
| ... | `src/...` | ... |

#### L3 — Function points
| ID | Function point | Path:line | Status tags |
|---|---|---|---|
| FP-{capability}-001 | ... | `src/file.py:120` | implemented, runnable |
| FP-{capability}-002 | ... | `[UNKNOWN]` — referenced in README but no code found | planned |

(Repeat L1 block per capability domain.)

## Engineering mapping
Map each L1 capability to engineering layers (frontend / backend / data / AI / deploy / ops). This is a secondary view; the L1 list above is the primary decomposition.

| L1 capability | Frontend | Backend | Data | AI/ML | Deploy/Ops |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

## Cross-view alignment
Single short table linking this view to `product-structure.md` and `work-breakdown.md`. Navigation only — do not duplicate detail.

| L1 capability | Primary product modules (→ `product-structure.md`) | Key function points | Open work items (→ `work-breakdown.md`) |
|---|---|---|---|
| ... | `subsystem-a`, `subsystem-b` | FP-{...}-001, FP-{...}-003 | WP-{...}-002, WP-{...}-005 |
