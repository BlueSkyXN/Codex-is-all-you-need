# Codex Is All You Need

[中文](README_CN.md) | English

`Codex Is All You Need` is a public-safe V2 Codex plugin-first preset system.
It is not a private machine dump. It distills a real local production setup
into a reusable source catalog, installable plugin package, sanitized examples,
management scripts, and a read-only dashboard.

In one line:

```text
source catalog -> plugin package -> marketplace install
```

Use this repository to:

1. Install Codex Next or focused standalone plugins from the repository marketplace.
2. Copy public-safe examples to build your own local agent / skill catalog.
3. Learn how to design Codex agents and skills around a plugin-first workflow.
4. Migrate or inspect old V1 suite/composition setups when needed.

## Who This Is For

- Developers who want to turn repeated workflows into Codex skills.
- Teams or individuals who want custom agents for different work domains.
- Users migrating Claude Code-style agent / skill patterns into Codex.
- People who want plugin-first shared skills, with V1 suite docs only for migration or local experiments.
- People who want to publish structure and examples without leaking private prompts, paths, templates, or machine state.

## What This Is Not

- It is not an official OpenAI directory standard.
- It is not a one-command installer for a complete production setup.
- It is not a mirror of a private `~/.codex` home or private business skills.
- It does not make a parent `.codex` automatically inherited by every child git repository. Codex repo-level discovery is bounded by the current project root. See [Architecture](docs/architecture.md) and [Discovery Boundaries](docs/discovery-boundaries.md).

## Repository Layout

```text
dashboard/
  build_dashboard.py              # read-only dashboard generator
  templates/index.html
  examples/config.example.toml

scripts/
  sync_codex_entrypoints.py       # batch sync repo-local .codex entrypoints

docs/
  usage-guide.md                  # full bilingual usage guide
  architecture.md                 # V2 plugin-first architecture
  agent-design.md                 # custom agent design
  skill-design.md                 # skill design
  agent-skill-map.md              # agent and skill responsibility map
  discovery-boundaries.md         # sanitized discovery boundary conclusions
  user-global-agents-example.md   # public-safe user-level AGENTS.md example
  model-catalog-override.md       # custom Codex model catalog override guide
  global-git-ignore.md            # user-level Git ignore profile
  v1/                             # legacy suite/composition docs and migration notes
  architecture-first-sdlc-flow.md
  claude-to-codex-migration.md
  public-private-strategy.md

plugins/
  codex-next/                      # installable skills plugin
  visual-brainstorming/            # opt-in local visual comparison plugin

examples/
  catalog/                        # sanitized public agent / skill source catalog
  runtime/                        # runtime AGENTS.md example
  suites/                         # V1 suite fixture pointer
```

## Current V2 Model

```text
source catalog
  Stores real agent TOML files and skill folders.
  Example: examples/catalog/dev/agents/dev_python_engineer.toml
           examples/catalog/dev/skills/dev-python-quality/SKILL.md

plugin package
  Production distribution surface for public-safe shared skills.
  Example: plugins/codex-next/skills/dev-python-quality/SKILL.md
           .agents/plugins/marketplace.json

marketplace install
  User-facing installation path for the plugin package.
  Example: codex plugin add codex-next@codex-is-all-you-need
```

V1 suite/composition docs are kept only for migration and compatibility. Start
there only if a machine still exposes shared skills through `~/.codex/suites`
or repo-local `.codex/skills` links: [docs/v1/](docs/v1/).

For the full V2 explanation, read [docs/usage-guide.md](docs/usage-guide.md)
and [docs/architecture.md](docs/architecture.md).

## 3-Minute Quick Start

### 1. Inspect the public catalog

```bash
find examples/catalog -maxdepth 3 \( -path '*/agents/*.toml' -o -path '*/skills/*/SKILL.md' \)
```

Public examples include:

