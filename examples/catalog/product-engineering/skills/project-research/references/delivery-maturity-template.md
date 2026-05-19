# Delivery Maturity: {project name}

Per-capability maturity assessment using the M0-M9 scale defined in `methodology.md` §2. Every level claim is backed by traced evidence; no level is averaged across sub-modules.

## Maturity table

| Capability (→ `capability-map.md`) | Level (M0-M9) | Status tags | Evidence anchor (path or `evidence-map.md` ref) | Notes |
|---|---|---|---|---|
| tasks | M5 | implemented, runnable, blocked | `evidence-map.md` row tasks/runnable; BLK-001 | runs locally; deploy blocked |
| audit | M4 | implemented, changed | `services/api/audit/`; target-shift entry 2025-04 | spec being rewritten |
| search | M3 | designed, blocked | `docs/search-design.md`; BLK-002 | no code yet |

## Detail (one block per capability)

### {Capability name}

- **Current level:** M{n} — {name from §2}
- **Why this level (recognition criterion satisfied):** {1-3 sentences with evidence paths}
- **Why not the next level:** {what specifically prevents M{n+1}; link to blocker IDs when applicable}
- **Status tags:** ...
- **Sub-module variance:** {if some parts reach a higher level, list them — do not average}
- **Path to next level:** {1-2 sentence sketch; detailed work belongs in `work-breakdown.md`}

(Repeat per capability.)

## Coverage summary

| Maturity level | Capability count |
|---|---:|
| M0 — Idea | 0 |
| M1 — Scoped | 1 |
| M2 — Specified | 0 |
| M3 — Designed | 2 |
| M4 — Implemented | 3 |
| M5 — Runnable | 2 |
| M6 — Integrated | 1 |
| M7 — Tested | 1 |
| M8 — Pilotable | 0 |
| M9 — Deliverable | 0 |

(No percentages. The shape of this table is the signal.)
