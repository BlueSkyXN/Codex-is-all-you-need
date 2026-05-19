# Target Shift Log: {project name}

Captures changes to project goals and scope across research runs. Append-only. Old entries are preserved so a reader can trace how the project's target evolved (see `methodology.md` §5.2 and §6.5).

## Entries

### {YYYY-MM-DD} — {short title}

- **Old goal:** {what the previous research run / project state stated}
- **Trigger / reason:** {what caused the shift — stakeholder request, blocker, new constraint, target customer change}
- **New goal:** {what is being pursued now}
- **Affected capabilities (→ `capability-map.md`):** {L1 names}
- **Reusable artifacts:** {code / specs / data that survive the shift}
- **Refactor / rework required:** {what must be redone}
- **Current status:** {planning / in progress / done}
- **Evidence source:** {commit, doc, chat thread reference if available}

(Add new entries on top; do not edit prior entries except to mark them superseded.)

## Removed claims

When an incremental run removes a previously asserted capability or function point, log it here so the removal is itself part of the research record.

| Date | Removed item | Was claimed in | Reason for removal |
|---|---|---|---|
| YYYY-MM-DD | FP-{...}-{nnn} | snapshot {hash} | `[REMOVED]` — code path no longer exists; commit `def456` |
