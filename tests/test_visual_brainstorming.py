from __future__ import annotations

import concurrent.futures
import contextlib
import hashlib
import http.client
import http.server
import importlib.util
import json
import os
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest
import urllib.parse
from pathlib import Path
from typing import Any
from unittest import mock


sys.dont_write_bytecode = True


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "visual-brainstorming"
SKILL_ROOT = PLUGIN_ROOT / "skills" / "visual-brainstorming"
SCRIPT = SKILL_ROOT / "scripts" / "companion.py"
CODEX_MANIFEST = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
CLAUDE_MANIFEST = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"
CODEX_MARKETPLACE = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
CLAUDE_MARKETPLACE = REPO_ROOT / ".claude-plugin" / "marketplace.json"


def load_companion() -> Any:
    spec = importlib.util.spec_from_file_location("visual_brainstorming_companion", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load companion module: {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


COMPANION = load_companion()


def cli_command(*arguments: str) -> list[str]:
    return [sys.executable, "-I", "-S", str(SCRIPT), *arguments]


def run_cli(
    project: Path,
    *arguments: str,
    check: bool = True,
    timeout: float = 15,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cli_command(*arguments, "--project-dir", str(project)),
        check=check,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def make_old_session(
    sessions_root: Path,
    name: str,
    *,
    age_days: int,
    content: str = "<p>old</p>",
) -> Path:
    session = sessions_root / name
    content_dir = session / "content"
    state_dir = session / "state"
    content_dir.mkdir(parents=True)
    state_dir.mkdir()
    screen = content_dir / "screen.html"
    screen.write_text(content, encoding="utf-8")
    timestamp = time.time() - age_days * 24 * 60 * 60
    for path in (screen, content_dir, state_dir, session):
        os.utime(path, (timestamp, timestamp))
    return session


class FakeOldServer:
    def __init__(self, project: Path, version: str = "2.3.0") -> None:
        self.project = COMPANION.resolve_project(project)
        self.version = version
        owner = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, _format: str, *_args: Any) -> None:
                return

            def _send(self, value: dict[str, Any]) -> None:
                body = (json.dumps(value) + "\n").encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self) -> None:  # noqa: N802
                if urllib.parse.urlsplit(self.path).path == "/api/health":
                    self._send(
                        {"ok": True, "version": owner.version, "pid": os.getpid()}
                    )
                    return
                self.send_error(404)

            def do_POST(self) -> None:  # noqa: N802
                if urllib.parse.urlsplit(self.path).path == "/api/shutdown":
                    self._send({"ok": True, "stopping": True})
                    threading.Thread(
                        target=owner.server.shutdown, daemon=True
                    ).start()
                    return
                self.send_error(404)

        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        session = COMPANION.prepare_session(self.project)
        info = COMPANION.build_info(
            session,
            "127.0.0.1",
            "127.0.0.1",
            int(self.server.server_address[1]),
            False,
            30,
        )
        info["pid"] = os.getpid()
        COMPANION.write_json(session.state_dir / "server-info.json", info, mode=0o600)
        COMPANION.write_json(
            COMPANION.current_file(self.project), info, mode=0o600
        )
        self.info = info

    def close(self) -> None:
        with contextlib.suppress(Exception):
            self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def __enter__(self) -> "FakeOldServer":
        return self

    def __exit__(self, _exc_type: Any, _exc: Any, _traceback: Any) -> None:
        self.close()


class ProxyCaptureServer:
    def __init__(self) -> None:
        owner = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, _format: str, *_args: Any) -> None:
                return

            def do_GET(self) -> None:  # noqa: N802
                owner.requests += 1
                self.send_error(502)

        self.requests = 0
        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.server.server_address[1]}"

    def __enter__(self) -> "ProxyCaptureServer":
        return self

    def __exit__(self, _exc_type: Any, _exc: Any, _traceback: Any) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)


