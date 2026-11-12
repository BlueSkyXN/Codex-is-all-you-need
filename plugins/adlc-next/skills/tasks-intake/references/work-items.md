# Work-item format

Shared by `tasks-intake` and `tasks-wrap-up`. Use the project's tracker when it
has one; this format applies to the work-items file and to the fields any
tracker entry should carry.

## Where items live

1. The project's existing tracker or backlog file, when there is one.
2. Otherwise the project settings: `tracker = "github-issues"` uses the
   repository's issues; `tracker = "file"` uses `work_items_file`.
3. Otherwise `local/adlc/WORK-ITEMS.md`.

Do not start a second, competing list next to an existing one. Writing to an
external tracker follows the authorization rule in
[the shared conventions](../../sdlc-solve/references/conventions.md).

## Fields

| Field | Content |
|---|---|
| ID | Stable identifier: the tracker's number, or `W1`, `W2`, ... in the file |
| Outcome | What will be true when the item is done |
| Done when | Observable completion condition |
| Depends on | Other items or external conditions it waits for |
| Status | `todo`, `in-progress`, `blocked`, `done`, or `dropped` |
| Next step | The first concrete action |
| Source | Where it came from: issue, review, task-file follow-up, feedback |

A `blocked` item names what unblocks it. A `dropped` item keeps a one-line
reason. A `done` item points to its evidence: merged PR, verified result.

## File layout

```markdown
# Work items

Last updated: <YYYY-MM-DD>

| ID | Outcome | Done when | Depends on | Status | Next step | Source |
|---|---|---|---|---|---|---|
| W1 | Customers see claim status in the portal | Status panel shows the four claim states | — | todo | Add the status endpoint | Issue #12 |

## Order

1. W1: no dependencies; unblocks W2 and W3.
```
