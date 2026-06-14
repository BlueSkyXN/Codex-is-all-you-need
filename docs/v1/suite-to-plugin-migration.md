# V1 To V2 Migration / 从 V1 Suite 迁移到 V2 Plugin

This guide documents the cleanup path from the V1 suite/composition model to
the V2 plugin-first model after Codex Next has replaced machine-local suite
exposure for shared skills.

本文说明在 Codex Next 已经取代本机 suite 暴露共享 skills 后，如何把生产运行态从
V1 suite-first 迁移到 V2 plugin-first。

## Target State / 目标状态

Use this target when shared workflow skills are distributed through an installed
plugin such as `codex-next`.

当共享工作流 skills 已经通过 `codex-next` 这类插件分发时，生产态建议满足：

- Shared workflow skills come from the plugin cache, not from
  `~/.codex/suites/<suite>/skills`.
- Repo-local `.codex/skills` symlinks that point into shared suites are removed.
- Repo-local `.codex/agents` symlinks are removed if custom agent TOML presets
  have also been retired.
- Old suite directories are archived first, then deleted later after a stable
  verification window.
- `.agents/plugins/marketplace.json` is kept when it is the repository
  marketplace entrypoint for the plugin.
- Project-owned `.agents/` or `.codex/` content is not removed just because the
  directory name matches runtime state.

## Keep And Remove / 保留与清理边界

Keep:

- `.agents/plugins/marketplace.json` when it exposes checked-in plugins.
- Installed plugin configuration, for example `codex-next@<marketplace>`.
- Real source catalog files, private or public.
- Project-owned files such as `<repo>/.codex/AGENTS.md` or
  `<repo>/.agents/maintainers.md`.
- User-level skills that are still intentionally configured outside the plugin.

Remove or archive:

- `<repo>/.codex/skills -> <workspace>/.codex/skills` style shared-suite links.
- `<repo>/.codex/agents -> <workspace>/.codex/agents` style custom-agent links
  when custom agent presets are retired.
- Workspace aggregate links such as `<workspace>/.codex/skills` and
  `<workspace>/.codex/agents` when they only expose retired suites.
- `~/.codex/suites/*` after moving it to a timestamped archive.

Do not remove:

- The plugin marketplace file.
- The plugin cache or installed plugin config.
- Source catalog material only because a suite symlink used to point at it.
- Non-empty `.codex` or `.agents` directories with project-owned files.

## Preflight / 迁移前检查

Confirm the plugin is installed and enabled:

```bash
codex plugin list --marketplace <marketplace-name> --available --json
```

Confirm current prompt input still shows suite roots before cleanup:

```bash
codex debug prompt-input 'suite migration preflight' \
  | rg '~/.codex/suites|<workspace>/.codex|codex-next'
```

Inventory active runtime symlinks:

```bash
find <workspace> -maxdepth 3 -type l \
  \( -path '*/.codex/skills' -o -path '*/.codex/agents' \) \
  | sort > /tmp/codex-suite-runtime-links-before.txt
```

Inspect project-owned `.agents` and `.codex` files before deleting anything:

```bash
find <workspace> -maxdepth 3 \
  \( -path '*/.agents/*' -o -path '*/.codex/*' \) \
  -type f -print | sort
```

## Cleanup Procedure / 清理流程

Use an archive rather than direct deletion:

```bash
export CODEX_WORKSPACE="/path/to/workspace"
archive="$HOME/.codex/suite-archives/$(date +%Y%m%d-%H%M%S)-plugin-migration"
export CODEX_SUITE_ARCHIVE="$archive"
mkdir -p "$archive/runtime-symlinks" "$archive/suites"
```

Move repo-local runtime symlinks out of active paths. Preserve enough path shape
to allow rollback:

```bash
python3 - <<'PY'
import os
from pathlib import Path

workspace = Path(os.environ["CODEX_WORKSPACE"])
archive = Path(os.environ["CODEX_SUITE_ARCHIVE"])
runtime_archive = archive / "runtime-symlinks"
runtime_archive.mkdir(parents=True, exist_ok=True)

for repo in [workspace] + sorted(p for p in workspace.iterdir() if p.is_dir()):
    codex_dir = repo / ".codex"
    for name in ("agents", "skills"):
        link = codex_dir / name
        if not link.is_symlink():
            continue
        dest = runtime_archive / repo.relative_to(workspace).as_posix() / ".codex" / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        link.rename(dest)
    if codex_dir.is_dir():
        try:
            codex_dir.rmdir()
        except OSError:
            pass
PY
```

Archive suite directories:

```bash
mkdir -p "$archive/suites"
for suite in "$HOME/.codex/suites"/*; do
  [ -d "$suite" ] || continue
  mv "$suite" "$archive/suites/"
done
rmdir "$HOME/.codex/suites" 2>/dev/null || true
```

If a user-global custom-agent symlink exists and the custom agent preset layer
is retired, archive it too:

```bash
if [ -L "$HOME/.codex/agents" ]; then
  mkdir -p "$archive/runtime-symlinks/dot-codex"
  mv "$HOME/.codex/agents" "$archive/runtime-symlinks/dot-codex/agents"
fi
```

## Validation / 验证

After cleanup, verify suite links are gone:

```bash
find <workspace> -maxdepth 3 -type l \
  \( -path '*/.codex/skills' -o -path '*/.codex/agents' \) \
  | wc -l
```

Verify prompt input no longer includes suite roots:

```bash
codex debug prompt-input 'suite migration validation' \
  | rg '~/.codex/suites|<workspace>/.codex'
```

The command above should return no matches. Then verify plugin skills are still
available:

```bash
codex debug prompt-input 'suite migration validation' \
  | rg 'codex-next:core-router|codex-next:sdlc-manager'
```

Verify the plugin is still enabled:

```bash
codex plugin list --marketplace <marketplace-name> --available --json
```

Inspect remaining `.codex` directories. Anything left should be project-owned
content, not suite exposure:

```bash
find <workspace> -maxdepth 3 -type d -name .codex -print | sort
```

## Rollback / 回滚

Rollback restores the archived runtime symlinks and suite directories.

回滚时把归档的 runtime symlinks 和 suite directories 移回原位。

```bash
archive="$HOME/.codex/suite-archives/<timestamp>-plugin-migration"

mkdir -p "$HOME/.codex/suites"
for suite in "$archive/suites"/*; do
  [ -d "$suite" ] || continue
  mv "$suite" "$HOME/.codex/suites/"
done

find "$archive/runtime-symlinks" -type l | while read -r link; do
  rel="${link#"$archive/runtime-symlinks/"}"
  case "$rel" in
    dot-codex/*)
      dest="$HOME/.codex/${rel#dot-codex/}"
      ;;
    *)
      dest="/path/to/workspace/$rel"
      ;;
  esac
  mkdir -p "$(dirname "$dest")"
  mv "$link" "$dest"
done
```

Run the preflight checks again after rollback.

## Documentation Updates / 文档更新

After a production migration, update public docs to make the active model clear:

- Plugin-first production: installed plugin is the shared workflow surface.
- V1 suites: legacy or local-development composition layer.
- Runtime `.codex/agents` and `.codex/skills`: only for project-specific
  needs, selective experiments, or legacy compatibility.
- `.agents/plugins/marketplace.json`: plugin marketplace source, not obsolete
  runtime state.
