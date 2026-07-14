#!/usr/bin/env python3
"""Audit, backfill, and gate public Skill version metadata.

The checker deliberately uses only the standard library.  It treats the plugin
packages as the canonical publishable surface and also checks the Codex Next
catalog mirrors, which are part of the public source catalog rather than a
second release surface.
"""

from __future__ import annotations

import argparse
import datetime as dt
import functools
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
VERSION_RE = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
JUNK_NAMES = frozenset({".ds_store", "thumbs.db", "desktop.ini"})
EXCLUDED_NAMES = frozenset({"readme", "license", "notice"})
BEHAVIOR_ROOTS = frozenset({"references", "scripts", "assets", "examples"})
VISUAL_BRAINSTORMING = ("0.1", "2026-07-14")


@dataclass(frozen=True)
class Skill:
    path: PurePosixPath
    directory: PurePosixPath
    name: str
    plugin: str | None
    mirror_of: PurePosixPath | None = None


@dataclass(frozen=True)
class Metadata:
    version: str | None
    updated: str | None
    errors: tuple[str, ...]


def git(repo: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return result.stdout


@functools.lru_cache(maxsize=None)
def tracked_paths(repo: Path, ref: str | None = None) -> frozenset[PurePosixPath]:
    if ref is None:
        raw = git(repo, "ls-files", "-z")
    else:
        raw = git(repo, "ls-tree", "-r", "-z", "--name-only", ref)
    return frozenset(PurePosixPath(path) for path in raw.split("\0") if path)


def discover_public_skills(repo: Path, *, ref: str | None = None) -> list[Skill]:
    """Discover tracked canonical plugin skills and Codex Next catalog mirrors."""
    paths = tracked_paths(repo, ref)
    canonical: list[Skill] = []
    canonical_by_name: dict[str, Skill] = {}
    for path in sorted(paths):
        parts = path.parts
        if (
            len(parts) == 5
            and parts[0] == "plugins"
            and parts[2] == "skills"
            and parts[4] == "SKILL.md"
            and "local" not in parts
        ):
            skill = Skill(path, path.parent, parts[3], parts[1])
            canonical.append(skill)
            if parts[1] == "codex-next":
                canonical_by_name[skill.name] = skill

    mirrors: list[Skill] = []
    for path in sorted(paths):
        parts = path.parts
        if (
            len(parts) == 6
            and parts[0] == "examples"
            and parts[1] == "catalog"
            and parts[3] == "skills"
            and parts[5] == "SKILL.md"
            and "local" not in parts
            and parts[2] != "local"
            and parts[3] != "local"
            and parts[2]  # catalog group
            and parts[4] in canonical_by_name
        ):
            mirrors.append(
                Skill(path, path.parent, parts[4], None, canonical_by_name[parts[4]].path)
            )
    return canonical + mirrors


def split_frontmatter(text: str) -> tuple[list[str], int | None]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return lines, None
    for index, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            return lines, index
    return lines, None


def is_quoted(value: str) -> bool:
    return len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}


def read_metadata(text: str) -> Metadata:
    lines, end = split_frontmatter(text)
    if end is None:
        return Metadata(None, None, ("missing or unterminated frontmatter",))
    metadata_line: int | None = None
    for index, line in enumerate(lines[1:end], 1):
        if re.match(r"^metadata\s*:\s*(?:#.*)?(?:\r?\n)?$", line):
            metadata_line = index
            break
    if metadata_line is None:
        return Metadata(None, None, ("missing metadata mapping",))

    values: dict[str, str] = {}
    errors: list[str] = []
    for line in lines[metadata_line + 1 : end]:
        if not line.startswith((" ", "\t")):
            break
        match = re.match(r"^\s+([A-Za-z0-9_-]+)\s*:\s*(.*?)\s*$", line)
        if not match:
            continue
        key, raw_value = match.groups()
        if key not in {"version", "updated"}:
            continue
        if not is_quoted(raw_value):
            errors.append(f"metadata.{key} must be a quoted string")
            continue
        values[key] = raw_value[1:-1]
    version = values.get("version")
    updated = values.get("updated")
    if version is None and not any("metadata.version" in error for error in errors):
        errors.append("missing metadata.version")
    if updated is None and not any("metadata.updated" in error for error in errors):
        errors.append("missing metadata.updated")
    if version is not None and not VERSION_RE.fullmatch(version):
        errors.append("metadata.version must use two-part A.B format")
    if updated is not None:
        if not DATE_RE.fullmatch(updated):
            errors.append("metadata.updated must use YYYY-MM-DD")
        else:
            try:
                parsed_date = dt.date.fromisoformat(updated)
            except ValueError:
                errors.append("metadata.updated must be a valid calendar date")
            else:
                if parsed_date > dt.date.today():
                    errors.append("metadata.updated cannot be in the future")
    return Metadata(version, updated, tuple(errors))