| Pack | Agents | Skills | Use Case |
|---|---:|---:|---|
| `common` | 6 | 2 | Planning, orchestration, docs verification, quality review, context summaries, file organization |
| `sdlc-manager` | 7 | 21 | Architecture-first SDLC control: BRD/URS/PRD, SRS/NFR, HLD/LLD, ADR, domain boundaries, SPEC, handoff |
| `dev` | 14 | 20 | Code mapping, implementation, tests, reviews, APIs, CLI, frontend, Python, security, performance |
| `data` | 5 | 4 | Data profiling, SQL, cleaning, pipelines, analysis reports |
| `office` | 5 | 5 | Meeting minutes, weekly reports, project reports, briefing notes, deck outlines |
| `research` | 4 | 3 | Material processing, evidence tables, deduplication, synthesis, gap review |

See [docs/agent-skill-map.md](docs/agent-skill-map.md) for the full responsibility map.

### 2. Install Codex Next

Codex Next packages the public-safe skills into one installable plugin. It does
not package `.codex/agents` custom agent TOML or V1 machine-local suite symlinks.
The plugin includes a `core-router` entrypoint skill for routing a task to the
smallest useful bundled workflow.

Plugin source:

```text
plugins/codex-next
```

Repo marketplace:

```text
.agents/plugins/marketplace.json
```

Install from the GitHub marketplace source:

```bash
codex plugin marketplace add https://github.com/BlueSkyXN/Codex-is-all-you-need.git
```

For local development, add the checked-out repository root instead:

```bash
codex plugin marketplace add /path/to/Codex-is-all-you-need
```

Confirm that Codex can see the uninstalled marketplace entry. The `--available`
flag is required for JSON output; without it, `codex plugin list --json` only
shows installed plugins.

```bash
codex plugin marketplace list --json
codex plugin list --marketplace codex-is-all-you-need --available --json
```

Then install from the configured marketplace:

```bash
codex plugin add codex-next@codex-is-all-you-need
```

After installation, invoke `$codex-next:core-router` or ask Codex to use Codex
Next for the task.

The same marketplace also exposes focused standalone plugins that remain
separate from Codex Next. Visual Brainstorming is an explicit opt-in because it
starts a project-local HTTP companion and opens a browser:

```bash
codex plugin add visual-brainstorming@codex-is-all-you-need
```

See [plugins/visual-brainstorming/README.md](plugins/visual-brainstorming/README.md)
for its runtime boundary and sparse-marketplace upgrade instructions.

If you are moving an existing V1 machine from suite-based runtime entrypoints
to Codex Next, see [V1 To V2 Migration](docs/v1/suite-to-plugin-migration.md).

### 3. Generate the read-only dashboard

First-time setup:

```bash
mkdir -p ~/.codex/dashboard
cp dashboard/examples/config.example.toml ~/.codex/dashboard/config.toml
```

Edit your local config:

```text
~/.codex/dashboard/config.toml
```

Generate the dashboard:

```bash
python3 dashboard/build_dashboard.py --config ~/.codex/dashboard/config.toml
open ~/.codex/dashboard/index.html
```

JSON-only validation:

```bash
python3 dashboard/build_dashboard.py \
  --config ~/.codex/dashboard/config.toml \
  --json-only
```

The dashboard is read-only. In V2 it is mainly for source-catalog inspection;
it can still report V1 legacy/local-dev suite visibility when that compatibility
path is configured. It does not create, delete, or modify symlinks. See
[dashboard/README.md](dashboard/README.md) for config fields and status meanings.

### 4. Optional V1 compatibility: sync legacy/local-dev repo entrypoints

Production shared skills should come from the installed Codex Next plugin. Use
this helper only for V1 legacy suite setups, local-development experiments, or
project-specific custom agent exposure. For the old suite model, see
[V1 Suite Composition](docs/v1/suite-composition.md).

Codex does not automatically inherit a parent `.codex` from child git repositories. If you have an already-aggregated workspace entrypoint such as:

```text
/path/to/workspace/.codex/agents
/path/to/workspace/.codex/skills
```

