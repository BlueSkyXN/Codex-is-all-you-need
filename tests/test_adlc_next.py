"""Package contract checks for the ADLC Next plugin."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "adlc-next"
SKILLS = PLUGIN / "skills"
CONVENTIONS = SKILLS / "sdlc-solve" / "references" / "conventions.md"
SETTINGS_EXAMPLE = SKILLS / "adlc-setup" / "assets" / "adlc-next.toml.example"
ROUTER = SKILLS / "adlc-router" / "SKILL.md"
CODEX_MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
CLAUDE_MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"

SURFACE_SCRIPT = ROOT / "scripts" / "check_codex_next_surface.py"
SURFACE_SPEC = importlib.util.spec_from_file_location(
    "check_codex_next_surface_for_adlc", SURFACE_SCRIPT
)
assert SURFACE_SPEC is not None and SURFACE_SPEC.loader is not None
surface = importlib.util.module_from_spec(SURFACE_SPEC)
sys.modules[SURFACE_SPEC.name] = surface
SURFACE_SPEC.loader.exec_module(surface)

EXPECTED_SKILLS = frozenset(
    {
        "sdlc-solve",
        "sdlc-implement",
        "sdlc-review",
        "sdlc-clarify",
        "sdlc-handoff",
        "sdlc-test-first",
        "sdlc-bugfix",
        "sdlc-ship",
        "ads-survey",
        "ads-requirements",
        "ads-architecture",
        "ads-domain",
        "ads-spec",
        "tasks-intake",
        "tasks-wrap-up",
        "improvement-retro",
        "improvement-skill-eval",
        "improvement-prompt-eval",
        "adlc-router",
        "adlc-setup",
    }
)
GROUP_PREFIXES = ("sdlc-", "ads-", "tasks-", "improvement-", "adlc-")
DELIVERY_POINTS = ("local", "commit", "pr", "merge", "release", "verified")
JUNK_FILES = frozenset({".DS_Store", "Thumbs.db", "desktop.ini"})
SIBLING_SKILL_MD_RE = re.compile(r"\.\./(?:\.\./)?([a-z0-9-]+)/SKILL\.md")


def skill_dirs() -> list[Path]:
    return sorted(
        path
        for path in SKILLS.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    )


class AdlcNextSkillSurfaceTest(unittest.TestCase):
    def test_skill_set_matches_the_published_index(self) -> None:
        self.assertEqual({path.name for path in skill_dirs()}, EXPECTED_SKILLS)
        for name in EXPECTED_SKILLS:
            self.assertTrue(name.startswith(GROUP_PREFIXES), name)

    def test_every_skill_directory_has_an_entry(self) -> None:
        for skill_dir in skill_dirs():
            self.assertTrue((skill_dir / "SKILL.md").is_file(), skill_dir)

    def test_frontmatter_follows_spec_and_names_explicit_commands(self) -> None:
        for skill_dir in skill_dirs():
            skill_file = skill_dir / "SKILL.md"
            frontmatter, errors, text = surface.parse_frontmatter(skill_file)
            surface.check_spec_frontmatter(skill_file, frontmatter, errors)
            self.assertEqual(errors, [], skill_file)
            self.assertEqual(frontmatter.get("name"), skill_dir.name)
            self.assertNotIn("disable-model-invocation", frontmatter)
            self.assertIn("metadata", frontmatter)

            name = skill_dir.name
            description = frontmatter.get("description", "")
            for command in (f"$adlc-next:{name}", f"/adlc-next:{name}"):
                self.assertIn(command, description, skill_file)
                self.assertIn(f"`{command}`", text, skill_file)
            self.assertIn("## Activation", text, skill_file)

            body_lines = len(text.splitlines())
            self.assertLessEqual(body_lines, surface.SPEC_BODY_LINE_BUDGET, skill_file)

    def test_every_skill_is_explicit_only_in_codex(self) -> None:
        for skill_dir in skill_dirs():
            errors: list[str] = []
            has_sidecar, allow_implicit = surface.inspect_openai_sidecar(
                skill_dir, errors=errors
            )
            self.assertEqual(errors, [], skill_dir)
            self.assertTrue(has_sidecar, skill_dir)
            self.assertIs(allow_implicit, False, skill_dir)

    def test_references_resolve_inside_the_package(self) -> None:
        errors: list[str] = []
        for skill_dir in skill_dirs():
            surface.check_skill_references(skill_dir, errors)
        self.assertEqual(errors, [])

    def test_no_skill_loads_another_skills_entry(self) -> None:
        for skill_dir in skill_dirs():
            for md_file in skill_dir.rglob("*.md"):
                text = md_file.read_text(encoding="utf-8")
                for target in SIBLING_SKILL_MD_RE.findall(text):
                    self.assertEqual(target, skill_dir.name, md_file)

    def test_package_ships_no_scripts(self) -> None:
        for path in PLUGIN.rglob("*"):
            if path.is_file() and path.name not in JUNK_FILES:
                self.assertNotIn("scripts", path.relative_to(PLUGIN).parts, path)


class AdlcNextPackageTest(unittest.TestCase):
    def test_manifests_are_aligned(self) -> None:
        codex = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        claude = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(codex["name"], PLUGIN.name)
        self.assertEqual(claude["name"], PLUGIN.name)
        self.assertEqual(codex["version"], claude["version"])
        self.assertRegex(codex["version"], r"^\d+\.\d+\.\d+$")
        self.assertEqual(codex["description"], claude["description"])
        self.assertEqual(codex["license"], "GPL-3.0-only")
        self.assertEqual(claude["license"], "GPL-3.0-only")
        self.assertEqual(codex["skills"], "./skills/")
        self.assertNotIn("interface", claude)
        for prompt in codex["interface"]["defaultPrompt"]:
            command = re.search(r"\$adlc-next:([a-z0-9-]+)", prompt)
            if command is None:
                self.fail(f"default prompt names no ADLC skill: {prompt}")
            self.assertIn(command.group(1), EXPECTED_SKILLS)

    def test_marketplaces_list_the_plugin_once(self) -> None:
        codex = json.loads(CODEX_MARKETPLACE.read_text(encoding="utf-8"))
        claude = json.loads(CLAUDE_MARKETPLACE.read_text(encoding="utf-8"))
        codex_entries = [item for item in codex["plugins"] if item["name"] == PLUGIN.name]
        claude_entries = [item for item in claude["plugins"] if item["name"] == PLUGIN.name]
        self.assertEqual(len(codex_entries), 1)
        self.assertEqual(len(claude_entries), 1)
        self.assertEqual(codex_entries[0]["source"]["path"], "./plugins/adlc-next")
        self.assertEqual(codex_entries[0]["policy"]["installation"], "AVAILABLE")
        self.assertEqual(claude_entries[0]["source"], "./plugins/adlc-next")

    def test_readme_and_router_index_every_skill(self) -> None:
        readme = (PLUGIN / "README.md").read_text(encoding="utf-8")
        router = ROUTER.read_text(encoding="utf-8")
        for name in EXPECTED_SKILLS:
            self.assertIn(f"`{name}`", readme, name)
            if name != "adlc-router":
                self.assertIn(f"`{name}`", router, name)

    def test_settings_example_matches_conventions(self) -> None:
        settings = tomllib.loads(SETTINGS_EXAMPLE.read_text(encoding="utf-8"))
        self.assertEqual(
            set(settings),
            {
                "version",
                "task_root",
                "default_delivery_point",
                "tracker",
                "work_items_file",
                "design_docs_dir",
                "language",
            },
        )
        self.assertIn(settings["default_delivery_point"], DELIVERY_POINTS)
        self.assertIn(settings["tracker"], {"file", "github-issues"})
        for key in ("task_root", "work_items_file"):
            self.assertFalse(Path(settings[key]).is_absolute(), key)
            self.assertNotIn("..", Path(settings[key]).parts, key)

        conventions = CONVENTIONS.read_text(encoding="utf-8")
        for code in DELIVERY_POINTS:
            self.assertIn(f"| `{code}` |", conventions, code)
        self.assertIn(".agents/adlc-next.toml", conventions)


if __name__ == "__main__":
    unittest.main()
