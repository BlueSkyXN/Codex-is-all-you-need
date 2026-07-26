#!/usr/bin/env python3
"""Check the packaged Codex Next skill surface."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
_METADATA_SPEC = importlib.util.spec_from_file_location(
    "check_skill_metadata", REPO_ROOT / "scripts" / "check_skill_metadata.py"
)
assert _METADATA_SPEC is not None and _METADATA_SPEC.loader is not None
_METADATA_MODULE = sys.modules.get(_METADATA_SPEC.name)
if _METADATA_MODULE is None:
    _METADATA_MODULE = importlib.util.module_from_spec(_METADATA_SPEC)
    sys.modules[_METADATA_SPEC.name] = _METADATA_MODULE
    _METADATA_SPEC.loader.exec_module(_METADATA_MODULE)
read_skill_metadata = _METADATA_MODULE.read_metadata
DEFAULT_PLUGIN_DIR = REPO_ROOT / "plugins" / "codex-next"
DEFAULT_CATALOG_DIR = REPO_ROOT / "examples" / "catalog"
PLUGIN_ONLY_SKILLS = frozenset({"core-router"})
EXPLICIT_CONTROL_SKILLS = frozenset(
    {
        "core-explore-unknowns",
        "core-goal-run",
        "core-grilling",
        "core-skill-eval",
        "sdlc-change-control",
        "sdlc-manager",
        "sdlc-readiness-review",
        "sdlc-requirements-workflow",
        "sdlc-router",
        "sdlc-solution-spec-workflow",
    }
)
EXPLICIT_HANDOFF_CONTRACT = (
    "When this workflow recommends an explicit-control skill, return its exact "
    "`$codex-next:<skill-name>` command as a recommendation only. Do not invoke, "
    "imitate, or begin the target skill. Stop this workflow and wait for the user "
    "to invoke that command explicitly; authorization for this skill does not "
    "transfer to another skill."
)
OPENAI_SIDECAR_FIELDS = {
    "interface": frozenset({"display_name", "short_description"}),
    "policy": frozenset({"allow_implicit_invocation"}),
}
JUNK_FILES = frozenset({".DS_Store", "Thumbs.db", "desktop.ini"})
WORD_RE = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_'-]*")
CHECKBOX_RE = re.compile(r"(?m)^\s*-\s+\[[ xX]\]")
DO_NOT_RE = re.compile(r"(?m)^## Do not\s*$")
DO_NOT_USE_WHEN_RE = re.compile(r"(?m)^## Do not use when\s*$")

# Agent Skills spec constraints (agentskills specification.md).
SPEC_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SPEC_NAME_MAX = 64
SPEC_DESCRIPTION_MAX = 1024
SPEC_COMPATIBILITY_MAX = 500
SPEC_BODY_LINE_BUDGET = 500
SPEC_FRONTMATTER_FIELDS = frozenset(
    {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
)
# Runtime extensions this repo deliberately allows on top of the spec fields.
FRONTMATTER_EXTENSIONS = frozenset({"disable-model-invocation"})
PARENT_REF_RE = re.compile(r"(?<![\w./])(?:\.\./)+[A-Za-z0-9_\-./]+")
MARKDOWN_LINK_RE = re.compile(r"\]\(([^)\s]+)\)")


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
        if raw[0] in {" ", "\t"}:
            # Nested value of a mapping field such as `metadata`; the spec
            # allows these, and they are not top-level keys.
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
            if is_quoted_scalar(value):
                value = value[1:-1]
            data[key] = value
    return data, errors, text


def check_spec_frontmatter(
    skill_file: Path,
    frontmatter: dict[str, Any],
    errors: list[str],
) -> None:
    """Enforce Agent Skills spec frontmatter constraints."""
    name = frontmatter.get("name")
    if isinstance(name, str):
        if len(name) > SPEC_NAME_MAX:
            errors.append(f"{skill_file}: name exceeds {SPEC_NAME_MAX} characters")
        if not SPEC_NAME_RE.fullmatch(name):
            errors.append(
                f"{skill_file}: name {name!r} violates spec charset "
                "(lowercase a-z, 0-9, single hyphens, no edge hyphens)"
            )

    description = frontmatter.get("description")
    if isinstance(description, str) and len(description) > SPEC_DESCRIPTION_MAX:
        errors.append(
            f"{skill_file}: description exceeds {SPEC_DESCRIPTION_MAX} characters"
        )

    compatibility = frontmatter.get("compatibility")
    if compatibility is not None:
        if not isinstance(compatibility, str) or not compatibility.strip():
            errors.append(f"{skill_file}: compatibility must be a non-empty string")
        elif len(compatibility) > SPEC_COMPATIBILITY_MAX:
            errors.append(
                f"{skill_file}: compatibility exceeds {SPEC_COMPATIBILITY_MAX} characters"
            )

    for key in frontmatter:
        if key not in SPEC_FRONTMATTER_FIELDS and key not in FRONTMATTER_EXTENSIONS:
            errors.append(
                f"{skill_file}: frontmatter field {key!r} is neither an Agent Skills "
                "spec field nor an allowlisted extension"
            )


def check_skill_references(skill_dir: Path, errors: list[str]) -> None:
    """Require relative references to resolve within the publishable skill root."""
    reference_root = skill_dir.parent.resolve()
    for md_file in sorted(skill_dir.rglob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        for match in PARENT_REF_RE.finditer(text):
            target = md_file.parent / match.group(0)
            if reference_escapes_root(target, reference_root):
                errors.append(
                    f"{md_file}: parent-path reference escapes skill root: {match.group(0)}"
                )
            elif not reference_exists(target, require_file=True):
                errors.append(
                    f"{md_file}: parent-path reference does not resolve: {match.group(0)}"
                )
        for match in MARKDOWN_LINK_RE.finditer(text):
            href = match.group(1)
            if href.startswith(("http://", "https://", "mailto:", "/")):
                continue
            path_part = href.split("#", 1)[0].split("?", 1)[0]
            if not path_part:
                continue
            target = md_file.parent / path_part
            if reference_escapes_root(target, reference_root):
                errors.append(f"{md_file}: relative link escapes skill root: {href}")
            elif not reference_exists(target, require_file=False):
                errors.append(f"{md_file}: relative link does not resolve: {href}")


def mask_non_behavioral_markdown(text: str) -> str:
    """Mask fenced blocks and HTML comments while preserving offsets and lines."""
    masked = list(text)

    for match in re.finditer(r"<!--.*?-->", text, re.DOTALL):
        for index in range(match.start(), match.end()):
            if masked[index] != "\n":
                masked[index] = " "

    fence_char: str | None = None
    fence_length = 0
    offset = 0
    for line in text.splitlines(keepends=True):
        stripped = line.lstrip(" \t")
        fence_match = re.match(r"(`{3,}|~{3,})", stripped)
        in_fence = fence_char is not None
        opens_fence = not in_fence and fence_match is not None
        closes_fence = False
        if in_fence and fence_match is not None:
            fence = fence_match.group(1)
            closes_fence = (
                fence[0] == fence_char
                and len(fence) >= fence_length
                and not stripped[len(fence) :].strip()
            )

        if in_fence or opens_fence:
            for index in range(offset, offset + len(line)):
                if masked[index] != "\n":
                    masked[index] = " "

        if opens_fence:
            assert fence_match is not None
            fence = fence_match.group(1)
            fence_char = fence[0]
            fence_length = len(fence)
        elif closes_fence:
            fence_char = None
            fence_length = 0
        offset += len(line)

    return "".join(masked)


def check_explicit_control_references(
    skill_dir: Path,
    text: str,
    errors: list[str],
) -> None:
    """Fail closed on non-canonical cross-skill explicit-control references."""
    visible = mask_non_behavioral_markdown(text)
    owner = skill_dir.name
    cross_skill_commands: set[str] = set()

    for target in sorted(EXPLICIT_CONTROL_SKILLS):
        if target == owner:
            continue

        target_pattern = re.compile(
            rf"(?<![A-Za-z0-9-]){re.escape(target)}(?![A-Za-z0-9-])",
            re.IGNORECASE,
        )
        command_pattern = re.compile(
            rf"(?<![A-Za-z0-9_$:/.-])\$codex-next:{re.escape(target)}"
            r"(?![A-Za-z0-9_:/.-])"
        )
        safe_reference_pattern = re.compile(
            rf"(?<![A-Za-z0-9_.-])\.\./{re.escape(target)}/references"
            r"(?:/[A-Za-z0-9_-][A-Za-z0-9_.-]*)+"
            r"(?:#[A-Za-z0-9_.:-]+)?"
            r"(?![A-Za-z0-9_./#?=&%+-])"
        )
        allowed_spans = [
            match.span()
            for pattern in (command_pattern, safe_reference_pattern)
            for match in pattern.finditer(text)
        ]
        if command_pattern.search(visible):
            cross_skill_commands.add(target)

        for match in target_pattern.finditer(text):
            if any(
                allowed_start <= match.start() and match.end() <= allowed_end
                for allowed_start, allowed_end in allowed_spans
            ):
                continue
            line_number = text.count("\n", 0, match.start()) + 1
            errors.append(
                f"{skill_dir / 'SKILL.md'}:{line_number}: explicit-control skill "
                f"{target!r} must use exact command "
                f"`$codex-next:{target}`; only sibling references/ paths are "
                "allowed as non-invocation technical references"
            )

    if cross_skill_commands:
        compact = " ".join(visible.split())
        contract_index = compact.find(EXPLICIT_HANDOFF_CONTRACT)
        first_command_index = min(
            compact.find(f"$codex-next:{target}")
            for target in cross_skill_commands
        )
        if contract_index < 0 or contract_index > first_command_index:
            errors.append(
                f"{skill_dir / 'SKILL.md'}: exact explicit-control commands require "
                "a preceding visible recommend-only, do-not-invoke, stop, wait, "
                "and non-transitive authorization contract"
            )


def reference_escapes_root(target: Path, reference_root: Path) -> bool:
    try:
        target.resolve(strict=False).relative_to(reference_root)
    except (OSError, ValueError):
        return True
    return False


def reference_exists(target: Path, *, require_file: bool) -> bool:
    try:
        resolved = target.resolve(strict=False)
    except OSError:
        return False
    return resolved.is_file() if require_file else resolved.exists()


def read_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    if not path.is_file():
        errors.append(f"missing manifest: {path}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return None


def parse_openai_sidecar(
    path: Path, errors: list[str]
) -> dict[str, dict[str, Any]]:
    """Read the canonical stdlib-only agents/openai.yaml subset.

    The authoritative plugin validator owns general YAML validation. This
    repository deliberately accepts a stricter two-level subset so invocation
    policy cannot be interpreted differently by this gate and the validator.
    Any unsupported syntax fails closed instead of being ignored.
    """
    data: dict[str, dict[str, Any]] = {}
    section: str | None = None
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        errors.append(f"{path}: cannot read OpenAI skill metadata: {exc}")
        return data

    for line_number, raw in enumerate(lines, start=1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        leading = raw[: len(raw) - len(raw.lstrip())]
        if "\t" in leading:
            errors.append(
                f"{path}:{line_number}: tabs are not supported in YAML indentation"
            )
            continue

        indent = len(raw) - len(raw.lstrip(" "))
        stripped = raw.strip()
        if indent == 0:
            if not stripped.endswith(":") or stripped.count(":") != 1:
                errors.append(
                    f"{path}:{line_number}: expected a top-level YAML mapping"
                )
                section = None
                continue
            candidate = stripped[:-1]
            if candidate not in OPENAI_SIDECAR_FIELDS:
                errors.append(
                    f"{path}:{line_number}: unsupported top-level section "
                    f"{candidate!r}"
                )
                section = None
                continue
            if candidate in data:
                errors.append(
                    f"{path}:{line_number}: duplicate top-level section "
                    f"{candidate!r}"
                )
                section = None
                continue
            section = candidate
            data[section] = {}
            continue

        if indent != 2:
            errors.append(
                f"{path}:{line_number}: unsupported indentation; "
                "sidecar fields must use exactly two spaces"
            )
            continue
        if section is None:
            errors.append(
                f"{path}:{line_number}: sidecar field has no recognized "
                "top-level section"
            )
            continue
        if ":" not in stripped:
            errors.append(f"{path}:{line_number}: expected key: value")
            continue
        key, raw_value = stripped.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if key not in OPENAI_SIDECAR_FIELDS[section]:
            errors.append(
                f"{path}:{line_number}: unsupported {section} field {key!r}"
            )
            continue
        if key in data[section]:
            errors.append(
                f"{path}:{line_number}: duplicate {section} field {key!r}"
            )
            continue

        if section == "interface":
            try:
                parsed = json.loads(value)
            except json.JSONDecodeError:
                errors.append(
                    f"{path}:{line_number}: interface.{key} must be a "
                    "double-quoted JSON string"
                )
                continue
            if not isinstance(parsed, str):
                errors.append(
                    f"{path}:{line_number}: interface.{key} must be a string"
                )
                continue
        elif value in {"true", "false"}:
            parsed = value == "true"
        else:
            errors.append(
                f"{path}:{line_number}: policy.{key} must be true or false"
            )
            continue
        data[section][key] = parsed
    return data


def inspect_openai_sidecar(
    skill_dir: Path, *, errors: list[str]
) -> tuple[bool, bool | None]:
    """Validate and return Codex invocation policy for one skill."""
    sidecar = skill_dir / "agents" / "openai.yaml"
    if not sidecar.is_file():
        return False, None

    data = parse_openai_sidecar(sidecar, errors)
    interface = data.get("interface", {})
    for key in ("display_name", "short_description"):
        value = interface.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{sidecar}: interface.{key} must be a non-empty string")

    policy = data.get("policy", {})
    allow_implicit = policy.get("allow_implicit_invocation")
    if allow_implicit is not None and not isinstance(allow_implicit, bool):
        errors.append(
            f"{sidecar}: policy.allow_implicit_invocation must be true or false"
        )
    return True, allow_implicit if isinstance(allow_implicit, bool) else None


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
        # Codex Next is a multi-skill package whose cross-runtime surface lives
        # in the standard root-level skills/ directory.
        default_skills = plugin_dir / "skills"
        if not default_skills.is_dir():
            errors.append("codex-next Claude default skills directory does not exist: ./skills/")
            return "missing_default_directory", warnings, manifest
        return "default_directory", warnings, manifest
    if isinstance(skills, str):
        check_codex_next_claude_skill_path(plugin_dir, skills, errors)
        return "explicit", warnings, manifest
    if isinstance(skills, list):
        for item in skills:
            if not isinstance(item, str):
                errors.append("claude manifest skills array contains non-string item")
                continue
            check_codex_next_claude_skill_path(plugin_dir, item, errors)
        return "explicit", warnings, manifest

    errors.append("claude manifest skills field is not a string or array")
    return "unsupported", warnings, manifest


def check_codex_next_claude_skill_path(
    plugin_dir: Path, item: str, errors: list[str]
) -> None:
    """Keep Claude paths inside Codex Next's canonical packaged skill surface."""
    if not item.startswith("./"):
        errors.append(f"claude manifest skill path must start with './': {item}")
        return

    target = plugin_dir / item
    if reference_escapes_root(target, plugin_dir.resolve()):
        errors.append(f"claude manifest skill path escapes plugin root: {item}")
        return
    if not target.exists():
        errors.append(f"claude manifest skill path does not exist: {item}")
        return
    if not target.is_dir():
        errors.append(f"claude manifest skill path is not a directory: {item}")
        return

    # Codex Next keeps one cross-runtime skill surface under skills/; custom
    # Claude paths must not introduce a second, Claude-only package surface.
    packaged_skills = (plugin_dir / "skills").resolve(strict=False)
    if reference_escapes_root(target, packaged_skills):
        errors.append(
            "codex-next Claude skill path is outside the packaged skills directory: "
            f"{item}"
        )
        return

    has_direct_skill = (target / "SKILL.md").is_file()
    has_nested_skill = any(
        (child / "SKILL.md").is_file()
        for child in target.iterdir()
        if child.is_dir() and not child.name.startswith(".")
    )
    if not has_direct_skill and not has_nested_skill:
        errors.append(f"claude manifest skill path contains no SKILL.md: {item}")


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


