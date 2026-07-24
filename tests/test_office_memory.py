from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "office-memory"
SKILL = PLUGIN / "skills" / "manage-office-memory"
SCRIPT = SKILL / "scripts" / "office_memory.py"


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(SCRIPT), *args], check=check, text=True, capture_output=True)


def write_config(root: Path, external: Path, *, source_path: Path | None = None) -> Path:
    source_path = source_path or external / "memory.md"
    config = root / "office-memory.toml"
    config.write_text(
        f'''version = "0.1"
manual_activation_only = true
project_id = "test-project"
project_root = "{root.as_posix()}"
allowed_scopes = ["project", "documents"]
awareness_file = ".agents/awareness/AWARENESS.md"
memory_file = ".agents/memory/MEMORY.md"

[[sources]]
id = "memory-source"
path = "{source_path.as_posix()}"
role = "memory"
default = true

[[sources]]
id = "profile-source"
path = "{(external / 'profile.md').as_posix()}"
role = "profile"
default = false

[[sources]]
id = "recent-source"
path = "{(external / 'recent').as_posix()}"
role = "recent"
default = false
include = ["*.md"]
''', encoding="utf-8")
    return config


def entry(**changes: str) -> str:
    fields = {"key": "reviewed.fact", "scope": "project", "kind": "fact", "sources": "memory-source#memory.md", "observed": "2026-07-24", "review": "2099-01-01", "summary": "A reviewed, conservative fact."}
    fields.update(changes)
    return "\n".join((f"## {fields['key']}", f"- Scope: {fields['scope']}", f"- Kind: {fields['kind']}", f"- Sources: {fields['sources']}", f"- Observed: {fields['observed']}", f"- Review: {fields['review']}", "", fields["summary"], ""))


def awareness() -> str:
    headings = ("Current understanding", "Relevant changes", "Conflicts and unknowns", "Needs attention", "Memory candidates")
    return "# Project Awareness\n- Updated: 2026-07-24\n- Focus: project\n- Sources checked: memory-source; project#documents/input.md\n\n" + "\n".join(f"## {heading}\n" for heading in headings)


