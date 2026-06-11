# Codex Next plugin navigation card

This directory is the canonical installable Codex Next plugin package. Read this
card before changing the plugin manifest, README, bundled skills, or package
layout.
Key files: `.codex-plugin/plugin.json`, `README.md`, and `skills/*/SKILL.md`.

## Local invariants

- `.codex-plugin/plugin.json` is the package manifest. Bundled components
  belong at the plugin root, not under `.codex-plugin/`.
- `skills/` is the packaged public-safe skill surface. It does not package
  custom agent TOML, suite symlinks, runtime `.codex` entrypoints, private
  prompts, private paths, credentials, or unpublished skills.
- The repo marketplace lives outside this package at
  `.agents/plugins/marketplace.json`. Do not move it into this directory.
- Keep this package aligned with `source catalog -> plugin package ->
  marketplace install`.

## Local rules

- When updating a public catalog skill that is distributed through Codex Next,
  keep `examples/catalog/.../skills/<skill>/` and
  `plugins/codex-next/skills/<skill>/` aligned unless the skill is explicitly
  plugin-only, such as `core-router`.
- Keep bundled skill names stable and domain-prefixed where applicable.
- Preserve relative manifest paths; plugin manifest paths are resolved from
  `plugins/codex-next/`.
- Keep README install instructions consistent with the repo marketplace path and
  root migration docs.

## Do not

- Do not add `.codex/agents`, suite symlinks, machine-local runtime state, or
  private source material to this package.
- Do not treat plugin installation as proof that custom agents are installed.

## Validation

- `python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/codex-next` - plugin manifest/package validation; requires the local system validator path.
- `git diff --check -- plugins/codex-next` - whitespace check for plugin package diffs.
- For bundled skill content mirrored from `examples/catalog/`, also run the root
  catalog validation command when the source catalog changed.
