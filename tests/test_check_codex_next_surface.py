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
        self.plugin = Path(self.tmp.name) / "codex-next"
        (self.plugin / ".codex-plugin").mkdir(parents=True)
        (self.plugin / ".claude-plugin").mkdir()
        (self.plugin / "skills" / "alpha-skill").mkdir(parents=True)
        (self.plugin / "skills" / "manual-skill").mkdir()
        (self.plugin / "README.md").write_text("core-router alpha-skill\n", encoding="utf-8")
        (self.plugin / ".codex-plugin" / "plugin.json").write_text(
            json.dumps({"name": "codex-next", "skills": "./skills/"}),
            encoding="utf-8",
        )
        (self.plugin / ".claude-plugin" / "plugin.json").write_text(
            json.dumps({"name": "codex-next"}),
            encoding="utf-8",
        )
        (self.plugin / "skills" / "alpha-skill" / "SKILL.md").write_text(
            "---\n"
            "name: alpha-skill\n"
            "description: Use for alpha checks.\n"
            "---\n"
            "# Alpha\n\n"
            "- [ ] done\n"
            "## Do not\n",
            encoding="utf-8",
        )
        (self.plugin / "skills" / "manual-skill" / "SKILL.md").write_text(
            "---\n"
            "name: manual-skill\n"
            "description: Manual check.\n"
            "disable-model-invocation: true\n"
            "---\n"
            "# Manual\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_surface_summary_counts_skills_and_manifest_modes(self) -> None:
        summary = check_codex_next_surface.run_check(self.plugin)

        self.assertEqual(summary["skills"], 2)
        self.assertEqual(summary["model_invoked"], 1)
        self.assertEqual(summary["user_invoked"], 1)
        self.assertEqual(summary["checkbox_markers"], 1)
        self.assertEqual(summary["do_not_sections"], 1)
        self.assertEqual(summary["codex_manifest_mode"], "directory")
        self.assertEqual(summary["claude_manifest_mode"], "implicit_or_unverified")
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

        summary = check_codex_next_surface.run_check(self.plugin)

        self.assertTrue(any("does not match directory" in error for error in summary["errors"]))


if __name__ == "__main__":
    unittest.main()
