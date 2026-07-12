# Codex Next

Codex Next is an installable Codex plugin that packages the public-safe skills
from this repository into one reusable workflow bundle.

It is meant to strengthen Codex with repeatable software delivery workflows:
task routing, project research, requirements, architecture, specs, validation,
handoff, implementation support, review, data work, office writing, and research
synthesis.

## What It Includes

- A plugin entrypoint skill, `core-router`, for routing work to the smallest
  useful bundled workflow, now with a flow map for direct-dev, PR delivery,
  SDLC, bugfix, context, and skill-quality paths.
- Core process skills from the common catalog: `core-grilling` for
  one-question-at-a-time plan interrogation, `core-explore-unknowns` for
  quadrant-walk requirement clarification when the user's request is ambiguous,
  `core-skill-eval` for golden-case skill behavior checks, and `core-goal-run`
  which tracks task-specific anchor state and uses it, with one safe-unit
  exception for legacy `DOING` or `VERIFYING` rows, to govern automatic
  continuation.
- SDLC and delivery skills such as `sdlc-manager`, `sdlc-router`,
  `sdlc-requirements-workflow`, `sdlc-solution-spec-workflow`,
  `sdlc-dev-handoff-planning`, and `sdlc-readiness-review`.
  `sdlc-readiness-review` checks source authority before necessity and separates
  missing justification, unnecessary work, scope reduction, and baseline
  change.
- Development skills such as `dev-repo-onboarding`, `dev-bugfix`,
  `dev-spec-driven-implementation`, `dev-git-workflow`, `dev-pr-review`,
  `dev-security-review`, `dev-test-strategy`, and `dev-release-check`.
  `dev-git-workflow` prepares reviewer-facing PR metadata and verifies remote
  review and merge gates; `dev-bugfix` requires a tight red-capable loop before
  root-cause work; `dev-pr-review` reports simplification findings for
  over-engineered diffs without treating repository-required artifacts as
  overhead.
- Data, office, research, and common workflow skills from the public catalog.

## What It Does Not Include

- Custom agent TOML files from `.codex/agents`.
- V1 machine-local suite symlinks or runtime `.codex` entrypoints.
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
components such as `skills/`, future `.mcp.json`, future `.app.json`, and
future `assets/` belong at the plugin root and are referenced from the manifest
with paths relative to this directory.

The package also carries `.claude-plugin/plugin.json` as compatibility metadata
for Claude-compatible runtimes. It mirrors the Codex manifest version. The
Claude compatibility manifest is not the Codex runtime contract: `codex plugin
add` installs against the Codex manifest and this package layout. Claude runtime
skill semantics are tracked separately and stay a checker warning, not a
release gate.

The repo marketplace is outside this package:

```text
.agents/plugins/marketplace.json
```

The marketplace exposes the checked-in plugin to Codex. It is a catalog entry,
not part of the plugin package itself.

## Install

For a network install from GitHub, add the marketplace source:

```bash
codex plugin marketplace add https://github.com/BlueSkyXN/Codex-is-all-you-need.git
```

For local development, add the checked-out repository root instead:

```bash
codex plugin marketplace add /path/to/Codex-is-all-you-need
```

Check that Codex can see the uninstalled marketplace entry. The `--available`
flag is required when using JSON output; without it, `codex plugin list --json`
only shows installed plugins.

```bash
codex plugin marketplace list --json
codex plugin list --marketplace codex-is-all-you-need --available --json
```

Then install the plugin from the configured marketplace:

```bash
codex plugin add codex-next@codex-is-all-you-need
```

After installation, start with:

```text
$codex-next:core-router
```

or ask Codex to use Codex Next for the task.

If you are migrating an existing V1 machine from suite-based runtime
entrypoints, see
[V1 To V2 Migration](../../docs/v1/suite-to-plugin-migration.md).

## Local Development

Validate the plugin manifest with:

```bash
python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py \
  plugins/codex-next
```

Check the packaged skill surface with:

```bash
python3 scripts/check_codex_next_surface.py
```

## License

Codex Next follows the repository license declared in the root `LICENSE` file.
