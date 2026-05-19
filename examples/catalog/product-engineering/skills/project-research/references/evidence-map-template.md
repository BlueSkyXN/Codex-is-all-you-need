# Evidence Map: {project name}

Per-function-point trace from claim to source. Every row must cite a real path. Rows without paths are not allowed — move them to `[UNKNOWN]` rows with what would resolve them.

## Function-point evidence

| Function point (→ `capability-map.md`) | Code path | Evidence type | Evidence strength (→ `methodology.md` §4) | Confidence | Notes |
|---|---|---|---|---|---|
| FP-tasks-001 create task | `services/api/tasks/routes.py:45-78` | API code | Code | High | request schema validated |
| FP-tasks-001 create task | `tests/test_tasks.py:12-40` | Test code | Tested | Very high | green in CI 2025-04-12 |
| FP-tasks-005 archive task | — | — | — | — | `[UNKNOWN]` — referenced in README but no code; ask owner |

## Coverage summary

| Capability domain | Function points total | With code evidence | With runnable evidence | With tested evidence |
|---|---:|---:|---:|---:|
| tasks | 8 | 7 | 5 | 3 |
| audit | 4 | 4 | 2 | 0 |

## Inferred entries

Items listed without direct code evidence. Each carries `[INFERRED]` and the inference source.

| Function point | Inferred from | What would promote it to evidenced |
|---|---|---|
| `[INFERRED]` FP-auth-003 session expiry | presence of `auth/session.py` + `SESSION_TTL` env var | grep for active TTL handling code |