and you want every selected repo under `/path/to/workspace/*` to see that capability set, create repo-local entrypoints. Choose the link mode explicitly; `directories` is recommended for workspace aggregates:

```bash
# dry-run
python3 scripts/sync_codex_entrypoints.py sync \
  --workspace /path/to/workspace \
  --source-root /path/to/workspace/.codex \
  --link-mode directories

# apply
python3 scripts/sync_codex_entrypoints.py sync \
  --workspace /path/to/workspace \
  --source-root /path/to/workspace/.codex \
  --link-mode directories \
  --apply
```

Recommended directory-mode result:

```text
<repo>/.codex/agents -> /path/to/workspace/.codex/agents
<repo>/.codex/skills -> /path/to/workspace/.codex/skills
```

Use `--link-mode entries` only when a repo must keep real `.codex/agents` or `.codex/skills` directories, selectively opt in to a small set of shared entries, or mix shared entries with local experiments:

```text
<repo>/.codex/agents/<agent>.toml -> /path/to/workspace/.codex/agents/<agent>.toml
<repo>/.codex/skills/<skill>      -> /path/to/workspace/.codex/skills/<skill>
```

Update and clean examples:

```bash
# directory mode updates automatically through the linked directories
python3 scripts/sync_codex_entrypoints.py sync \
  --workspace /path/to/workspace \
  --source-root /path/to/workspace/.codex \
  --link-mode directories \
  --apply

# entries mode can also remove stale symlinks
python3 scripts/sync_codex_entrypoints.py sync \
  --workspace /path/to/workspace \
  --source-root /path/to/workspace/.codex \
  --link-mode entries \
  --prune \
  --apply

# remove managed entrypoints
python3 scripts/sync_codex_entrypoints.py clean \
  --workspace /path/to/workspace \
  --source-root /path/to/workspace/.codex \
  --link-mode directories \
  --apply
```

The script only manages symlinks that point into the selected `--source-root`. It does not delete real files, real directories, or project-specific entrypoints. If a real directory contains local content, directory mode reports a conflict instead of replacing it.

Keep `.agents/skills` for project-only skills. Do not deploy shared plugin or
V1 suite skills there. For production shared skills, install the plugin; for
V1 legacy/local-dev suite visibility, use `.codex/skills` directory or entry links.

## Supported Agents And Skills

The public catalog is grouped by work domain. The most commonly reused entries are:

```text
common
  common_task_planner
  common_orchestrator
  common_context_summarizer
  common_docs_researcher
  common_quality_reviewer
  common_file_organizer

sdlc-manager
  sdlc_project_researcher
  sdlc_requirements_manager
  sdlc_srs_specifier
  sdlc_solution_spec_manager
  sdlc_delivery_planner
  sdlc_readiness_reviewer
  sdlc_change_manager

dev
  dev_code_mapper
  dev_implementer
  dev_code_reviewer
  dev_python_engineer
  dev_backend_engineer
  dev_frontend_engineer
  dev_api_designer
  dev_test_runner
  dev_security_reviewer
  dev_performance_engineer
  dev_cli_engineer
  dev_docs_engineer
  dev_docs_researcher
  dev_architect_reviewer
```

Commonly reused skills:

```text
sdlc-prd-workflow
sdlc-manager
sdlc-project-research
sdlc-srs-workflow
sdlc-nfr-spec
sdlc-hld-workflow
sdlc-lld-workflow
sdlc-domain-boundary-modeling
sdlc-architecture-decision-record
sdlc-solution-spec-workflow
sdlc-spec-slice-writer
sdlc-dev-handoff-planning
sdlc-requirements-traceability
sdlc-readiness-review
sdlc-change-control

dev-repo-onboarding
dev-spec-driven-implementation
dev-bugfix
dev-pr-review
dev-test-strategy
dev-python-quality
dev-api-contract-review
dev-frontend-ui-implementation
dev-security-review
dev-performance-diagnosis
dev-release-check
```

