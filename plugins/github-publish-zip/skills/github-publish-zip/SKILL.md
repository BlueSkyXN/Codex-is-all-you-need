---
name: github-publish-zip
description: Create a ZIP archive from the files in a Git worktree that would be publishable to GitHub, using configurable compression backend priority. Use when the user asks to package, archive, zip, or prepare a repository for GitHub publication while respecting project and user ignore rules, excluding .git metadata, and writing the archive to the project's local directory.
metadata:
  version: "0.1"
  updated: "2026-06-21"
---

# GitHub Publish Zip

## Workflow

Use `scripts/pack_github_publish_zip.py` from this skill. Prefer passing the target project path explicitly:

```bash
python3 /path/to/github-publish-zip/scripts/pack_github_publish_zip.py /path/to/project
```

Run a dry run first when the target repository is large or the user asks to inspect scope:

```bash
python3 /path/to/github-publish-zip/scripts/pack_github_publish_zip.py /path/to/project --dry-run --list-files
```

The script:

- Finds the Git top-level directory from the supplied path or current directory.
- Builds the file list with `git ls-files --cached --others --exclude-standard --deduplicate`.
- Uses the working tree contents, including tracked modifications and untracked files that are not ignored.
- Respects `.gitignore`, `.git/info/exclude`, and user/global Git ignore rules.
- Excludes `.git` metadata, the output archive, and the configured output directory contents.
- Creates the project `local/` directory when needed.
- Writes `<project-name>-YYYYMMDD-hhmm.zip` under `local/`.
- Uses compression backend priority and reports the actual backend used.

## Compression Priority

Default priority is:

```text
zip,7z,python
```

This means: use system `zip -9` first, then system `7z`, then Python `zipfile` as the last fallback.

For maximum compression preference, use:

```bash
python3 /path/to/github-publish-zip/scripts/pack_github_publish_zip.py /path/to/project --max-compression
```

`--max-compression` changes the default priority to:

```text
7z,zip,python
```

To make the priority explicit, pass:

```bash
python3 /path/to/github-publish-zip/scripts/pack_github_publish_zip.py /path/to/project --backend-priority 7z,zip,python
```

## Boundary Rules

Do not use `git archive` for this workflow; it does not include untracked publishable files or unstaged working tree content. Do not manually glob the filesystem because that bypasses Git ignore rules.

Do not silently hide backend fallback. The script must report the selected backend and any unavailable higher-priority backends in normal or JSON output.

If the minute-based archive already exists, the script stops by default. Use `--force` only when the user accepts overwriting that local archive.

## Verification

After creating an archive, report the archive path, included file count, and selected backend from the script output. Inspect archive contents before calling it done, using whichever tool is available:

```bash
unzip -l /path/to/project/local/project-YYYYMMDD-hhmm.zip
# or
7z l /path/to/project/local/project-YYYYMMDD-hhmm.zip
```

Confirm that no path starts with `.git/`. If the dry run or creation reports skipped missing tracked files, mention that the worktree has tracked paths missing on disk.
