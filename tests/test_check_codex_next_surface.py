from __future__ import annotations

import contextlib
import importlib.util
import io
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
            self.catalog / "common" / "skills" / "manual-skill",
            "manual-skill",
            disable_model_invocation=True,
            body="# Manual\n",
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

    def test_catalog_plugin_content_drift_is_hard_error(self) -> None:
        skill_md = self.plugin / "skills" / "alpha-skill" / "SKILL.md"
        skill_md.write_text(
            skill_md.read_text(encoding="utf-8") + "\nplugin-only edit\n",
            encoding="utf-8",
        )

        summary = check_codex_next_surface.run_check(self.plugin, self.catalog)

        self.assertIn("alpha-skill", summary["catalog_content_drift"])
        self.assertTrue(
            any(
                "catalog/plugin content drift in skill alpha-skill" in error
                for error in summary["errors"]
            )
        )

    def test_reference_file_missing_from_one_copy_is_hard_error(self) -> None:
        references = self.plugin / "skills" / "manual-skill" / "references"
        references.mkdir()
        (references / "extra.md").write_text("# Extra\n", encoding="utf-8")

        summary = check_codex_next_surface.run_check(self.plugin, self.catalog)

        self.assertEqual(
            summary["catalog_content_drift"].get("manual-skill"),
            ["references/extra.md (only in plugin)"],
        )
        self.assertTrue(
            any(
                "catalog/plugin content drift in skill manual-skill" in error
                for error in summary["errors"]
            )
        )

    def test_identical_copies_report_no_content_drift(self) -> None:
        summary = check_codex_next_surface.run_check(self.plugin, self.catalog)

        self.assertEqual(summary["catalog_content_drift"], {})
        self.assertEqual(summary["errors"], [])

    def test_junk_files_do_not_report_content_drift(self) -> None:
        (self.plugin / "skills" / "alpha-skill" / ".DS_Store").write_bytes(b"local")

        summary = check_codex_next_surface.run_check(self.plugin, self.catalog)

        self.assertEqual(summary["catalog_content_drift"], {})
        self.assertEqual(summary["errors"], [])

    def test_manifest_version_mismatch_is_hard_error(self) -> None:
        (self.plugin / ".claude-plugin" / "plugin.json").write_text(
            json.dumps({"name": "codex-next", "version": "0.9.0"}),
            encoding="utf-8",
        )

        summary = check_codex_next_surface.run_check(self.plugin, self.catalog)

        self.assertTrue(
            any("manifest version mismatch" in error for error in summary["errors"])
        )

    def test_spec_invalid_name_charset_is_hard_error(self) -> None:
        skill_dir = self.plugin / "skills" / "bad--name"
        self.write_skill(skill_dir, "bad--name")
        self.write_skill(self.catalog / "common" / "skills" / "bad--name", "bad--name")

        summary = check_codex_next_surface.run_check(self.plugin, self.catalog)

        self.assertTrue(
            any("violates spec charset" in error for error in summary["errors"])
        )

    def test_spec_unknown_frontmatter_field_is_hard_error(self) -> None:
        (self.plugin / "skills" / "alpha-skill" / "SKILL.md").write_text(
            "---\n"
            "name: alpha-skill\n"
            "description: Use for alpha-skill checks.\n"
            "invoke-priority: high\n"
            "---\n"
            "# Alpha\n",
            encoding="utf-8",
        )

        summary = check_codex_next_surface.run_check(self.plugin, self.catalog)

        self.assertTrue(
            any(
                "neither an Agent Skills spec field nor an allowlisted extension"
                in error
                for error in summary["errors"]
            )
        )

    def test_spec_overlong_description_is_hard_error(self) -> None:
        (self.plugin / "skills" / "alpha-skill" / "SKILL.md").write_text(
            "---\n"
            "name: alpha-skill\n"
            f"description: {'x' * 1030}\n"
            "---\n"
            "# Alpha\n",
            encoding="utf-8",
        )

        summary = check_codex_next_surface.run_check(self.plugin, self.catalog)

        self.assertTrue(
            any("description exceeds 1024" in error for error in summary["errors"])
        )

    def test_spec_body_line_budget_is_warning_only(self) -> None:
        over_budget_body = "\n".join(f"line {index}" for index in range(501))
        for root in (
            self.plugin / "skills" / "alpha-skill",
            self.catalog / "common" / "skills" / "alpha-skill",
        ):
            self.write_skill(root, "alpha-skill", body=over_budget_body)

        summary = check_codex_next_surface.run_check(self.plugin, self.catalog)

        self.assertEqual(summary["errors"], [])
        self.assertTrue(
            any(
                "exceeds the spec's 500-line SKILL.md budget" in warning
                for warning in summary["warnings"]
            )
        )
        with contextlib.redirect_stdout(io.StringIO()):
            exit_code = check_codex_next_surface.main(
                [
                    "--plugin-dir",
                    str(self.plugin),
                    "--catalog-dir",
                    str(self.catalog),
                ]
            )
        self.assertEqual(exit_code, 0)

    def test_spec_overlong_compatibility_is_hard_error(self) -> None:
        (self.plugin / "skills" / "alpha-skill" / "SKILL.md").write_text(
            "---\n"
            "name: alpha-skill\n"
            "description: Use for alpha-skill checks.\n"
            f"compatibility: {'x' * 501}\n"
            "---\n"
            "# Alpha\n",
            encoding="utf-8",
        )

        summary = check_codex_next_surface.run_check(self.plugin, self.catalog)

        self.assertTrue(
            any("compatibility exceeds 500" in error for error in summary["errors"])
        )

    def test_spec_invalid_compatibility_value_is_hard_error(self) -> None:
        cases = ("compatibility: true\n", "compatibility:\n")
        for compatibility_line in cases:
            with self.subTest(compatibility_line=compatibility_line.strip()):
                (self.plugin / "skills" / "alpha-skill" / "SKILL.md").write_text(
                    "---\n"
                    "name: alpha-skill\n"
                    "description: Use for alpha-skill checks.\n"
                    f"{compatibility_line}"
                    "---\n"
                    "# Alpha\n",
                    encoding="utf-8",
                )

                summary = check_codex_next_surface.run_check(self.plugin, self.catalog)

                self.assertTrue(
                    any(
                        "compatibility must be a non-empty string" in error
                        for error in summary["errors"]
                    )
                )

    def test_parse_frontmatter_strips_only_balanced_outer_quotes(self) -> None:
        skill_file = self.plugin / "skills" / "alpha-skill" / "SKILL.md"
        skill_file.write_text(
            "---\n"
            "name: alpha-skill\n"
            "description: Supports users'\n"
            'compatibility: "Codex runtime"\n'
            "---\n"
            "# Alpha\n",
            encoding="utf-8",
        )

        frontmatter, errors, _ = check_codex_next_surface.parse_frontmatter(skill_file)

        self.assertEqual(errors, [])
        self.assertEqual(frontmatter["description"], "Supports users'")
        self.assertEqual(frontmatter["compatibility"], "Codex runtime")

    def test_nested_metadata_mapping_is_not_flagged(self) -> None:
        content = (
            "---\n"
            "name: alpha-skill\n"
            "description: Use for alpha-skill checks.\n"
            "metadata:\n"
            "  author: example-org\n"
            "  version: \"1.0\"\n"
            "---\n"
            "# Alpha\n"
        )
        (self.plugin / "skills" / "alpha-skill" / "SKILL.md").write_text(
            content, encoding="utf-8"
        )
        (self.catalog / "common" / "skills" / "alpha-skill" / "SKILL.md").write_text(
            content, encoding="utf-8"
        )

        summary = check_codex_next_surface.run_check(self.plugin, self.catalog)

        self.assertEqual(summary["errors"], [])

    def test_dangling_relative_link_is_hard_error(self) -> None:
        content = (
            "---\n"
            "name: alpha-skill\n"
            "description: Use for alpha-skill checks.\n"
            "---\n"
            "# Alpha\n\nSee [missing](references/missing.md).\n"
        )
        (self.plugin / "skills" / "alpha-skill" / "SKILL.md").write_text(
            content, encoding="utf-8"
        )
        (self.catalog / "common" / "skills" / "alpha-skill" / "SKILL.md").write_text(
            content, encoding="utf-8"
        )

        summary = check_codex_next_surface.run_check(self.plugin, self.catalog)

        self.assertTrue(
            any("relative link does not resolve" in error for error in summary["errors"])
        )

    def test_dangling_relative_link_with_fragment_is_hard_error(self) -> None:
        content = (
            "---\n"
            "name: alpha-skill\n"
            "description: Use for alpha-skill checks.\n"
            "---\n"
            "# Alpha\n\nSee [missing](references/missing.md#anchor).\n"
        )
        (self.plugin / "skills" / "alpha-skill" / "SKILL.md").write_text(
            content, encoding="utf-8"
        )
        (self.catalog / "common" / "skills" / "alpha-skill" / "SKILL.md").write_text(
            content, encoding="utf-8"
        )

        summary = check_codex_next_surface.run_check(self.plugin, self.catalog)

        self.assertTrue(
            any("relative link does not resolve" in error for error in summary["errors"])
        )

    def test_existing_relative_link_with_fragment_is_allowed(self) -> None:
        content = (
            "---\n"
            "name: alpha-skill\n"
            "description: Use for alpha-skill checks.\n"
            "---\n"
            "# Alpha\n\nSee [guide](references/guide.md#anchor).\n"
        )
        for root in (
            self.plugin / "skills" / "alpha-skill",
            self.catalog / "common" / "skills" / "alpha-skill",
        ):
            root.joinpath("references").mkdir()
            root.joinpath("references", "guide.md").write_text(
                "# Guide\n", encoding="utf-8"
            )
            root.joinpath("SKILL.md").write_text(content, encoding="utf-8")

        summary = check_codex_next_surface.run_check(self.plugin, self.catalog)

        self.assertEqual(summary["errors"], [])

    def test_dangling_parent_path_reference_is_hard_error(self) -> None:
        content = (
            "---\n"
            "name: alpha-skill\n"
            "description: Use for alpha-skill checks.\n"
            "---\n"
            "# Alpha\n\nUse ../missing-skill/references/model.md for definitions.\n"
        )
        (self.plugin / "skills" / "alpha-skill" / "SKILL.md").write_text(
            content, encoding="utf-8"
        )
        (self.catalog / "common" / "skills" / "alpha-skill" / "SKILL.md").write_text(
            content, encoding="utf-8"
        )

        summary = check_codex_next_surface.run_check(self.plugin, self.catalog)

        self.assertTrue(
            any(
                "parent-path reference does not resolve" in error
                for error in summary["errors"]
            )
        )

    def test_parent_path_reference_outside_skill_root_is_hard_error(self) -> None:
        content = (
            "---\n"
            "name: alpha-skill\n"
            "description: Use for alpha-skill checks.\n"
            "---\n"
            "# Alpha\n\nDo not rely on ../../README.md for runtime behavior.\n"
        )
        (self.plugin / "skills" / "alpha-skill" / "SKILL.md").write_text(
            content, encoding="utf-8"
        )
        (self.catalog / "common" / "skills" / "alpha-skill" / "SKILL.md").write_text(
            content, encoding="utf-8"
        )

        summary = check_codex_next_surface.run_check(self.plugin, self.catalog)

        self.assertTrue(
            any(
                "parent-path reference escapes skill root" in error
                for error in summary["errors"]
            )
        )


if __name__ == "__main__":
    unittest.main()