def normalize_skill_markdown(text: str) -> bytes:
    """Remove only metadata.version/updated from SKILL.md behavior identity."""
    lines, end = split_frontmatter(text)
    if end is None:
        return text.encode("utf-8")
    output: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if index < end and re.match(r"^metadata\s*:\s*(?:#.*)?(?:\r?\n)?$", line):
            block_end = index + 1
            while block_end < end and lines[block_end].startswith((" ", "\t")):
                block_end += 1
            remaining = [
                child
                for child in lines[index + 1 : block_end]
                if not re.match(r"^\s+(version|updated)\s*:", child)
            ]
            if any(child.strip() and not child.lstrip().startswith("#") for child in remaining):
                output.append(line)
                output.extend(remaining)
            index = block_end
            continue
        output.append(line)
        index += 1
    return "".join(output).encode("utf-8")


def relevant_file(relative: PurePosixPath) -> bool:
    name = relative.name.lower()
    stem = relative.stem.lower()
    if name in JUNK_NAMES or any(name.startswith(prefix) for prefix in EXCLUDED_NAMES):
        return False
    if relative == PurePosixPath("SKILL.md"):
        return True
    if relative == PurePosixPath("agents/openai.yaml"):
        return True
    return bool(relative.parts) and relative.parts[0] in BEHAVIOR_ROOTS


