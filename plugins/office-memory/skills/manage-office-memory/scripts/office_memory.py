from __future__ import annotations

import argparse
import errno
import fnmatch
import hashlib
import json
import os
import re
import tempfile
import tomllib
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable


SOURCE_ID = re.compile(r"^[a-z][a-z0-9-]{0,63}$")
KEY = re.compile(r"^[a-z][a-z0-9.-]{0,79}$")
DAILY_FILE = re.compile(r"^(\d{4}-\d{2}-\d{2})\.md$")
SECRET = re.compile(r"(?:-----BEGIN [A-Z ]*PRIVATE KEY-----|\b(?:AKIA|ASIA)[0-9A-Z]{16}\b|\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|hf_[A-Za-z0-9]{20,}|npm_[A-Za-z0-9]{20,}|glpat-[A-Za-z0-9_-]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{35}|sk-[A-Za-z0-9_-]{16,})\b|\bauthorization\s*:\s*bearer\s+[A-Za-z0-9._~+/=-]{8,}|(?<![A-Za-z0-9])(?:password|passwd|secret|token|api[ _-]?key|access[ _-]?key|client[ _-]?secret)\s*[:=]\s*[^\s]{8,})", re.I)
KINDS = {"fact", "preference", "decision", "runbook", "lesson"}
AWARENESS_SECTIONS = ("Current understanding", "Relevant changes", "Conflicts and unknowns", "Needs attention", "Memory candidates")
DAILY_SECTIONS = ("Meaningful changes", "Decisions and constraints", "Conflicts and unknowns", "Long-term candidates")


class ContractError(ValueError):
    pass


@dataclass(frozen=True)
class Source:
    id: str
    path: Path
    role: str
    default: bool
    include: tuple[str, ...]


@dataclass(frozen=True)
class Config:
    project_id: str
    root: Path
    allowed_scopes: tuple[str, ...]
    awareness: Path
    memory: Path
    sources: tuple[Source, ...]


def resolve(value: str | Path, root: Path | None = None, strict: bool = False) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute() and root is not None:
        path = root / path
    return path.resolve(strict=strict)


def within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def output_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def load_config(path_value: str) -> Config:
    path = resolve(path_value, strict=True)
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise ContractError(f"cannot parse config: {error}") from error
    if data.get("version") != "0.1" or data.get("manual_activation_only") is not True:
        raise ContractError("version must be 0.1 and manual_activation_only must be true")
    project_id, root_value = data.get("project_id"), data.get("project_root")
    if not isinstance(project_id, str) or not project_id or not isinstance(root_value, str) or not root_value:
        raise ContractError("project_id and project_root are required strings")
    root = resolve(root_value, path.parent, strict=True)
    scopes = data.get("allowed_scopes")
    if not isinstance(scopes, list) or not scopes or not all(isinstance(scope, str) and scope and not Path(scope).is_absolute() and ".." not in Path(scope).parts for scope in scopes):
        raise ContractError("allowed_scopes must be non-empty relative scope names")
    outputs: list[Path] = []
    for key in ("awareness_file", "memory_file"):
        value = data.get(key)
        if not isinstance(value, str) or not value:
            raise ContractError(f"{key} is required")
        candidate = resolve(value, root)
        expected = "AWARENESS.md" if key == "awareness_file" else "MEMORY.md"
        if not within(candidate, root) or candidate.name != expected:
            raise ContractError(f"{key} must be a project-root descendant named {expected}")
        outputs.append(candidate)
    if outputs[0] == outputs[1]:
        raise ContractError("awareness_file and memory_file must be unique")
    if outputs[1].parent == root:
        raise ContractError("memory_file must live in a dedicated project-root descendant directory")
    raw_sources = data.get("sources", [])
    if not isinstance(raw_sources, list):
        raise ContractError("sources must be an array of tables")
    sources: list[Source] = []
    for raw in raw_sources:
        if not isinstance(raw, dict) or not isinstance(raw.get("id"), str) or not SOURCE_ID.fullmatch(raw["id"]) or not isinstance(raw.get("path"), str) or raw.get("role") not in {"profile", "memory", "recent"} or not isinstance(raw.get("default"), bool):
            raise ContractError("each source needs id, path, role, and default")
        if raw["id"] == "project":
            raise ContractError("source id 'project' is reserved for explicit project materials")
        if raw["role"] in {"profile", "recent"} and raw["default"]:
            raise ContractError("profile and recent sources must default to false")
        include = raw.get("include", ["*"])
        if not isinstance(include, list) or not include or not all(isinstance(item, str) and item and ".." not in Path(item).parts for item in include):
            raise ContractError("source include must be a non-empty relative glob array")
        sources.append(Source(raw["id"], resolve(raw["path"], root, strict=False), raw["role"], raw["default"], tuple(include)))
    if len({source.id for source in sources}) != len(sources):
        raise ContractError("source ids must be unique")
    daily_dir = outputs[1].parent
    for source in sources:
        if any(source.path == output or within(output, source.path) or within(source.path, output) for output in outputs) or within(source.path, daily_dir):
            raise ContractError(f"source overlaps an output path: {source.id}")
    return Config(project_id, root, tuple(scopes), outputs[0], outputs[1], tuple(sources))