def discover_catalog_skills(catalog_dir: Path, errors: list[str]) -> dict[str, Path]:
    if not catalog_dir.is_dir():
        errors.append(f"missing source catalog directory: {catalog_dir}")
        return {}

    skill_paths: dict[str, Path] = {}
    for path in sorted(catalog_dir.glob("*/skills/*")):
        if not path.is_dir() or path.name.startswith("."):
            continue
        if not (path / "SKILL.md").is_file():
            errors.append(f"missing catalog SKILL.md: {path}")
            continue
        if path.name in skill_paths:
            errors.append(
                f"duplicate catalog skill name: {path.name} "
                f"({skill_paths[path.name]} and {path})"
            )
            continue
        skill_paths[path.name] = path
    return skill_paths


def diff_skill_content(catalog_path: Path, plugin_path: Path) -> list[str]:
    """List relative files whose presence or bytes differ between the copies."""
    catalog_files = {
        path.relative_to(catalog_path).as_posix(): path
        for path in catalog_path.rglob("*")
        if path.is_file() and path.name not in JUNK_FILES
    }
    plugin_files = {
        path.relative_to(plugin_path).as_posix(): path
        for path in plugin_path.rglob("*")
        if path.is_file() and path.name not in JUNK_FILES
    }
    drifted: list[str] = []
    for rel in sorted(set(catalog_files) | set(plugin_files)):
        if rel not in catalog_files:
            drifted.append(f"{rel} (only in plugin)")
        elif rel not in plugin_files:
            drifted.append(f"{rel} (only in catalog)")
        elif catalog_files[rel].read_bytes() != plugin_files[rel].read_bytes():
            drifted.append(f"{rel} (content differs)")
    return drifted


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
    claude_model_invoked = 0
    claude_user_invoked = 0
    description_words = 0
    references_dirs = 0
    scripts_dirs = 0
    checkbox_markers = 0
    do_not_sections = 0
    do_not_use_when_sections = 0
    openai_sidecars = 0
    codex_explicit_skills: set[str] = set()
    skill_names: list[str] = []

    for skill_dir in skill_dirs:
        skill_names.append(skill_dir.name)
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"missing SKILL.md: {skill_dir}")
            continue

        frontmatter, fm_errors, text = parse_frontmatter(skill_file)
        errors.extend(fm_errors)
        metadata = read_skill_metadata(text)
        errors.extend(f"{skill_file}: {error}" for error in metadata.errors)

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
                claude_user_invoked += 1
            else:
                claude_model_invoked += 1
        else:
            errors.append(f"{skill_file}: disable-model-invocation must be true or false")

        if disable is True:
            errors.append(
                f"{skill_file}: Codex plugin ingestion requires "
                "disable-model-invocation to be false or omitted; use "
                "agents/openai.yaml for Codex invocation policy"
            )
        has_openai_sidecar, allow_implicit = inspect_openai_sidecar(
            skill_dir, errors=errors
        )
        openai_sidecars += int(has_openai_sidecar)
        if allow_implicit is False:
            user_invoked += 1
            codex_explicit_skills.add(skill_dir.name)
        else:
            model_invoked += 1

        check_spec_frontmatter(skill_file, frontmatter, errors)
        check_skill_references(skill_dir, errors)
        check_explicit_control_references(skill_dir, text, errors)
        body_lines = len(text.splitlines())
        if body_lines > SPEC_BODY_LINE_BUDGET:
            warnings.append(
                f"{skill_file}: {body_lines} lines exceeds the spec's "
                f"{SPEC_BODY_LINE_BUDGET}-line SKILL.md budget; move detail into references/"
            )

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

    catalog_skill_paths = discover_catalog_skills(catalog_dir, errors)
    catalog_skill_set = set(catalog_skill_paths)
    plugin_skill_set = set(skill_names)
    expected_explicit_skills = set(EXPLICIT_CONTROL_SKILLS)
    missing_explicit_skills = sorted(expected_explicit_skills - plugin_skill_set)
    unexpected_explicit_skills = sorted(
        codex_explicit_skills - expected_explicit_skills
    )
    unenforced_explicit_skills = sorted(
        (expected_explicit_skills & plugin_skill_set) - codex_explicit_skills
    )
    if missing_explicit_skills:
        errors.append(
            "explicit control skills missing from plugin package: "
            + ", ".join(missing_explicit_skills)
        )
    if unexpected_explicit_skills:
        errors.append(
            "plugin skills disable implicit Codex invocation without "
            "classification: "
            + ", ".join(unexpected_explicit_skills)
        )
    if unenforced_explicit_skills:
        errors.append(
            "explicit control skills must set policy.allow_implicit_invocation "
            "to false: "
            + ", ".join(unenforced_explicit_skills)
        )
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

    content_drift: dict[str, list[str]] = {}
    for name in sorted(catalog_skill_set & plugin_skill_set):
        drifted = diff_skill_content(catalog_skill_paths[name], skills_dir / name)
        if drifted:
            content_drift[name] = drifted
            errors.append(
                f"catalog/plugin content drift in skill {name}: "
                + ", ".join(drifted)
            )

    # Cross-skill references resolve against sibling directories, so the
    # catalog copies must be checked in their own bucket layout too.
    for name in sorted(catalog_skill_paths):
        check_skill_references(catalog_skill_paths[name], errors)

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
        "codex_explicit_skills": sorted(codex_explicit_skills),
        "missing_explicit_control_skills": missing_explicit_skills,
        "unexpected_explicit_skills": unexpected_explicit_skills,
        "unenforced_explicit_control_skills": unenforced_explicit_skills,
        "claude_frontmatter_model_invoked": claude_model_invoked,
        "claude_frontmatter_user_invoked": claude_user_invoked,
        "claude_invocation_basis": (
            "packaged_frontmatter_inventory_runtime_unverified"
        ),
        # Compatibility aliases for existing JSON consumers. These counts are
        # static packaged-frontmatter inventory, not live runtime evidence.
        "claude_model_invoked": claude_model_invoked,
        "claude_user_invoked": claude_user_invoked,
        "openai_sidecars": openai_sidecars,
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
        "source_catalog_skills": len(catalog_skill_paths),
        "catalog_content_drift": content_drift,
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
    print(f"- Codex model-invoked: {summary['model_invoked']}")
    print(f"- Codex user-invoked: {summary['user_invoked']}")
    print(
        "- Claude frontmatter model-invoked inventory: "
        f"{summary['claude_frontmatter_model_invoked']}"
    )
    print(
        "- Claude frontmatter user-invoked inventory: "
        f"{summary['claude_frontmatter_user_invoked']}"
    )
    print(f"- Claude invocation basis: {summary['claude_invocation_basis']}")
    print(f"- OpenAI sidecars: {summary['openai_sidecars']}")
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
        "- catalog content drift: "
        + (", ".join(sorted(summary["catalog_content_drift"])) or "none")
    )
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
