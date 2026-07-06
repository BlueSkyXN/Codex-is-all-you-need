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

## Skill authoring discipline

Optimize skills for predictable process, not verbose advice.

- Invocation: keep a skill model-invoked only when Codex must automatically
  reach it or another skill must compose with it. Human-started, expensive, or
  side-effect-heavy workflows should first prove their runtime invocation
  semantics before using user-invoked frontmatter or moving in/out of `skills/`.
- Information hierarchy: put load-bearing steps in `SKILL.md`, short lookup
  material in `references/`, and deterministic repeat work in `scripts/`.
  Avoid copying large reference content into the main skill body.
- Completion criteria: prefer checkboxes for gates that must be satisfied before
  moving on. "Summarize the work" is not a gate; "one red-capable command has
  been run" is.
- Leading words: use compact behavior anchors such as `tight`, `red`, `seam`,
  `load-bearing`, `vertical slice`, and `deepening` when they carry real process
  weight. A leading word too weak to beat the model's default is a no-op; the
  fix is a stronger word, not more sentences.
- Embargo escape valve: ordered workflows must never withhold information. A
  finding that bears on a decision in flight is disclosed immediately, then filed
  at its proper stage.
- Failure-mode self-check: before shipping a substantial skill edit, look for
  premature completion, duplicated rules, sediment, sprawl, no-op `Do not`
  bullets, implementation indexes (file paths and line numbers that rot), and
  war stories (play-by-play of one bug's trajectory instead of the transferable
  principle).
- Behavior eval: static validation only proves shape. For major new or rewritten
  skills, use `core-skill-eval` with golden cases, blind runs, and a separate
  judge when practical.

## Do not

- Do not add `.codex/agents`, suite symlinks, machine-local runtime state, or
  private source material to this package.
- Do not treat plugin installation as proof that custom agents are installed.

## Validation

- `python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/codex-next` - plugin manifest/package validation; requires the local system validator path.
- `git diff --check -- plugins/codex-next` - whitespace check for plugin package diffs.
- For bundled skill content mirrored from `examples/catalog/`, also run the root
  catalog validation command when the source catalog changed.
