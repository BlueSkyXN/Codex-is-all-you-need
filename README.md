# Codex Is All You Need

[中文](README_CN.md) | English

`Codex Is All You Need` is a public-safe version of a Codex agent / skill preset system. It is not a private machine dump. It distills a real local production setup into a reusable structure, sanitized examples, management scripts, and a read-only dashboard.

In one line:

```text
source catalog -> local suites -> runtime .codex entrypoints
```

Use this repository to:

1. Learn how to manage Codex agents, skills, suites, and runtime entrypoints.
2. Copy public-safe examples to build your own local agent / skill catalog.
3. Inspect, deploy, and maintain local Codex presets with a dashboard and scripts.

## Who This Is For

- Developers who want to turn repeated workflows into Codex skills.
- Teams or individuals who want custom agents for different work domains.
- Users migrating Claude Code-style agent / skill patterns into Codex.
- People who want one source catalog, multiple suite compositions, and several runtime entrypoints.
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
  architecture.md                 # source / suite / runtime architecture
  agent-design.md                 # custom agent design
  skill-design.md                 # skill design
  agent-skill-map.md              # agent and skill responsibility map
  discovery-boundaries.md         # sanitized discovery boundary conclusions
  product-engineering-flow.md
  claude-to-codex-migration.md
  public-private-strategy.md

examples/
  catalog/                        # sanitized public agent / skill source catalog
  runtime/                        # runtime AGENTS.md example
  suites/                         # suite symlink pattern notes
```

## Core Model

```text
source catalog
  Stores real agent TOML files and skill folders.
  Example: examples/catalog/dev/agents/dev_python_engineer.toml
           examples/catalog/dev/skills/python-quality/SKILL.md