class OfficeMemoryLiteTest(unittest.TestCase):
    def test_manual_contract_runtime_budget_and_example(self) -> None:
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("$office-memory:manage-office-memory", skill)
        self.assertIn("If it is absent, stop immediately", skill)
        self.assertIn("allow_implicit_invocation: false", (SKILL / "agents/openai.yaml").read_text(encoding="utf-8"))
        self.assertEqual({path.relative_to(SKILL).as_posix() for path in SKILL.rglob("*") if path.is_file()}, {"SKILL.md", "agents/openai.yaml", "scripts/office_memory.py"})
        self.assertLessEqual(len(SCRIPT.read_text(encoding="utf-8").splitlines()), 450)
        example = tomllib.loads((PLUGIN / "office-memory.toml.example").read_text(encoding="utf-8"))
        self.assertEqual((example["awareness_file"], example["memory_file"]), ("awareness/AWARENESS.md", "memory/MEMORY.md"))
        recent = next(item for item in example["sources"] if item["id"] == "qoder-recent")
        self.assertEqual((recent["role"], recent["default"]), ("recent", False))

    def test_status_snapshot_focus_and_source_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as root_text, tempfile.TemporaryDirectory() as external_text:
            root, external = Path(root_text), Path(external_text)
            (root / "documents").mkdir(); (external / "recent").mkdir()
            source, profile, recent = external / "memory.md", external / "profile.md", external / "recent/recent.md"
            material = root / "documents/input.md"
            for path, text in ((source, "memory"), (profile, "profile"), (recent, "recent"), (material, "material")):
                path.write_text(text, encoding="utf-8")
            cfg = write_config(root, external)
            before = {path: (hashlib.sha256(path.read_bytes()).hexdigest(), path.stat().st_mtime_ns) for path in (source, profile, recent, material)}
            source.unlink()
            status = json.loads(run("check-config", "--config", str(cfg)).stdout)
            self.assertEqual(status["outputs"]["awareness"]["exists"], False)
            self.assertEqual(status["outputs"]["memory"]["exists"], False)
            source.write_text("memory", encoding="utf-8")
            before[source] = (hashlib.sha256(source.read_bytes()).hexdigest(), source.stat().st_mtime_ns)
            self.assertEqual(json.loads(run("snapshot", "--config", str(cfg)).stdout)["source_ids"], ["memory-source"])
            self.assertNotEqual(run("snapshot", "--config", str(cfg), "--material", "documents/input.md", check=False).returncode, 0)
            explicit = json.loads(run("snapshot", "--config", str(cfg), "--source", "profile-source", "--source", "recent-source", "--focus", "documents", "--material", "documents/input.md").stdout)
            self.assertIn("project#documents/input.md", {row["file_id"] for row in explicit["files"]})
            self.assertEqual(before, {path: (hashlib.sha256(path.read_bytes()).hexdigest(), path.stat().st_mtime_ns) for path in before})
            self.assertNotIn(external.as_posix(), json.dumps(explicit))
            self.assertNotEqual(run("snapshot", "--config", str(cfg), "--focus", "project", "--material", str(profile), check=False).returncode, 0)
            self.assertNotEqual(run("snapshot", "--config", str(cfg), "--focus", "documents", "--material", "office-memory.toml", check=False).returncode, 0)
            escape = root / "documents/escape.md"
            try:
                escape.symlink_to(profile)
            except OSError:
                pass
            else:
                self.assertNotEqual(run("snapshot", "--config", str(cfg), "--focus", "documents", "--material", "documents/escape.md", check=False).returncode, 0)
            repeated = tuple(value for _ in range(21) for value in ("--material", "documents/input.md"))
            self.assertNotEqual(run("snapshot", "--config", str(cfg), "--focus", "documents", *repeated, check=False).returncode, 0)

    def test_output_boundaries_missing_results_and_init_nonoverwrite(self) -> None:
        with tempfile.TemporaryDirectory() as root_text, tempfile.TemporaryDirectory() as external_text:
            root, external = Path(root_text), Path(external_text)
            (external / "memory.md").write_text("source", encoding="utf-8"); (external / "profile.md").write_text("profile", encoding="utf-8")
            cfg = write_config(root, external)
            self.assertNotEqual(run("validate", "--config", str(cfg), check=False).returncode, 0)
            self.assertNotEqual(run("init", "--config", str(cfg), "--apply", "--material", "missing.md", check=False).returncode, 0)
            self.assertTrue(json.loads(run("init", "--config", str(cfg)).stdout)["dry_run"])
            run("init", "--config", str(cfg), "--apply")
            files = {path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()}
            self.assertEqual(files, {"office-memory.toml", ".agents/awareness/AWARENESS.md", ".agents/memory/MEMORY.md"})
            awareness = root / ".agents/awareness/AWARENESS.md"
            awareness.write_text("custom", encoding="utf-8")
            self.assertEqual(json.loads(run("init", "--config", str(cfg), "--apply").stdout)["changed"], [])
            self.assertEqual(awareness.read_text(encoding="utf-8"), "custom")
            overlap = write_config(root, external, source_path=root / ".agents/awareness")
            self.assertNotEqual(run("check-config", "--config", str(overlap), check=False).returncode, 0)

    def test_awareness_memory_schema_and_limits(self) -> None:
        with tempfile.TemporaryDirectory() as root_text, tempfile.TemporaryDirectory() as external_text:
            root, external = Path(root_text), Path(external_text)
            (external / "memory.md").write_text("source", encoding="utf-8"); (external / "profile.md").write_text("profile", encoding="utf-8")
            cfg = write_config(root, external)
            run("init", "--config", str(cfg), "--apply")
            awareness_path = root / ".agents/awareness/AWARENESS.md"; memory_path = root / ".agents/memory/MEMORY.md"
            self.assertNotEqual(run("validate", "--config", str(cfg), check=False).returncode, 0)
            (root / "documents").mkdir()
            (root / "documents/input.md").write_text("material", encoding="utf-8")
            awareness_path.write_text(awareness(), encoding="utf-8")
            self.assertEqual(run("validate", "--config", str(cfg)).returncode, 0)
            awareness_path.write_text("# Project Awareness\n- Updated:\n- Focus:\n- Sources checked:\n\n## Current understanding\n", encoding="utf-8")
            self.assertNotEqual(run("validate", "--config", str(cfg), check=False).returncode, 0)
            awareness_path.write_text(awareness().replace("- Focus: project", "- Focus: other"), encoding="utf-8")
            self.assertIn("Focus", "\n".join(json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"]))
            awareness_path.write_text(awareness().replace("memory-source; project#documents/input.md", "unknown-source"), encoding="utf-8")
            self.assertIn("Sources checked", "\n".join(json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"]))
            awareness_path.write_text(awareness().replace("## Needs attention", "token=not-safe-value\n\n## Needs attention"), encoding="utf-8")
            self.assertIn("secret-like", "\n".join(json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"]))
            awareness_path.write_text(awareness(), encoding="utf-8")
            memory_path.write_text("# Project Memory\n\n" + entry() + entry(key="reviewed.fact", summary="token=not-safe-value") + entry(key="cross-scope", scope="other") + entry(key="expired", review="2000-01-01") + entry(key="missing-locator", sources="memory-source"), encoding="utf-8")
            errors = "\n".join(json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"])
            for expected in ("duplicate", "secret-like", "invalid scope", "expired", "invalid sources"):
                self.assertIn(expected, errors)
            awareness_path.write_text("x" * (16 * 1024 + 1), encoding="utf-8")
            self.assertIn("16 KiB", "\n".join(json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"]))


if __name__ == "__main__":
    unittest.main()
