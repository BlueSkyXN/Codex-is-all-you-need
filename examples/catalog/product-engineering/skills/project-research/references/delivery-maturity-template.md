# Delivery Maturity: {project name}

Per-capability maturity assessment using the M0-M9 scale defined in `methodology.md` §2. Every level claim is backed by traced evidence; no level is averaged across sub-modules.

CSV companion: write capability maturity rows to `tables/maturity.csv`.

## Maturity table

| Capability (→ `capability-map.md`) | Baseline maturity | Critical path maturity | Status tags | Evidence anchor (path or `evidence-map.md` ref) | Notes |
|---|---|---|---|---|---|
| tasks | M5 | M6 | implemented, runnable, blocked | `evidence-map.md` row tasks/runnable; BLK-001 | core flow integrated; deploy blocked |
| audit | M4 | M5 | implemented, changed | `services/api/audit/`; target-shift entry 2025-04 | main code exists; spec being rewritten |
| search | M3 | M3 | designed, blocked | `docs/search-design.md`; BLK-002 | no code yet |

## Detail (one block per capability)

### {Capability name}

- **Baseline maturity:** M{n} — {name from §2}; conservative maturity for the whole capability.
- **Critical path maturity:** M{n} — {name from §2}; maturity of the main demonstrable path when different from baseline.
- **Why these levels (recognition criteria satisfied):** {1-3 sentences with evidence paths}
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