def is_office_memory_result(path: Path, cfg: Config) -> bool:
    if path in {cfg.awareness, cfg.memory}:
        return True
    if path.parent != cfg.memory.parent:
        return False
    match = DAILY_FILE.fullmatch(path.name)
    if match is None:
        return False
    try:
        date.fromisoformat(match.group(1))
    except ValueError:
        return False
    return True


def gate_materials(cfg: Config, values: Iterable[str]) -> tuple[Path, ...]:
    raw_values = tuple(values)
    if len(raw_values) > 20:
        raise ContractError("at most 20 explicit --material files are allowed")
    result: list[Path] = []
    for value in raw_values:
        raw = Path(value)
        if raw.is_absolute():
            raise ContractError("--material must be project-relative")
        path = resolve(raw, cfg.root, strict=True)
        if not within(path, cfg.root):
            raise ContractError("--material escapes project_root")
        if not path.is_file():
            raise ContractError("--material must name an explicit file; V1 Lite does not recurse directories")
        if is_office_memory_result(path, cfg):
            raise ContractError("--material must not name an Office Memory result file")
        if path not in result:
            result.append(path)
    return tuple(result)


def gate_focus(cfg: Config, focus: str | None, materials: tuple[Path, ...]) -> None:
    if materials and focus is None:
        raise ContractError("--focus is required whenever --material is used")
    if focus is None or focus == "project":
        return
    if focus not in cfg.allowed_scopes or focus == "project":
        raise ContractError("--focus must be project or an exact allowed scope")
    scope_root = resolve(focus, cfg.root, strict=True)
    if any(not within(material, scope_root) for material in materials):
        raise ContractError("--material is outside the exact --focus scope")


def select_sources(cfg: Config, selected: Iterable[str]) -> tuple[Source, ...]:
    by_id = {source.id: source for source in cfg.sources}
    ids = tuple(selected)
    if any(identifier not in by_id for identifier in ids):
        raise ContractError("--source accepts only a configured source id")
    return tuple(by_id[identifier] for identifier in ids) if ids else tuple(source for source in cfg.sources if source.default)


