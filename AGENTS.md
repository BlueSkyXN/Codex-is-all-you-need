# Repository agent instructions

## Purpose

This repository publishes a public-safe Codex preset system: sanitized agent and
skill catalog examples, an installable Codex Next plugin, architecture and
migration documentation, a read-only dashboard generator, and legacy/local-dev
scripts for managing repo-local Codex runtime entrypoints.

The V2 production storyline is "source catalog -> plugin package ->
marketplace install". Local suites and repo-local `.codex` entrypoint symlinks
are V1 legacy or local-development compatibility paths. Keep changes aligned
with that plugin-first model and with the architecture-first SDLC catalog shape.

## Codex startup behavior

- Codex is normally started from the repository root, so this file is the
  startup router for repo-local instructions.
- Subdirectory `AGENTS.md` files are on-demand navigation cards. They are not
  guaranteed to be in the startup context when Codex starts from the root.
- Before editing under any directory whose row below says `Yes`, read that
  directory's `AGENTS.md` with `cat <path>/AGENTS.md`.
- If multiple nested `AGENTS.md` files apply, read them from shallow to deep
  before making changes.
- If started from a subdirectory, Codex may automatically load the nearest
  path-chain `AGENTS.md`; still use this root file as the directory router.
- `AGENTS_CN.md` files are human-facing translation/reference files. Codex does
  not treat them as project instruction files unless the user explicitly asks
  to read or update them.

## Directory map

| Path | Responsibility | Local AGENTS.md | Read when |
|---|---|---:|---|
| `README.md`, `README_CN.md` | Top-level English and Chinese project introductions | No | Keep them aligned with public catalog structure when editing user-facing docs |
| `AGENTS.md` | Root startup router for Codex agents | This file | Any repository task from the root |
| `AGENTS_CN.md` | Chinese reference for repository guidelines, not a Codex-loaded instruction file | No | Only when the user asks to sync Chinese guidance |
| `docs/` | Architecture, usage, discovery, migration, public/private, and model catalog documentation | No | Read the specific doc being changed and adjacent docs that reference the same public model |
| `dashboard/` | Stdlib Python read-only dashboard generator, HTML template, and example config | Yes | Before editing `build_dashboard.py`, dashboard templates, config examples, or dashboard docs |
| `scripts/` | Legacy/local-dev filesystem automation for repo-local `.codex` entrypoint symlinks, plus the read-only Codex Next surface checker | Yes | Before editing symlink management behavior, CLI flags, cleanup logic, surface-check gates, or related tests |
| `tests/` | Unit tests for repository scripts | No | Follow `scripts/AGENTS.md` when changing tests for `scripts/` behavior |
| `examples/catalog/` | Sanitized public agent and skill source catalog | Yes | Before changing agent TOML, skill folders, catalog group docs, or publication boundaries |
| `examples/runtime/` | Public-safe example runtime `AGENTS.md` instructions | Yes | Before changing runtime instruction examples |
| `examples/suites/` | V1 legacy/local-dev suite symlink pattern notes and examples | No | Read `examples/suites/README.md` before changing suite documentation |
| `plugins/` | Installable Codex plugin package parent directory | No | Read the specific plugin card when a plugin package has one |
| `plugins/codex-next/` | Canonical packaged Codex Next plugin built from public-safe skills | Yes | Before changing the plugin manifest, README, bundled skills, package layout, or validation guidance |
| `.agents/plugins/marketplace.json` | Repo marketplace that exposes checked-in plugins | No | Before changing plugin availability or marketplace metadata |
| `.codex/` | Machine-local runtime entrypoint symlinks or project-owned local state | No | Do not edit unless the task explicitly targets runtime entrypoints and the user accepts local filesystem changes |

## On-demand cat protocol

Before editing files under a directory with a local `AGENTS.md`:

1. Run `cat <path>/AGENTS.md` for the nearest listed directory.
2. Follow any stricter local rules in that file.
3. If the target spans multiple listed directories, read each relevant card
   before editing.