local suites
  Machine-local composition layer. Each suite chooses visible agents / skills
  through symlinks.
  Example: ~/.codex/suites/github/agents/*.toml
           ~/.codex/suites/github/skills/*

runtime entrypoints
  The .codex/agents and .codex/skills entries that Codex can discover from the
  current working directory.
  Example: <repo>/.codex/agents/<agent>.toml
           <repo>/.codex/skills/<skill>
```

For the full explanation, read [docs/usage-guide.md](docs/usage-guide.md) and [docs/architecture.md](docs/architecture.md).

## 3-Minute Quick Start

### 1. Inspect the public catalog

```bash
find examples/catalog -maxdepth 3 \( -path '*/agents/*.toml' -o -path '*/skills/*/SKILL.md' \)
```

Public examples include:

| Pack | Agents | Skills | Use Case |
|---|---:|---:|---|
| `common` | 6 | 0 | Planning, orchestration, docs verification, quality review, context summaries, file organization |
| `product-engineering` | 6 | 6 | PRDs, functional specs, technical bridges, task planning, readiness review |
| `dev` | 14 | 19 | Code mapping, implementation, tests, reviews, APIs, CLI, frontend, Python, security, performance |
| `data` | 5 | 4 | Data profiling, SQL, cleaning, pipelines, analysis reports |
| `office` | 5 | 5 | Meeting minutes, weekly reports, project reports, briefing notes, deck outlines |
| `research` | 4 | 3 | Material processing, evidence tables, deduplication, synthesis, gap review |

See [docs/agent-skill-map.md](docs/agent-skill-map.md) for the full responsibility map.

### 2. Generate the read-only dashboard

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

The dashboard is read-only. It does not create, delete, or modify symlinks. See [dashboard/README.md](dashboard/README.md) for config fields and status meanings.

### 3. Sync repo entrypoints in bulk

Codex does not automatically inherit a parent `.codex` from child git repositories. If you have an already-aggregated workspace entrypoint such as:

```text
/Users/sky/GitHub/.codex/agents
/Users/sky/GitHub/.codex/skills
```

and you want every selected repo under `/Users/sky/GitHub/*` to see that capability set, create repo-local entrypoints. Choose the link mode explicitly; `directories` is recommended for workspace aggregates:

```bash
# dry-run
python3 scripts/sync_codex_entrypoints.py sync \
  --workspace /Users/sky/GitHub \
  --source-root /Users/sky/GitHub/.codex \
  --link-mode directories

# apply
python3 scripts/sync_codex_entrypoints.py sync \
  --workspace /Users/sky/GitHub \
  --source-root /Users/sky/GitHub/.codex \
  --link-mode directories \
  --apply
```

Recommended directory-mode result:

```text
<repo>/.codex/agents -> /Users/sky/GitHub/.codex/agents
<repo>/.codex/skills -> /Users/sky/GitHub/.codex/skills
```

Use `--link-mode entries` only when a repo must keep real `.codex/agents` or `.codex/skills` directories, selectively opt in to a small set of shared entries, or mix shared entries with local experiments:

```text
<repo>/.codex/agents/<agent>.toml -> /Users/sky/GitHub/.codex/agents/<agent>.toml
<repo>/.codex/skills/<skill>      -> /Users/sky/GitHub/.codex/skills/<skill>
```

Update and clean examples:

```bash
# directory mode updates automatically through the linked directories
python3 scripts/sync_codex_entrypoints.py sync \
  --workspace /Users/sky/GitHub \
  --source-root /Users/sky/GitHub/.codex \
  --link-mode directories \
  --apply

# entries mode can also remove stale symlinks
python3 scripts/sync_codex_entrypoints.py sync \
  --workspace /Users/sky/GitHub \
  --source-root /Users/sky/GitHub/.codex \
  --link-mode entries \
  --prune \
  --apply

# remove managed entrypoints
python3 scripts/sync_codex_entrypoints.py clean \
  --workspace /Users/sky/GitHub \
  --source-root /Users/sky/GitHub/.codex \
  --link-mode directories \
  --apply
```

The script only manages symlinks that point into the selected `--source-root`. It does not delete real files, real directories, or project-specific entrypoints. If a real directory contains local content, directory mode reports a conflict instead of replacing it.

Keep `.agents/skills` for project-only skills. Do not deploy shared suite skills there; use `.codex/skills` directory or entry links for shared runtime visibility.

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
prd-workflow
functional-spec
technical-spec-bridge
delivery-task-planning
readiness-review
change-spec-adapter

repo-onboarding
bugfix
pr-review
test-strategy
python-quality
api-contract-review
frontend-ui-implementation
security-review
performance-diagnosis
release-check
```

For the complete catalog and recommended pairings, read [docs/agent-skill-map.md](docs/agent-skill-map.md). Pack-level READMEs live here:

```text
examples/catalog/common/README.md
examples/catalog/product-engineering/README.md
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

Recommended skills: python-quality, test-strategy.

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

Important: repo-local custom agents are discovered from `.codex/agents/*.toml`, not `.agents/agents`.

## How To Imitate A Skill

Minimal skill:

```markdown
---
name: python-quality
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
<source>/dev/skills/python-quality/SKILL.md
```

Runtime-visible location:

```text
<repo>/.codex/skills/python-quality/SKILL.md
```

Project-only skills may also live under:

```text
<repo>/.agents/skills/<project-skill>/SKILL.md
```

## Maintenance Principles

Recommended order:

```text
1. Maintain the source catalog first.
2. Maintain local suites second.
3. Expose runtime entrypoints last.
4. Verify with the dashboard and Codex visibility checks.
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
- Use symlinks in suites and keep real files in the source catalog.
- Keep private production catalogs separate from public examples.
- Run `dashboard/build_dashboard.py --json-only` after suite changes.

## Public And Private Boundary

This repository is the public-safe layer. It may contain:

- Dashboard source code.
- Sanitized agent / skill examples.
- Suite / runtime management patterns.
- Sanitized discovery boundary conclusions.
- Reusable entrypoint sync scripts.

It should not contain:

- Private skill content.
- Real runtime config.
- Real dashboard output.
- Machine-local symlink state.
- Tokens, account names, internal URLs, or private templates.

See [docs/public-private-strategy.md](docs/public-private-strategy.md) for the full boundary.
