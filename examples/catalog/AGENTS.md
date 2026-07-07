# Catalog navigation card

This directory is the sanitized, public-safe source catalog for Codex agents and
skills. Read this card before changing agent TOML, skill folders, group README
files, or publication-boundary docs under `examples/catalog/`.
Key files: `PUBLIC-SUBSET.md`, group `README.md` files, `*/agents/*.toml`,
and `*/skills/*/SKILL.md`.

## Structure

Each group follows the same layout:

```text
<group>/
  agents/*.toml
  skills/<skill-name>/SKILL.md
```

Current groups are `common`, `sdlc-manager`, `dev`, `data`, `office`, and `research`. Agent files use snake_case names such as `dev_python_engineer.toml`. Skill folders use domain-prefixed kebab-case names such as `dev-python-quality/`.

## Local invariants

- This catalog is a reusable public subset, not a dump of private runtime state.
- Keep the architecture-first SDLC control plane centered on `sdlc-manager`;
  direct development fallback belongs in `dev`.
- Production shared-skill visibility is provided by the Codex Next plugin when
  packaged. Custom agent and V1 legacy/local-dev local visibility is decided by
  filesystem placement and suites, not by agent prose alone.

## Agent TOML Rules

- Keep agent roles generic and reusable.
- Use only public-safe `description`, `developer_instructions`, and `nickname_candidates`.
- Do not set model policy fields by default; agents should inherit runtime configuration unless an override is explicitly justified.
- Keep at most one `nickname_candidates` entry.
- Recommended skills must reference public skills in this catalog or generic
  plugin-installed/runtime-visible workflows.

## Skill Rules

- Every skill directory must contain `SKILL.md`.
- Use concise frontmatter with `name` and `description` when present.
- Do not add private scripts, proprietary templates, private examples, or
  symlinks to private skill libraries.
- Keep examples abstract unless they are safe to publish.

## Do not

- Do not publish private absolute paths, internal URLs, credentials, customer
  data, unpublished private skill names, or machine-local suite state.
- Do not copy private symlinked skills into this catalog.
- Do not remove `sdlc-manager` or collapse it back into a generic development
  group without explicitly updating the public architecture docs.

## Validation

After catalog edits, run at least:

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
git diff --check -- examples/catalog
```

If the edited skill is mirrored into `plugins/codex-next/skills/`, also run
`python3 scripts/check_codex_next_surface.py` from the repo root: catalog and
plugin copies must stay content-identical file by file.

For publication boundaries, compare changes with `PUBLIC-SUBSET.md`.

## Public-Safety Boundary

Do not commit private symlinked skills, machine paths, generated dashboard state, local suite state, unpublished private skill names, credentials, or business-specific process details.