4. If a target directory ever contains `AGENTS.override.md`, stop and ask the
   user how to handle the override; do not add or update an ignored plain
   `AGENTS.md` in the same directory.

## Commands

This repository has no committed package manager config, Makefile, or CI
workflow. Confirmed commands come from the checked-in Python scripts, tests, and
repository docs.

| Command | Purpose | Scope | Sandbox notes |
|---|---|---|---|
| `python3 -m unittest discover -s tests -v` | Run committed unit tests for the `scripts/` tools | repo | OK; uses temporary directories |
| `python3 dashboard/build_dashboard.py --help` | Validate dashboard CLI loads | `dashboard/` | OK |
| `python3 dashboard/build_dashboard.py --config ~/.codex/dashboard/config.toml --json-only` | Generate dashboard state without rendering HTML | `dashboard/` plus configured local paths | Requires local config outside repo; may read local Codex roots and write configured output, normally outside repo |
| `python3 dashboard/build_dashboard.py --config ~/.codex/dashboard/config.toml` | Generate dashboard JSON and HTML | `dashboard/` plus configured local paths | Requires local config; output must stay outside the public repository unless explicitly configured for a local experiment |
| `open ~/.codex/dashboard/index.html` | Preview generated dashboard | local machine | macOS GUI command; not a sandbox validation step |
| `python3 scripts/sync_codex_entrypoints.py --help` | Validate entrypoint sync CLI loads | `scripts/` | OK |
| `python3 scripts/check_codex_next_surface.py` | Validate the packaged Codex Next skill surface: catalog/plugin content parity, manifest version parity, Agent Skills frontmatter gates, and reference resolution | `plugins/codex-next/`, `examples/catalog/` | OK; read-only, exits 1 on gate failure |
| `python3 scripts/sync_codex_entrypoints.py sync --workspace <workspace> --source-root <workspace>/.codex --link-mode directories` | Dry-run legacy/local-dev repo-local `.codex` directory link sync | local workspace | Replace placeholders before running; dry-run by default; reads local workspace paths; do not add `--apply` without explicit user request |
| `python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/codex-next` | Validate the Codex Next plugin manifest and package shape | `plugins/codex-next/` | Requires the local system `plugin-creator` validator path; if unavailable, state that it was skipped |
| `git diff --check` | Check whitespace in the current diff | repo | OK; read-only |
| `git status --short --branch` | Inspect current working tree | repo | OK; read-only |

Catalog validation command:

```bash
python3 - <<'PY'
from pathlib import Path
import tomllib

root = Path("examples/catalog")
for path in root.glob("*/agents/*.toml"):
    tomllib.loads(path.read_text())
for path in root.glob("*/skills/*"):
    if path.name.startswith("."):
        continue
    if not (path / "SKILL.md").is_file():
        raise SystemExit(f"missing SKILL.md: {path}")
print("catalog structure ok")
PY
```

Use `git diff --check -- examples/catalog` after catalog edits.

## Global rules

- Keep this repository public-safe. Do not add private absolute paths, internal
  URLs, credentials, `.env` values, customer data, private template content, or
  unpublished private skill names.
- Prefer placeholders such as `~/.codex`, `<workspace>`, `<repo>`, and
  `/path/to/...` in public docs and examples.
- Preserve the separation between source catalog, plugin package, marketplace,
  V1 local suites, and runtime `.codex` entrypoints. Do not imply that suite
  symlinks are the production default after Codex Next is installed, and do not
  imply that Codex automatically inherits a parent `.codex` directory across
  child git repositories.
- Keep `dashboard/` read-only with respect to source catalogs, suites, runtime
  folders, `.codex`, `.agents`, agent TOML, and `SKILL.md` files.
- Keep `scripts/sync_codex_entrypoints.py` conservative: dry-run by default,
  explicit link mode, no replacement of real local content, and no deletion of
  non-managed files.
- Python changes should stay stdlib-first unless a long-term dependency is
  explicitly justified. Use `pathlib.Path` for filesystem work and type hints
  where they clarify behavior.
