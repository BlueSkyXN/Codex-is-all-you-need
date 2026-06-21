#!/usr/bin/env python3
"""Create a GitHub-publishable ZIP from the current Git worktree."""

from __future__ import annotations

import argparse
import datetime as dt
from dataclasses import dataclass
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


DEFAULT_BACKEND_PRIORITY = ["zip", "7z", "python"]
MAX_BACKEND_PRIORITY = ["7z", "zip", "python"]
VALID_BACKENDS = {"zip", "7z", "python"}
SEVENZIP_COMPRESSION_ARGS = ["-tzip", "-mx=9", "-mfb=258", "-mpass=15", "-scsUTF-8"]
ZIP_COMPRESSION_ARGS = ["-9", "-X"]


@dataclass(frozen=True)
class BackendSelection:
    name: str
    executable: str | None
    priority: list[str]
    unavailable: dict[str, str]


def run_git(args: list[str], cwd: Path, *, text: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
    )


def find_git_root(start: Path) -> Path:
    try:
        result = run_git(["rev-parse", "--show-toplevel"], start)
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() or "not a Git worktree"
        raise SystemExit(f"error: cannot find Git root from {start}: {message}") from exc
    return Path(result.stdout.strip()).resolve()


def resolve_binary(binary: str) -> str | None:
    candidate = Path(binary).expanduser()
    if candidate.parent != Path(".") and candidate.exists():
        return str(candidate)

    return shutil.which(binary)


def parse_backend_priority(raw: str | None, *, max_compression: bool) -> list[str]:
    if raw:
        priority = [item.strip().lower() for item in raw.split(",") if item.strip()]
    else:
        priority = list(MAX_BACKEND_PRIORITY if max_compression else DEFAULT_BACKEND_PRIORITY)

    if not priority:
        raise SystemExit("error: backend priority cannot be empty")

    invalid = sorted({item for item in priority if item not in VALID_BACKENDS})
    if invalid:
        allowed = ", ".join(sorted(VALID_BACKENDS))
        raise SystemExit(f"error: invalid backend in --backend-priority: {', '.join(invalid)}. Allowed: {allowed}")

    deduped: list[str] = []
    for item in priority:
        if item not in deduped:
            deduped.append(item)
    return deduped


def select_backend(
    priority: list[str],
    *,
    sevenzip_binary: str,
    zip_binary: str,
) -> BackendSelection:
    unavailable: dict[str, str] = {}
    for backend in priority:
        if backend == "python":
            return BackendSelection(backend, None, priority, unavailable)
        if backend == "7z":
            executable = resolve_binary(sevenzip_binary)
            if executable:
                return BackendSelection(backend, executable, priority, unavailable)
            unavailable[backend] = f"{sevenzip_binary} not found"
            continue
        if backend == "zip":
            executable = resolve_binary(zip_binary)
            if executable:
                return BackendSelection(backend, executable, priority, unavailable)
            unavailable[backend] = f"{zip_binary} not found"
            continue

    raise SystemExit("error: no usable ZIP backend found from priority: " + ",".join(priority))


def decode_git_paths(raw: bytes) -> list[str]:
    paths: list[str] = []
    for item in raw.split(b"\0"):
        if not item:
            continue
        paths.append(os.fsdecode(item))
    return paths


def collect_publishable_files(
    root: Path,
    archive_path: Path,
    output_dir: Path,
) -> tuple[list[str], list[str], list[str]]:
    try:
        result = run_git(
            ["ls-files", "-z", "--cached", "--others", "--exclude-standard", "--deduplicate"],
            root,
            text=False,
        )
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.decode(errors="replace").strip()
        raise SystemExit(f"error: git ls-files failed: {message}") from exc

    archive_rel = None
    try:
        archive_rel = archive_path.resolve().relative_to(root).as_posix()
    except ValueError:
        pass
    output_rel = None
    try:
        candidate = output_dir.resolve().relative_to(root).as_posix()
        if candidate not in ("", "."):
            output_rel = candidate.rstrip("/")
    except ValueError:
        pass

    files: list[str] = []
    missing: list[str] = []
    skipped_dirs: list[str] = []
    seen: set[str] = set()

    for rel in decode_git_paths(result.stdout):
        rel = rel.replace(os.sep, "/")
        if rel in seen:
            continue
        seen.add(rel)

        if rel == archive_rel:
            continue
        if output_rel and (rel == output_rel or rel.startswith(f"{output_rel}/")):
            continue
        if rel == ".git" or rel.startswith(".git/"):
            continue
        if "\n" in rel or "\r" in rel:
            raise SystemExit(f"error: list files cannot safely encode newline path: {rel!r}")

        path = root / rel
        if not path.exists() and not path.is_symlink():
            missing.append(rel)
            continue
        if path.is_dir() and not path.is_symlink():
            skipped_dirs.append(rel)
            continue
        files.append(rel)

    if not files:
        raise SystemExit("error: no publishable files found")

    return files, missing, skipped_dirs


