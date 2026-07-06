#!/usr/bin/env python3
"""Check the packaged Codex Next skill surface."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLUGIN_DIR = REPO_ROOT / "plugins" / "codex-next"
WORD_RE = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_'-]*")
CHECKBOX_RE = re.compile(r"(?m)^\s*-\s+\[[ xX]\]")
DO_NOT_RE = re.compile(r"(?m)^## Do not\s*$")
DO_NOT_USE_WHEN_RE = re.compile(r"(?m)^## Do not use when\s*$")


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], list[str], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    errors: list[str] = []
    if not lines or lines[0].strip() != "---":
        return {}, [f"{path}: missing frontmatter"], text

    end_index: int | None = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = index
            break
    if end_index is None:
        return {}, [f"{path}: unterminated frontmatter"], text

    data: dict[str, Any] = {}
    for raw in lines[1:end_index]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if ":" not in raw:
            errors.append(f"{path}: unsupported frontmatter line: {raw}")
            continue
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value.lower() in {"true", "false"}:
            data[key] = value.lower() == "true"
        else:
            data[key] = value.strip("'\"")
    return data, errors, text


def read_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    if not path.is_file():
        errors.append(f"missing manifest: {path}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return None


def inspect_codex_manifest(plugin_dir: Path, errors: list[str]) -> tuple[str, list[str]]:
    warnings: list[str] = []
    manifest = read_json(plugin_dir / ".codex-plugin" / "plugin.json", errors)
    if manifest is None:
        return "missing", warnings

    skills = manifest.get("skills")
    if isinstance(skills, str):
        target = plugin_dir / skills
        if not target.is_dir():
            errors.append(f"codex manifest skills path does not exist: {skills}")
        return "directory", warnings
    if isinstance(skills, list):
        for item in skills:
            if not isinstance(item, str):
                errors.append("codex manifest skills array contains non-string item")
                continue
            if not (plugin_dir / item).exists():
                errors.append(f"codex manifest skill path does not exist: {item}")
        return "explicit", warnings

    errors.append("codex manifest missing supported skills field")
    return "unsupported", warnings


def inspect_claude_manifest(plugin_dir: Path, errors: list[str]) -> tuple[str, list[str]]:
    warnings: list[str] = []
    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    if not manifest_path.exists():
        warnings.append("claude manifest missing; Claude runtime semantics unverified")
        return "missing", warnings

    manifest = read_json(manifest_path, errors)
    if manifest is None:
        return "invalid", warnings

    skills = manifest.get("skills")
    if skills is None:
        warnings.append("claude manifest has no explicit skills field; runtime semantics unverified")
        return "implicit_or_unverified", warnings
    if isinstance(skills, list):
        for item in skills:
            if not isinstance(item, str):
                errors.append("claude manifest skills array contains non-string item")
                continue
            if not (plugin_dir / item).exists():
                errors.append(f"claude manifest skill path does not exist: {item}")
        return "explicit", warnings

    errors.append("claude manifest skills field is not an array")
    return "unsupported", warnings


def run_check(plugin_dir: Path = DEFAULT_PLUGIN_DIR) -> dict[str, Any]:
    plugin_dir = plugin_dir.resolve()
    skills_dir = plugin_dir / "skills"
    errors: list[str] = []
    warnings: list[str] = []

    if skills_dir.is_dir():
        skill_dirs = sorted(
            path
            for path in skills_dir.iterdir()
            if path.is_dir() and not path.name.startswith(".")
        )
    else:
        errors.append(f"missing skills directory: {skills_dir}")
        skill_dirs = []
    model_invoked = 0
    user_invoked = 0
    description_words = 0
    references_dirs = 0
    scripts_dirs = 0
    checkbox_markers = 0
    do_not_sections = 0
    do_not_use_when_sections = 0
    skill_names: list[str] = []

    for skill_dir in skill_dirs:
        skill_names.append(skill_dir.name)
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"missing SKILL.md: {skill_dir}")
            continue

        frontmatter, fm_errors, text = parse_frontmatter(skill_file)
        errors.extend(fm_errors)

        name = frontmatter.get("name")
        if name != skill_dir.name:
            errors.append(
                f"{skill_file}: frontmatter name {name!r} does not match directory {skill_dir.name!r}"
            )

        description = frontmatter.get("description")
        if not isinstance(description, str) or not description.strip():
            errors.append(f"{skill_file}: missing description")
        else:
            description_words += len(WORD_RE.findall(description))

        disable = frontmatter.get("disable-model-invocation", False)
        if isinstance(disable, bool):
            if disable:
                user_invoked += 1
            else:
                model_invoked += 1
        else:
            errors.append(f"{skill_file}: disable-model-invocation must be true or false")

        references_dirs += int((skill_dir / "references").is_dir())
        scripts_dirs += int((skill_dir / "scripts").is_dir())
        checkbox_markers += len(CHECKBOX_RE.findall(text))
        do_not_sections += len(DO_NOT_RE.findall(text))
        do_not_use_when_sections += len(DO_NOT_USE_WHEN_RE.findall(text))

    codex_manifest_mode, codex_warnings = inspect_codex_manifest(plugin_dir, errors)
    claude_manifest_mode, claude_warnings = inspect_claude_manifest(plugin_dir, errors)
    warnings.extend(codex_warnings)
    warnings.extend(claude_warnings)

    readme = plugin_dir / "README.md"
    readme_mentions: list[str] = []
    if readme.is_file():
        readme_text = readme.read_text(encoding="utf-8")
        readme_mentions = [name for name in skill_names if name in readme_text]
        if "core-router" not in readme_text:
            warnings.append("README does not mention core-router")
    else:
        warnings.append("README.md missing from plugin package")

    return {
        "plugin_dir": str(plugin_dir),
        "skills": len(skill_dirs),
        "skill_names": skill_names,
        "model_invoked": model_invoked,
        "user_invoked": user_invoked,
        "description_words": description_words,
        "references_dirs": references_dirs,
        "scripts_dirs": scripts_dirs,
        "checkbox_markers": checkbox_markers,
        "do_not_sections": do_not_sections,
        "do_not_use_when_sections": do_not_use_when_sections,
        "codex_manifest_mode": codex_manifest_mode,
        "claude_manifest_mode": claude_manifest_mode,
        "readme_skill_mentions": len(readme_mentions),
        "readme_unmentioned": [name for name in skill_names if name not in readme_mentions],
        "warnings": warnings,
        "errors": errors,
    }


def print_text(summary: dict[str, Any]) -> None:
    print("Codex Next surface check")
    print(f"- skills: {summary['skills']}")
    print(f"- model-invoked: {summary['model_invoked']}")
    print(f"- user-invoked: {summary['user_invoked']}")
    print(f"- description words: {summary['description_words']}")
    print(f"- references dirs: {summary['references_dirs']}")
    print(f"- scripts dirs: {summary['scripts_dirs']}")
    print(f"- checkbox markers: {summary['checkbox_markers']}")
    print(f"- do-not behavior sections: {summary['do_not_sections']}")
    print(f"- do-not-use-when sections: {summary['do_not_use_when_sections']}")
    print(f"- codex manifest: {summary['codex_manifest_mode']}")
    print(f"- claude manifest: {summary['claude_manifest_mode']}")
    print(f"- README skill mentions: {summary['readme_skill_mentions']}/{summary['skills']}")

    if summary["warnings"]:
        print("\nWARNINGS")
        for warning in summary["warnings"]:
            print(f"- {warning}")

    if summary["errors"]:
        print("\nERRORS")
        for error in summary["errors"]:
            print(f"- {error}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--plugin-dir",
        type=Path,
        default=DEFAULT_PLUGIN_DIR,
        help="Path to the Codex Next plugin package.",
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args(argv)

    summary = run_check(args.plugin_dir)
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print_text(summary)
    return 1 if summary["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
