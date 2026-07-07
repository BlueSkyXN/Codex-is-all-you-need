from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_codex_next_surface.py"
SPEC = importlib.util.spec_from_file_location("check_codex_next_surface", SCRIPT)
check_codex_next_surface = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = check_codex_next_surface
SPEC.loader.exec_module(check_codex_next_surface)


class CheckCodexNextSurfaceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.plugin = self.root / "plugins" / "codex-next"
        self.catalog = self.root / "examples" / "catalog"
        (self.plugin / ".codex-plugin").mkdir(parents=True)
        (self.plugin / ".claude-plugin").mkdir()
        (self.catalog / "common" / "skills").mkdir(parents=True)
        (self.plugin / "skills" / "alpha-skill").mkdir(parents=True)
        (self.plugin / "skills" / "manual-skill").mkdir()
        (self.plugin / "README.md").write_text("core-router alpha-skill\n", encoding="utf-8")
        (self.plugin / ".codex-plugin" / "plugin.json").write_text(
            json.dumps(
                {"name": "codex-next", "version": "1.0.0", "skills": "./skills/"}
            ),
            encoding="utf-8",
        )
        (self.plugin / ".claude-plugin" / "plugin.json").write_text(
            json.dumps({"name": "codex-next", "version": "1.0.0"}),
            encoding="utf-8",
        )
        self.write_skill(self.plugin / "skills" / "alpha-skill", "alpha-skill")
        self.write_skill(
            self.plugin / "skills" / "manual-skill",
            "manual-skill",
            disable_model_invocation=True,
            body="# Manual\n",
        )
        self.write_skill(
            self.catalog / "common" / "skills" / "alpha-skill", "alpha-skill"
        )
        self.write_skill(
            self.catalog / "common" / "skills" / "manual-skill", "manual-skill"
        )

    def write_skill(
        self,
        path: Path,
        name: str,
        *,
        disable_model_invocation: bool = False,
        body: str = "# Alpha\n\n- [ ] done\n## Do not\n",
    ) -> None:
        path.mkdir(parents=True, exist_ok=True)
        invocation_line = (
            "disable-model-invocation: true\n" if disable_model_invocation else ""
        )
        path.joinpath("SKILL.md").write_text(
            "---\n"
            f"name: {name}\n"
            f"description: Use for {name} checks.\n"
            f"{invocation_line}"
            "---\n"
            f"{body}",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_surface_summary_counts_skills_and_manifest_modes(self) -> None:
        summary = check_codex_next_surface.run_check(self.plugin, self.catalog)

        self.assertEqual(summary["skills"], 2)
        self.assertEqual(summary["model_invoked"], 1)
        self.assertEqual(summary["user_invoked"], 1)
        self.assertEqual(summary["checkbox_markers"], 1)
        self.assertEqual(summary["do_not_sections"], 1)
        self.assertEqual(summary["codex_manifest_mode"], "directory")
        self.assertEqual(summary["codex_manifest_version"], "1.0.0")
        self.assertEqual(summary["claude_manifest_mode"], "implicit_or_unverified")
        self.assertEqual(summary["claude_manifest_version"], "1.0.0")
        self.assertEqual(summary["source_catalog_skills"], 2)
        self.assertEqual(summary["plugin_only_skills"], [])
        self.assertEqual(summary["errors"], [])
        self.assertTrue(summary["warnings"])

    def test_name_mismatch_is_hard_error(self) -> None:
        (self.plugin / "skills" / "manual-skill" / "SKILL.md").write_text(
            "---\n"
            "name: wrong-name\n"
            "description: Manual check.\n"
            "---\n"
            "# Manual\n",
            encoding="utf-8",
        )

        summary = check_codex_next_surface.run_check(self.plugin, self.catalog)

        self.assertTrue(
            any("does not match directory" in error for error in summary["errors"])
        )

    def test_unquoted_frontmatter_colon_space_is_hard_error(self) -> None:
        (self.plugin / "skills" / "manual-skill" / "SKILL.md").write_text(
            "---\n"
            "name: manual-skill\n"
            "description: Pairs with core-router: use after routing.\n"
            "---\n"
            "# Manual\n",
            encoding="utf-8",
        )

        summary = check_codex_next_surface.run_check(self.plugin, self.catalog)

        self.assertTrue(
            any("contains ': ' and must be quoted" in error for error in summary["errors"])
        )

    def test_unexpected_plugin_only_skill_is_hard_error(self) -> None:
        self.write_skill(self.plugin / "skills" / "beta-skill", "beta-skill")

        summary = check_codex_next_surface.run_check(self.plugin, self.catalog)

        self.assertEqual(summary["unexpected_plugin_only_skills"], ["beta-skill"])
        self.assertTrue(
            any(
                "plugin skills missing from source catalog" in error
                for error in summary["errors"]
            )
        )

    def test_core_router_is_allowed_plugin_only_skill(self) -> None:
        self.write_skill(self.plugin / "skills" / "core-router", "core-router")

        summary = check_codex_next_surface.run_check(self.plugin, self.catalog)

        self.assertEqual(summary["plugin_only_skills"], ["core-router"])
        self.assertEqual(summary["unexpected_plugin_only_skills"], [])
        self.assertFalse(
            any(
                "plugin skills missing from source catalog" in error
                for error in summary["errors"]
            )
        )

    def test_manifest_version_mismatch_is_hard_error(self) -> None:
        (self.plugin / ".claude-plugin" / "plugin.json").write_text(
            json.dumps({"name": "codex-next", "version": "0.9.0"}),
            encoding="utf-8",
        )

        summary = check_codex_next_surface.run_check(self.plugin, self.catalog)

        self.assertTrue(
            any("manifest version mismatch" in error for error in summary["errors"])
        )


if __name__ == "__main__":
    unittest.main()
