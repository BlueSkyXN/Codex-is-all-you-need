# Repository Guidelines

[中文](AGENTS_CN.md) | English

## Project Structure & Module Organization

This repository publishes public-safe Codex preset documentation, examples, and a read-only dashboard.

- `README.md` and `README_CN.md`: top-level English and Chinese project introductions.
- `docs/`: architecture, agent design, skill design, migration, and public/private strategy notes.
- `examples/catalog/`: sanitized preset catalog grouped by `common`, `sdlc-manager`, `dev`, `data`, `office`, and `research`; agents live in `agents/*.toml`, skills live in `skills/<skill-name>/SKILL.md`.
- `examples/runtime/` and `examples/suites/`: runtime and suite layout examples.
- `dashboard/`: Python static dashboard generator, HTML template, and example config.

## Build, Test, and Development Commands

- `python3 dashboard/build_dashboard.py --config ~/.codex/dashboard/config.toml`: generate dashboard JSON and HTML using a local config outside the repo.
- `python3 dashboard/build_dashboard.py --config ~/.codex/dashboard/config.toml --json-only`: validate scan output without rendering HTML.
- `open ~/.codex/dashboard/index.html`: preview the generated dashboard locally.

For first-time setup:

```bash
mkdir -p ~/.codex/dashboard
cp dashboard/examples/config.example.toml ~/.codex/dashboard/config.toml
```

Do not commit real runtime configs or generated dashboard output.

## Coding Style & Naming Conventions

Python code should target the current stdlib-first style in `dashboard/build_dashboard.py`: clear functions, type hints where useful, `pathlib.Path` for filesystem work, and short explanatory comments only around non-obvious behavior. Use 4-space indentation for Python. Keep Markdown concise and bilingual only when the surrounding document is already bilingual.

Agent files use snake_case names such as `dev_python_engineer.toml`. Skill directories use kebab-case names such as `python-quality/`, with the entrypoint named `SKILL.md`.

## Testing Guidelines

There is no committed test framework yet. For dashboard changes, run the smallest meaningful smoke check with a local config:

```bash
python3 dashboard/build_dashboard.py --config ~/.codex/dashboard/config.toml --json-only
```

For documentation or catalog changes, inspect links, headings, TOML syntax, and public-safety wording manually. Do not claim coverage unless you add and run actual tests.

## Commit & Pull Request Guidelines

Recent history uses short, imperative, Conventional-style messages, mostly `docs:`; examples include `docs: add public Codex preset catalog` and `docs: split README translations`. Prefer `docs:`, `dashboard:`, or `examples:` scopes when they reflect the changed area.

Pull requests should describe the changed files, why the change is public-safe, and any validation run. Include screenshots only for dashboard UI changes.

## Security & Configuration Tips

Keep private skills, runtime paths, generated scan results, machine-specific symlink state, and real `~/.codex/dashboard/config.toml` values out of the repository. The dashboard is intended to stay read-only; changes should not create, delete, or rewrite `.codex`, `.agents`, suite symlinks, or source catalog files unless explicitly requested.
