#!/usr/bin/env python3
"""Manage repo-local Codex entrypoint symlinks from an aggregated `.codex`.

Choose `--link-mode directories` to link runtime entrypoint directories:
`.codex/agents -> <source-root>/agents` and
`.codex/skills -> <source-root>/skills`. Prefer this for workspace aggregates
such as `/Users/sky/GitHub/.codex`.

Choose `--link-mode entries` when a repo must keep real `.codex/agents` or
`.codex/skills` directories and expose each shared agent or skill one by one.
The script never links the whole `.codex` directory, so repo-local
`.codex/config.toml` can stay private to the runtime.
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_WORKSPACE = Path("/Users/sky/GitHub")
IGNORE_LINES = (".codex/", ".agents/")
IGNORE_HEADER = "# Codex local entrypoint symlinks"


@dataclass(frozen=True)
class Entry:
    kind: str
    name: str
    source: Path
    target_rel: Path


@dataclass(frozen=True)
class DirectoryLink:
    kind: str
    source: Path
    target_rel: Path


@dataclass
class Counters:
    created: int = 0
    updated: int = 0
    unchanged: int = 0
    conflicts: int = 0
    pruned: int = 0
    removed: int = 0
    ignored: int = 0
    skipped: int = 0


def abs_lexical(path: Path) -> Path:
    """Return an absolute path without resolving symlink hops."""

    return Path(os.path.abspath(os.fspath(path)))


def symlink_target_abs(link: Path) -> Path:
    raw_target = Path(os.readlink(link))
    if raw_target.is_absolute():
        return abs_lexical(raw_target)
    return abs_lexical(link.parent / raw_target)


def same_symlink_target(link: Path, desired: Path) -> bool:
    return symlink_target_abs(link) == abs_lexical(desired)


def path_is_relative_to(path: Path, parent: Path) -> bool:
    try:
        abs_lexical(path).relative_to(abs_lexical(parent))
    except ValueError:
        return False
    return True


def symlink_ancestor(repo: Path, rel_path: Path) -> Path | None:
    current = repo
    for part in rel_path.parts:
        current = current / part
        if current.is_symlink():
            return current
    return None


def is_repo(path: Path) -> bool:
    return (path / ".git").exists()


def discover_repos(workspace: Path, recursive: bool) -> list[Path]:
    if not recursive:
        return sorted(
            child
            for child in workspace.iterdir()
            if child.is_dir() and not child.name.startswith(".") and is_repo(child)
        )

    repos: list[Path] = []
    for root, dirs, _files in os.walk(workspace):
        root_path = Path(root)
        if ".git" in dirs or (root_path / ".git").is_file():
            repos.append(root_path)
            dirs[:] = []
            continue
        dirs[:] = [d for d in dirs if not d.startswith(".")]
    return sorted(repos)


def match_patterns(repo: Path, workspace: Path, patterns: list[str]) -> bool:
    if not patterns:
        return True
    rel = os.fspath(repo.relative_to(workspace)) if repo.is_relative_to(workspace) else os.fspath(repo)
    return any(
        fnmatch.fnmatch(repo.name, pattern) or fnmatch.fnmatch(rel, pattern) or fnmatch.fnmatch(os.fspath(repo), pattern)
        for pattern in patterns
    )


def select_repos(args: argparse.Namespace) -> list[Path]:
    workspace = args.workspace
    if args.repo:
        repos = []
        for raw in args.repo:
            candidate = Path(raw).expanduser()
            if not candidate.is_absolute():
                candidate = workspace / candidate
            repos.append(candidate)
    else:
        repos = discover_repos(workspace, args.recursive)

    selected: list[Path] = []
    for repo in repos:
        repo = abs_lexical(repo)
        if not is_repo(repo):
            print(f"SKIP repo without .git: {repo}")
            continue
        if not match_patterns(repo, workspace, args.include):
            continue
        if args.exclude and match_patterns(repo, workspace, args.exclude):
            continue
        selected.append(repo)
    return sorted(dict.fromkeys(selected))


def collect_entries(source_root: Path) -> tuple[list[Entry], list[str]]:
    warnings: list[str] = []
    entries: list[Entry] = []
    agents_dir = source_root / "agents"
    skills_dir = source_root / "skills"

    if agents_dir.is_dir():
        for item in sorted(agents_dir.iterdir()):
            if item.name.startswith("."):
                continue
            if item.suffix != ".toml":
                continue
            if not item.exists():
                warnings.append(f"broken agent entry skipped: {item}")
                continue
            entries.append(
                Entry(
                    kind="agent",
                    name=item.name,
                    source=agents_dir / item.name,
                    target_rel=Path(".codex/agents") / item.name,
                )
            )
    else:
        warnings.append(f"missing source agents directory: {agents_dir}")

    if skills_dir.is_dir():
        for item in sorted(skills_dir.iterdir()):
            if item.name.startswith("."):
                continue
            if not (item / "SKILL.md").exists():
                warnings.append(f"skill without SKILL.md skipped: {item}")
                continue
            entries.append(
                Entry(
                    kind="skill",
                    name=item.name,
                    source=skills_dir / item.name,
                    target_rel=Path(".codex/skills") / item.name,
                )
            )
    else:
        warnings.append(f"missing source skills directory: {skills_dir}")

    return entries, warnings


def collect_directory_links(source_root: Path) -> tuple[list[DirectoryLink], list[str]]:
    warnings: list[str] = []
    links: list[DirectoryLink] = []
    for name in ("agents", "skills"):
        source = source_root / name
        if source.is_dir():
            links.append(DirectoryLink(kind=name, source=source, target_rel=Path(".codex") / name))
        else:
            warnings.append(f"missing source {name} directory: {source}")
    return links, warnings


def git_info_exclude(repo: Path) -> Path:
    result = subprocess.run(
        ["git", "-C", os.fspath(repo), "rev-parse", "--git-path", "info/exclude"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    raw = Path(result.stdout.strip())
    if raw.is_absolute():
        return raw
    return repo / raw


def ensure_local_ignore(repo: Path, apply: bool, counters: Counters) -> None:
    exclude = git_info_exclude(repo)
    existing = exclude.read_text(encoding="utf-8") if exclude.exists() else ""
    missing = [line for line in IGNORE_LINES if line not in existing.splitlines()]
    if not missing:
        counters.unchanged += 1
        return

    if not apply:
        print(f"DRY ignore {repo}: add {', '.join(missing)} to {exclude}")
        counters.ignored += len(missing)
        return

    exclude.parent.mkdir(parents=True, exist_ok=True)
    needs_leading_newline = bool(existing and not existing.endswith("\n"))
    with exclude.open("a", encoding="utf-8") as handle:
        if needs_leading_newline:
            handle.write("\n")
        if IGNORE_HEADER not in existing:
            handle.write(f"\n{IGNORE_HEADER}\n" if existing and existing.endswith("\n") else f"{IGNORE_HEADER}\n")
        for line in missing:
            handle.write(f"{line}\n")
    print(f"WRITE ignore {repo}: added {', '.join(missing)}")
    counters.ignored += len(missing)


def remove_local_ignore(repo: Path, apply: bool, counters: Counters) -> None:
    exclude = git_info_exclude(repo)
    if not exclude.exists():
        counters.unchanged += 1
        return

    lines = exclude.read_text(encoding="utf-8").splitlines()
    kept: list[str] = []
    removed: list[str] = []
    for line in lines:
        if line == IGNORE_HEADER or line in IGNORE_LINES:
            removed.append(line)
            continue
        kept.append(line)

    if not removed:
        counters.unchanged += 1
        return

    if not apply:
        print(f"DRY ignore-clean {repo}: remove {', '.join(removed)} from {exclude}")
        counters.ignored += len(removed)
        return

    exclude.write_text("\n".join(kept).rstrip() + "\n", encoding="utf-8")
    print(f"WRITE ignore-clean {repo}: removed {', '.join(removed)}")
    counters.ignored += len(removed)


def sync_entry(repo: Path, entry: Entry, apply: bool, counters: Counters) -> None:
    target = repo / entry.target_rel
    linked_parent = symlink_ancestor(repo, entry.target_rel.parent)
    if linked_parent is not None:
        print(f"CONFLICT {linked_parent}: symlinked directory; refusing to write through it")
        counters.conflicts += 1
        return

    if target.is_symlink():
        if same_symlink_target(target, entry.source):
            counters.unchanged += 1
            return
        current = os.readlink(target)
        if apply:
            target.unlink()
            target.symlink_to(entry.source)
            print(f"UPDATE {target} -> {entry.source} (was {current})")
        else:
            print(f"DRY update {target} -> {entry.source} (was {current})")
        counters.updated += 1
        return

    if target.exists():
        print(f"CONFLICT {target}: existing non-symlink, wanted -> {entry.source}")
        counters.conflicts += 1
        return

    if apply:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.symlink_to(entry.source)
        print(f"CREATE {target} -> {entry.source}")
    else:
        print(f"DRY create {target} -> {entry.source}")
    counters.created += 1


def sync_entries(repo: Path, entries: list[Entry], apply: bool, counters: Counters) -> None:
    reported_symlinked_parents: set[Path] = set()
    for entry in entries:
        linked_parent = symlink_ancestor(repo, entry.target_rel.parent)
        if linked_parent is not None:
            if linked_parent not in reported_symlinked_parents:
                print(f"CONFLICT {linked_parent}: symlinked directory; refusing to write through it")
                counters.conflicts += 1
                reported_symlinked_parents.add(linked_parent)
            else:
                counters.skipped += 1
            continue
        sync_entry(repo, entry, apply, counters)


def managed_entry_dir(target_dir: Path, source_dir: Path) -> bool:
    if not target_dir.is_dir() or target_dir.is_symlink():
        return False

    for child in sorted(target_dir.iterdir()):
        if not child.is_symlink():
            return False
        if not path_is_relative_to(symlink_target_abs(child), source_dir):
            return False
    return True


def replace_managed_entry_dir(target_dir: Path, apply: bool) -> None:
    if not apply:
        return

    for child in sorted(target_dir.iterdir()):
        child.unlink()
    target_dir.rmdir()


def sync_directory_link(repo: Path, link: DirectoryLink, apply: bool, counters: Counters) -> None:
    target = repo / link.target_rel
    linked_parent = symlink_ancestor(repo, link.target_rel.parent)
    if linked_parent is not None:
        print(f"CONFLICT {linked_parent}: symlinked directory; refusing to write through it")
        counters.conflicts += 1
        return

    if target.is_symlink():
        if same_symlink_target(target, link.source):
            counters.unchanged += 1
            return
        current = os.readlink(target)
        if apply:
            target.unlink()
            target.symlink_to(link.source)
            print(f"UPDATE {target} -> {link.source} (was {current})")
        else:
            print(f"DRY update {target} -> {link.source} (was {current})")
        counters.updated += 1
        return

    if target.exists():
        if managed_entry_dir(target, link.source):
            if apply:
                replace_managed_entry_dir(target, apply=True)
                target.symlink_to(link.source)
                print(f"REPLACE-DIR {target} -> {link.source}")
            else:
                print(f"DRY replace-dir {target} -> {link.source}")
            counters.updated += 1
            return

        print(
            f"CONFLICT {target}: existing non-symlink with local content, "
            f"wanted directory link -> {link.source}"
        )
        counters.conflicts += 1
        return

    if apply:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.symlink_to(link.source)
        print(f"CREATE {target} -> {link.source}")
    else:
        print(f"DRY create {target} -> {link.source}")
    counters.created += 1


def prune_stale(repo: Path, entries: list[Entry], apply: bool, counters: Counters) -> None:
    valid_by_dir: dict[Path, set[str]] = {}
    source_by_dir: dict[Path, Path] = {}
    for entry in entries:
        target_dir = repo / entry.target_rel.parent
        valid_by_dir.setdefault(target_dir, set()).add(entry.target_rel.name)
        source_by_dir[target_dir] = entry.source.parent

    for target_dir, valid_names in valid_by_dir.items():
        linked_parent = symlink_ancestor(repo, target_dir.relative_to(repo))
        if linked_parent is not None:
            print(f"SKIP prune {linked_parent}: symlinked directory")
            counters.skipped += 1
            continue
        if not target_dir.is_dir():
            continue
        source_dir = abs_lexical(source_by_dir[target_dir])
        for child in sorted(target_dir.iterdir()):
            if not child.is_symlink() or child.name in valid_names:
                continue
            current = symlink_target_abs(child)
            if not path_is_relative_to(current, source_dir):
                continue
            if apply:
                child.unlink()
                print(f"PRUNE {child}")
            else:
                print(f"DRY prune {child}")
            counters.pruned += 1


def managed_dirs(repo: Path, source_root: Path) -> list[tuple[Path, Path]]:
    return [
        (repo / ".codex/agents", source_root / "agents"),
        (repo / ".codex/skills", source_root / "skills"),
    ]


def clean_entrypoints(repo: Path, source_root: Path, apply: bool, remove_empty_dirs: bool, counters: Counters) -> None:
    for target_dir, source_dir in managed_dirs(repo, source_root):
        linked_parent = symlink_ancestor(repo, target_dir.relative_to(repo))
        if linked_parent is not None:
            print(f"CONFLICT {linked_parent}: symlinked directory; refusing to clean through it")
            counters.conflicts += 1
            continue

        if not target_dir.exists():
            counters.unchanged += 1
            continue
        if not target_dir.is_dir():
            print(f"CONFLICT {target_dir}: existing non-directory")
            counters.conflicts += 1
            continue

        for child in sorted(target_dir.iterdir()):
            if not child.is_symlink():
                continue
            if not path_is_relative_to(symlink_target_abs(child), source_dir):
                continue
            if apply:
                child.unlink()
                print(f"CLEAN {child}")
            else:
                print(f"DRY clean {child}")
            counters.removed += 1

    if remove_empty_dirs:
        for directory in [repo / ".codex/agents", repo / ".codex/skills", repo / ".codex"]:
            if directory.is_symlink() or not directory.is_dir():
                continue
            try:
                next(directory.iterdir())
            except StopIteration:
                if apply:
                    directory.rmdir()
                    print(f"RMDIR {directory}")
                else:
                    print(f"DRY rmdir {directory}")
                counters.removed += 1


def clean_directory_links(repo: Path, source_root: Path, apply: bool, remove_empty_dirs: bool, counters: Counters) -> None:
    for target_dir, source_dir in managed_dirs(repo, source_root):
        linked_parent = symlink_ancestor(repo, target_dir.parent.relative_to(repo))
        if linked_parent is not None:
            print(f"CONFLICT {linked_parent}: symlinked directory; refusing to clean through it")
            counters.conflicts += 1
            continue

        if target_dir.is_symlink():
            if not same_symlink_target(target_dir, source_dir):
                print(f"SKIP clean {target_dir}: not managed by {source_dir}")
                counters.skipped += 1
                continue
            if apply:
                target_dir.unlink()
                print(f"CLEAN {target_dir}")
            else:
                print(f"DRY clean {target_dir}")
            counters.removed += 1
            continue

        if target_dir.exists():
            counters.unchanged += 1
            continue

        counters.unchanged += 1

    if remove_empty_dirs:
        directory = repo / ".codex"
        if not directory.is_symlink() and directory.is_dir():
            try:
                next(directory.iterdir())
            except StopIteration:
                if apply:
                    directory.rmdir()
                    print(f"RMDIR {directory}")
                else:
                    print(f"DRY rmdir {directory}")
                counters.removed += 1


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync or clean repo-local .codex entrypoint symlinks from an aggregated workspace .codex.",
    )
    parser.add_argument(
        "action",
        nargs="?",
        default="sync",
        choices=("sync", "clean"),
        help="operation to run; default: sync",
    )
    parser.add_argument("--workspace", type=Path, default=DEFAULT_WORKSPACE, help="workspace containing git repos")
    parser.add_argument(
        "--source-root",
        type=Path,
        default=None,
        help="aggregated .codex root; default: <workspace>/.codex",
    )
    parser.add_argument("--repo", action="append", default=[], help="specific repo path or repo name; repeatable")
    parser.add_argument("--include", action="append", default=[], help="include glob matched against repo name/path")
    parser.add_argument("--exclude", action="append", default=[], help="exclude glob matched against repo name/path")
    parser.add_argument("--recursive", action="store_true", help="discover nested git repos instead of direct children only")
    parser.add_argument(
        "--link-mode",
        choices=("directories", "entries"),
        default=None,
        help=(
            "directories links .codex/agents and .codex/skills to source directories; "
            "entries links each agent/skill under real target directories; "
            "recommended: directories for workspace aggregates"
        ),
    )
    parser.add_argument("--prune", action="store_true", help="with sync, remove stale symlinks that point into the source root")
    parser.add_argument("--no-ignore", action="store_true", help="do not update .git/info/exclude")
    parser.add_argument("--remove-ignore", action="store_true", help="with clean, remove the local .codex/.agents ignore lines")
    parser.add_argument("--remove-empty-dirs", action="store_true", help="with clean, remove empty .codex entrypoint directories")
    parser.add_argument("--apply", action="store_true", help="write changes; default is dry-run")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    args.workspace = abs_lexical(args.workspace.expanduser())
    args.source_root = abs_lexical((args.source_root or (args.workspace / ".codex")).expanduser())

    if args.link_mode is None:
        print(
            "Choose --link-mode directories or --link-mode entries. "
            "Recommended: directories for workspace aggregates such as /Users/sky/GitHub/.codex; "
            "use entries when the repo must keep real .codex/agents or .codex/skills directories."
        )
        return 2

    entries: list[Entry] = []
    directory_links: list[DirectoryLink] = []
    warnings: list[str] = []
    if args.action == "sync":
        if args.link_mode == "entries":
            entries, warnings = collect_entries(args.source_root)
        else:
            directory_links, warnings = collect_directory_links(args.source_root)
    repos = select_repos(args)
    mode = "APPLY" if args.apply else "DRY-RUN"

    print(f"action: {args.action}")
    print(f"mode: {mode}")
    print(f"link_mode: {args.link_mode}")
    print(f"workspace: {args.workspace}")
    print(f"source_root: {args.source_root}")
    print(f"repos: {len(repos)}")
    if args.action == "sync":
        if args.link_mode == "entries":
            print(f"entries: {len(entries)}")
        else:
            print(f"directory_links: {len(directory_links)}")
            if args.prune:
                print("WARN --prune has no effect with --link-mode directories")
    for warning in warnings:
        print(f"WARN {warning}")

    if args.action == "sync" and args.link_mode == "entries" and not entries:
        print("No entries found; aborting.")
        return 2
    if args.action == "sync" and args.link_mode == "directories" and not directory_links:
        print("No entries found; aborting.")
        return 2
    if not repos:
        print("No repositories selected; aborting.")
        return 2

    counters = Counters()
    for repo in repos:
        print(f"\n== {repo} ==")
        if args.action == "sync" and not args.no_ignore:
            ensure_local_ignore(repo, args.apply, counters)
        if args.action == "sync" and args.link_mode == "entries":
            sync_entries(repo, entries, args.apply, counters)
            if args.prune:
                prune_stale(repo, entries, args.apply, counters)
        elif args.action == "sync":
            for link in directory_links:
                sync_directory_link(repo, link, args.apply, counters)
        else:
            if args.link_mode == "entries":
                clean_entrypoints(repo, args.source_root, args.apply, args.remove_empty_dirs, counters)
            else:
                clean_directory_links(repo, args.source_root, args.apply, args.remove_empty_dirs, counters)
            if args.remove_ignore and not args.no_ignore:
                remove_local_ignore(repo, args.apply, counters)

    print(
        "\nsummary: "
        f"created={counters.created} "
        f"updated={counters.updated} "
        f"unchanged={counters.unchanged} "
        f"conflicts={counters.conflicts} "
        f"pruned={counters.pruned} "
        f"removed={counters.removed} "
        f"ignore_lines={counters.ignored} "
        f"skipped={counters.skipped}"
    )
    return 1 if counters.conflicts else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