def fingerprint_files(files: Iterable[tuple[PurePosixPath, bytes]]) -> str:
    digest = hashlib.sha256()
    included = 0
    for relative, content in sorted(files):
        if not relevant_file(relative):
            continue
        if relative == PurePosixPath("SKILL.md"):
            content = normalize_skill_markdown(content.decode("utf-8"))
        digest.update(relative.as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(content)
        digest.update(b"\0")
        included += 1
    if not included:
        return ""
    return digest.hexdigest()


def fingerprint_worktree(repo: Path, skill: Skill) -> str:
    files = (
        (PurePosixPath(path.relative_to(repo / skill.directory).as_posix()), path.read_bytes())
        for path in (repo / skill.directory).rglob("*")
        if path.is_file()
    )
    return fingerprint_files(files)


def tree_files(repo: Path, ref: str, directory: PurePosixPath) -> tuple[tuple[PurePosixPath, bytes], ...]:
    prefix = directory.as_posix() + "/"
    names = git(repo, "ls-tree", "-r", "--name-only", ref, "--", directory.as_posix()).splitlines()
    result: list[tuple[PurePosixPath, bytes]] = []
    for name in names:
        if not name.startswith(prefix):
            continue
        relative = PurePosixPath(name[len(prefix) :])
        content = subprocess.run(
            ["git", "-C", str(repo), "show", f"{ref}:{name}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if content.returncode == 0:
            result.append((relative, content.stdout))
    return tuple(result)


@functools.lru_cache(maxsize=None)
def fingerprint_tree(repo: Path, ref: str, directory: PurePosixPath) -> str | None:
    files = tree_files(repo, ref, directory)
    if not any(relative == PurePosixPath("SKILL.md") for relative, _ in files):
        return None
    return fingerprint_files(files)


@functools.lru_cache(maxsize=None)
def followed_directories(
    repo: Path, history_ref: str, skill_path: PurePosixPath
) -> tuple[PurePosixPath, ...]:
    """Return every skill directory reached by Git rename/copy following."""
    directories = {skill_path.parent}
    output = git(
        repo,
        "log",
        "--follow",
        "--find-renames=50%",
        "--name-status",
        "--format=",
        history_ref,
        "--",
        skill_path.as_posix(),
    )
    for line in output.splitlines():
        fields = line.split("\t")
        if len(fields) < 2:
            continue
        for candidate in fields[1:]:
            parts = PurePosixPath(candidate).parts
            if len(parts) >= 2 and parts[-1] == "SKILL.md":
                directories.add(PurePosixPath(candidate).parent)
    return tuple(sorted(directories))


def lineage_directories(repo: Path, history_ref: str, skill: Skill) -> tuple[PurePosixPath, ...]:
    seeds = [skill.path]
    if skill.plugin == "codex-next":
        for path in tracked_paths(repo, history_ref):
            parts = path.parts
            if (
                len(parts) == 6
                and parts[:2] == ("examples", "catalog")
                and parts[3] == "skills"
                and parts[4] == skill.name
                and parts[5] == "SKILL.md"
            ):
                seeds.append(path)
    directories: set[PurePosixPath] = set()
    for seed in seeds:
        directories.update(followed_directories(repo, history_ref, seed))
    return tuple(sorted(directories))


@functools.lru_cache(maxsize=None)
def git_date(repo: Path, commit: str) -> str:
    return git(repo, "show", "-s", "--format=%cI", commit).strip()[:10]


def history_plan(
    repo: Path, history_ref: str, skill: Skill
) -> tuple[str, str, int, str]:
    if skill.name == "visual-brainstorming":
        evidence = git(repo, "log", "-1", "--format=%H", history_ref, "--", skill.directory.as_posix()).strip()
        return (*VISUAL_BRAINSTORMING, 1, evidence)
    directories = lineage_directories(repo, history_ref, skill)
    commits = git(
        repo,
        "log",
        "--reverse",
        "--format=%H",
        history_ref,
        "--",
        *(directory.as_posix() for directory in directories),
    ).splitlines()
    ordered: list[tuple[str, str, str]] = []
    for commit in commits:
        plugin_dirs = [directory for directory in directories if directory.parts[0] == "plugins"]
        catalog_dirs = [directory for directory in directories if directory.parts[:2] == ("examples", "catalog")]
        candidates = [
            fp
            for directory in plugin_dirs
            if (fp := fingerprint_tree(repo, commit, directory)) is not None
        ]
        if not candidates:
            candidates = [
                fp
                for directory in catalog_dirs
                if (fp := fingerprint_tree(repo, commit, directory)) is not None
            ]
        if not candidates:
            continue
        fingerprint = sorted(candidates)[0]
        if not ordered or fingerprint != ordered[-1][0]:
            ordered.append((fingerprint, git_date(repo, commit), commit))
    current = fingerprint_worktree(repo, skill)
    if not ordered or current != ordered[-1][0]:
        # The current worktree can contain an uncommitted behavior edit.  It is
        # still a state and gets today's date when backfilled deliberately.
        ordered.append((current, dt.date.today().isoformat(), "WORKTREE"))
    number = len(ordered)
    _, updated, evidence = ordered[-1]
    return f"0.{number}", updated, number, evidence


def read_worktree_skill(repo: Path, skill: Skill) -> str:
    return (repo / skill.path).read_text(encoding="utf-8")


def replace_metadata(text: str, version: str, updated: str) -> str:
    lines, end = split_frontmatter(text)
    if end is None:
        raise ValueError("cannot write metadata without valid frontmatter")
    metadata_start: int | None = None
    metadata_end: int | None = None
    for index, line in enumerate(lines[1:end], 1):
        if re.match(r"^metadata\s*:\s*(?:#.*)?(?:\r?\n)?$", line):
            metadata_start = index
            metadata_end = index + 1
            while metadata_end < end and lines[metadata_end].startswith((" ", "\t")):
                metadata_end += 1
            break
    newline = "\r\n" if "\r\n" in text else "\n"
    wanted = {"version": version, "updated": updated}
    if metadata_start is None:
        insertion = ["metadata:" + newline, f'  version: "{version}"{newline}', f'  updated: "{updated}"{newline}']
        lines[end:end] = insertion
        return "".join(lines)
    assert metadata_end is not None
    existing = lines[metadata_start + 1 : metadata_end]
    replacement: list[str] = [lines[metadata_start]]
    present: set[str] = set()
    for line in existing:
        match = re.match(r"^(\s+)(version|updated)(\s*:\s*).*?(\r?\n)?$", line)
        if match:
            indent, key, _, ending = match.groups()
            replacement.append(f'{indent}{key}: "{wanted[key]}"{ending or newline}')
            present.add(key)
        else:
            replacement.append(line)
    for key in ("version", "updated"):
        if key not in present:
            replacement.append(f'  {key}: "{wanted[key]}"{newline}')
    lines[metadata_start:metadata_end] = replacement
    return "".join(lines)


def audit(repo: Path, history_ref: str) -> dict[str, Any]:
    git(repo, "rev-parse", "--verify", history_ref)
    skills = discover_public_skills(repo)
    canonical = [skill for skill in skills if skill.mirror_of is None]
    proposals = {skill.path: history_plan(repo, history_ref, skill) for skill in canonical}
    records: list[dict[str, Any]] = []
    for skill in skills:
        source = skill.mirror_of or skill.path
        proposed_version, proposed_updated, states, evidence = proposals[source]
        metadata = read_metadata(read_worktree_skill(repo, skill))
        record = {
            "path": skill.path.as_posix(),
            "canonical": skill.mirror_of is None,
            "mirror_of": skill.mirror_of.as_posix() if skill.mirror_of else None,
            "version": metadata.version,
            "updated": metadata.updated,
            "current_errors": list(metadata.errors),
            "proposed_version": proposed_version,
            "proposed_updated": proposed_updated,
            "states": states,
            "evidence": evidence,
        }
        records.append(record)
    return {
        "command": "audit",
        "history_ref": history_ref,
        "skills": records,
        "errors": [],
    }


def backfill(repo: Path, history_ref: str, *, apply: bool) -> dict[str, Any]:
    git(repo, "rev-parse", "--verify", history_ref)
    skills = discover_public_skills(repo)
    canonical = [skill for skill in skills if skill.mirror_of is None]
    proposals: dict[PurePosixPath, tuple[str, str, int, str]] = {}
    for skill in canonical:
        proposals[skill.path] = history_plan(repo, history_ref, skill)
    records: list[dict[str, Any]] = []
    for skill in skills:
        source = skill.mirror_of or skill.path
        version, updated, states, evidence = proposals[source]
        old = read_metadata(read_worktree_skill(repo, skill))
        changed = old.version != version or old.updated != updated or bool(old.errors)
        if apply and changed:
            path = repo / skill.path
            path.write_text(replace_metadata(path.read_text(encoding="utf-8"), version, updated), encoding="utf-8")
        records.append({
            "path": skill.path.as_posix(), "version": version, "updated": updated,
            "states": states, "changed": changed,
            "evidence": evidence,
            "mirror_of": skill.mirror_of.as_posix() if skill.mirror_of else None,
        })
    return {"command": "backfill", "history_ref": history_ref, "apply": apply, "skills": records, "errors": []}


def valid_transition(old: str, new: str) -> bool:
    old_a, old_b = (int(part) for part in old.split("."))
    new_a, new_b = (int(part) for part in new.split("."))
    return (new_a == old_a and new_b == old_b + 1) or (new_a == old_a + 1 and new_b == 0)


def show_at(repo: Path, ref: str, path: PurePosixPath) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(repo), "show", f"{ref}:{path.as_posix()}"],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    return result.stdout if result.returncode == 0 else None


def check(repo: Path, base_ref: str) -> dict[str, Any]:
    git(repo, "rev-parse", "--verify", base_ref)
    skills = discover_public_skills(repo)
    errors: list[str] = []
    records: list[dict[str, Any]] = []
    current_by_path = {skill.path: skill for skill in skills}
    for skill in skills:
        text = read_worktree_skill(repo, skill)
        current = read_metadata(text)
        for error in current.errors:
            errors.append(f"{skill.path}: {error}")
        old_text = show_at(repo, base_ref, skill.path)
        baseline = read_metadata(old_text) if old_text is not None else None
        behavior_changed: bool | None = None
        if old_text is not None and baseline is not None and not baseline.errors and not current.errors:
            behavior_changed = fingerprint_files([(PurePosixPath("SKILL.md"), old_text.encode())]) != fingerprint_files([(PurePosixPath("SKILL.md"), text.encode())])
            # Compare all behavior files too, using base tree if the skill was present.
            old_fp = fingerprint_tree(repo, base_ref, skill.directory)
            new_fp = fingerprint_worktree(repo, skill)
            behavior_changed = old_fp != new_fp
            if not behavior_changed and (baseline.version != current.version or baseline.updated != current.updated):
                errors.append(f"{skill.path}: metadata changed without behavior change")
            if behavior_changed:
                if not valid_transition(baseline.version or "", current.version or ""):
                    errors.append(f"{skill.path}: behavior change requires one patch or minor version step")
                if (current.updated or "") < (baseline.updated or ""):
                    errors.append(f"{skill.path}: behavior change cannot move metadata.updated backward")
                if skill.mirror_of is None and current.updated:
                    expected_updated = history_plan(repo, "HEAD", skill)[1]
                    if current.updated != expected_updated:
                        errors.append(
                            f"{skill.path}: metadata.updated {current.updated!r} does not match "
                            f"latest substantive state date {expected_updated!r}"
                        )
        records.append({"path": skill.path.as_posix(), "behavior_changed": behavior_changed, "initial_backfill": old_text is None or (baseline is not None and bool(baseline.errors))})

    # Catalog mirrors must keep both behavior identity and published metadata equal.
    for skill in skills:
        if skill.mirror_of is None:
            continue
        canonical = current_by_path.get(skill.mirror_of)
        if canonical is None:
            errors.append(f"{skill.path}: mirror canonical skill is missing")
            continue
        mirror_text = read_worktree_skill(repo, skill)
        canonical_text = read_worktree_skill(repo, canonical)
        mirror_meta = read_metadata(mirror_text)
        canonical_meta = read_metadata(canonical_text)
        if fingerprint_worktree(repo, skill) != fingerprint_worktree(repo, canonical):
            errors.append(f"{skill.path}: catalog mirror behavior differs from {canonical.path}")
        if (mirror_meta.version, mirror_meta.updated) != (canonical_meta.version, canonical_meta.updated):
            errors.append(f"{skill.path}: catalog mirror metadata differs from {canonical.path}")
    return {"command": "check", "base_ref": base_ref, "skills": records, "errors": sorted(errors)}


def emit(summary: dict[str, Any], json_path: Path | None) -> None:
    rendered = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    if json_path is not None:
        if str(json_path) == "-":
            sys.stdout.write(rendered)
        else:
            json_path.write_text(rendered, encoding="utf-8")
    else:
        print(f"Skill metadata {summary['command']}: {len(summary['skills'])} skills")
        for error in summary["errors"]:
            print(f"ERROR: {error}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=REPO_ROOT, help="Repository root (default: this repository).")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command, ref_name in (("audit", "history_ref"), ("backfill", "history_ref"), ("check", "base_ref")):
        sub = subparsers.add_parser(command)
        sub.add_argument(f"--{ref_name.replace('_', '-')}", required=True)
        if command == "backfill":
            sub.add_argument("--apply", action="store_true", help="Write proposed metadata (default is dry-run).")
        sub.add_argument("--json", type=Path, help="Write the auditable JSON report; use - for stdout.")
    args = parser.parse_args(argv)
    repo = args.repo.resolve()
    try:
        if args.command == "audit":
            summary = audit(repo, args.history_ref)
        elif args.command == "backfill":
            summary = backfill(repo, args.history_ref, apply=args.apply)
        else:
            summary = check(repo, args.base_ref)
    except (OSError, RuntimeError, ValueError) as exc:
        summary = {"command": args.command, "skills": [], "errors": [str(exc)]}
    emit(summary, args.json)
    return 1 if summary["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