- Markdown should be concise. Keep bilingual content only where the surrounding
  document is already bilingual or the file is explicitly a bilingual reference.
- Agent TOML files use snake_case names such as `dev_python_engineer.toml`.
  Skill directories use domain-prefixed kebab-case names such as
  `dev-python-quality/`, with the entrypoint named `SKILL.md`.
- For public catalog refreshes, verify current filesystem counts instead of
  copying older numbers from memory or docs.
- Treat `plugins/codex-next` as the canonical packaged surface for
  public-safe distributable skills. When a public catalog skill is updated for
  distribution, keep `examples/catalog/.../skills/<skill>/` and
  `plugins/codex-next/skills/<skill>/` aligned unless the skill is explicitly
  plugin-only, such as the `core-router` router entrypoint.
- Treat existing non-AGENTS working tree changes as user work unless the user
  asks to modify them.

## Do not

- Do not commit real runtime configs, generated dashboard output, machine-local
  symlink state, `.codex/config.toml`, private suite state, or private catalog
  material.
- Do not treat the checked-in repo marketplace at `.agents/plugins/marketplace.json`
  as machine-local runtime state.
- Do not create, delete, or rewrite `.codex`, `.agents`, suite symlinks, runtime
  entrypoints, or source catalog files unless the user explicitly requested that
  filesystem operation.
- Do not run `scripts/sync_codex_entrypoints.py` with `--apply`, `clean`,
  `--prune`, `--remove-ignore`, or `--remove-empty-dirs` against a real
  workspace unless the user explicitly asked for that operation and the target
  paths were inspected first.
- Do not publish private model policy overrides in public agent TOML. Public
  examples should inherit runtime configuration unless an override is explicitly
  documented and safe.
- Do not add private scripts, proprietary templates, private examples, or
  symlinks to private skill libraries under `examples/catalog/`.
- Do not claim test, dashboard, or catalog validation passed unless the command
  was actually run in this turn.
- Do not update `AGENTS_CN.md` or other translation/reference files just because
  `AGENTS.md` changed; translate only when the user requests that scope.

## Validation

Choose the smallest validation that matches the files changed:

1. Any Python script behavior change:
   `python3 -m unittest discover -s tests -v`
2. Dashboard code, template, or config example change:
   `python3 dashboard/build_dashboard.py --help`, then run the JSON-only
   dashboard command if a valid local config is available and safe to use.
3. Catalog agent or skill change:
   run the catalog validation snippet above and
   `git diff --check -- examples/catalog`; if the changed skill is mirrored
   into the Codex Next plugin, also run
   `python3 scripts/check_codex_next_surface.py`.
4. `plugins/codex-next/` plugin manifest, package layout, or bundled skill
   change:
   run `python3 scripts/check_codex_next_surface.py`, then the plugin validator
   if the local system validator is available:
   `python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/codex-next`
   and run `git diff --check -- plugins/codex-next`.
5. `scripts/sync_codex_entrypoints.py` change:
   `python3 -m unittest discover -s tests -v` and
   `python3 scripts/sync_codex_entrypoints.py --help`.
6. Documentation-only change:
   inspect affected links/headings and run `git diff --check` for the touched
   paths.
7. AGENTS-only change:
   confirm `find . -name AGENTS.override.md` is empty or does not affect the
   target, check file sizes, and run `git diff --check` with the actual touched
   `AGENTS.md` paths.

When a validation command depends on local config, GUI access, or external
filesystem state, state whether it was skipped or run and why.

## Notes for future agents

- The public catalog currently uses groups `common`, `sdlc-manager`, `dev`,
  `data`, `office`, and `research`. Verify counts from the filesystem before
  reporting them.
- `examples/catalog/common/skills/core-codex-agents-md-builder/` is the public copy
  of the AGENTS design workflow. When editing it, keep the skill body and
  references self-contained and public-safe.
- Production use should prefer the checked-in Codex Next plugin and marketplace
  path. Local `.codex/agents` and `.codex/skills` symlinks may still appear for
  legacy or local-development experiments; they are local state, not public
  source.
