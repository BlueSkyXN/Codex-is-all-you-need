#!/usr/bin/env python3
"""Build a read-only Codex preset dashboard from filesystem state."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tomllib
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_CONFIG = Path.home() / ".codex" / "dashboard" / "config.toml"
SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE = SCRIPT_DIR / "templates" / "index.html"


def expand_path(value: str | Path) -> Path:
    return Path(os.path.expanduser(str(value))).resolve(strict=False)


def safe_readlink(path: Path) -> str | None:
    if not path.is_symlink():
        return None
    try:
        return os.readlink(path)
    except OSError:
        return None


def is_inside(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=False))
        return True
    except ValueError:
        return False


def classify_path(path: Path, *, codex_root: Path, private_roots: list[Path], public_roots: list[Path]) -> str:
    resolved = path.resolve(strict=False)
    if any(is_inside(resolved, root) for root in private_roots):
        return "private"
    if any(is_inside(resolved, root) for root in public_roots):
        return "public"
    if is_inside(resolved, codex_root):
        return "production"
    return "external"


def add_issue(issues: list[dict[str, str]], severity: str, area: str, message: str, path: Path | str | None = None) -> None:
    item = {"severity": severity, "area": area, "message": message}
    if path is not None:
        item["path"] = str(path)
    issues.append(item)


def load_config(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise SystemExit(f"Missing config: {path}")
    with path.open("rb") as fh:
        config = tomllib.load(fh)
    if "source" not in config:
        raise SystemExit("Config missing [source]")
    return config


def parse_agent_toml(path: Path, issues: list[dict[str, str]]) -> tuple[dict[str, Any], bool]:
    try:
        with path.open("rb") as fh:
            data = tomllib.load(fh)
        return data, True
    except Exception as exc:  # noqa: BLE001 - report parse failures in dashboard state
        add_issue(issues, "error", "agent", f"Invalid TOML: {exc}", path)
        return {}, False


def extract_recommended_skills(text: str, skill_names: set[str]) -> list[str]:
    """Read explicit `Recommended skills:` hints without substring false positives."""
    found: set[str] = set()
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line.lower().startswith("recommended skills:"):
            continue
        _, _, value = line.partition(":")
        for item in value.split(","):
            name = item.strip().strip(".` ")
            if name.lower().startswith("or "):
                name = name[3:].strip().strip(".` ")
            if name in skill_names:
                found.add(name)
    return sorted(found)


def list_group_dirs(codex_root: Path) -> list[Path]:
    if not codex_root.is_dir():
        return []
    groups = []
    for child in sorted(codex_root.iterdir(), key=lambda p: p.name):
        if child.name.startswith("."):
            continue
        if (child / "agents").is_dir() or (child / "skills").is_dir():
            groups.append(child)
    return groups


def scan_source(
    codex_root: Path,
    private_roots: list[Path],
    public_roots: list[Path],
    issues: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    agents: list[dict[str, Any]] = []
    skills: list[dict[str, Any]] = []
    groups: list[dict[str, Any]] = []

    if not codex_root.is_dir():
        add_issue(issues, "error", "source", "codex_root does not exist or is not a directory", codex_root)
        return groups, agents, skills

    for group_dir in list_group_dirs(codex_root):
        group_name = group_dir.name
        group_agents: list[dict[str, Any]] = []
        group_skills: list[dict[str, Any]] = []

        agents_dir = group_dir / "agents"
        if agents_dir.is_dir():
            for path in sorted(agents_dir.glob("*.toml"), key=lambda p: p.name):
                data, valid = parse_agent_toml(path, issues)
                nicknames = data.get("nickname_candidates") or []
                if isinstance(nicknames, str):
                    nicknames = [nicknames]
                if isinstance(nicknames, list) and len(nicknames) > 1:
                    add_issue(issues, "warning", "agent", "nickname_candidates has more than one entry", path)
                agent = {
                    "name": path.stem,
                    "group": group_name,
                    "path": str(path),
                    "realpath": str(path.resolve(strict=False)),
                    "is_symlink": path.is_symlink(),
                    "valid_toml": valid,
                    "nickname": nicknames[0] if isinstance(nicknames, list) and nicknames else "",
                    "developer_instructions": data.get("developer_instructions", ""),
                    "recommended_skills": [],
                    "used_by_suites": [],
                }
                agents.append(agent)
                group_agents.append(agent)

        skills_dir = group_dir / "skills"
        if skills_dir.is_dir():
            for path in sorted(skills_dir.iterdir(), key=lambda p: p.name):
                if path.name.startswith("."):
                    continue
                exists = path.exists()
                has_skill = (path / "SKILL.md").is_file()
                realpath = path.resolve(strict=False)
                if path.is_symlink() and not exists:
                    add_issue(issues, "error", "skill", "Broken source skill symlink", path)
                if exists and not has_skill:
                    add_issue(issues, "error", "skill", "Source skill missing SKILL.md", path)
                skill = {
                    "name": path.name,
                    "group": group_name,
                    "path": str(path),
                    "realpath": str(realpath),
                    "is_symlink": path.is_symlink(),
                    "target": safe_readlink(path) or "",
                    "exists": exists,
                    "has_skill": has_skill,
                    "scope": classify_path(realpath, codex_root=codex_root, private_roots=private_roots, public_roots=public_roots),
                    "used_by_suites": [],
                }
                skills.append(skill)
                group_skills.append(skill)

        groups.append(
            {
                "name": group_name,
                "agents": len(group_agents),
                "skills": len(group_skills),
                "private_skills": sum(1 for item in group_skills if item["scope"] == "private"),
            }
        )

    skill_names = {skill["name"] for skill in skills}
    for agent in agents:
        text = str(agent.get("developer_instructions") or "")
        agent["recommended_skills"] = extract_recommended_skills(text, skill_names)

    return groups, agents, skills


def scan_suites(
    suites_root: Path,
    agents: list[dict[str, Any]],
    skills: list[dict[str, Any]],
    issues: list[dict[str, str]],
) -> list[dict[str, Any]]:
    suite_items: list[dict[str, Any]] = []
    agents_by_real = {item["realpath"]: item for item in agents}
    skills_by_real = {item["realpath"]: item for item in skills}

    if not suites_root.is_dir():
        add_issue(issues, "error", "suite", "suites_root does not exist or is not a directory", suites_root)
        return suite_items

    for suite_dir in sorted((p for p in suites_root.iterdir() if p.is_dir()), key=lambda p: p.name):
        suite_agents: list[dict[str, Any]] = []
        suite_skills: list[dict[str, Any]] = []

        for kind, bucket, source_by_real in (
            ("agents", suite_agents, agents_by_real),
            ("skills", suite_skills, skills_by_real),
        ):
            kind_dir = suite_dir / kind
            if not kind_dir.is_dir():
                add_issue(issues, "error", "suite", f"Suite missing {kind}/ directory", kind_dir)
                continue
            for entry in sorted(kind_dir.iterdir(), key=lambda p: p.name):
                if entry.name.startswith("."):
                    continue
                realpath = str(entry.resolve(strict=False))
                source = source_by_real.get(realpath)
                if not entry.is_symlink():
                    add_issue(issues, "warning", "suite", f"Suite {kind} entry is not a symlink", entry)
                if entry.is_symlink() and not entry.exists():
                    add_issue(issues, "error", "suite", f"Broken suite {kind} symlink", entry)
                if kind == "skills" and entry.exists() and not (entry / "SKILL.md").is_file():
                    add_issue(issues, "error", "suite", "Suite skill target missing SKILL.md", entry)
                if source is not None:
                    source["used_by_suites"].append(suite_dir.name)
                bucket.append(
                    {
                        "name": entry.stem if kind == "agents" else entry.name,
                        "path": str(entry),
                        "target": safe_readlink(entry) or "",
                        "realpath": realpath,
                        "is_symlink": entry.is_symlink(),
                        "exists": entry.exists(),
                        "source_group": source.get("group", "") if source else "",
                        "source_scope": source.get("scope", "production") if source else "",
                    }
                )

        suite_items.append(
            {
                "name": suite_dir.name,
                "path": str(suite_dir),
                "agents": suite_agents,
                "skills": suite_skills,
                "agent_count": len(suite_agents),
                "skill_count": len(suite_skills),
                "private_skill_count": sum(1 for item in suite_skills if item.get("source_scope") == "private"),
            }
        )

    return suite_items


def inspect_runtime_entry(entry: Path) -> dict[str, Any]:
    return {
        "path": str(entry),
        "exists": entry.exists() or entry.is_symlink(),
        "is_symlink": entry.is_symlink(),
        "target": safe_readlink(entry) or "",
        "realpath": str(entry.resolve(strict=False)),
        "is_dir": entry.is_dir(),
    }


def scan_runtimes(config: dict[str, Any], suites_root: Path, issues: list[dict[str, str]]) -> list[dict[str, Any]]:
    runtimes: list[dict[str, Any]] = []
    for item in config.get("runtimes", []):
        name = item.get("name") or item.get("path") or "runtime"
        runtime_path = expand_path(item["path"])
        expected_suite = item.get("expected_suite", "")
        codex_dir = runtime_path / ".codex"
        agents_entry = codex_dir / "agents"
        skills_entry = codex_dir / "skills"
        agents_info = inspect_runtime_entry(agents_entry)
        skills_info = inspect_runtime_entry(skills_entry)

        expected_agents = suites_root / expected_suite / "agents" if expected_suite else None
        expected_skills = suites_root / expected_suite / "skills" if expected_suite else None
        agents_ok = bool(expected_agents and agents_info["is_symlink"] and expand_path(agents_info["realpath"]) == expected_agents.resolve(strict=False))
        skills_ok = bool(expected_skills and skills_info["is_symlink"] and expand_path(skills_info["realpath"]) == expected_skills.resolve(strict=False))

        occupied = any(info["exists"] and not info["is_symlink"] for info in (agents_info, skills_info))
        if agents_ok and skills_ok:
            status = "connected"
        elif not agents_info["exists"] and not skills_info["exists"]:
            status = "missing"
        elif occupied:
            status = "occupied"
        elif agents_ok or skills_ok:
            status = "partial"
        else:
            status = "wrong-target" if agents_info["exists"] or skills_info["exists"] else "missing"

        if status in {"wrong-target", "occupied", "partial"}:
            add_issue(issues, "warning", "runtime", f"Runtime {name} status is {status}", runtime_path)

        runtimes.append(
            {
                "name": name,
                "path": str(runtime_path),
                "codex_dir": str(codex_dir),
                "expected_suite": expected_suite,
                "status": status,
                "agents": agents_info,
                "skills": skills_info,
            }
        )

    forbidden_roots = config.get("checks", {}).get("forbidden_runtime_roots", [])
    for raw_root in forbidden_roots:
        root = expand_path(raw_root)
        forbidden = root / ".codex"
        if forbidden.exists() or forbidden.is_symlink():
            add_issue(issues, "warning", "runtime", "Forbidden root-level .codex exists; inspect before deploying suites", forbidden)

    return runtimes


def build_state(config_path: Path) -> tuple[dict[str, Any], Path, Path]:
    config = load_config(config_path)
    source = config["source"]
    codex_root = expand_path(source["codex_root"])
    suites_root = expand_path(source["suites_root"])
    private_roots = [expand_path(p) for p in source.get("private_roots", [])]
    public_roots = [expand_path(p) for p in source.get("public_roots", [])]
    issues: list[dict[str, str]] = []

    groups, agents, skills = scan_source(codex_root, private_roots, public_roots, issues)
    suites = scan_suites(suites_root, agents, skills, issues)
    runtimes = scan_runtimes(config, suites_root, issues)

    output = config.get("output", {})
    output_dir = expand_path(output.get("dir", Path.home() / ".codex" / "dashboard"))
    state_path = output_dir / output.get("state_file", "preset-state.json")
    html_path = output_dir / output.get("html_file", "index.html")

    state = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "config_path": str(config_path),
        "source": {
            "name": source.get("name", "local production"),
            "codex_root": str(codex_root),
            "suites_root": str(suites_root),
            "private_roots": [str(p) for p in private_roots],
            "public_roots": [str(p) for p in public_roots],
        },
        "summary": {
            "groups": len(groups),
            "agents": len(agents),
            "skills": len(skills),
            "private_skills": sum(1 for item in skills if item["scope"] == "private"),
            "suites": len(suites),
            "suite_agent_links": sum(item["agent_count"] for item in suites),
            "suite_skill_links": sum(item["skill_count"] for item in suites),
            "runtimes": len(runtimes),
            "connected_runtimes": sum(1 for item in runtimes if item["status"] == "connected"),
            "issues": len(issues),
            "errors": sum(1 for item in issues if item["severity"] == "error"),
            "warnings": sum(1 for item in issues if item["severity"] == "warning"),
        },
        "groups": groups,
        "agents": agents,
        "skills": skills,
        "suites": suites,
        "runtimes": runtimes,
        "issues": issues,
    }
    return state, state_path, html_path


def render_html(state: dict[str, Any], html_path: Path) -> None:
    if not TEMPLATE.is_file():
        raise SystemExit(f"Missing template: {TEMPLATE}")
    template = TEMPLATE.read_text(encoding="utf-8")
    payload = json.dumps(state, ensure_ascii=False, indent=2)
    html = template.replace("__STATE_JSON__", payload)
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(html, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a read-only Codex preset dashboard.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help=f"Config TOML path. Default: {DEFAULT_CONFIG}")
    parser.add_argument("--json-only", action="store_true", help="Write JSON state without rendering HTML.")
    args = parser.parse_args(argv)

    state, state_path, html_path = build_state(args.config.resolve(strict=False))
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not args.json_only:
        render_html(state, html_path)

    print(f"state: {state_path}")
    if not args.json_only:
        print(f"html:  {html_path}")
    print(
        "summary: "
        f"groups={state['summary']['groups']} "
        f"agents={state['summary']['agents']} "
        f"skills={state['summary']['skills']} "
        f"suites={state['summary']['suites']} "
        f"issues={state['summary']['issues']}"
    )
    if shutil.which("open") and not args.json_only:
        print(f"open:  open {html_path}")
    return 0 if state["summary"]["errors"] == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