def build_archive_name(root: Path, timestamp: str | None) -> str:
    stamp = timestamp or dt.datetime.now().strftime("%Y%m%d-%H%M")
    if not re.fullmatch(r"\d{8}-\d{4}", stamp):
        raise SystemExit("error: --timestamp must use format YYYYMMDD-hhmm")
    return f"{root.name}-{stamp}.zip"


def write_listfile(paths: list[str], directory: Path) -> Path:
    listfile = directory / "zip-files.txt"
    listfile.write_text("".join(f"{path}\n" for path in paths), encoding="utf-8")
    return listfile


def create_archive_with_7z(
    executable: str,
    root: Path,
    archive_path: Path,
    files: list[str],
    *,
    verbose: bool,
) -> list[str]:
    with tempfile.TemporaryDirectory(prefix="github-publish-zip-") as tmp:
        listfile = write_listfile(files, Path(tmp))
        command = [
            executable,
            "a",
            *SEVENZIP_COMPRESSION_ARGS,
            str(archive_path),
            f"@{listfile}",
        ]
        if verbose:
            print("command:", " ".join(command), file=sys.stderr)
        result = subprocess.run(
            command,
            cwd=str(root),
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if verbose:
            if result.stdout:
                print(result.stdout, file=sys.stderr, end="")
            if result.stderr:
                print(result.stderr, file=sys.stderr, end="")
        return command


def create_archive_with_zip(
    executable: str,
    root: Path,
    archive_path: Path,
    files: list[str],
    *,
    verbose: bool,
) -> list[str]:
    command = [
        executable,
        *ZIP_COMPRESSION_ARGS,
        str(archive_path),
        "-@",
    ]
    if verbose:
        print("command:", " ".join(command), file=sys.stderr)
    result = subprocess.run(
        command,
        cwd=str(root),
        check=True,
        input="\n".join(files) + "\n",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if verbose:
        if result.stdout:
            print(result.stdout, file=sys.stderr, end="")
        if result.stderr:
            print(result.stderr, file=sys.stderr, end="")
    return command


def add_python_zip_entry(zip_file: zipfile.ZipFile, root: Path, rel: str) -> None:
    path = root / rel
    st = path.lstat()
    if path.is_symlink():
        info = zipfile.ZipInfo(rel)
        info.create_system = 3
        info.external_attr = (0o120777 & 0xFFFF) << 16
        zip_file.writestr(info, os.readlink(path))
        return

    info = zipfile.ZipInfo.from_file(path, arcname=rel)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = (st.st_mode & 0xFFFF) << 16
    with path.open("rb") as source:
        zip_file.writestr(info, source.read(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def create_archive_with_python(
    root: Path,
    archive_path: Path,
    files: list[str],
) -> list[str]:
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zip_file:
        for rel in files:
            add_python_zip_entry(zip_file, root, rel)
    return ["python-zipfile", str(archive_path)]


def create_archive(
    backend: BackendSelection,
    root: Path,
    archive_path: Path,
    files: list[str],
    *,
    verbose: bool,
) -> list[str]:
    if backend.name == "7z":
        if backend.executable is None:
            raise SystemExit("error: selected 7z backend has no executable")
        return create_archive_with_7z(backend.executable, root, archive_path, files, verbose=verbose)
    if backend.name == "zip":
        if backend.executable is None:
            raise SystemExit("error: selected zip backend has no executable")
        return create_archive_with_zip(backend.executable, root, archive_path, files, verbose=verbose)
    if backend.name == "python":
        return create_archive_with_python(root, archive_path, files)
    raise SystemExit(f"error: unsupported backend selected: {backend.name}")


def print_summary(
    *,
    root: Path,
    archive_path: Path,
    files: list[str],
    missing: list[str],
    skipped_dirs: list[str],
    dry_run: bool,
    as_json: bool,
    backend: BackendSelection | None = None,
    command: list[str] | None = None,
    include_files: bool = False,
) -> None:
    payload = {
        "root": str(root),
        "archive": str(archive_path),
        "file_count": len(files),
        "missing_tracked_count": len(missing),
        "skipped_directory_count": len(skipped_dirs),
        "dry_run": dry_run,
        "command": command,
    }
    if backend:
        payload["backend"] = backend.name
        payload["backend_priority"] = backend.priority
        payload["unavailable_backends"] = backend.unavailable
    if include_files:
        payload["files"] = files
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    prefix = "Dry run" if dry_run else "Created"
    print(f"{prefix}: {archive_path}")
    print(f"Included files: {len(files)}")
    if backend:
        print(f"Backend: {backend.name}")
        print(f"Backend priority: {','.join(backend.priority)}")
        if backend.unavailable:
            unavailable = "; ".join(f"{name}: {reason}" for name, reason in backend.unavailable.items())
            print(f"Unavailable higher-priority backends: {unavailable}", file=sys.stderr)
    if include_files:
        for path in files:
            print(path)
    if missing:
        print(f"Skipped missing tracked files: {len(missing)}", file=sys.stderr)
        for path in missing[:20]:
            print(f"  missing: {path}", file=sys.stderr)
        if len(missing) > 20:
            print(f"  ... {len(missing) - 20} more", file=sys.stderr)
    if skipped_dirs:
        print(f"Skipped directory entries: {len(skipped_dirs)}", file=sys.stderr)
        for path in skipped_dirs[:20]:
            print(f"  directory: {path}", file=sys.stderr)
        if len(skipped_dirs) > 20:
            print(f"  ... {len(skipped_dirs) - 20} more", file=sys.stderr)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Package GitHub-publishable Git worktree files into local/<project>-YYYYMMDD-hhmm.zip.",
    )
    parser.add_argument(
        "project",
        nargs="?",
        default=".",
        help="Project path inside the target Git worktree. Defaults to current directory.",
    )
    parser.add_argument(
        "--output-dir",
        default="local",
        help="Archive output directory. Relative paths are resolved from the Git root. Default: local",
    )
    parser.add_argument(
        "--timestamp",
        help="Override timestamp for deterministic output, format YYYYMMDD-hhmm.",
    )
    parser.add_argument(
        "--sevenzip",
        default="7z",
        help="System 7z executable name or path. Default: 7z",
    )
    parser.add_argument(
        "--zip-binary",
        default="zip",
        help="System zip executable name or path. Default: zip",
    )
    parser.add_argument(
        "--backend-priority",
        help="Comma-separated backend priority using zip,7z,python. Default: zip,7z,python; with --max-compression: 7z,zip,python.",
    )
    parser.add_argument(
        "--max-compression",
        action="store_true",
        help="Prefer maximum compression by changing default backend priority to 7z,zip,python.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing same-minute archive.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the planned archive path, file count, and selected backend without creating the archive.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable summary JSON.",
    )
    parser.add_argument(
        "--list-files",
        action="store_true",
        help="Include the publishable file list in the output.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print the external compression command before running it.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    project = Path(args.project).expanduser().resolve()
    root = find_git_root(project)

    output_dir = Path(args.output_dir).expanduser()
    if not output_dir.is_absolute():
        output_dir = root / output_dir
    output_dir = output_dir.resolve()
    archive_path = output_dir / build_archive_name(root, args.timestamp)

    files, missing, skipped_dirs = collect_publishable_files(root, archive_path, output_dir)
    priority = parse_backend_priority(args.backend_priority, max_compression=args.max_compression)
    backend = select_backend(priority, sevenzip_binary=args.sevenzip, zip_binary=args.zip_binary)

    if args.dry_run:
        print_summary(
            root=root,
            archive_path=archive_path,
            files=files,
            missing=missing,
            skipped_dirs=skipped_dirs,
            dry_run=True,
            as_json=args.json,
            backend=backend,
            include_files=args.list_files,
        )
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    if archive_path.exists():
        if not args.force:
            raise SystemExit(f"error: archive already exists: {archive_path}. Re-run with --force to overwrite.")
        archive_path.unlink()

    try:
        command = create_archive(backend, root, archive_path, files, verbose=args.verbose)
    except subprocess.CalledProcessError as exc:
        output = (exc.stderr or exc.stdout or "").strip()
        details = f": {output}" if output else ""
        raise SystemExit(f"error: {backend.name} backend failed with exit code {exc.returncode}{details}") from exc

    print_summary(
        root=root,
        archive_path=archive_path,
        files=files,
        missing=missing,
        skipped_dirs=skipped_dirs,
        dry_run=False,
        as_json=args.json,
        backend=backend,
        command=command,
        include_files=args.list_files,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