def source_files(source: Source) -> Iterable[Path]:
    if not source.path.exists():
        raise ContractError(f"configured source does not exist: {source.id}")
    root = source.path.resolve()
    if root.is_file():
        yield root
        return
    for candidate in sorted(root.iterdir()):
        if candidate.is_file() and not candidate.is_symlink() and any(fnmatch.fnmatchcase(candidate.name, glob) for glob in source.include):
            yield candidate


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def snapshot(cfg: Config, selected: Iterable[str], materials: Iterable[Path]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for source in select_sources(cfg, selected):
        for path in source_files(source):
            stat = path.stat()
            rows.append({"source_id": source.id, "file_id": path.name if source.path.is_dir() else source.path.name, "mtime_ns": stat.st_mtime_ns, "sha256": digest(path)})
    for path in materials:
        stat = path.stat()
        rows.append({"source_id": "project", "file_id": f"project#{path.relative_to(cfg.root).as_posix()}", "mtime_ns": stat.st_mtime_ns, "sha256": digest(path)})
    return {"source_ids": sorted({row["source_id"] for row in rows}), "file_count": len(rows), "files": sorted(rows, key=lambda row: (row["source_id"], row["file_id"]))}


def write_sync(handle: Any, content: str) -> None:
    handle.write(content)
    handle.flush()
    os.fsync(handle.fileno())


def atomic_create(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            write_sync(handle, content)
        try:
            os.link(temporary, path)
        except FileExistsError:
            return False
        except OSError as error:
            unsupported = {errno.EPERM, getattr(errno, "ENOTSUP", -1), getattr(errno, "EOPNOTSUPP", -1)}
            if error.errno not in unsupported:
                raise
            try:
                descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                with os.fdopen(descriptor, "w", encoding="utf-8") as target:
                    write_sync(target, content)
            except FileExistsError:
                return False
            except (OSError, UnicodeError):
                path.unlink(missing_ok=True)
                raise
        return True
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def exact_fields(text: str, names: tuple[str, ...]) -> dict[str, str] | None:
    matches = re.findall(r"^- (" + "|".join(names) + r"):[ \t]*(.+)$", text, re.MULTILINE)
    return dict(matches) if len(matches) == len(names) and {name for name, _ in matches} == set(names) else None


def header_block(text: str) -> str:
    return re.split(r"^## ", text, maxsplit=1, flags=re.MULTILINE)[0]


def awareness_errors(text: str, cfg: Config) -> list[str]:
    if len(text.encode("utf-8")) > 16 * 1024:
        return ["AWARENESS.md exceeds 16 KiB; compress it without splitting files"]
    if not text.startswith("# Project Awareness\n"):
        return ["AWARENESS.md must start with # Project Awareness"]
    fields = exact_fields(header_block(text), ("Updated", "Focus", "Sources checked"))
    if fields is None:
        return ["AWARENESS.md needs non-empty Updated, Focus, and Sources checked values"]
    try:
        date.fromisoformat(fields["Updated"])
    except ValueError:
        return ["AWARENESS.md Updated must be an ISO date"]
    if fields["Focus"] not in {"project", *cfg.allowed_scopes}:
        return ["AWARENESS.md Focus must be project or an exact allowed scope"]
    if not valid_checked_sources(fields["Sources checked"], cfg, fields["Focus"]):
        return ["AWARENESS.md Sources checked contains an unknown or unsafe reference"]
    headings = re.findall(r"^## (.+)$", text, re.MULTILINE)
    if headings != list(AWARENESS_SECTIONS):
        return ["AWARENESS.md must contain exactly the five required sections in order"]
    return ["secret-like content in AWARENESS.md"] if SECRET.search(text) else []


def valid_locator(value: str) -> bool:
    path = Path(value)
    return bool(value) and not path.is_absolute() and ".." not in path.parts


def valid_sources(value: str, cfg: Config, scope: str = "project") -> bool:
    configured = {source.id for source in cfg.sources}
    refs = [item.strip() for item in value.split(";") if item.strip()]
    if not refs:
        return False
    for ref in refs:
        if "#" not in ref:
            return False
        identifier, locator = ref.split("#", 1)
        if identifier == "project":
            project_path, separator, nested = locator.partition(":")
            if not valid_locator(project_path) or (separator and not valid_locator(nested)):
                return False
            candidate = resolve(project_path, cfg.root, strict=False)
            if not within(candidate, cfg.root):
                return False
            if is_office_memory_result(candidate, cfg):
                return False
            if scope != "project" and not within(candidate, resolve(scope, cfg.root, strict=False)):
                return False
        elif identifier not in configured or not valid_locator(locator):
            return False
    return True


def valid_checked_sources(value: str, cfg: Config, scope: str = "project") -> bool:
    configured = {source.id for source in cfg.sources}
    refs = [item.strip() for item in value.split(";") if item.strip()]
    return bool(refs) and all(item in configured or valid_sources(item, cfg, scope) for item in refs)


def daily_records(cfg: Config) -> tuple[list[Path], list[str]]:
    records: list[Path] = []
    errors: list[str] = []
    directory = cfg.memory.parent
    if not directory.exists():
        return records, errors
    canonical = {cfg.memory, cfg.awareness}
    for path in sorted(directory.iterdir()):
        if path in canonical or path.name == ".DS_Store":
            continue
        match = DAILY_FILE.fullmatch(path.name)
        if match is None:
            errors.append(f"unexpected project memory artifact: {path.name}")
            continue
        try:
            date.fromisoformat(match.group(1))
        except ValueError:
            errors.append(f"daily memory filename is not a valid date: {path.name}")
            continue
        if path.is_symlink() or not path.is_file():
            errors.append(f"unsafe daily memory path: {path.name}")
        else:
            records.append(path)
    return records, errors


def daily_errors(path: Path, text: str, cfg: Config) -> list[str]:
    errors: list[str] = []
    if len(text.encode("utf-8")) > 12 * 1024:
        return ["exceeds 12 KiB; curate it without splitting the day"]
    match = DAILY_FILE.fullmatch(path.name)
    if match is None:
        return ["invalid daily filename"]
    day = match.group(1)
    try:
        date.fromisoformat(day)
    except ValueError:
        errors.append("filename is not a valid date")
    if not text.startswith(f"# Daily Project Memory — {day}\n"):
        errors.append("heading date must match filename")
    fields = exact_fields(header_block(text), ("Focus", "Sources checked"))
    if fields is None:
        errors.append("needs non-empty Focus and Sources checked values")
    else:
        if fields["Focus"] not in {"project", *cfg.allowed_scopes}:
            errors.append("Focus must be project or an exact allowed scope")
        if not valid_checked_sources(fields["Sources checked"], cfg, fields["Focus"]):
            errors.append("Sources checked contains an unknown or unsafe reference")
    headings = re.findall(r"^## (.+)$", text, re.MULTILINE)
    if headings != list(DAILY_SECTIONS):
        errors.append("must contain exactly the four daily sections in order")
    elif not any(section.strip() for section in re.split(r"^## .+$", text, flags=re.MULTILINE)[1:]):
        errors.append("must contain at least one curated item")
    if SECRET.search(text):
        errors.append("contains secret-like content")
    return errors


def memory_errors(text: str, cfg: Config) -> list[str]:
    errors: list[str] = []
    if len(text.encode("utf-8")) > 64 * 1024:
        return ["MEMORY.md exceeds 64 KiB; compress it without splitting files"]
    if not text.startswith("# Project Memory\n"):
        return ["MEMORY.md must start with # Project Memory"]
    if SECRET.search(text):
        errors.append("secret-like content in MEMORY.md")
    sections = re.split(r"^## ([^\n]+)\n", text, flags=re.MULTILINE)
    keys: set[str] = set()
    if sections[0].strip() != "# Project Memory":
        errors.append("content outside memory entries")
    if len(sections) == 1:
        return errors
    for index in range(1, len(sections), 2):
        key, body = sections[index].strip(), sections[index + 1]
        if not KEY.fullmatch(key) or key in keys:
            errors.append(f"invalid or duplicate memory key: {key}")
        keys.add(key)
        fields = exact_fields(body.partition("\n\n")[0], ("Scope", "Kind", "Sources", "Observed", "Review"))
        if fields is None:
            errors.append(f"missing memory entry fields: {key}")
            continue
        metadata = "\n".join(f"- {field}: {fields.get(field, '')}" for field in ("Scope", "Kind", "Sources", "Observed", "Review"))
        summary = body.replace(metadata, "", 1)
        if not re.match(r"^\n[ \t]*\n\S", summary) or summary.lstrip().startswith("Summary:"):
            errors.append(f"missing memory entry fields: {key}")
            continue
        if fields["Scope"] not in {"project", *cfg.allowed_scopes}:
            errors.append(f"invalid scope: {key}")
        if fields["Kind"] not in KINDS:
            errors.append(f"invalid kind: {key}")
        if not valid_sources(fields["Sources"], cfg, fields["Scope"]):
            errors.append(f"invalid sources: {key}")
        for field in ("Observed", "Review"):
            try:
                parsed = date.fromisoformat(fields[field])
                if field == "Review" and parsed < date.today():
                    errors.append(f"expired review: {key}")
            except ValueError:
                errors.append(f"invalid date: {key}")
    return errors


def command_check(cfg: Config) -> int:
    daily, invalid = daily_records(cfg)
    output_json({
        "valid": True,
        "project_id": cfg.project_id,
        "source_ids": [source.id for source in cfg.sources],
        "outputs": {
            "awareness": {"path": cfg.awareness.relative_to(cfg.root).as_posix(), "exists": cfg.awareness.is_file()},
            "memory": {"path": cfg.memory.relative_to(cfg.root).as_posix(), "exists": cfg.memory.is_file()},
            "daily": {"directory": cfg.memory.parent.relative_to(cfg.root).as_posix(), "count": len(daily), "latest": daily[-1].stem if daily else None, "invalid": len(invalid)},
        },
    })
    return 0


def command_init(cfg: Config, apply: bool) -> int:
    plan = {"write_files": [cfg.awareness.relative_to(cfg.root).as_posix(), cfg.memory.relative_to(cfg.root).as_posix()], "never_overwrite": True}
    if not apply:
        output_json({"dry_run": True, "plan": plan})
        return 0
    for path in (cfg.awareness, cfg.memory):
        if path.exists() and not path.is_file():
            raise ContractError(f"output exists but is not a regular file: {path.name}")
    changed = []
    awareness = "# Project Awareness\n- Updated:\n- Focus:\n- Sources checked:\n\n" + "\n".join(f"## {heading}\n" for heading in AWARENESS_SECTIONS)
    if atomic_create(cfg.awareness, awareness):
        changed.append(plan["write_files"][0])
    if atomic_create(cfg.memory, "# Project Memory\n\n"):
        changed.append(plan["write_files"][1])
    output_json({"applied": True, "changed": changed, "never_overwrite": True})
    return 0


def command_validate(cfg: Config) -> int:
    errors: list[str] = []
    if not cfg.awareness.is_file():
        errors.append("AWARENESS.md is missing or not a regular file")
    else:
        errors.extend(awareness_errors(cfg.awareness.read_text(encoding="utf-8"), cfg))
    if not cfg.memory.is_file():
        errors.append("MEMORY.md is missing or not a regular file")
    else:
        errors.extend(memory_errors(cfg.memory.read_text(encoding="utf-8"), cfg))
    daily, daily_path_errors = daily_records(cfg)
    errors.extend(daily_path_errors)
    for path in daily:
        errors.extend(f"{path.name}: {error}" for error in daily_errors(path, path.read_text(encoding="utf-8"), cfg))
    output_json({"valid": not errors, "errors": errors})
    return 0 if not errors else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate two canonical office-memory results and AI-curated daily records.")
    parser.add_argument("command", choices=("check-config", "snapshot", "validate", "init"))
    parser.add_argument("--config", required=True, help="Path to office-memory.toml.")
    parser.add_argument("--source", action="append", default=[], help="Configured source id; repeatable.")
    parser.add_argument("--material", action="append", default=[], help="Explicit project-relative material path; repeatable.")
    parser.add_argument("--focus", help="project or an exact configured scope when materials are supplied.")
    parser.add_argument("--apply", action="store_true", help="Required for init writes; other commands never write.")
    args = parser.parse_args()
    try:
        cfg = load_config(args.config)
        if args.apply and args.command != "init":
            raise ContractError("--apply is valid only for init")
        if args.command != "snapshot" and (args.source or args.material or args.focus is not None):
            raise ContractError("--source, --material, and --focus are valid only for snapshot")
        if args.command == "check-config":
            return command_check(cfg)
        if args.command == "snapshot":
            materials = gate_materials(cfg, args.material)
            gate_focus(cfg, args.focus, materials)
            output_json(snapshot(cfg, args.source, materials))
            return 0
        if args.command == "init":
            return command_init(cfg, args.apply)
        return command_validate(cfg)
    except (ContractError, OSError, UnicodeError) as error:
        parser.error(str(error))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
