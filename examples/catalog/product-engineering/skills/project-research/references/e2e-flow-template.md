# End-to-End Flow: {project name}

Single primary flow from external input to archived output and audit log. If the project has more than one primary flow, list each separately and mark which is the dominant path for the current research goal.

## Primary flow

```
{actor / event}
  ↓
{step 1}
  ↓
{step 2}
  ↓
...
  ↓
{output / archive / audit}
```

## Step detail

| # | Step | Triggered by | Component (→ `product-structure.md`) | Function points (→ `capability-map.md`) | Human-in-loop? | AI/ML involved? | Status | Evidence (path:line) |
|---|---|---|---|---|---|---|---|---|
| 1 | ... | user click | web/TaskForm | FP-tasks-001 | no | no | runnable | `web/TaskForm.tsx:80` |
| 2 | ... | API call | api/tasks | FP-tasks-001, FP-tasks-002 | no | no | runnable, integrated | `services/api/tasks/routes.py:45` |
| 3 | ... | review queue pickup | api/review | FP-review-003 | yes | yes (suggestion model) | implemented, blocked | BLK-002 |

## Failure points

Where the chain breaks today.

| Step | Failure mode | Impact | Linked blocker |
|---|---|---|---|
| 3 | review suggestion schema drift | review pickup hangs | BLK-002 |

## Alternative or secondary flows

Briefly. Each gets its own table if it deserves detail.

| Flow | When it runs | Status |
|---|---|---|
| ... | ... | ... |

## Demo chain

For capabilities tagged `demoable`, the actual path a human uses to show it working.

- **Input sample:** {file or fixture path}
- **Steps to reproduce:** {short numbered list}
- **Expected output:** {observable artifact / response}
- **Failure fallback:** {what to show if the live demo breaks}
