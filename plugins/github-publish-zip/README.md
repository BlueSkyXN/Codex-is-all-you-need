# GitHub Publish Zip

GitHub Publish Zip is an installable Codex plugin for packaging a Git worktree
into a local ZIP archive using the files that would be publishable to GitHub.

It respects Git ignore rules, excludes `.git` metadata, excludes the configured
output directory, and writes archives to `local/<project-name>-YYYYMMDD-hhmm.zip`.

## Included Skill

- `github-publish-zip`: create a GitHub-publishable ZIP archive from a Git
  worktree with configurable compression backend priority.

## Compression Priority

Default backend priority is:

```text
zip,7z,python
```

Use `--max-compression` to prefer:

```text
7z,zip,python
```

The script reports the selected backend and unavailable higher-priority
backends instead of silently hiding fallback.

## Install

This plugin is published through the repository marketplace:

```bash
codex plugin marketplace add /path/to/Codex-is-all-you-need
codex plugin add github-publish-zip@codex-is-all-you-need
```

After installation, invoke:

```text
$github-publish-zip:github-publish-zip
```

## Validate

From the repository root:

```bash
python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py \
  plugins/github-publish-zip
```
