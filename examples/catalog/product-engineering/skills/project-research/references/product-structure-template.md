# Product Structure (PBS): {project name}

Describes what the system actually ships — subsystems, modules, components, integrations, and runtime artifacts. This is the engineering-shipped view, not an idealized architecture diagram.

## Top-level subsystems

| Subsystem | Path / location | Role | Tech stack |
|---|---|---|---|
| ... | `services/api/` | ... | Python/FastAPI |
| ... | `web/` | ... | TypeScript/React |

## Modules and components

For each subsystem, list the major modules and components it ships.

### {Subsystem name}

| Module / component | Path | Responsibility | Notes |
|---|---|---|---|
| ... | `services/api/auth/` | ... | shared by web + mobile |
| ... | `services/api/tasks/` | ... | depends on auth |

(Repeat per subsystem.)

## External integrations

| Integration | Where it is wired | Direction | Auth / contract |
|---|---|---|---|
| ... | `services/api/clients/x.py` | outbound | API key in `.env` |

## Runtime artifacts

What actually gets deployed, packaged, or shipped to a user.

| Artifact | Build origin | Where it runs | Distribution |
|---|---|---|---|
| `app-server` Docker image | `Dockerfile` | container runtime | internal registry |
| `web` static bundle | `web/dist/` | CDN | public |
| CLI binary | `cmd/cli/` | user laptop | GitHub releases |

## Shared infrastructure

Cross-cutting components used by multiple subsystems (logging, auth, feature flags, config, observability).

| Component | Path | Used by |
|---|---|---|
| ... | `pkg/log/` | api, worker |

## What is NOT shipped

Items present in the repo but not part of the shipped product (research scripts, abandoned prototypes, vendored examples, legacy folders). List them so they are not mistaken for live capabilities.

| Item | Path | Reason | Status tag |
|---|---|---|---|
| ... | `experiments/` | exploratory; not in build | deprecated / exploration |
