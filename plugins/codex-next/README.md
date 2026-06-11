# Codex Next

Codex Next is an installable Codex plugin that packages the public-safe skills
from this repository into one reusable workflow bundle.

It is meant to strengthen Codex with repeatable software delivery workflows:
task routing, project research, requirements, architecture, specs, validation,
handoff, implementation support, review, data work, office writing, and research
synthesis.

## What It Includes

- A plugin entrypoint skill, `codex-next`, for routing work to the smallest
  useful bundled workflow.
- SDLC and delivery skills such as `artifact-profile-router`,
  `requirements-workflow`, `solution-spec-workflow`,
  `dev-handoff-planning`, and `sdlc-readiness-review`.
- Development skills such as `repo-onboarding`, `bugfix`,
  `spec-driven-implementation`, `pr-review`, `security-review`,
  `test-strategy`, and `release-check`.
- Data, office, research, and common workflow skills from the public catalog.

## What It Does Not Include

- Custom agent TOML files from `.codex/agents`.
- Machine-local suite symlinks or runtime `.codex` entrypoints.
- Private prompts, private paths, credentials, or unpublished skills.

Custom agents remain a separate Codex subagent configuration layer. This plugin
ships reusable skills.

## Package Layout

This directory is the plugin package:

```text
plugins/codex-next/
  .codex-plugin/plugin.json
  README.md
  skills/
    <skill-name>/
      SKILL.md
      references/
      scripts/
      assets/
```

Only `.codex-plugin/plugin.json` belongs inside `.codex-plugin/`. Bundled
components such as `skills/`, future `.mcp.json`, future `.app.json`, future
`hooks/`, and future `assets/` belong at the plugin root and are referenced
from the manifest with paths relative to this directory.

The repo marketplace is outside this package:

```text
.agents/plugins/marketplace.json
```

The marketplace exposes the checked-in plugin to Codex. It is a catalog entry,
not part of the plugin package itself.

## Install

From the repository root, add the repo marketplace if it is not already
configured:

```bash
codex plugin marketplace add /path/to/Codex-is-all-you-need
```

Then install the plugin:

```bash
codex plugin add codex-next@codex-is-all-you-need
```

After installation, start with:

```text
$codex-next
```

or ask Codex to use Codex Next for the task.

## Local Development

Validate the plugin manifest with:

```bash
python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py \
  plugins/codex-next
```

## License

Codex Next follows the repository license declared in the root `LICENSE` file.
