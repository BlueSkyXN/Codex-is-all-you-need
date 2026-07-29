from __future__ import annotations

import contextlib
import datetime as dt
import importlib.util
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_skill_metadata.py"
SPEC = importlib.util.spec_from_file_location("check_skill_metadata", SCRIPT)
metadata = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = metadata
SPEC.loader.exec_module(metadata)


class SkillMetadataTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        self.git("init")
        self.git("config", "user.name", "Unit Test")
        self.git("config", "user.email", "unit@example.test")
        self.write_skill("alpha", version="0.1", updated="2026-01-01")
        self.commit("initial")
        self.base = self.rev("HEAD")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def git(self, *args: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(self.repo), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return result.stdout.strip()

    def rev(self, ref: str) -> str:
        return self.git("rev-parse", ref)

    def commit(self, subject: str) -> None:
        self.git("add", ".")
        self.git("commit", "-m", subject)

    def skill_dir(self, name: str, *, catalog: bool = False) -> Path:
        if catalog:
            return self.repo / "examples" / "catalog" / "common" / "skills" / name
        return self.repo / "plugins" / "codex-next" / "skills" / name

    def write_skill(
        self,
        name: str,
        *,
        version: str | None = None,
        updated: str | None = None,
        body: str = "# Alpha\n",
        catalog: bool = True,
        extras: str = "",
    ) -> None:
        frontmatter = "---\nname: " + name + "\ndescription: test\n"
        if version is not None or updated is not None or extras:
            frontmatter += "metadata:\n"
            if version is not None:
                frontmatter += f'  version: "{version}"\n'
            if updated is not None:
                frontmatter += f'  updated: "{updated}"\n'
            frontmatter += extras
        text = frontmatter + "---\n" + body
        targets = [self.skill_dir(name)]
        if catalog:
            targets.append(self.skill_dir(name, catalog=True))
        for target in targets:
            target.mkdir(parents=True, exist_ok=True)
            (target / "SKILL.md").write_text(text, encoding="utf-8")

    def test_schema_requires_quoted_two_part_version_and_real_date(self) -> None:
        cases = {
            "missing": "---\nname: alpha\ndescription: test\n---\n# x\n",
            "number": "---\nmetadata:\n  version: 1.0\n  updated: \"2026-01-01\"\n---\n",
            "three": "---\nmetadata:\n  version: \"1.0.1\"\n  updated: \"2026-01-01\"\n---\n",
            "date": "---\nmetadata:\n  version: \"1.0\"\n  updated: \"2026-02-30\"\n---\n",
            "future": "---\nmetadata:\n  version: \"1.0\"\n  updated: \"2999-01-01\"\n---\n",
        }
        for name, text in cases.items():
            with self.subTest(name=name):
                parsed = metadata.read_metadata(text)
                self.assertTrue(parsed.errors)

    def test_transition_allows_0_9_to_0_10_and_0_10_to_1_0(self) -> None:
        today = dt.date.today().isoformat()
        self.write_skill("alpha", version="0.9", updated="2026-01-01")
        self.commit("set 0.9 baseline")
        base = self.rev("HEAD")
        self.write_skill("alpha", version="0.10", updated=today, body="# Changed\n")
        self.assertEqual(metadata.check(self.repo, base)["errors"], [])
        self.commit("patch")
        base = self.rev("HEAD")
        self.write_skill("alpha", version="1.0", updated=today, body="# Changed again\n")
        self.assertEqual(metadata.check(self.repo, base)["errors"], [])

    def test_check_rejects_jump_and_metadata_only_change(self) -> None:
        self.write_skill("alpha", version="0.3", updated="2026-01-02", body="# Changed\n")
        errors = metadata.check(self.repo, self.base)["errors"]
        self.assertTrue(any("one patch or minor" in error for error in errors))
        self.write_skill("alpha", version="0.2", updated="2026-01-02")
        errors = metadata.check(self.repo, self.base)["errors"]
        self.assertTrue(any("without behavior" in error for error in errors))

    def test_check_rejects_stale_updated_date_for_behavior_change(self) -> None:
        self.write_skill("alpha", version="0.2", updated="2026-01-02", body="# Changed\n")
        errors = metadata.check(self.repo, self.base)["errors"]
        self.assertTrue(any("does not match latest substantive state date" in error for error in errors))

    def test_new_canonical_skill_must_start_at_0_1(self) -> None:
        self.write_skill("beta", version="0.1", updated=dt.date.today().isoformat())
        self.commit("add beta")
        self.assertEqual(metadata.check(self.repo, self.base)["errors"], [])

        for version in ("0.2", "9.9"):
            with self.subTest(version=version):
                self.write_skill("beta", version=version, updated=dt.date.today().isoformat())
                errors = metadata.check(self.repo, self.base)["errors"]
                self.assertTrue(any("new canonical skill must use metadata.version '0.1'" in error for error in errors))

    def test_new_staged_canonical_skill_uses_worktree_date(self) -> None:
        self.write_skill("beta", version="0.1", updated=dt.date.today().isoformat())
        self.git("add", ".")
        self.assertEqual(metadata.check(self.repo, self.base)["errors"], [])

    def test_new_canonical_skill_requires_latest_substantive_date(self) -> None:
        self.write_skill("beta", version="0.1", updated="2026-01-01")
        self.commit("add beta")
        errors = metadata.check(self.repo, self.base)["errors"]
        self.assertTrue(any("does not match latest substantive state date" in error for error in errors))

    def test_behavior_files_count_but_readme_license_and_notice_do_not(self) -> None:
        root = self.skill_dir("alpha")
        (root / "README.md").write_text("ignored", encoding="utf-8")
        (root / "LICENSE").write_text("ignored", encoding="utf-8")
        (root / "NOTICE.txt").write_text("ignored", encoding="utf-8")
        self.assertEqual(metadata.check(self.repo, self.base)["errors"], [])
        (root / "references").mkdir()
        (root / "references" / "rule.md").write_text("behavior", encoding="utf-8")
        errors = metadata.check(self.repo, self.base)["errors"]
        self.assertTrue(any("one patch or minor" in error for error in errors))

    def test_governance_and_presentation_only_changes_do_not_require_version_bump(self) -> None:
        for catalog in (False, True):
            skill_md = self.skill_dir("alpha", catalog=catalog) / "SKILL.md"
            text = skill_md.read_text(encoding="utf-8")
            text = text.replace(
                "description: test\n",
                'description: test\ndisplay_name: "Alpha UI"\n',
            ).replace(
                '  updated: "2026-01-01"\n',
                '  updated: "2026-01-01"\n'
                '  maintainer: "Alice"\n'
                '  updated_by: "Alice, Bob"\n',
            )
            skill_md.write_text(text, encoding="utf-8")
            sidecar = skill_md.parent / "agents" / "openai.yaml"
            sidecar.parent.mkdir()
            sidecar.write_text(
                'interface:\n'
                '  display_name: "Alpha"\n'
                '  short_description: "Alpha UI description"\n'
                '  icon_small: "./assets/icon.png"\n'
                '  brand_color: "#123456"\n',
                encoding="utf-8",
            )
        self.assertEqual(metadata.check(self.repo, self.base)["errors"], [])

    def test_openai_behavior_fields_still_require_version_bump(self) -> None:
        for catalog in (False, True):
            sidecar = self.skill_dir("alpha", catalog=catalog) / "agents" / "openai.yaml"
            sidecar.parent.mkdir()
            sidecar.write_text(
                'interface:\n'
                '  display_name: "Alpha"\n'
                '  short_description: "Alpha UI description"\n'
                '  default_prompt: "Run $alpha with the current input."\n',
                encoding="utf-8",
            )
        errors = metadata.check(self.repo, self.base)["errors"]
        self.assertTrue(any("one patch or minor" in error for error in errors))

    def test_initial_backfill_is_allowed_and_extra_metadata_is_preserved(self) -> None:
        self.write_skill("alpha", version=None, updated=None, extras="  owner: example\n")
        self.commit("remove version metadata")
        base = self.rev("HEAD")
        proposed = metadata.backfill(self.repo, "HEAD", apply=True)
        self.assertEqual(proposed["errors"], [])
        self.assertIn("owner: example", (self.skill_dir("alpha") / "SKILL.md").read_text())
        self.assertEqual(metadata.check(self.repo, base)["errors"], [])
        self.assertEqual(metadata.audit(self.repo, "HEAD")["errors"], [])

    def test_backfill_dedupes_mirror_copy_and_rename_and_is_idempotent(self) -> None:
        self.write_skill("alpha", version=None, updated=None)
        self.commit("drop metadata")
        # A behavior state made in one commit across both copies is one state.
        self.write_skill("alpha", version=None, updated=None, body="# State two\n")
        self.commit("behavior")
        for catalog in (False, True):
            source = self.skill_dir("alpha", catalog=catalog)
            target = self.skill_dir("beta", catalog=catalog)
            target.parent.mkdir(parents=True, exist_ok=True)
            source.rename(target)
        self.commit("rename alpha to beta")
        # Current plugin/canonical skill is beta and historical alpha follows it.
        first = metadata.backfill(self.repo, "HEAD", apply=True)
        beta = next(item for item in first["skills"] if item["path"].endswith("/beta/SKILL.md") and item["mirror_of"] is None)
        self.assertEqual(beta["version"], "0.2")
        second = metadata.backfill(self.repo, "HEAD", apply=False)
        self.assertFalse(any(item["changed"] for item in second["skills"]))

    def test_backfill_never_overwrites_valid_independent_versions(self) -> None:
        self.write_skill("alpha", version="2.3", updated="2026-01-01")
        result = metadata.backfill(self.repo, "HEAD", apply=True)
        alpha = next(
            item
            for item in result["skills"]
            if item["path"].endswith("/alpha/SKILL.md") and item["mirror_of"] is None
        )
        self.assertFalse(alpha["changed"])
        self.assertEqual(alpha["version"], "2.3")
        self.assertIn('version: "2.3"', self.skill_dir("alpha").joinpath("SKILL.md").read_text())

    def test_core_router_is_canonical_not_a_catalog_mirror(self) -> None:
        self.write_skill("core-router", version="0.1", updated="2026-01-01", catalog=False)
        self.commit("add core router")
        skills = metadata.discover_public_skills(self.repo)
        router = [skill for skill in skills if skill.name == "core-router"]
        self.assertEqual(len(router), 1)
        self.assertIsNone(router[0].mirror_of)

    def test_history_plan_uses_generic_committed_fingerprint_history(self) -> None:
        self.write_skill("beta", version=None, updated=None)
        self.commit("add beta")
        self.write_skill("beta", version=None, updated=None, body="# Beta state two\n")
        self.commit("change beta")
        plan = metadata.backfill(self.repo, "HEAD", apply=False)
        beta = next(
            item
            for item in plan["skills"]
            if item["path"].endswith("/beta/SKILL.md") and item["mirror_of"] is None
        )
        self.assertEqual(beta["version"], "0.2")
        self.assertEqual(beta["updated"], metadata.git_date(self.repo, "HEAD"))
        self.assertEqual(beta["states"], 2)
        self.assertEqual(beta["evidence"], self.rev("HEAD"))

    def test_relevant_behavior_and_excluded_paths(self) -> None:
        included = (
            "SKILL.md",
            "agents/openai.yaml",
            "references/rule.md",
            "scripts/tool.py",
            "assets/template.txt",
            "examples/sample.md",
        )
        excluded = (
            "README.md",
            "README_CN.md",
            "LICENSE.txt",
            "NOTICE.md",
            ".DS_Store",
        )
        for path in included:
            self.assertTrue(metadata.relevant_file(metadata.PurePosixPath(path)), path)
        for path in excluded:
            self.assertFalse(metadata.relevant_file(metadata.PurePosixPath(path)), path)

    def test_json_cli_and_help_are_auditable(self) -> None:
        output = self.repo / "audit.json"
        with contextlib.redirect_stdout(io.StringIO()):
            code = metadata.main(
                ["--repo", str(self.repo), "audit", "--history-ref", "HEAD", "--json", str(output)]
            )
        self.assertEqual(code, 0)
        self.assertIn('"command": "audit"', output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