class RunningCompanion:
    def __init__(
        self,
        project: Path,
        *,
        idle_timeout: int = 30,
        extra_arguments: list[str] | None = None,
    ) -> None:
        self.project = project.expanduser().resolve()
        result = subprocess.run(
            cli_command(
                "demo",
                "--project-dir",
                str(self.project),
                "--idle-timeout",
                str(idle_timeout),
                *(extra_arguments or []),
            ),
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode != 0:
            raise RuntimeError(
                "companion demo failed "
                f"with exit {result.returncode}: stdout={result.stdout!r} "
                f"stderr={result.stderr!r}"
            )
        self.show_result = json.loads(result.stdout)
        self.info = json.loads(
            (self.project / ".visual-brainstorming" / "current.json").read_text(
                encoding="utf-8"
            )
        )
        parsed = urllib.parse.urlsplit(self.info["control_url"])
        self.host = parsed.hostname or "127.0.0.1"
        self.port = parsed.port or 0
        self.key = (urllib.parse.parse_qs(parsed.query).get("key") or [""])[0]

    def __enter__(self) -> "RunningCompanion":
        return self

    def __exit__(self, _exc_type: Any, _exc: Any, _traceback: Any) -> None:
        self.stop()

    def request(
        self,
        path: str,
        *,
        method: str = "GET",
        headers: dict[str, str] | None = None,
        body: bytes | None = None,
    ) -> tuple[int, dict[str, str], bytes]:
        connection = http.client.HTTPConnection(self.host, self.port, timeout=3)
        connection.request(method, path, body=body, headers=headers or {})
        response = connection.getresponse()
        data = response.read()
        response_headers = dict(response.getheaders())
        status = response.status
        connection.close()
        return status, response_headers, data

    def keyed(self, path: str) -> str:
        separator = "&" if "?" in path else "?"
        return f"{path}{separator}key={urllib.parse.quote(self.key)}"

    def capability(self, path: str) -> str:
        return f"/_vb/{urllib.parse.quote(self.key, safe='')}{path}"

    def _force_terminate(self) -> None:
        try:
            pid = int(self.info.get("pid", 0))
        except (AttributeError, TypeError, ValueError):
            return
        if pid <= 0 or not COMPANION.process_is_alive(pid):
            return
        if os.name == "nt":
            subprocess.run(
                ["taskkill", "/PID", str(pid), "/T", "/F"],
                capture_output=True,
                text=True,
                check=False,
            )
            return
        with contextlib.suppress(OSError):
            os.kill(pid, signal.SIGTERM)
        deadline = time.time() + 2
        while time.time() < deadline and COMPANION.process_is_alive(pid):
            time.sleep(0.05)
        if COMPANION.process_is_alive(pid):
            with contextlib.suppress(OSError):
                os.kill(pid, signal.SIGKILL)

    def stop(self) -> None:
        if not self.project.is_dir():
            raise RuntimeError(
                f"cannot stop companion after project removal: {self.project}"
            )
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-I",
                    "-S",
                    str(SCRIPT),
                    "stop",
                    "--project-dir",
                    str(self.project),
                ],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            outcome = json.loads(result.stdout) if result.returncode == 0 else {}
            deadline = time.time() + 3
            pid = int(getattr(self, "info", {}).get("pid", 0))
            while (
                pid > 0
                and time.time() < deadline
                and COMPANION.process_is_alive(pid)
            ):
                time.sleep(0.05)
            stopped = pid <= 0 or not COMPANION.process_is_alive(pid)
            if result.returncode == 0 and stopped and (
                outcome.get("stopped") is True
                or outcome.get("reason")
                in {"server is not running", "no current session"}
            ):
                return
            detail = outcome or {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
            raise RuntimeError(f"companion shutdown was not confirmed: {detail}")
        except Exception:
            self._force_terminate()
            raise


class VisualBrainstormingPackageTest(unittest.TestCase):
    def test_manifests_marketplaces_and_version_are_aligned(self) -> None:
        codex = json.loads(CODEX_MANIFEST.read_text(encoding="utf-8"))
        claude = json.loads(CLAUDE_MANIFEST.read_text(encoding="utf-8"))
        codex_marketplace = json.loads(CODEX_MARKETPLACE.read_text(encoding="utf-8"))
        claude_marketplace = json.loads(CLAUDE_MARKETPLACE.read_text(encoding="utf-8"))

        self.assertEqual(codex["name"], PLUGIN_ROOT.name)
        self.assertEqual(claude["name"], codex["name"])
        self.assertEqual(codex["version"], COMPANION.VERSION)
        self.assertEqual(claude["version"], COMPANION.VERSION)
        self.assertEqual(codex["license"], "MIT")
        self.assertEqual(claude["license"], "MIT")
        self.assertEqual(codex["skills"], "./skills/")
        self.assertEqual(
            (PLUGIN_ROOT / "LICENSE.txt").read_bytes(),
            (SKILL_ROOT / "LICENSE.txt").read_bytes(),
        )
        self.assertIn(
            "skills/visual-brainstorming/references/SOURCES.md",
            (PLUGIN_ROOT / "NOTICE.md").read_text(encoding="utf-8"),
        )

        codex_names = [item["name"] for item in codex_marketplace["plugins"]]
        claude_names = [item["name"] for item in claude_marketplace["plugins"]]
        self.assertEqual(len(codex_names), len(set(codex_names)))
        self.assertEqual(len(claude_names), len(set(claude_names)))
        self.assertEqual(codex_names.count("visual-brainstorming"), 1)
        self.assertEqual(claude_names.count("visual-brainstorming"), 1)
        codex_entries = {
            item["name"]: item for item in codex_marketplace["plugins"]
        }
        claude_entries = {
            item["name"]: item for item in claude_marketplace["plugins"]
        }
        codex_entry = codex_entries["visual-brainstorming"]
        self.assertEqual(
            codex_entry["source"]["path"],
            "./plugins/visual-brainstorming",
        )
        self.assertEqual(codex_entry["policy"]["installation"], "AVAILABLE")
        self.assertEqual(codex_entry["policy"]["authentication"], "ON_INSTALL")
        self.assertEqual(codex_entry["category"], "Productivity")
        self.assertEqual(
            claude_entries["visual-brainstorming"]["source"],
            "./plugins/visual-brainstorming",
        )

        junk = [
            path
            for path in PLUGIN_ROOT.rglob("*")
            if path.name in {".DS_Store", "Thumbs.db", "desktop.ini", "__pycache__"}
            or path.suffix == ".pyc"
        ]
        self.assertEqual(junk, [])

    def test_runtime_gitignore_is_exact_and_hides_state(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            subprocess.run(
                ["git", "init", "--quiet", str(project)],
                check=True,
                capture_output=True,
                text=True,
            )
            with RunningCompanion(project):
                ignore_file = project / ".visual-brainstorming" / ".gitignore"
                self.assertEqual(ignore_file.read_text(encoding="utf-8"), "*\n")
                status = subprocess.check_output(
                    ["git", "status", "--porcelain", "--untracked-files=all"],
                    cwd=project,
                    text=True,
                )
                self.assertEqual(status, "")
                if os.name != "nt":
                    self.assertEqual(ignore_file.stat().st_mode & 0o777, 0o600)

    def test_runtime_gitignore_rejects_symlink_and_non_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary, tempfile.TemporaryDirectory() as outside:
            root = Path(temporary) / ".visual-brainstorming"
            root.mkdir()
            ignore_file = root / ".gitignore"
            target = Path(outside) / "ignore"
            target.write_text("keep\n", encoding="utf-8")
            try:
                ignore_file.symlink_to(target)
            except (NotImplementedError, OSError) as exc:
                self.skipTest(f"symlink creation unavailable: {exc}")
            with self.assertRaisesRegex(COMPANION.CompanionError, "symlinked"):
                COMPANION.ensure_runtime_ignore(root)
            ignore_file.unlink()
            ignore_file.mkdir()
            with self.assertRaisesRegex(COMPANION.CompanionError, "not a file"):
                COMPANION.ensure_runtime_ignore(root)

    def test_url_host_contract_rejects_external_or_unassigned_addresses(self) -> None:
        COMPANION.validate_url_host("127.0.0.1", allow_remote=False)
        self.assertEqual(
            COMPANION.parse_http_authority("[::1]:54321"),
            ("::1", 54321),
        )
        self.assertEqual(
            COMPANION.parse_http_origin("http://[::1]:54321"),
            ("::1", 54321),
        )
        self.assertIsNone(COMPANION.parse_http_authority("::1:54321"))
        with self.assertRaisesRegex(COMPANION.CompanionError, "loopback"):
            COMPANION.validate_url_host("10.0.0.5", allow_remote=False)

        private_resolution = [
            (
                socket.AF_INET,
                socket.SOCK_STREAM,
                socket.IPPROTO_TCP,
                "",
                ("10.0.0.5", 0),
            )
        ]
        with mock.patch.object(
            COMPANION.socket, "getaddrinfo", return_value=private_resolution
        ), mock.patch.object(
            COMPANION, "address_is_assigned_locally", return_value=True
        ):
            COMPANION.validate_url_host("10.0.0.5", allow_remote=True)

        with mock.patch.object(
            COMPANION.socket, "getaddrinfo", return_value=private_resolution
        ), mock.patch.object(
            COMPANION, "address_is_assigned_locally", return_value=False
        ):
            with self.assertRaisesRegex(COMPANION.CompanionError, "assigned"):
                COMPANION.validate_url_host("10.0.0.5", allow_remote=True)

        public_resolution = [
            (
                socket.AF_INET,
                socket.SOCK_STREAM,
                socket.IPPROTO_TCP,
                "",
                ("8.8.8.8", 0),
            )
        ]
        with mock.patch.object(
            COMPANION.socket, "getaddrinfo", return_value=public_resolution
        ):
            with self.assertRaisesRegex(COMPANION.CompanionError, "loopback, private"):
                COMPANION.validate_url_host("8.8.8.8", allow_remote=True)

        with self.assertRaisesRegex(COMPANION.CompanionError, "literal IP"):
            COMPANION.validate_url_host("example.com", allow_remote=True)
        with self.assertRaisesRegex(COMPANION.CompanionError, "literal IP"):
            COMPANION.validate_url_host("localhost", allow_remote=True)

    def test_wildcard_server_bind_does_not_resolve_hostname(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            session = COMPANION.prepare_session(Path(temporary))
            context = COMPANION.ServerContext(
                session=session,
                host="0.0.0.0",
                url_host="127.0.0.1",
                port=0,
                allow_remote=True,
                idle_timeout_seconds=30,
            )
            with mock.patch.object(
                COMPANION.socket,
                "getfqdn",
                side_effect=AssertionError("reverse DNS must not run during bind"),
            ):
                server = COMPANION.CompanionHTTPServer(
                    ("0.0.0.0", 0),
                    COMPANION.Handler,
                    context,
                )
            try:
                self.assertEqual(server.server_name, "127.0.0.1")
                self.assertEqual(server.server_port, server.server_address[1])
            finally:
                server.server_close()

    def test_control_requests_ignore_proxy_environment(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            with RunningCompanion(project) as running, ProxyCaptureServer() as proxy:
                with mock.patch.dict(
                    os.environ,
                    {"HTTP_PROXY": proxy.url, "http_proxy": proxy.url},
                    clear=False,
                ):
                    health = COMPANION.http_json(
                        COMPANION.endpoint_from_info(running.info, "/api/health")
                    )
                self.assertTrue(health["ok"])
                self.assertEqual(proxy.requests, 0)

    def test_bridge_is_bound_to_each_screen_version(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            with RunningCompanion(project) as running:
                status, _, body = running.request(running.keyed("/api/latest"))
                self.assertEqual(status, 200)
                first = json.loads(body)
                self.assertTrue(first["bridge"])
                status, _, body = running.request(
                    running.keyed(f"/screen/{urllib.parse.quote(first['name'])}")
                )
                self.assertEqual(status, 200)
                rendered = body.decode("utf-8")
                self.assertIn(f'const BRIDGE = "{first["bridge"]}"', rendered)
                self.assertNotIn("__VB_BRIDGE_TOKEN__", rendered)

                published = COMPANION.publish_impl(
                    running.project,
                    SKILL_ROOT / "examples" / "01-product-layout.html",
                    "bridge-change",
                    expected_session=Path(running.info["session_dir"]),
                )
                status, _, body = running.request(running.keyed("/api/latest"))
                self.assertEqual(status, 200)
                second = json.loads(body)
                self.assertEqual(second["name"], published["name"])
                self.assertNotEqual(second["bridge"], first["bridge"])

                shell_js = (SKILL_ROOT / "assets" / "browser-shell.js").read_text(
                    encoding="utf-8"
                )
                self.assertIn(
                    "message.data.bridge !== currentBridge",
                    shell_js,
                )

    def test_runtime_does_not_accept_session_key_from_cookie(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with RunningCompanion(Path(temporary)) as running:
                cookie_name = "vb_" + hashlib.sha256(
                    str(Path(running.info["session_dir"])).encode("utf-8")
                ).hexdigest()[:12]
                status, _, _ = running.request(
                    "/api/session",
                    headers={"Cookie": f"{cookie_name}={running.key}"},
                )
                self.assertEqual(status, 403)

    def test_current_info_accepts_fragment_and_legacy_query_but_rejects_ambiguity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            session = COMPANION.prepare_session(project)
            info = COMPANION.build_info(
                session,
                "127.0.0.1",
                "127.0.0.1",
                54321,
                False,
                30,
            )
            current_path = COMPANION.current_file(project)

            COMPANION.write_json(current_path, info, mode=0o600)
            self.assertIsNotNone(COMPANION.current_info(project))

            legacy = dict(info)
            legacy["url"] = f"http://127.0.0.1:54321/?key={session.key}"
            COMPANION.write_json(current_path, legacy, mode=0o600)
            self.assertIsNotNone(COMPANION.current_info(project))

            invalid_urls = [
                f"http://127.0.0.1:54321/?key=wrong#key={session.key}",
                f"http://127.0.0.1:54321/#key={session.key}&key={session.key}",
                f"http://127.0.0.1:54321/unexpected#key={session.key}",
                f"http://127.0.0.1:54322/#key={session.key}",
            ]
            for invalid_url in invalid_urls:
                with self.subTest(url=invalid_url):
                    invalid = dict(info)
                    invalid["url"] = invalid_url
                    COMPANION.write_json(current_path, invalid, mode=0o600)
                    self.assertIsNone(COMPANION.current_info(project))

    def test_runtime_auth_security_events_and_favicon(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with RunningCompanion(Path(temporary)) as running:
                browser_url = urllib.parse.urlsplit(running.info["url"])
                self.assertEqual(browser_url.query, "")
                self.assertEqual(
                    (urllib.parse.parse_qs(browser_url.fragment).get("key") or [""])[0],
                    running.key,
                )

                status, headers, body = running.request("/")
                self.assertEqual(status, 200)
                self.assertIn(b"sandbox=\"allow-scripts\"", body)
                self.assertIn(b'href="/favicon.svg"', body)
                self.assertIn(b"sessionStorage", body)
                self.assertIn(b"/_vb/", body)
                self.assertIn(b"invalidLocationKey", body)
                self.assertNotIn(running.key.encode("utf-8"), body)
                self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
                self.assertEqual(headers["Referrer-Policy"], "no-referrer")
                self.assertIn("Content-Security-Policy", headers)
                self.assertNotIn("Set-Cookie", headers)

                status, _, body = running.request(
                    running.capability("/api/session")
                )
                self.assertEqual(status, 200)
                public_session = json.loads(body)
                self.assertNotIn("control_url", public_session)
                self.assertNotIn(running.key, body.decode("utf-8"))

                status, _, body = running.request(running.capability("/api/latest"))
                self.assertEqual(status, 200)
                latest = json.loads(body)
                screen_route = running.capability(
                    f"/screen/{urllib.parse.quote(latest['name'])}"
                )
                status, screen_headers, _ = running.request(screen_route)
                self.assertEqual(status, 200)
                self.assertEqual(screen_headers["Referrer-Policy"], "same-origin")

                asset = Path(running.info["screen_dir"]) / "asset.txt"
                asset.write_text("asset", encoding="utf-8")
                status, _, _ = running.request("/files/asset.txt")
                self.assertEqual(status, 403)
                status, _, asset_body = running.request(
                    running.capability("/files/asset.txt")
                )
                self.assertEqual(status, 200)
                self.assertEqual(asset_body, b"asset")
                status, _, asset_body = running.request(
                    "/files/asset.txt",
                    headers={
                        "Referer": f"http://{running.host}:{running.port}{screen_route}"
                    },
                )
                self.assertEqual(status, 200)
                self.assertEqual(asset_body, b"asset")
                status, _, _ = running.request(
                    "/files/asset.txt",
                    headers={
                        "Referer": f"http://{running.host}:{running.port + 1}{screen_route}"
                    },
                )
                self.assertEqual(status, 403)

                status, _, _ = running.request(
                    f"/api/session?key={urllib.parse.quote(running.key)}&key={urllib.parse.quote(running.key)}"
                )
                self.assertEqual(status, 403)

                status, _, _ = running.request(
                    running.keyed("/api/health"), headers={"Host": "evil.example"}
                )
                self.assertEqual(status, 403)

                status, _, _ = running.request(
                    running.keyed("/files/%2e%2e/state/session-key")
                )
                self.assertEqual(status, 404)

                payload = json.dumps(
                    {"type": "choice", "choice": "blocked"}
                ).encode()
                status, _, _ = running.request(
                    running.keyed("/api/events"),
                    method="POST",
                    headers={
                        "Content-Type": "application/json",
                        "X-VB-Client": "1",
                        "Origin": "http://evil.example",
                    },
                    body=payload,
                )
                self.assertEqual(status, 403)

                status, _, _ = running.request(
                    running.keyed("/api/events"),
                    method="POST",
                    headers={"Content-Type": "application/json"},
                    body=payload,
                )
                self.assertEqual(status, 403)

                event_headers = {
                    "Content-Type": "application/json",
                    "X-VB-Client": "1",
                }

                def post_event(index: int) -> int:
                    event = json.dumps(
                        {"type": "choice", "choice": f"choice-{index}"}
                    ).encode()
                    status, _, _ = running.request(
                        running.capability("/api/events"),
                        method="POST",
                        headers={
                            **event_headers,
                            "Origin": f"http://{running.host}:{running.port}",
                        },
                        body=event,
                    )
                    return status

                with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
                    statuses = list(executor.map(post_event, range(24)))
                self.assertEqual(statuses, [201] * 24)

                events = COMPANION.read_events(
                    Path(running.info["state_dir"]) / "events.jsonl"
                )
                self.assertEqual(
                    sorted(event["id"] for event in events), list(range(1, 25))
                )

                for route in ("/favicon.svg", "/favicon.ico"):
                    status, headers, body = running.request(route)
                    self.assertEqual(status, 200)
                    self.assertEqual(
                        headers["Content-Type"], "image/svg+xml; charset=utf-8"
                    )
                    self.assertTrue(body.startswith(b"<svg"))

                if os.name != "nt":
                    session_mode = (
                        Path(running.info["session_dir"]).stat().st_mode & 0o777
                    )
                    key_mode = (
                        Path(running.info["state_dir"]) / "session-key"
                    ).stat().st_mode & 0o777
                    self.assertEqual(session_mode, 0o700)
                    self.assertEqual(key_mode, 0o600)

                running.stop()
                status_output = subprocess.check_output(
                    [
                        sys.executable,
                        "-I",
                        "-S",
                        str(SCRIPT),
                        "status",
                        "--project-dir",
                        temporary,
                    ],
                    text=True,
                    timeout=10,
                )
                self.assertFalse(json.loads(status_output)["running"])

    def test_host_authority_requires_the_actual_server_port(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with RunningCompanion(Path(temporary)) as running:
                wrong_port = (
                    running.port - 1
                    if running.port == 65535
                    else running.port + 1
                )
                wrong_authority = f"{running.host}:{wrong_port}"

                status, _, _ = running.request(
                    running.capability("/api/session"),
                    headers={"Host": wrong_authority},
                )
                self.assertEqual(status, 403)

                status, _, _ = running.request(
                    running.capability("/api/session"),
                    headers={"Host": running.host},
                )
                self.assertEqual(status, 403)

                payload = json.dumps(
                    {"type": "choice", "choice": "wrong-authority"}
                ).encode()
                status, _, _ = running.request(
                    running.capability("/api/events"),
                    method="POST",
                    headers={
                        "Host": wrong_authority,
                        "Origin": f"http://{wrong_authority}",
                        "X-VB-Client": "1",
                        "Content-Type": "application/json",
                    },
                    body=payload,
                )
                self.assertEqual(status, 403)

                asset = Path(running.info["screen_dir"]) / "legacy.txt"
                asset.write_text("legacy", encoding="utf-8")
                status, _, _ = running.request(
                    "/files/legacy.txt",
                    headers={
                        "Host": wrong_authority,
                        "Referer": (
                            f"http://{wrong_authority}"
                            f"{running.capability('/screen/legacy.html')}"
                        ),
                    },
                )
                self.assertEqual(status, 403)

                status, _, _ = running.request(
                    running.capability("/api/session"),
                    headers={"Host": f"::1:{running.port}"},
                )
                self.assertEqual(status, 403)

    def test_capability_posts_require_origin_but_cli_shutdown_does_not(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with RunningCompanion(Path(temporary)) as running:
                headers = {
                    "X-VB-Client": "1",
                    "Content-Type": "application/json",
                }
                event = json.dumps(
                    {"type": "choice", "choice": "origin-required"}
                ).encode()

                status, _, _ = running.request(
                    running.capability("/api/events"),
                    method="POST",
                    headers=headers,
                    body=event,
                )
                self.assertEqual(status, 403)

                status, _, _ = running.request(
                    running.capability("/api/shutdown"),
                    method="POST",
                    headers=headers,
                    body=b"{}",
                )
                self.assertEqual(status, 403)

                exact_origin = f"http://{running.host}:{running.port}"
                status, _, _ = running.request(
                    running.capability("/api/events"),
                    method="POST",
                    headers={**headers, "Origin": exact_origin},
                    body=event,
                )
                self.assertEqual(status, 201)

                status, _, _ = running.request(
                    running.capability("/api/shutdown"),
                    method="POST",
                    headers={**headers, "Origin": exact_origin},
                    body=b"{}",
                )
                self.assertEqual(status, 200)

        with tempfile.TemporaryDirectory() as temporary:
            with RunningCompanion(Path(temporary)) as running:
                invalid_query = (
                    "/api/shutdown?key="
                    f"{urllib.parse.quote(running.key)}&unexpected=1"
                )
                status, _, _ = running.request(
                    invalid_query,
                    method="POST",
                    headers={
                        "X-VB-Client": "1",
                        "Content-Type": "application/json",
                    },
                    body=b"{}",
                )
                self.assertEqual(status, 403)

                status, _, _ = running.request(
                    running.keyed("/api/shutdown"),
                    method="POST",
                    headers={
                        "X-VB-Client": "1",
                        "Content-Type": "application/json",
                    },
                    body=b"{}",
                )
                self.assertEqual(status, 200)

    def test_event_count_and_size_limits_do_not_consume_ids_on_rejection(self) -> None:
        self.assertEqual(COMPANION.MAX_EVENTS_PER_SESSION, 10_000)
        self.assertEqual(COMPANION.MAX_EVENTS_FILE_BYTES, 5 * 1024 * 1024)
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            session = COMPANION.prepare_session(project)
            (session.content_dir / "screen.html").write_text(
                "<p>screen</p>", encoding="utf-8"
            )
            context = COMPANION.ServerContext(
                session=session,
                host="127.0.0.1",
                url_host="127.0.0.1",
                port=0,
                allow_remote=False,
                idle_timeout_seconds=30,
            )
            with mock.patch.object(COMPANION, "MAX_EVENTS_PER_SESSION", 2):
                self.assertEqual(
                    context.append_event({"type": "choice", "choice": "one"})["id"],
                    1,
                )
                self.assertEqual(
                    context.append_event({"type": "choice", "choice": "two"})["id"],
                    2,
                )
                with self.assertRaisesRegex(COMPANION.CompanionError, "event limit"):
                    context.append_event({"type": "choice", "choice": "blocked"})
            self.assertEqual(context.event_counter, 2)

            events_path = session.state_dir / "events.jsonl"
            tiny_limit = events_path.stat().st_size + 10
            with mock.patch.object(
                COMPANION, "MAX_EVENTS_FILE_BYTES", tiny_limit
            ):
                with self.assertRaisesRegex(COMPANION.CompanionError, "size limit"):
                    context.append_event(
                        {
                            "type": "choice",
                            "choice": "too-large",
                            "detail": "x" * 500,
                        }
                    )
            self.assertEqual(context.event_counter, 2)
            self.assertEqual(
                context.append_event({"type": "choice", "choice": "three"})["id"],
                3,
            )

    def test_server_log_is_secret_free_and_bounded(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            with RunningCompanion(project) as running:
                log_path = Path(running.info["state_dir"]) / "server.log"
                before = log_path.read_bytes()
                for _ in range(100):
                    status, _, _ = running.request("/missing?key=attacker-value")
                    self.assertEqual(status, 403)
                self.assertEqual(log_path.read_bytes(), before)
                self.assertNotIn(running.key, before.decode("utf-8"))

                session = COMPANION.prepare_session(
                    running.project, Path(running.info["session_dir"])
                )
                context = COMPANION.ServerContext(
                    session=session,
                    host="127.0.0.1",
                    url_host="127.0.0.1",
                    port=running.port,
                    allow_remote=False,
                    idle_timeout_seconds=30,
                )
                for _ in range(100):
                    context.log(
                        f"key={running.key} fragment=#key={running.key} "
                        f"path=/_vb/{running.key}/api/latest "
                        + "x" * 8192
                    )
                logged = log_path.read_bytes()
                self.assertLessEqual(len(logged), COMPANION.MAX_SERVER_LOG_BYTES)
                self.assertNotIn(running.key.encode("utf-8"), logged)
                self.assertIn(b"<redacted>", logged)
                if os.name != "nt":
                    self.assertEqual(log_path.stat().st_mode & 0o777, 0o600)
                    outside_log = project / "outside.log"
                    outside_log.write_text("outside\n", encoding="utf-8")
                    outside_mode = outside_log.stat().st_mode & 0o777
                    log_path.rename(log_path.with_name("server-original.log"))
                    log_path.symlink_to(outside_log)
                    context.log(f"must-not-escape key={running.key}")
                    self.assertEqual(
                        outside_log.read_text(encoding="utf-8"), "outside\n"
                    )
                    self.assertEqual(
                        outside_log.stat().st_mode & 0o777, outside_mode
                    )

    def test_publish_updates_latest_screen(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            with RunningCompanion(project) as running:
                source = SKILL_ROOT / "examples" / "01-product-layout.html"

                result = subprocess.run(
                    [
                        sys.executable,
                        "-I",
                        "-S",
                        str(SCRIPT),
                        "show",
                        "--project-dir",
                        str(project),
                        "--source",
                        str(source),
                    "--name",
                    "product-layout",
                    "--idle-timeout",
                    "30",
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=15,
                )
                published = json.loads(result.stdout)["screen"]
                status, _, body = running.request(running.keyed("/api/latest"))
                self.assertEqual(status, 200)
                latest = json.loads(body)
                self.assertEqual(latest["name"], published["name"])
                self.assertIn("product-layout", latest["name"])

    def test_publish_rejects_a_changed_current_session(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            with RunningCompanion(project):
                with self.assertRaisesRegex(
                    COMPANION.CompanionError, "Current session changed"
                ):
                    COMPANION.publish_impl(
                        COMPANION.resolve_project(project),
                        SKILL_ROOT / "examples" / "01-product-layout.html",
                        "wrong-session",
                        expected_session=project / "not-current",
                    )

    def test_show_serializes_publish_against_new_session_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = COMPANION.resolve_project(Path(temporary))
            first_source = SKILL_ROOT / "examples" / "01-product-layout.html"
            second_source = SKILL_ROOT / "examples" / "02-model-routing.html"

            def arguments(*, new: bool) -> Any:
                return COMPANION.argparse.Namespace(
                    project_dir=project,
                    host="127.0.0.1",
                    port=0,
                    url_host=None,
                    allow_remote=False,
                    idle_timeout=30,
                    open=False,
                    new=new,
                )

            entered_publish = threading.Event()
            release_publish = threading.Event()
            original_publish = COMPANION.publish_impl
            original_popen = subprocess.Popen
            launched: list[subprocess.Popen[Any]] = []

            def delayed_publish(*args: Any, **kwargs: Any) -> dict[str, Any]:
                if args[2] == "first":
                    entered_publish.set()
                    if not release_publish.wait(timeout=5):
                        raise RuntimeError("timed out waiting to release first publish")
                return original_publish(*args, **kwargs)

            def tracking_popen(*args: Any, **kwargs: Any) -> subprocess.Popen[Any]:
                process = original_popen(*args, **kwargs)
                launched.append(process)
                return process

            try:
                with mock.patch.object(
                    COMPANION, "publish_impl", side_effect=delayed_publish
                ), mock.patch.object(
                    COMPANION.subprocess, "Popen", side_effect=tracking_popen
                ), concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                    first_future = executor.submit(
                        COMPANION.show_impl,
                        arguments(new=False),
                        first_source,
                        "first",
                    )
                    self.assertTrue(entered_publish.wait(timeout=5))
                    second_future = executor.submit(
                        COMPANION.show_impl,
                        arguments(new=True),
                        second_source,
                        "second",
                    )
                    time.sleep(0.2)
                    self.assertFalse(second_future.done())
                    release_publish.set()
                    first = first_future.result(timeout=15)
                    second = second_future.result(timeout=15)

                self.assertNotEqual(first["session_dir"], second["session_dir"])
                self.assertEqual(
                    Path(first["screen"]["path"]).parent.parent,
                    Path(first["session_dir"]),
                )
                self.assertEqual(
                    Path(second["screen"]["path"]).parent.parent,
                    Path(second["session_dir"]),
                )
                current = COMPANION.current_info(project)
                self.assertIsNotNone(current)
                self.assertEqual(current["session_dir"], second["session_dir"])
            finally:
                release_publish.set()
                with contextlib.suppress(Exception):
                    run_cli(project, "stop")
                for process in launched:
                    with contextlib.suppress(subprocess.TimeoutExpired):
                        process.wait(timeout=3)

    def test_concurrent_starts_reuse_one_server_without_orphans(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)

            def start_once(_index: int) -> dict[str, Any]:
                result = run_cli(
                    project,
                    "start",
                    "--idle-timeout",
                    "30",
                    timeout=20,
                )
                return json.loads(result.stdout)

            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                results = list(executor.map(start_once, range(4)))
            self.assertEqual(len({item["pid"] for item in results}), 1)
            self.assertEqual(len({item["session_dir"] for item in results}), 1)

            sessions_root = project / ".visual-brainstorming" / "sessions"
            launchers = [
                json.loads(path.read_text(encoding="utf-8"))
                for path in sessions_root.glob("*/state/launcher.json")
            ]
            launcher_pids = [item["pid"] for item in launchers]
            self.assertEqual(launcher_pids, [results[0]["pid"]])
            self.assertNotIn("--launch-managed", launchers[0]["command"])
            self.assertEqual(
                len(
                    [
                        item
                        for item in launchers[0]["command"]
                        if item.startswith("--launch-managed=")
                    ]
                ),
                1,
            )
            stopped = json.loads(run_cli(project, "stop").stdout)
            self.assertTrue(stopped["stopped"])
            deadline = time.time() + 3
            while time.time() < deadline and any(
                COMPANION.process_is_alive(pid) for pid in launcher_pids
            ):
                time.sleep(0.05)
            self.assertFalse(
                any(COMPANION.process_is_alive(pid) for pid in launcher_pids)
            )

    def test_stale_lock_metadata_never_allows_overlapping_owners(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = COMPANION.resolve_project(Path(temporary))
            root = COMPANION.runtime_root(project)
            COMPANION.ensure_directory_without_symlink(root)
            COMPANION.ensure_runtime_ignore(root)
            lock_path = root / ".launch.lock"
            lock_path.write_text(
                json.dumps(
                    {
                        "pid": 999_999_999,
                        "token": "stale",
                        "padding": "x" * 1_000_000,
                    }
                ),
                encoding="utf-8",
            )
            trace = project / "lock-trace.jsonl"
            gate = project / "start-workers"
            worker = r'''
import importlib.util
import json
import os
import sys
import time
from pathlib import Path

script = Path(sys.argv[1])
project = Path(sys.argv[2])
trace = Path(sys.argv[3])
gate = Path(sys.argv[4])
spec = importlib.util.spec_from_file_location("vb_lock_worker", script)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
while not gate.exists():
    time.sleep(0.005)
lock = module.acquire_runtime_lock(project, "launch", timeout=10.0)
try:
    descriptor = os.open(trace, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    try:
        os.write(descriptor, (json.dumps({"pid": os.getpid(), "phase": "start", "at": time.time_ns()}) + "\n").encode())
        time.sleep(0.04)
        os.write(descriptor, (json.dumps({"pid": os.getpid(), "phase": "end", "at": time.time_ns()}) + "\n").encode())
    finally:
        os.close(descriptor)
finally:
    lock.release()
'''
            processes = [
                subprocess.Popen(
                    [
                        sys.executable,
                        "-B",
                        "-c",
                        worker,
                        str(SCRIPT),
                        str(project),
                        str(trace),
                        str(gate),
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                for _ in range(12)
            ]
            gate.touch()
            failures = []
            for process in processes:
                stdout, stderr = process.communicate(timeout=15)
                if process.returncode != 0:
                    failures.append((process.returncode, stdout, stderr))
            self.assertEqual(failures, [])

            records = [
                json.loads(line)
                for line in trace.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            intervals: dict[int, dict[str, int]] = {}
            for record in records:
                intervals.setdefault(record["pid"], {})[record["phase"]] = record["at"]
            self.assertEqual(len(intervals), 12)
            ordered = sorted(
                (value["start"], value["end"]) for value in intervals.values()
            )
            self.assertTrue(all(start < end for start, end in ordered))
            self.assertTrue(
                all(previous[1] <= current[0] for previous, current in zip(ordered, ordered[1:]))
            )
            self.assertTrue(lock_path.is_file())

    def test_windows_liveness_probe_never_uses_os_kill_zero(self) -> None:
        with mock.patch.object(COMPANION.os, "name", "nt"), mock.patch.object(
            COMPANION, "windows_process_is_alive", return_value=True
        ) as windows_probe, mock.patch.object(COMPANION.os, "kill") as kill:
            self.assertTrue(COMPANION.process_is_alive(1234))
        windows_probe.assert_called_once_with(1234)
        kill.assert_not_called()

    def test_remote_session_is_not_reused_by_default_local_show(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            with RunningCompanion(
                project,
                extra_arguments=[
                    "--host",
                    "0.0.0.0",
                    "--url-host",
                    "127.0.0.1",
                    "--allow-remote",
                ],
            ) as running:
                result = run_cli(
                    project,
                    "show",
                    "--source",
                    str(SKILL_ROOT / "examples" / "01-product-layout.html"),
                    check=False,
                )
                self.assertEqual(result.returncode, 2)
                self.assertIn("settings differ", result.stderr)
                current = json.loads(
                    (project / ".visual-brainstorming" / "current.json").read_text(
                        encoding="utf-8"
                    )
                )
                self.assertEqual(current["pid"], running.info["pid"])
                self.assertTrue(current["allow_remote"])

    def test_remote_wildcard_start_stop_is_repeatable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            for _ in range(10):
                with RunningCompanion(
                    project,
                    extra_arguments=[
                        "--host",
                        "0.0.0.0",
                        "--url-host",
                        "127.0.0.1",
                        "--allow-remote",
                    ],
                ) as running:
                    status = json.loads(run_cli(project, "status").stdout)
                    self.assertTrue(status["running"])
                    self.assertTrue(status["compatible"])
                    self.assertTrue(running.info["allow_remote"])

    def test_old_server_status_requires_new_before_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            with FakeOldServer(project) as old:
                status = json.loads(run_cli(project, "status").stdout)
                self.assertTrue(status["running"])
                self.assertFalse(status["compatible"])
                self.assertEqual(status["server_version"], "2.3.0")
                self.assertTrue(COMPANION.server_reachable(old.info))
                self.assertFalse(COMPANION.is_server_alive(old.info))

                refused = run_cli(project, "start", check=False)
                self.assertEqual(refused.returncode, 2)
                self.assertIn("different companion version", refused.stderr)

                replacement = json.loads(
                    run_cli(
                        project,
                        "start",
                        "--new",
                        "--idle-timeout",
                        "30",
                        timeout=20,
                    ).stdout
                )
                self.assertNotEqual(replacement["pid"], old.info["pid"])
                self.assertEqual(replacement["version"], COMPANION.VERSION)
                self.assertTrue(json.loads(run_cli(project, "stop").stdout)["stopped"])

    def test_content_and_state_live_swaps_are_rejected_but_shutdown_works(self) -> None:
        if os.name == "nt":
            self.skipTest("live directory symlink swap test is POSIX-only")

        with tempfile.TemporaryDirectory() as temporary, tempfile.TemporaryDirectory() as outside:
            project = Path(temporary)
            outside_root = Path(outside)
            (outside_root / "secret.html").write_text(
                "<p>outside</p>", encoding="utf-8"
            )
            (outside_root / "secret.txt").write_text("outside", encoding="utf-8")
            with RunningCompanion(project) as running:
                content = Path(running.info["screen_dir"])
                backup = content.with_name("content-original")
                content.rename(backup)
                content.symlink_to(outside_root, target_is_directory=True)
                for route in (
                    "/api/latest",
                    "/screen/secret.html",
                    "/files/secret.txt",
                ):
                    status, _, _ = running.request(running.keyed(route))
                    self.assertEqual(status, 409)
                running.stop()

        with tempfile.TemporaryDirectory() as temporary, tempfile.TemporaryDirectory() as outside:
            project = Path(temporary)
            outside_root = Path(outside)
            (outside_root / "events.jsonl").write_text(
                '{"id":999,"type":"choice"}\n', encoding="utf-8"
            )
            with RunningCompanion(project) as running:
                state = Path(running.info["state_dir"])
                backup = state.with_name("state-original")
                state.rename(backup)
                state.symlink_to(outside_root, target_is_directory=True)
                status, _, _ = running.request(running.keyed("/api/events"))
                self.assertEqual(status, 409)
                status, _, _ = running.request(
                    running.capability("/api/events"),
                    method="POST",
                    headers={
                        "Content-Type": "application/json",
                        "X-VB-Client": "1",
                        "Origin": f"http://{running.host}:{running.port}",
                    },
                    body=b'{"type":"choice","choice":"blocked"}',
                )
                self.assertEqual(status, 409)
                self.assertEqual(
                    (outside_root / "events.jsonl").read_text(encoding="utf-8"),
                    '{"id":999,"type":"choice"}\n',
                )
                self.assertFalse((outside_root / "server.log").exists())
                running.stop()

    def test_event_log_leaf_symlink_is_rejected_for_reads_and_writes(self) -> None:
        if os.name == "nt":
            self.skipTest("event leaf symlink test is POSIX-only")
        with tempfile.TemporaryDirectory() as temporary, tempfile.TemporaryDirectory() as outside:
            project = Path(temporary)
            outside_events = Path(outside) / "events.jsonl"
            original = '{"id":41,"type":"choice","choice":"outside"}\n'
            outside_events.write_text(original, encoding="utf-8")
            original_mode = outside_events.stat().st_mode & 0o777
            with RunningCompanion(project) as running:
                events_path = Path(running.info["state_dir"]) / "events.jsonl"
                events_path.symlink_to(outside_events)

                status, _, _ = running.request(running.keyed("/api/events"))
                self.assertEqual(status, 409)
                status, _, _ = running.request(
                    running.capability("/api/events"),
                    method="POST",
                    headers={
                        "Content-Type": "application/json",
                        "X-VB-Client": "1",
                        "Origin": f"http://{running.host}:{running.port}",
                    },
                    body=b'{"type":"choice","choice":"must-not-escape"}',
                )
                self.assertEqual(status, 422)
                with self.assertRaisesRegex(COMPANION.CompanionError, "symlinked"):
                    COMPANION.read_events(events_path)
                self.assertEqual(outside_events.read_text(encoding="utf-8"), original)
                self.assertEqual(outside_events.stat().st_mode & 0o777, original_mode)

    def test_unauthenticated_bootstrap_does_not_defeat_idle_timeout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            with RunningCompanion(project, idle_timeout=1) as running:
                for _ in range(8):
                    try:
                        running.request("/")
                    except OSError:
                        pass
                    time.sleep(0.25)

                status = json.loads(run_cli(project, "status").stdout)
                self.assertFalse(status["running"])

    def test_polling_does_not_defeat_idle_timeout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            with RunningCompanion(project, idle_timeout=1) as running:
                for _ in range(8):
                    try:
                        running.request(running.keyed("/api/latest"))
                    except OSError:
                        pass
                    time.sleep(0.25)

                output = subprocess.check_output(
                    [
                        sys.executable,
                        "-I",
                        "-S",
                        str(SCRIPT),
                        "status",
                        "--project-dir",
                        str(project),
                    ],
                    text=True,
                    timeout=10,
                )
                self.assertFalse(json.loads(output)["running"])

    def test_prune_is_dry_run_and_preserves_current_session(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = COMPANION.resolve_project(Path(temporary))
            with RunningCompanion(project) as running:
                sessions_root = project / ".visual-brainstorming" / "sessions"
                old_sessions = [
                    make_old_session(sessions_root, name, age_days=40)
                    for name in ("old-a", "old-b")
                ]
                recent = make_old_session(sessions_root, "recent", age_days=1)
                active = make_old_session(sessions_root, "active", age_days=40)
                COMPANION.write_json(
                    active / "state" / "server-info.json",
                    running.info,
                    mode=0o600,
                )

                dry_run = COMPANION.prune_impl(
                    project, keep=0, older_than_days=30, apply=False
                )
                self.assertTrue(dry_run["dry_run"])
                self.assertEqual(len(dry_run["candidates"]), 2)
                self.assertEqual(dry_run["deleted"], [])
                self.assertRegex(dry_run["plan"], r"^[0-9a-f]{64}$")
                self.assertTrue(all(path.exists() for path in old_sessions))
                self.assertTrue(Path(running.info["session_dir"]).exists())
                self.assertTrue(active.exists())
                self.assertTrue(recent.exists())

                surprise = make_old_session(
                    sessions_root, "old-created-after-review", age_days=40
                )
                with self.assertRaisesRegex(COMPANION.CompanionError, "plan changed"):
                    COMPANION.prune_impl(
                        project,
                        keep=0,
                        older_than_days=30,
                        apply=True,
                        plan=dry_run["plan"],
                    )
                self.assertTrue(all(path.exists() for path in old_sessions))
                self.assertTrue(surprise.exists())

                refreshed = COMPANION.prune_impl(
                    project, keep=0, older_than_days=30, apply=False
                )
                self.assertEqual(len(refreshed["candidates"]), 3)

                applied = COMPANION.prune_impl(
                    project,
                    keep=0,
                    older_than_days=30,
                    apply=True,
                    plan=refreshed["plan"],
                )
                self.assertFalse(applied["dry_run"])
                self.assertEqual(applied["candidates"], [])
                self.assertEqual(len(applied["deleted"]), 3)
                self.assertTrue(all(not path.exists() for path in old_sessions))
                self.assertFalse(surprise.exists())
                self.assertTrue(Path(running.info["session_dir"]).exists())
                self.assertTrue(active.exists())
                self.assertTrue(recent.exists())

    def test_prune_cli_requires_plan_and_honors_keep(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = COMPANION.resolve_project(Path(temporary))
            COMPANION.ensure_directory_without_symlink(COMPANION.runtime_root(project))
            COMPANION.ensure_runtime_ignore(COMPANION.runtime_root(project))
            sessions_root = COMPANION.runtime_root(project) / "sessions"
            sessions_root.mkdir()
            oldest = make_old_session(sessions_root, "oldest", age_days=50)
            newest = make_old_session(sessions_root, "newest", age_days=40)

            preview = json.loads(
                run_cli(
                    project,
                    "prune",
                    "--keep",
                    "1",
                    "--older-than-days",
                    "30",
                ).stdout
            )
            self.assertEqual(
                [Path(item["session_dir"]).name for item in preview["candidates"]],
                ["oldest"],
            )
            refused = run_cli(
                project,
                "prune",
                "--keep",
                "1",
                "--older-than-days",
                "30",
                "--apply",
                check=False,
            )
            self.assertEqual(refused.returncode, 2)
            self.assertIn("requires the exact --plan", refused.stderr)

            applied = json.loads(
                run_cli(
                    project,
                    "prune",
                    "--keep",
                    "1",
                    "--older-than-days",
                    "30",
                    "--apply",
                    "--plan",
                    preview["plan"],
                ).stdout
            )
            self.assertFalse(oldest.exists())
            self.assertTrue(newest.exists())
            self.assertEqual(
                [Path(item["session_dir"]).name for item in applied["deleted"]],
                ["oldest"],
            )

            with self.assertRaisesRegex(COMPANION.CompanionError, "--keep"):
                COMPANION.prune_impl(
                    project, keep=-1, older_than_days=0, apply=False
                )

            COMPANION.current_file(project).write_text("{broken", encoding="utf-8")
            with self.assertRaisesRegex(COMPANION.CompanionError, "pointer is invalid"):
                COMPANION.prune_impl(
                    project, keep=0, older_than_days=0, apply=False
                )

    def test_symlinked_runtime_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary, tempfile.TemporaryDirectory() as outside:
            project = Path(temporary)
            try:
                (project / ".visual-brainstorming").symlink_to(
                    Path(outside), target_is_directory=True
                )
            except (NotImplementedError, OSError) as exc:
                self.skipTest(f"symlink creation unavailable: {exc}")
            result = subprocess.run(
                [
                    sys.executable,
                    "-I",
                    "-S",
                    str(SCRIPT),
                    "demo",
                    "--project-dir",
                    str(project),
                ],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("Refusing symlinked runtime directory", result.stderr)

    def test_implicit_remote_binding_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result = subprocess.run(
                [
                    sys.executable,
                    "-I",
                    "-S",
                    str(SCRIPT),
                    "start",
                    "--project-dir",
                    temporary,
                    "--host",
                    "0.0.0.0",
                ],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("requires --allow-remote", result.stderr)

        with tempfile.TemporaryDirectory() as temporary:
            result = run_cli(
                Path(temporary),
                "start",
                "--host",
                "0.0.0.0",
                "--allow-remote",
                "--url-host",
                "example.com",
                "--open",
                check=False,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("literal IP address assigned to this machine", result.stderr)
            self.assertFalse(
                (Path(temporary) / ".visual-brainstorming" / "current.json").exists()
            )

    def test_managed_serve_requires_the_parent_launch_token(self) -> None:
        parsed = COMPANION.build_parser().parse_args(
            ["serve", "--launch-managed=-leading-dash-token"]
        )
        self.assertEqual(parsed.launch_managed, "-leading-dash-token")

        with tempfile.TemporaryDirectory() as temporary:
            result = run_cli(
                Path(temporary),
                "serve",
                "--launch-managed",
                "not-a-real-token",
                check=False,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("active parent launch lock", result.stderr)

    def test_shutdown_failure_is_visible_to_test_cleanup(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            running = object.__new__(RunningCompanion)
            running.project = Path(temporary)
            failed = subprocess.CompletedProcess(
                args=[],
                returncode=0,
                stdout='{"stopped": false, "reason": "shutdown rejected"}\n',
                stderr="",
            )
            with mock.patch.object(subprocess, "run", return_value=failed):
                with self.assertRaisesRegex(RuntimeError, "was not confirmed"):
                    running.stop()


if __name__ == "__main__":
    unittest.main()
