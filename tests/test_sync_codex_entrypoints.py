from __future__ import annotations

import importlib.util
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "sync_codex_entrypoints.py"
SPEC = importlib.util.spec_from_file_location("sync_codex_entrypoints", SCRIPT)
sync_codex_entrypoints = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = sync_codex_entrypoints
SPEC.loader.exec_module(sync_codex_entrypoints)


class SyncCodexEntrypointsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.tmp.name)
        self.source = self.workspace / ".codex"
        (self.source / "agents").mkdir(parents=True)
        (self.source / "agents" / "dev_python_engineer.toml").write_text("name = 'dev_python_engineer'\n")
        skill_dir = self.source / "skills" / "python-quality"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("# Python Quality\n")

        self.repo = self.workspace / "demo-repo"
        self.repo.mkdir()
        (self.repo / ".git").mkdir()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_script(self, *args: str) -> int:
        with redirect_stdout(io.StringIO()):
            return sync_codex_entrypoints.main(
                [
                    *args,
                    "--workspace",
                    os.fspath(self.workspace),
                    "--source-root",
                    os.fspath(self.source),
                    "--repo",
                    os.fspath(self.repo),
                    "--no-ignore",
                    "--apply",
                ]
            )

    def test_directory_mode_links_entrypoint_directories(self) -> None:
        self.assertEqual(self.run_script("sync", "--link-mode", "directories"), 0)

        agents = self.repo / ".codex" / "agents"
        skills = self.repo / ".codex" / "skills"
        self.assertTrue((self.repo / ".codex").is_dir())
        self.assertTrue(agents.is_symlink())
        self.assertTrue(skills.is_symlink())
        self.assertEqual(os.readlink(agents), os.fspath(self.source / "agents"))
        self.assertEqual(os.readlink(skills), os.fspath(self.source / "skills"))

    def test_entries_mode_links_each_agent_and_skill(self) -> None:
        self.assertEqual(self.run_script("sync", "--link-mode", "entries"), 0)

        agents = self.repo / ".codex" / "agents"
        skill = self.repo / ".codex" / "skills" / "python-quality"
        self.assertTrue(agents.is_dir())
        self.assertFalse(agents.is_symlink())
        self.assertTrue((agents / "dev_python_engineer.toml").is_symlink())
        self.assertTrue(skill.is_symlink())

    def test_directory_mode_replaces_managed_entry_directories(self) -> None:
        self.assertEqual(self.run_script("sync", "--link-mode", "entries"), 0)
        self.assertTrue((self.repo / ".codex" / "agents").is_dir())

        self.assertEqual(self.run_script("sync", "--link-mode", "directories"), 0)

        agents = self.repo / ".codex" / "agents"
        skills = self.repo / ".codex" / "skills"
        self.assertTrue(agents.is_symlink())
        self.assertTrue(skills.is_symlink())
        self.assertEqual(os.readlink(agents), os.fspath(self.source / "agents"))
        self.assertEqual(os.readlink(skills), os.fspath(self.source / "skills"))

    def test_directory_mode_conflicts_on_local_real_content(self) -> None:
        agents = self.repo / ".codex" / "agents"
        agents.mkdir(parents=True)
        (agents / "local.toml").write_text("name = 'local'\n")

        self.assertEqual(self.run_script("sync", "--link-mode", "directories"), 1)

        self.assertFalse(agents.is_symlink())
        self.assertTrue((agents / "local.toml").is_file())

    def test_link_mode_must_be_explicit(self) -> None:
        with redirect_stdout(io.StringIO()):
            result = sync_codex_entrypoints.main(
                [
                    "sync",
                    "--workspace",
                    os.fspath(self.workspace),
                    "--source-root",
                    os.fspath(self.source),
                    "--repo",
                    os.fspath(self.repo),
                    "--no-ignore",
                    "--apply",
                ]
            )

        self.assertEqual(result, 2)


if __name__ == "__main__":
    unittest.main()
