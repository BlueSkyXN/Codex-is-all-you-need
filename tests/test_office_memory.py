from __future__ import annotations

import errno
import hashlib
import importlib.util
import json
import stat
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest import mock


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "office-memory"
SKILL = PLUGIN / "skills" / "manage-office-memory"
SCRIPT = SKILL / "scripts" / "office_memory.py"


def load_helper():
    spec = importlib.util.spec_from_file_location("office_memory_test_module", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Office Memory helper")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


HELPER = load_helper()


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


def daily_record(*, day: str = "2026-07-24", focus: str = "project", sources: str = "memory-source", content: str = "- A meaningful reviewed change.\n") -> str:
    headings = ("Meaningful changes", "Decisions and constraints", "Conflicts and unknowns", "Long-term candidates")
    sections = [f"## {heading}\n{content if index == 0 else ''}" for index, heading in enumerate(headings)]
    return f"# Daily Project Memory — {day}\n- Focus: {focus}\n- Sources checked: {sources}\n\n" + "\n".join(sections)


class OfficeMemoryLiteTest(unittest.TestCase):
    def test_manual_contract_runtime_budget_and_example(self) -> None:
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("$manage-office-memory", skill)
        self.assertIn("$office-memory:manage-office-memory", skill)
        self.assertIn("/manage-office-memory", skill)
        self.assertIn("/office-memory:manage-office-memory", skill)
        self.assertIn("disable-model-invocation: true", skill)
        self.assertIn("If neither invocation", skill)
        self.assertIn("A descriptive request alone does not activate", skill)
        self.assertIn("| `daily` |", skill)
        self.assertIn("Rewrite the whole day", skill)
        self.assertIn("delete old dates", skill)
        self.assertIn('SKILL_DIR/scripts/office_memory.py', skill)
        self.assertNotIn('Run `office_memory.py', skill)
        sidecar = (SKILL / "agents/openai.yaml").read_text(encoding="utf-8")
        self.assertIn("$manage-office-memory", sidecar)
        self.assertIn("allow_implicit_invocation: false", sidecar)
        self.assertEqual({path.relative_to(SKILL).as_posix() for path in SKILL.rglob("*") if path.is_file()}, {"SKILL.md", "agents/openai.yaml", "scripts/office_memory.py"})
        self.assertLessEqual(len(SCRIPT.read_text(encoding="utf-8").splitlines()), 500)
        codex_manifest = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        claude_manifest = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual((codex_manifest["version"], claude_manifest["version"]), ("0.1.0", "0.1.0"))
        self.assertIn('version: "0.1"', skill)
        example = tomllib.loads((PLUGIN / "office-memory.toml.example").read_text(encoding="utf-8"))
        self.assertEqual((example["project_root"], example["awareness_file"], example["memory_file"]), ("..", ".agents/awareness/AWARENESS.md", ".agents/memory/MEMORY.md"))
        recent = next(item for item in example["sources"] if item["id"] == "qoder-recent")
        self.assertEqual((recent["role"], recent["default"]), ("recent", False))
        self.assertNotIn("--config office-memory.toml", skill)
        self.assertIn("--config .agents/office-memory.toml", skill)

    def test_init_falls_back_without_hardlink_and_leaves_no_temporary_file(self) -> None:
        with tempfile.TemporaryDirectory() as root_text:
            root = Path(root_text)
            output = root / "AWARENESS.md"
            with mock.patch.object(HELPER.os, "link", side_effect=OSError(errno.EOPNOTSUPP, "hardlinks unsupported")):
                self.assertTrue(HELPER.atomic_create(output, "complete\n"))
            self.assertEqual(output.read_text(encoding="utf-8"), "complete\n")
            self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o600)
            self.assertEqual([path.name for path in root.iterdir()], ["AWARENESS.md"])
            self.assertFalse(HELPER.atomic_create(output, "replacement\n"))
            self.assertEqual(output.read_text(encoding="utf-8"), "complete\n")
            with mock.patch.object(HELPER, "write_sync", side_effect=OSError("write failed")):
                with self.assertRaises(OSError):
                    HELPER.atomic_create(root / "MEMORY.md", "partial\n")
            self.assertEqual([path.name for path in root.iterdir()], ["AWARENESS.md"])

    def test_snapshot_rejects_a_file_that_changes_during_hashing(self) -> None:
        with tempfile.TemporaryDirectory() as root_text:
            path = Path(root_text) / "source.md"
            path.write_text("source", encoding="utf-8")
            stable = path.stat()
            changed = mock.Mock(st_dev=stable.st_dev, st_ino=stable.st_ino, st_size=stable.st_size + 1, st_mtime_ns=stable.st_mtime_ns, st_ctime_ns=stable.st_ctime_ns)
            with mock.patch.object(HELPER.os, "fstat", side_effect=(stable, changed)):
                with self.assertRaisesRegex(HELPER.ContractError, "changed while snapshotting"):
                    HELPER.snapshot_digest(path)

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
            self.assertEqual(status["outputs"]["daily"], {"count": 0, "directory": ".agents/memory", "invalid": 0, "latest": None})
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
            missing = run("snapshot", "--config", str(cfg), "--focus", "documents", "--material", "documents/missing.md", check=False)
            self.assertNotEqual(missing.returncode, 0)
            self.assertNotIn("Traceback", missing.stderr)
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
            reverse_overlap = write_config(root, external, source_path=root / ".agents/awareness/AWARENESS.md/source")
            self.assertNotEqual(run("check-config", "--config", str(reverse_overlap), check=False).returncode, 0)
            daily_overlap = write_config(root, external, source_path=root / ".agents/memory/2099-01-01.md")
            self.assertNotEqual(run("check-config", "--config", str(daily_overlap), check=False).returncode, 0)

            cfg = write_config(root, external)
            awareness.unlink()
            awareness.mkdir()
            result = run("validate", "--config", str(cfg), check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("not a regular file", result.stdout)
            self.assertNotIn("Traceback", result.stderr)
            result = run("init", "--config", str(cfg), "--apply", check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("Traceback", result.stderr)

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
            awareness_path.write_text(awareness().replace("- Focus: project", "- Focus: project\n- Focus: project"), encoding="utf-8")
            self.assertIn("needs non-empty", "\n".join(json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"]))
            awareness_path.write_text(awareness().replace("## Needs attention", "token=not-safe-value\n\n## Needs attention"), encoding="utf-8")
            self.assertIn("secret-like", "\n".join(json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"]))
            awareness_path.write_text(awareness(), encoding="utf-8")
            memory_path.write_text("# Project Memory\n\n" + entry() + entry(key="reviewed.fact", summary="token=not-safe-value") + entry(key="cross-scope", scope="other") + entry(key="expired", review="2000-01-01") + entry(key="missing-locator", sources="memory-source"), encoding="utf-8")
            errors = "\n".join(json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"])
            for expected in ("duplicate", "secret-like", "invalid scope", "expired", "invalid sources"):
                self.assertIn(expected, errors)
            awareness_path.write_text("x" * (16 * 1024 + 1), encoding="utf-8")
            self.assertIn("16 KiB", "\n".join(json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"]))

    def test_review_rejects_secret_without_memory_entries(self) -> None:
        with tempfile.TemporaryDirectory() as root_text, tempfile.TemporaryDirectory() as external_text:
            root, external = Path(root_text), Path(external_text)
            (external / "memory.md").write_text("source", encoding="utf-8")
            cfg = write_config(root, external)
            run("init", "--config", str(cfg), "--apply")
            (root / "documents").mkdir()
            (root / "documents/input.md").write_text("material", encoding="utf-8")
            (root / ".agents/awareness/AWARENESS.md").write_text(awareness(), encoding="utf-8")
            (root / ".agents/memory/MEMORY.md").write_text("# Project Memory\n\npassword=not-safe-value\n", encoding="utf-8")
            errors = json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"]
            self.assertTrue(any("secret-like" in error for error in errors), errors)

    def test_review_rejects_reserved_project_source_id(self) -> None:
        with tempfile.TemporaryDirectory() as root_text, tempfile.TemporaryDirectory() as external_text:
            root, external = Path(root_text), Path(external_text)
            (external / "memory.md").write_text("source", encoding="utf-8")
            cfg = write_config(root, external)
            cfg.write_text(cfg.read_text(encoding="utf-8").replace('id = "memory-source"', 'id = "project"', 1), encoding="utf-8")
            result = run("check-config", "--config", str(cfg), check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("reserved", result.stderr)

    def test_review_rejects_result_materials_and_root_memory_directory(self) -> None:
        with tempfile.TemporaryDirectory() as root_text, tempfile.TemporaryDirectory() as external_text:
            root, external = Path(root_text), Path(external_text)
            (external / "memory.md").write_text("source", encoding="utf-8")
            cfg = write_config(root, external)
            run("init", "--config", str(cfg), "--apply")
            daily_path = root / ".agents/memory/2026-07-24.md"
            daily_path.write_text(daily_record(), encoding="utf-8")
            for material in (".agents/awareness/AWARENESS.md", ".agents/memory/MEMORY.md", ".agents/memory/2026-07-24.md"):
                result = run("snapshot", "--config", str(cfg), "--focus", "project", "--material", material, check=False)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Office Memory result", result.stderr)

            (root / "documents").mkdir()
            (root / "documents/input.md").write_text("material", encoding="utf-8")
            (root / ".agents/awareness/AWARENESS.md").write_text(awareness(), encoding="utf-8")
            (root / ".agents/memory/MEMORY.md").write_text("# Project Memory\n\n" + entry(sources="project#.agents/memory/MEMORY.md"), encoding="utf-8")
            errors = "\n".join(json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"])
            self.assertIn("invalid sources", errors)

            cfg.write_text(cfg.read_text(encoding="utf-8").replace('memory_file = ".agents/memory/MEMORY.md"', 'memory_file = "MEMORY.md"'), encoding="utf-8")
            result = run("check-config", "--config", str(cfg), check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("dedicated", result.stderr)

    def test_review_rejects_non_directory_roots_and_nested_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as root_text, tempfile.TemporaryDirectory() as external_text:
            root, external = Path(root_text), Path(external_text)
            (external / "memory.md").write_text("source", encoding="utf-8")
            cfg = write_config(root, external)
            regular_file = root / "not-a-directory.md"
            regular_file.write_text("not a directory", encoding="utf-8")
            cfg.write_text(cfg.read_text(encoding="utf-8").replace(f'project_root = "{root.as_posix()}"', f'project_root = "{regular_file.as_posix()}"'), encoding="utf-8")
            result = run("check-config", "--config", str(cfg), check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("existing directory", result.stderr)

            for awareness_file, memory_file in ((".agents/memory/MEMORY.md/AWARENESS.md", ".agents/memory/MEMORY.md"), (".agents/awareness/AWARENESS.md", ".agents/awareness/AWARENESS.md/MEMORY.md")):
                cfg = write_config(root, external)
                content = cfg.read_text(encoding="utf-8").replace('awareness_file = ".agents/awareness/AWARENESS.md"', f'awareness_file = "{awareness_file}"').replace('memory_file = ".agents/memory/MEMORY.md"', f'memory_file = "{memory_file}"')
                cfg.write_text(content, encoding="utf-8")
                result = run("check-config", "--config", str(cfg), check=False)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("not nest", result.stderr)

    def test_review_skill_uses_real_focus_flag(self) -> None:
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("pass `--focus project`", skill)
        self.assertNotIn("pass `focus=project`", skill)

    def test_review_readme_uses_bundled_helper_path(self) -> None:
        readme = (PLUGIN / "README.md").read_text(encoding="utf-8")
        helper = SCRIPT.relative_to(PLUGIN).as_posix()
        self.assertIn(f"python3 {helper} check-config", readme)
        self.assertNotIn("python3 office_memory.py", readme)
        self.assertIn(".agents/office-memory.toml", readme)
        ignored = subprocess.run(["git", "check-ignore", "-q", "--no-index", ".agents/office-memory.toml"], cwd=ROOT)
        self.assertEqual(ignored.returncode, 0)

    def test_common_credentials_are_rejected_across_all_results(self) -> None:
        with tempfile.TemporaryDirectory() as root_text, tempfile.TemporaryDirectory() as external_text:
            root, external = Path(root_text), Path(external_text)
            (external / "memory.md").write_text("source", encoding="utf-8")
            cfg = write_config(root, external)
            run("init", "--config", str(cfg), "--apply")
            awareness_path = root / ".agents/awareness/AWARENESS.md"
            memory_path = root / ".agents/memory/MEMORY.md"
            daily_path = root / ".agents/memory/2026-07-24.md"

            awareness_path.write_text(awareness().replace("## Needs attention", "ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890\n\n## Needs attention"), encoding="utf-8")
            memory_path.write_text("# Project Memory\n\n", encoding="utf-8")
            self.assertIn("secret-like", "\n".join(json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"]))

            awareness_path.write_text(awareness(), encoding="utf-8")
            daily_path.write_text(daily_record(content="- hf_ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890\n"), encoding="utf-8")
            self.assertIn("secret-like", "\n".join(json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"]))

            daily_path.unlink()
            for credential in (
                "Authorization: Bearer abcdefghijklmnopqrstuvwxyz",
                "api key: abcdefghijklmnopqrstuvwxyz",
                "github_pat_ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890",
                "OPENAI_API_KEY=abcdefghijklmnop",
                "GITHUB_TOKEN=abcdefghijklmnop",
                "AWS_SECRET_ACCESS_KEY=abcdefghijklmnop",
                "ASIAIOSFODNN7EXAMPLE",
            ):
                memory_path.write_text("# Project Memory\n\n" + entry(summary=credential), encoding="utf-8")
                self.assertIn("secret-like", "\n".join(json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"]))

            memory_path.write_text("# Project Memory\n\n" + entry(summary="A stable note about token budgets without a credential."), encoding="utf-8")
            self.assertEqual(run("validate", "--config", str(cfg)).returncode, 0)

    def test_metadata_must_live_in_header_and_scope_refs_stay_in_scope(self) -> None:
        with tempfile.TemporaryDirectory() as root_text, tempfile.TemporaryDirectory() as external_text:
            root, external = Path(root_text), Path(external_text)
            (external / "memory.md").write_text("source", encoding="utf-8")
            cfg = write_config(root, external)
            run("init", "--config", str(cfg), "--apply")
            (root / "documents").mkdir()
            (root / "documents/input.md").write_text("material", encoding="utf-8")
            awareness_path = root / ".agents/awareness/AWARENESS.md"
            memory_path = root / ".agents/memory/MEMORY.md"
            daily_path = root / ".agents/memory/2026-07-24.md"

            awareness_path.write_text(awareness(), encoding="utf-8")
            memory_path.write_text("# Project Memory\n\n", encoding="utf-8")
            self.assertEqual(run("validate", "--config", str(cfg)).returncode, 0)

            misplaced = awareness().replace("- Focus: project\n", "").replace("## Current understanding\n", "## Current understanding\n- Focus: project\n")
            awareness_path.write_text(misplaced, encoding="utf-8")
            self.assertIn("needs non-empty", "\n".join(json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"]))

            cross_line = awareness().replace("- Focus: project", "- Focus:\nproject")
            awareness_path.write_text(cross_line, encoding="utf-8")
            self.assertIn("needs non-empty", "\n".join(json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"]))

            daily_path.write_text(daily_record().replace("- Focus: project\n", "").replace("## Meaningful changes\n", "## Meaningful changes\n- Focus: project\n"), encoding="utf-8")
            errors = "\n".join(json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"])
            self.assertIn("non-empty Focus", errors)
            daily_path.unlink()

            daily_path.write_text(daily_record().replace("- Focus: project", "- Focus:\nproject"), encoding="utf-8")
            errors = "\n".join(json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"])
            self.assertIn("non-empty Focus", errors)
            daily_path.unlink()

            awareness_path.write_text(awareness().replace("- Focus: project", "- Focus: documents").replace("project#documents/input.md", "project#other/input.md"), encoding="utf-8")
            self.assertIn("Sources checked", "\n".join(json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"]))
            awareness_path.write_text(awareness().replace("- Focus: project", "- Focus: documents"), encoding="utf-8")
            self.assertEqual(run("validate", "--config", str(cfg)).returncode, 0)

            memory_path.write_text("# Project Memory\n\nUnsourced prose before entries.\n", encoding="utf-8")
            self.assertIn("outside memory entries", "\n".join(json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"]))

            memory_path.write_text("# Project Memory\n\n" + entry(scope="documents", sources="memory-source#memory.md; project#other/input.md"), encoding="utf-8")
            self.assertIn("invalid sources", "\n".join(json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"]))
            memory_path.write_text("# Project Memory\n\n" + entry(scope="documents", sources="memory-source#memory.md; project#documents/input.md"), encoding="utf-8")
            self.assertEqual(run("validate", "--config", str(cfg)).returncode, 0)

            misplaced_entry = entry().replace("- Kind: fact\n", "").replace("A reviewed, conservative fact.", "- Kind: fact\nA reviewed, conservative fact.")
            memory_path.write_text("# Project Memory\n\n" + misplaced_entry, encoding="utf-8")
            self.assertIn("missing memory entry fields", "\n".join(json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"]))

            cross_line_entry = entry().replace("- Scope: project", "- Scope:\nproject")
            memory_path.write_text("# Project Memory\n\n" + cross_line_entry, encoding="utf-8")
            self.assertIn("missing memory entry fields", "\n".join(json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"]))

    def test_daily_status_and_valid_schema(self) -> None:
        with tempfile.TemporaryDirectory() as root_text, tempfile.TemporaryDirectory() as external_text:
            root, external = Path(root_text), Path(external_text)
            (external / "memory.md").write_text("source", encoding="utf-8")
            cfg = write_config(root, external)
            run("init", "--config", str(cfg), "--apply")
            (root / "documents").mkdir()
            (root / "documents/input.md").write_text("material", encoding="utf-8")
            (root / ".agents/awareness/AWARENESS.md").write_text(awareness(), encoding="utf-8")
            daily_dir = root / ".agents/memory"
            (daily_dir / "2026-07-23.md").write_text(daily_record(day="2026-07-23"), encoding="utf-8")
            (daily_dir / "2026-07-24.md").write_text(daily_record(), encoding="utf-8")
            self.assertEqual(run("validate", "--config", str(cfg)).returncode, 0)
            status = json.loads(run("check-config", "--config", str(cfg)).stdout)["outputs"]["daily"]
            self.assertEqual((status["count"], status["latest"], status["invalid"]), (2, "2026-07-24", 0))

    def test_daily_schema_rejects_unsafe_or_empty_records(self) -> None:
        with tempfile.TemporaryDirectory() as root_text, tempfile.TemporaryDirectory() as external_text:
            root, external = Path(root_text), Path(external_text)
            (external / "memory.md").write_text("source", encoding="utf-8")
            cfg = write_config(root, external)
            run("init", "--config", str(cfg), "--apply")
            (root / "documents").mkdir()
            (root / "documents/input.md").write_text("material", encoding="utf-8")
            (root / ".agents/awareness/AWARENESS.md").write_text(awareness(), encoding="utf-8")
            path = root / ".agents/memory/2026-07-24.md"

            cases = (
                (daily_record(day="2026-07-23"), "heading date"),
                (daily_record(focus="other"), "Focus"),
                (daily_record(sources="unknown-source"), "Sources checked"),
                (daily_record(content="password=not-safe-value\n"), "secret-like"),
                (daily_record(content=""), "curated item"),
                (daily_record(content="x" * (13 * 1024)), "12 KiB"),
                (daily_record().replace("- Focus: project", "- Focus: project\n- Focus: project"), "non-empty Focus"),
            )
            for content, expected in cases:
                path.write_text(content, encoding="utf-8")
                errors = "\n".join(json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"])
                self.assertIn(expected, errors)

            path.write_text(daily_record(), encoding="utf-8")
            invalid_date = root / ".agents/memory/2026-13-40.md"
            invalid_date.write_text(daily_record(day="2026-13-40"), encoding="utf-8")
            errors = "\n".join(json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"])
            self.assertIn("valid date", errors)
            status = json.loads(run("check-config", "--config", str(cfg)).stdout)["outputs"]["daily"]
            self.assertEqual((status["count"], status["latest"], status["invalid"]), (1, "2026-07-24", 1))
            invalid_date.unlink()

            unexpected = root / ".agents/memory/notes.md"
            unexpected.write_text("not a daily record", encoding="utf-8")
            errors = "\n".join(json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"])
            self.assertIn("unexpected project memory artifact", errors)
            unexpected.unlink()

            state = root / ".agents/memory/state.json"
            state.write_text("{}", encoding="utf-8")
            errors = "\n".join(json.loads(run("validate", "--config", str(cfg), check=False).stdout)["errors"])
            self.assertIn("unexpected project memory artifact", errors)


if __name__ == "__main__":
    unittest.main()
