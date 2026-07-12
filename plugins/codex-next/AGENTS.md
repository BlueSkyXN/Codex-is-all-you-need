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
  `plugins/codex-next/skills/<skill>/` content-identical unless the skill is
  explicitly plugin-only; `scripts/check_codex_next_surface.py` enforces this
  file-by-file. The current plugin-only allowlist is `core-router`; document
  and validate any future addition.
- Keep bundled skill names stable and domain-prefixed where applicable.
- Preserve relative manifest paths; plugin manifest paths are resolved from
  `plugins/codex-next/`.
- Keep README install instructions consistent with the repo marketplace path and
  root migration docs.

## Skill authoring discipline

Write skills as operational controls, not essays. The goal is repeatable agent
process: the next run should follow the same useful path even if the wording of
the user's task differs.

- Spec alignment: skill frontmatter uses Agent Skills spec fields only (`name`,
  `description`, `license`, `compatibility`, `metadata`, `allowed-tools`) plus
  the allowlisted runtime extension `disable-model-invocation`. Spec `name` and
  `description` constraints, unknown-field rejection, and the 500-line SKILL.md
  budget are enforced by `scripts/check_codex_next_surface.py`.
- Cross-skill references: a skill may point at a sibling skill's reference file
  (for example the shared SDLC operating model) with a `../<skill>/...` path.
  Every such path must resolve in both the plugin package and the source
  catalog bucket; the surface checker fails on dangling parent-path references
  and dangling relative links.
- Invocation: keep a skill model-invoked only when Codex should discover it
  without the user naming it, or when another skill routes to it. Expensive or
  human-started workflows need an explicit reason to be always visible.
- Information hierarchy: keep the next required action in `SKILL.md`, move
  conditional detail into `references/`, and place repeatable fragile operations
  in `scripts/`.
- Completion criteria: give stages observable finish lines. "Run one command
  that can catch this bug" is useful; "be thorough" is not.
- Behavior anchors: use compact terms such as `tight`, `red`, `seam`,
  `load-bearing`, or `vertical slice` only when they change what the agent does.
  If a word does not change behavior, replace the rule rather than padding it.
- Ordered workflows: order controls presentation, not disclosure. If a fact
  affects a decision the user is making now, disclose it now and then file it in
  the appropriate stage.
- Self-check: before shipping a substantial skill edit, sweep for the same
  defect taxonomy `core-skill-eval` judges against — premature completion,
  vague done condition, missing rule, weak trigger, no-op instruction,
  duplication, sediment, sprawl, and missing reference split — plus
  implementation breadcrumbs that will rot and bug-story narration that should
  be a durable principle instead.
- Behavior eval: static checks only verify package shape. For major behavior
  rewrites, prefer `core-skill-eval` with representative cases, isolated runs,
  and independent judging when practical.

## Do not

- Do not add `.codex/agents`, suite symlinks, machine-local runtime state, or
  private source material to this package.
- Do not treat plugin installation as proof that custom agents are installed.

## Validation

- `python3 scripts/check_codex_next_surface.py` (from the repo root) - hard gate
  for catalog/plugin content parity, manifest version parity, Agent Skills spec
  frontmatter, and reference resolution.
- `python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/codex-next` - plugin manifest/package validation; requires the local system validator path.
- `claude plugin validate --strict plugins/codex-next` - validate the Claude
  compatibility manifest and its default root-level component discovery when
  the Claude CLI is available.
- `git diff --check -- plugins/codex-next` - whitespace check for plugin package diffs.
- For bundled skill content mirrored from `examples/catalog/`, also run the root
  catalog validation command when the source catalog changed.
