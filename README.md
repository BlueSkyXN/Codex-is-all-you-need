# Codex Is All You Need

[中文](README_CN.md) | English

Public-safe tooling for Codex preset catalogs, local suite inspection, and a read-only bilingual dashboard.

This repository is intentionally not a complete copy of any private production setup. It contains public-safe tooling, design docs, and a sanitized production-derived example catalog. Private skills, runtime paths, generated scan results, and machine-specific symlink state should stay outside this repository.

## Repository Layout

```text
dashboard/
  build_dashboard.py
  templates/index.html
  examples/config.example.toml

docs/
  architecture.md
  agent-design.md
  agent-skill-map.md
  skill-design.md
  claude-to-codex-migration.md
  public-private-strategy.md

examples/
  catalog/
    common/
    dev/
    data/
    office/
    research/
  runtime/
    AGENTS.md
  suites/
```

## What This Repo Contains

```text
Dashboard
  A read-only static dashboard generator for catalog, suite, and runtime
  connection inspection.

Design guides
  Public-safe rules for designing Codex agents, skills, and suite overlays.

Migration notes
  How to learn from Claude Code style agents and skills without copying
  private operational content.

Examples
  Sanitized production-derived agents, skills, and suite layout examples.
```

## Dashboard

The dashboard scans a configurable Codex preset environment:

```text
source catalog -> local suites -> runtime .codex/agents and .codex/skills
```

It is read-only. It does not create, delete, or modify symlinks.

Typical local usage:

```bash
python3 dashboard/build_dashboard.py --config ~/.codex/dashboard/config.toml
open ~/.codex/dashboard/index.html
```

Use `dashboard/examples/config.example.toml` as the starting point for a local config. Do not commit real runtime configs or generated dashboard output.

The generated HTML supports Chinese and English through a `中文 / EN` switch.

See [dashboard/README.md](dashboard/README.md) for setup, config fields, status meanings, and troubleshooting.

## Design Guides

- [Architecture](docs/architecture.md)
- [Agent Design](docs/agent-design.md)
- [Agent Skill Map](docs/agent-skill-map.md)
- [Skill Design](docs/skill-design.md)
- [Claude To Codex Migration](docs/claude-to-codex-migration.md)
- [Public And Private Strategy](docs/public-private-strategy.md)

## Examples

The files under `examples/` are public-safe templates derived from a real production preset design. They are not intended to be installed as-is into a real machine without review.

```text
examples/catalog/
  common/       6 agents, 0 public skills
  dev/         12 agents, 17 public skills
  data/         4 agents, 4 public skills
  office/       4 agents, 5 public skills
  research/     4 agents, 3 public skills

examples/runtime/
  AGENTS.md

examples/suites/
  README.md
```

The public catalog intentionally excludes private symlinked skills and any generated local dashboard state.
