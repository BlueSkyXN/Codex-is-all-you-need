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
DEFAULT_CATALOG_DIR = REPO_ROOT / "examples" / "catalog"
PLUGIN_ONLY_SKILLS = frozenset({"core-router"})
WORD_RE = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_'-]*")
CHECKBOX_RE = re.compile(r"(?m)^\s*-\s+\[[ xX]\]")
DO_NOT_RE = re.compile(r"(?m)^## Do not\s*$")
DO_NOT_USE_WHEN_RE = re.compile(r"(?m)^## Do not use when\s*$")


def is_quoted_scalar(value: str) -> bool:
    return len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}


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
        if ": " in value and not is_quoted_scalar(value):
            errors.append(
                f"{path}: frontmatter value for {key!r} contains ': ' and must be quoted"
            )
            continue
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


def inspect_codex_manifest(
    plugin_dir: Path, errors: list[str]
) -> tuple[str, list[str], dict[str, Any] | None]:
    warnings: list[str] = []
    manifest = read_json(plugin_dir / ".codex-plugin" / "plugin.json", errors)
    if manifest is None:
        return "missing", warnings, None

    skills = manifest.get("skills")
    if isinstance(skills, str):
        target = plugin_dir / skills
        if not target.is_dir():
            errors.append(f"codex manifest skills path does not exist: {skills}")
        return "directory", warnings, manifest
    if isinstance(skills, list):
        for item in skills:
            if not isinstance(item, str):
                errors.append("codex manifest skills array contains non-string item")
                continue
            if not (plugin_dir / item).exists():
                errors.append(f"codex manifest skill path does not exist: {item}")
        return "explicit", warnings, manifest

    errors.append("codex manifest missing supported skills field")
    return "unsupported", warnings, manifest


def inspect_claude_manifest(
    plugin_dir: Path, errors: list[str]
) -> tuple[str, list[str], dict[str, Any] | None]:
    warnings: list[str] = []
    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    if not manifest_path.exists():
        warnings.append("claude manifest missing; Claude runtime semantics unverified")
        return "missing", warnings, None

    manifest = read_json(manifest_path, errors)
    if manifest is None:
        return "invalid", warnings, None

    skills = manifest.get("skills")
    if skills is None:
        warnings.append("claude manifest has no explicit skills field; runtime semantics unverified")
        return "implicit_or_unverified", warnings, manifest
    if isinstance(skills, list):
        for item in skills:
            if not isinstance(item, str):
                errors.append("claude manifest skills array contains non-string item")
                continue
            if not (plugin_dir / item).exists():
                errors.append(f"claude manifest skill path does not exist: {item}")
        return "explicit", warnings, manifest

    errors.append("claude manifest skills field is not an array")
    return "unsupported", warnings, manifest


def inspect_manifest_version_parity(
    codex_manifest: dict[str, Any] | None,
    claude_manifest: dict[str, Any] | None,
    errors: list[str],
) -> tuple[str | None, str | None]:
    codex_version = None
    claude_version = None

    if codex_manifest is not None:
        version = codex_manifest.get("version")
        if isinstance(version, str) and version:
            codex_version = version
        else:
            errors.append("codex manifest missing string version")

    if claude_manifest is not None:
        version = claude_manifest.get("version")
        if isinstance(version, str) and version:
            claude_version = version
        else:
            errors.append("claude manifest missing string version")

    if codex_version and claude_version and codex_version != claude_version:
        errors.append(
            f"manifest version mismatch: codex {codex_version} != claude {claude_version}"
        )

    return codex_version, claude_version


def discover_catalog_skills(catalog_dir: Path, errors: list[str]) -> list[str]:
    if not catalog_dir.is_dir():
        errors.append(f"missing source catalog directory: {catalog_dir}")
        return []

    skill_names: list[str] = []
    for path in sorted(catalog_dir.glob("*/skills/*")):
        if not path.is_dir() or path.name.startswith("."):
            continue
        if not (path / "SKILL.md").is_file():
            errors.append(f"missing catalog SKILL.md: {path}")
            continue
        skill_names.append(path.name)
    return skill_names


def run_check(
    plugin_dir: Path = DEFAULT_PLUGIN_DIR,
    catalog_dir: Path = DEFAULT_CATALOG_DIR,
) -> dict[str, Any]:
    plugin_dir = plugin_dir.resolve()
    catalog_dir = catalog_dir.resolve()
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

    codex_manifest_mode, codex_warnings, codex_manifest = inspect_codex_manifest(
        plugin_dir, errors
    )
    claude_manifest_mode, claude_warnings, claude_manifest = inspect_claude_manifest(
        plugin_dir, errors
    )
    warnings.extend(codex_warnings)
    warnings.extend(claude_warnings)
    codex_manifest_version, claude_manifest_version = inspect_manifest_version_parity(
        codex_manifest, claude_manifest, errors
    )

    catalog_skill_names = discover_catalog_skills(catalog_dir, errors)
    catalog_skill_set = set(catalog_skill_names)
    plugin_skill_set = set(skill_names)
    plugin_only_skills = sorted(plugin_skill_set - catalog_skill_set)
    unexpected_plugin_only = [
        name for name in plugin_only_skills if name not in PLUGIN_ONLY_SKILLS
    ]
    missing_from_plugin = sorted(catalog_skill_set - plugin_skill_set)
    if unexpected_plugin_only:
        errors.append(
            "plugin skills missing from source catalog: "
            + ", ".join(unexpected_plugin_only)
        )
    if missing_from_plugin:
        errors.append(
            "source catalog skills missing from plugin package: "
            + ", ".join(missing_from_plugin)
        )

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
        "codex_manifest_version": codex_manifest_version,
        "claude_manifest_mode": claude_manifest_mode,
        "claude_manifest_version": claude_manifest_version,
        "source_catalog_skills": len(catalog_skill_names),
        "plugin_only_skills": plugin_only_skills,
        "allowed_plugin_only_skills": sorted(PLUGIN_ONLY_SKILLS),
        "unexpected_plugin_only_skills": unexpected_plugin_only,
        "source_catalog_missing_from_plugin": missing_from_plugin,
        "readme_skill_mentions": len(readme_mentions),
        "readme_unmentioned": [
            name for name in skill_names if name not in readme_mentions
        ],
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
    print(f"- codex manifest version: {summary['codex_manifest_version']}")
    print(f"- claude manifest: {summary['claude_manifest_mode']}")
    print(f"- claude manifest version: {summary['claude_manifest_version']}")
    print(f"- source catalog skills: {summary['source_catalog_skills']}")
    print(
        "- plugin-only skills: "
        + (", ".join(summary["plugin_only_skills"]) or "none")
    )
    print(
        f"- README skill mentions: "
        f"{summary['readme_skill_mentions']}/{summary['skills']}"
    )

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
    parser.add_argument(
        "--catalog-dir",
        type=Path,
        default=DEFAULT_CATALOG_DIR,
        help="Path to the public source catalog.",
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args(argv)

    summary = run_check(args.plugin_dir, args.catalog_dir)
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print_text(summary)
    return 1 if summary["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
