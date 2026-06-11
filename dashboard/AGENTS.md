# dashboard navigation card

This directory contains the stdlib Python generator for a read-only Codex preset
dashboard. Read this card before modifying `build_dashboard.py`, templates,
example config, or dashboard docs.
Key files: `build_dashboard.py`, `templates/index.html`,
`examples/config.example.toml`, and `README.md`.

## Local invariants

- The dashboard is read-only with respect to source catalogs, suites, runtime
  folders, `.codex`, `.agents`, agent TOML, and `SKILL.md`.
- Generated dashboard state should normally be written outside this repository,
  for example under `~/.codex/dashboard/`.
- Config examples must use placeholders and public-safe paths only.
- Keep implementation stdlib-first unless a new dependency is explicitly
  justified by the task.

## Local rules

- Preserve the `--json-only` mode for machine-readable validation.
- Keep UI language behavior aligned with `README.md`: generated output supports
  Chinese and English.
- When changing scanner behavior, update status wording consistently across the
  Python code, template, and dashboard docs if that scope is requested.
- Do not make dashboard generation create, delete, or rewrite runtime
  entrypoints.

## Do not

- Do not commit generated `preset-state.json`, generated `index.html`, or a real
  local dashboard config.
- Do not write private roots, internal URLs, or machine-specific absolute paths
  into `examples/config.example.toml`.
- Do not treat dashboard warnings about local production state as proof of this
  public repository's catalog health.

## Validation

- `python3 dashboard/build_dashboard.py --help` - CLI import and argument smoke.
- `python3 dashboard/build_dashboard.py --config ~/.codex/dashboard/config.toml --json-only` - requires a local config and may read local Codex roots/write configured output.
- Use root validation guidance when dashboard changes touch shared docs or
  catalog assumptions.