For the complete catalog and recommended pairings, read [docs/agent-skill-map.md](docs/agent-skill-map.md). Pack-level READMEs live here:

```text
examples/catalog/common/README.md
examples/catalog/sdlc-manager/README.md
examples/catalog/dev/README.md
examples/catalog/data/README.md
examples/catalog/office/README.md
examples/catalog/research/README.md
```

## How To Imitate An Agent

Minimal custom agent:

```toml
name = "dev_python_engineer"
description = "Use for Python code, scripts, APIs, CLIs, pytest, typing, packaging, and Python performance work."

sandbox_mode = "workspace-write"

developer_instructions = """
You implement Python software using the project's actual conventions.

Recommended skills: dev-python-quality, dev-test-strategy.

Do:
- Inspect project config and tests first.
- Keep changes scoped and validated.

Return:
1. Scope
2. Changes
3. Checks run
4. Remaining risk
"""
```

Source location:

```text
<source>/dev/agents/dev_python_engineer.toml
```

Runtime-visible location:

```text
<repo>/.codex/agents/dev_python_engineer.toml
```

Important: repo-local custom agents are discovered from `.codex/agents/*.toml`,
not `.agents/agents`. Codex Next does not package these custom agent TOML files.

## How To Imitate A Skill

Minimal skill:

```markdown
---
name: dev-python-quality
description: Use for Python implementation, modernization, typing, packaging, pytest, ruff/mypy checks, and maintainability work.
---

# Python quality workflow

Use this workflow when Python code, packaging, tests, scripts, or modernization are the main task.

## Steps

1. Read project conventions.
2. Define the Python change.
3. Implement idiomatically.
4. Validate with the smallest relevant checks.
5. Report compatibility notes and remaining risk.
```

Source location:

```text
<source>/dev/skills/dev-python-quality/SKILL.md
```

Runtime-visible location:

```text
<repo>/.codex/skills/dev-python-quality/SKILL.md
```

For production shared skills, use the installed `codex-next` plugin. The
repo-local `.codex/skills` path above is for V1 legacy, local-development, or
project-specific exposure.

Project-only skills may also live under:

```text
<repo>/.agents/skills/<project-skill>/SKILL.md
```

## Maintenance Principles

Recommended order:

```text
1. Maintain the source catalog first.
2. Keep plugins/codex-next aligned as the packaged skill surface.
3. Keep V1 local suites out of the default production path.
4. Expose runtime entrypoints only for migration, custom agents, or project-specific overlays.
5. Verify with plugin, dashboard, and Codex visibility checks.
```

Do not:

- Do not symlink the entire `.codex` directory.
- Do not commit private material into this public repository.
- Do not assume a parent `.codex` is inherited by every child repo.
- Do not symlink only `SKILL.md`; link the whole skill folder.
- Do not use `config.toml` as an agent / skill cwd routing table.

Recommended:

- Run every bulk script in dry-run mode first.
- Ignore `.codex/` and `.agents/` as local entrypoint state.
- Keep cross-repository personal ignore rules in `~/.config/git/ignore`; see
  [Global Git Ignore Profile](docs/global-git-ignore.md).
- Keep plugin-packaged public skills aligned with the source catalog.
- Use V1 suite symlinks only for migration or explicit local-development setups.
- Keep private production catalogs separate from public examples.
- Run `dashboard/build_dashboard.py --json-only` after suite changes, and use
  Codex plugin listing commands after plugin packaging changes.

## Public And Private Boundary

This repository is the public-safe layer. It may contain:

- Dashboard source code.
- Sanitized agent / skill examples.
- Codex plugin packages and marketplace metadata.
- V1 legacy suite / runtime management patterns.
- Sanitized discovery boundary conclusions.
- Reusable entrypoint sync scripts.

It should not contain:

- Private skill content.
- Real runtime config.
- Real dashboard output.
- Machine-local symlink state.
- Tokens, account names, internal URLs, or private templates.

See [docs/public-private-strategy.md](docs/public-private-strategy.md) for the full boundary.
