# AGENTS.md Builder

AGENTS.md Builder designs and maintains repository instruction hierarchies shared
by Codex and Claude Code. It provides one skill, `agents-md-builder`, for root
routing files, directory cards, validation commands, and client-specific imports.

## Scope

- Design, create, audit, or restructure an AGENTS.md hierarchy.
- Check which instruction files each client loads, including ancestor files,
  overrides, and Claude Code project-instruction settings.
- Keep shared rules in AGENTS.md and configure existing or necessary Claude
  entry files to import them.
- Preserve human-maintained rules and report changes requiring a separate decision.

The workflow edits instruction files within the requested scope. Client settings,
application code, and personal CLAUDE.local.md files remain separate decisions.
Other clients require verification against their own loading rules.

## Install

For Codex:

```bash
codex plugin marketplace add https://github.com/BlueSkyXN/Codex-is-all-you-need.git
codex plugin add agents-md-builder@codex-is-all-you-need
```

For Claude Code:

```bash
claude plugin marketplace add BlueSkyXN/Codex-is-all-you-need
claude plugin install agents-md-builder@codex-is-all-you-need
```

For local development, use this repository's checked-out root as the marketplace
source. If an existing marketplace uses sparse checkout, include
`plugins/agents-md-builder` before refreshing it.

Invoke the skill with:

```text
$agents-md-builder:agents-md-builder   # Codex
/agents-md-builder:agents-md-builder   # Claude Code
```

It is also available for matching requests such as designing an AGENTS.md
hierarchy or arranging AGENTS.md and CLAUDE.md to work together.

## Migration from Codex Next

Codex Next 0.6.0 moves the former `core-codex-agents-md-builder` skill into this
standalone plugin. Refresh the marketplace, install `agents-md-builder`, and
update explicit invocations to the commands above. Existing repository instruction
files are maintained in place when you request work on them.

## Package and validation

The package version is `0.1.0`; the skill has its own public lifecycle version
`0.1`. The canonical skill source is `skills/agents-md-builder/` in this package.

From the repository root:

```bash
python3 scripts/check_skill_metadata.py check --base-ref origin/main
claude plugin validate --strict plugins/agents-md-builder
```

These checks validate metadata and packaging. Verify instruction loading in the
target client session using the methods in
[loading-model.md](skills/agents-md-builder/references/loading-model.md).

## License

GPL-3.0-only; see [LICENSE](LICENSE).
