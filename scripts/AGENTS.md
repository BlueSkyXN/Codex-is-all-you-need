# scripts navigation card

This directory contains legacy/local-development filesystem automation for
managing repo-local Codex runtime entrypoint symlinks. Production shared skills
should come from the installed plugin. Read this card before changing CLI flags,
sync or clean behavior, conflict handling, ignore-file behavior, or tests for
the sync script.
Key files: `sync_codex_entrypoints.py` and
`../tests/test_sync_codex_entrypoints.py`.

## Why this is high-risk

- The sync script can create, update, prune, or remove `.codex/agents` and
  `.codex/skills` symlinks across many local repositories when `--apply` is
  used.
- The script can edit each target repository's local `.git/info/exclude`.
- Mistakes can affect a user's runtime Codex visibility even though they are not
  committed to Git.

## Required before changes

- Read the script and the unit tests before editing behavior.
- Confirm whether the requested change affects dry-run output, `--apply`,
  `sync`, `clean`, `directories`, `entries`, `--prune`, or ignore management.
- Prefer temp-directory tests for filesystem behavior; do not rely on live
  workspace mutation for validation.

## Do not

- Do not run the script against a real workspace with `--apply`, `clean`,
  `--prune`, `--remove-ignore`, or `--remove-empty-dirs` unless the user
  explicitly requested that operation.
- Do not replace real `.codex/agents` or `.codex/skills` directories that
  contain local content.
- Do not delete files or directories that are not managed symlinks pointing into
  the selected `--source-root`.
- Do not change the default from dry-run to apply.

## Validation

- `python3 -m unittest discover -s tests -v` - exercises sync behavior in
  temporary directories.
- `python3 scripts/sync_codex_entrypoints.py --help` - CLI argument smoke.
- Real-workspace dry runs may be useful for inspection, but they read local
  paths and should not be treated as required sandbox validation.
