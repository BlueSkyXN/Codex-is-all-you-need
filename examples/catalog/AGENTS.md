# Catalog Guidelines

[中文](AGENTS_CN.md) | English

These instructions apply to `examples/catalog/` and all nested catalog groups.

## Purpose

This directory is a sanitized, public-safe source catalog derived from a private Codex preset catalog. Keep it generic, reusable, and free of machine-specific or business-private details.

## Structure

Each group follows the same layout:

```text
<group>/
  agents/*.toml
  skills/<skill-name>/SKILL.md
```

Current groups are `common`, `sdlc-manager`, `dev`, `data`, `office`, and `research`. Agent files use snake_case names such as `dev_python_engineer.toml`. Skill folders use kebab-case names such as `python-quality/`.

## Agent TOML Rules

- Keep agent roles generic and reusable.
- Use only public-safe `description`, `developer_instructions`, and `nickname_candidates`.
- Do not set model policy fields by default; agents should inherit runtime configuration unless an override is explicitly justified.
- Keep at most one `nickname_candidates` entry.
- Recommended skills must reference public skills in this catalog or generic runtime-visible workflows.

## Skill Rules

- Every skill directory must contain `SKILL.md`.
- Use concise frontmatter with `name` and `description` when present.
- Do not add private scripts, proprietary templates, private examples, or symlinks to private skill libraries.
- Keep examples abstract unless they are safe to publish.

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

For publication boundaries, compare changes with `PUBLIC-SUBSET.md`.

## Public-Safety Boundary

Do not commit private symlinked skills, machine paths, generated dashboard state, local suite state, unpublished private skill names, credentials, or business-specific process details.
