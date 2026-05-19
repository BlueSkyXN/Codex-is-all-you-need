# Deployment and Operations Review: {project name}

Deep-tier artifact. Treats deployment and operations as first-class capabilities (see `methodology.md` §5.5), not chores.

## Startup

- **Entry command(s):** ...
- **Required env vars:** {name — purpose — example value source}
- **Required external services:** {db, queue, cache, third-party APIs}
- **Build steps before run:** ...
- **Observed startup time:** ...
- **Known startup failures:** ...

## Dependency management

- **Package manifest(s):** {paths}
- **Lockfile present?:** yes / no — {path}
- **Version pinning policy:** {observed from manifest comments / CI / commits}
- **Outdated or vulnerable deps observed:** ...

## Configuration

- **Config source(s):** {`.env` / env vars / config files / secret manager}
- **`.env.example` present?:** ...
- **Config validation at startup?:** ...
- **Secret handling:** {where secrets live, how they reach runtime, anything `[UNKNOWN]`}

## Deployment

| Aspect | Status | Evidence |
|---|---|---|
| Container image build | ... | `Dockerfile` |
| Compose / orchestration | ... | `docker-compose.yml` / k8s manifests |
| CI/CD pipeline | ... | `.github/workflows/` |
| Health endpoint | ... | path or `[UNKNOWN]` |
| Migration handling | ... | ... |
| Rollback path | ... | ... |

## Observability

- **Application logs:** {where they go, what format}
- **Metrics / monitoring:** ...
- **Tracing:** ...
- **Alerting:** ...
- **Crash reporting:** ...

## Operational readiness

| Capability | Status tag | Evidence | Gap |
|---|---|---|---|
| Can start with one command | runnable / blocked | ... | ... |
| Config clearly documented | ... | ... | ... |
| Logs are searchable | ... | ... | ... |
| Failure produces actionable error | ... | ... | ... |
| Rollback / restore possible | ... | ... | ... |
| Version upgrade path documented | ... | ... | ... |
| Handoff doc exists | ... | ... | ... |

## Open blockers (→ `blocker-list.md`)

- BLK-{id} — {summary}
