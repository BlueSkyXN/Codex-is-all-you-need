# Blocker List: {project name}

Blockers are first-class artifacts. Each entry is a triple: symptom + hypothesis + next step. Complaints without a next step are not blockers.

CSV companion: write active and recently closed blocker rows to `tables/blockers.csv`.

## Active blockers

| ID | Title | Type | Capability impacted (→ `capability-map.md`) | Severity | Status | Blocks e2e? |
|---|---|---|---|---|---|---|
| BLK-001 | local Docker compose fails on `db` | deployment | audit, tasks | major | open | yes |
| BLK-002 | AI rerank output schema drift | ai-output | search | major | investigating | partial |

## Detail (one block per blocker)

### BLK-{id}: {short title}

- **Type:** need / spec / code / data / AI-output / deployment / test / ops / dependency
- **Symptom:** {what is observed; include error message or path}
- **Hypothesis (root cause):** {best current guess; note `[INFERRED]` if not confirmed}
- **Attempted fixes:** {bullet list with outcome of each}
- **Current evidence:** {paths, logs, commit hashes}
- **Next step:** {single concrete action}
- **Blocks end-to-end delivery?:** yes / no / partial
- **First seen:** {date or commit}
- **Owner / asker:** {if known}

(Repeat per blocker.)

## Recently closed blockers

| ID | Title | Closed on | Resolution evidence |
|---|---|---|---|
| BLK-000 | ... | YYYY-MM-DD | commit `abc123`, test green |

Preserved as part of the research history — useful for incremental runs and target-shift analysis.
