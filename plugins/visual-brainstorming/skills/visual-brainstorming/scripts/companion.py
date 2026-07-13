#!/usr/bin/env python3
"""Local browser companion for visual brainstorming.

The script is intentionally dependency-free. It serves the newest HTML screen,
wraps fragments in a reusable frame, and records browser choices as JSONL.
"""

from __future__ import annotations

import argparse
import contextlib
import ctypes
import datetime as dt
import errno
import hashlib
import hmac
import http.client
import ipaddress
import json
import mimetypes
import os
import re
import secrets
import signal
import shutil
import socket
import stat as stat_module
import subprocess
import sys
import tempfile
import threading
import time
import urllib.parse
import webbrowser
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path, PurePosixPath
from typing import Any, Dict, List, Optional, Tuple

VERSION = "2.4.0"
RUNTIME_DIR = ".visual-brainstorming"
BROWSER_PATH_PREFIX = "/_vb/"
MAX_SCREEN_BYTES = 5 * 1024 * 1024
MAX_ASSET_BYTES = 10 * 1024 * 1024
MAX_REQUEST_BYTES = 64 * 1024
MAX_PAYLOAD_BYTES = 10 * 1024
MAX_EVENTS_PER_SESSION = 10_000
MAX_EVENTS_FILE_BYTES = 5 * 1024 * 1024
MAX_SERVER_LOG_BYTES = 256 * 1024
MAX_SERVER_LOG_LINE_BYTES = 4 * 1024
MAX_HTTP_THREADS = 32
HTTP_CONNECTION_TIMEOUT_SECONDS = 10
DEFAULT_IDLE_TIMEOUT_SECONDS = 2 * 60 * 60
DEFAULT_PRUNE_KEEP = 5
DEFAULT_PRUNE_OLDER_THAN_DAYS = 30
PRUNE_PLAN_VERSION = 1
SKILL_ROOT = Path(__file__).resolve().parents[1]
FRAME_CSS_PATH = SKILL_ROOT / "assets" / "frame.css"
SHELL_HTML_PATH = SKILL_ROOT / "assets" / "browser-shell.html"
SHELL_CSS_PATH = SKILL_ROOT / "assets" / "browser-shell.css"
SHELL_JS_PATH = SKILL_ROOT / "assets" / "browser-shell.js"
HELPER_CSS_PATH = SKILL_ROOT / "assets" / "injected-helper.css"
HELPER_JS_PATH = SKILL_ROOT / "assets" / "injected-helper.js"
ICON_PATH = SKILL_ROOT / "assets" / "icon.svg"
DEMO_PATH = SKILL_ROOT / "assets" / "templates" / "demo.html"


class CompanionError(RuntimeError):
    """Expected, user-facing companion error."""


def read_asset_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise CompanionError(f"Required Skill asset is unavailable: {path}") from exc


def utc_now() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def json_dumps(value: Any, *, pretty: bool = False) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        indent=2 if pretty else None,
        sort_keys=pretty,
    )


def safe_chmod(path: Path, mode: int) -> None:
    with contextlib.suppress(OSError, NotImplementedError):
        path.chmod(mode)


def sanitized_log_message(message: str, secret: str = "") -> str:
    value = str(message)
    if secret:
        value = value.replace(secret, "<redacted>")
    value = re.sub(
        r"(?i)([?&#]key=)[^&#\s]+",
        r"\1<redacted>",
        value,
    )
    value = "".join(char if char.isprintable() else " " for char in value)
    encoded = value.encode("utf-8")[:MAX_SERVER_LOG_LINE_BYTES]
    return encoded.decode("utf-8", errors="ignore").strip()


def append_bounded_log(session: "SessionPaths", message: str) -> None:
    line = f"{utc_now()} {sanitized_log_message(message, session.key)}\n".encode(
        "utf-8"
    )
    try:
        descriptor = open_session_state_fd(
            session,
            "server.log",
            os.O_RDWR | os.O_CREAT | os.O_APPEND,
        )
    except (CompanionError, OSError):
        return
    try:
        file_stat = os.fstat(descriptor)
        if not stat_module.S_ISREG(file_stat.st_mode):
            return
        if file_stat.st_size + len(line) > MAX_SERVER_LOG_BYTES:
            marker = f"{utc_now()} log rotated at {MAX_SERVER_LOG_BYTES} bytes\n".encode(
                "utf-8"
            )
            os.ftruncate(descriptor, 0)
            os.lseek(descriptor, 0, os.SEEK_SET)
            os.write(descriptor, marker)
        os.write(descriptor, line)
        with contextlib.suppress(OSError, AttributeError):
            os.fchmod(descriptor, 0o600)
    except OSError:
        return
    finally:
        os.close(descriptor)


def atomic_write_bytes(path: Path, data: bytes, mode: Optional[int] = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    temp_path = Path(temporary)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        if mode is not None:
            safe_chmod(temp_path, mode)
        os.replace(temp_path, path)
        if mode is not None:
            safe_chmod(path, mode)
    finally:
        with contextlib.suppress(FileNotFoundError):
            temp_path.unlink()


def atomic_write_text(path: Path, text: str, mode: Optional[int] = None) -> None:
    atomic_write_bytes(path, text.encode("utf-8"), mode=mode)


def write_json(path: Path, value: Any, mode: Optional[int] = None) -> None:
    atomic_write_text(path, json_dumps(value, pretty=True) + "\n", mode=mode)


def read_json(path: Path) -> Optional[Dict[str, Any]]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError, UnicodeError):
        return None
    return value if isinstance(value, dict) else None


def resolve_project(path: Path) -> Path:
    project = path.expanduser().resolve()
    if not project.exists():
        raise CompanionError(f"Project directory does not exist: {project}")
    if not project.is_dir():
        raise CompanionError(f"Project path is not a directory: {project}")
    return project


def runtime_root(project: Path) -> Path:
    return project / RUNTIME_DIR


def current_file(project: Path) -> Path:
    return runtime_root(project) / "current.json"


def ensure_directory_without_symlink(path: Path) -> None:
    if path.exists() and path.is_symlink():
        raise CompanionError(f"Refusing symlinked runtime directory: {path}")
    path.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        raise CompanionError(f"Refusing symlinked runtime directory: {path}")
    safe_chmod(path, 0o700)


def ensure_runtime_ignore(root: Path) -> None:
    ignore_file = root / ".gitignore"
    if ignore_file.is_symlink():
        raise CompanionError(f"Refusing symlinked runtime ignore file: {ignore_file}")
    if ignore_file.exists() and not ignore_file.is_file():
        raise CompanionError(f"Runtime ignore path is not a file: {ignore_file}")
    expected = "*\n"
    try:
        current = ignore_file.read_text(encoding="utf-8") if ignore_file.exists() else None
    except (OSError, UnicodeError) as exc:
        raise CompanionError(f"Runtime ignore file is not readable UTF-8 text: {ignore_file}") from exc
    if current != expected:
        atomic_write_text(ignore_file, expected, mode=0o600)


def path_has_symlink(base: Path, target: Path) -> bool:
    try:
        relative = target.relative_to(base)
    except ValueError:
        return True
    current = base
    if current.is_symlink():
        return True
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            return True
    return False


def normalize_host(host: str) -> str:
    return host.strip().strip("[]").lower()


def is_loopback_host(host: str) -> bool:
    normalized = normalize_host(host)
    if normalized == "localhost":
        return True
    try:
        return ipaddress.ip_address(normalized).is_loopback
    except ValueError:
        return False


def validate_bind_host(host: str, allow_remote: bool) -> None:
    normalized = normalize_host(host)
    if is_loopback_host(normalized):
        return
    if not allow_remote:
        raise CompanionError("Non-loopback binding requires --allow-remote")
    if normalized not in {"0.0.0.0", "::"}:
        raise CompanionError("Remote mode must bind 0.0.0.0 or ::; use --url-host for the browser address")


def validate_url_host(host: str, allow_remote: bool) -> None:
    normalized = normalize_host(host)
    if not normalized or any(char.isspace() for char in normalized):
        raise CompanionError("URL host must be a non-empty host name or IP address")
    if any(char in normalized for char in "/?#@"):
        raise CompanionError("URL host must not contain a scheme, path, query, fragment, or user info")
    candidate = f"http://[{normalized}]:1" if ":" in normalized else f"http://{normalized}:1"
    try:
        parsed = urllib.parse.urlsplit(candidate)
        parsed_port = parsed.port
    except ValueError as exc:
        raise CompanionError(f"Invalid URL host: {host}") from exc
    if parsed.hostname != normalized or parsed_port != 1 or parsed.username or parsed.password:
        raise CompanionError(f"Invalid URL host: {host}")
    if not allow_remote:
        if not is_loopback_host(normalized):
            raise CompanionError("Loopback binding requires a loopback --url-host")
        return

    literal = normalized.split("%", 1)[0]
    try:
        ipaddress.ip_address(literal)
    except ValueError as exc:
        raise CompanionError(
            "Remote URL host must be a literal IP address assigned to this machine"
        ) from exc

    try:
        resolved = socket.getaddrinfo(normalized, 0, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise CompanionError(f"Remote URL host does not resolve: {host}") from exc
    if not resolved:
        raise CompanionError(f"Remote URL host does not resolve: {host}")
    for family, socktype, protocol, _, sockaddr in resolved:
        address = str(sockaddr[0]).split("%", 1)[0]
        try:
            parsed_address = ipaddress.ip_address(address)
        except ValueError as exc:
            raise CompanionError(f"Remote URL host resolved to an invalid address: {address}") from exc
        if not (
            parsed_address.is_loopback
            or parsed_address.is_private
            or parsed_address.is_link_local
        ) or parsed_address.is_unspecified:
            raise CompanionError(
                "Remote URL host must resolve only to loopback, private, or link-local addresses"
            )
        if not address_is_assigned_locally(family, socktype, protocol, sockaddr):
            raise CompanionError(
                "Remote URL host must resolve only to addresses assigned to this machine"
            )


def address_is_assigned_locally(
    family: int,
    socktype: int,
    protocol: int,
    sockaddr: Tuple[Any, ...],
) -> bool:
    try:
        probe = socket.socket(family, socktype, protocol)
    except OSError:
        return False
    try:
        probe.bind(sockaddr)
    except OSError:
        return False
    finally:
        probe.close()
    return True


def validate_port(port: int) -> None:
    if port < 0 or port > 65535:
        raise CompanionError("Port must be between 0 and 65535")


def validate_idle_timeout(seconds: int) -> None:
    if seconds < 0:
        raise CompanionError("Idle timeout must be zero or a positive number of seconds")


def windows_process_is_alive(pid: int) -> bool:
    process_query_limited_information = 0x1000
    still_active = 259
    error_access_denied = 5
    error_invalid_parameter = 87
    try:
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)  # type: ignore[attr-defined]
    except (AttributeError, OSError):
        return False
    open_process = kernel32.OpenProcess
    open_process.argtypes = [ctypes.c_ulong, ctypes.c_int, ctypes.c_ulong]
    open_process.restype = ctypes.c_void_p
    get_exit_code = kernel32.GetExitCodeProcess
    get_exit_code.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong)]
    get_exit_code.restype = ctypes.c_int
    close_handle = kernel32.CloseHandle
    close_handle.argtypes = [ctypes.c_void_p]
    close_handle.restype = ctypes.c_int
    handle = open_process(
        process_query_limited_information,
        False,
        pid,
    )
    if not handle:
        get_last_error = getattr(ctypes, "get_last_error", lambda: 0)
        error = int(get_last_error())
        if error == error_access_denied:
            return True
        if error == error_invalid_parameter:
            return False
        return False
    try:
        exit_code = ctypes.c_ulong()
        if not get_exit_code(handle, ctypes.byref(exit_code)):
            return True
        return exit_code.value == still_active
    finally:
        close_handle(handle)


def process_is_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    if os.name == "nt":
        return windows_process_is_alive(pid)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


_RUNTIME_THREAD_LOCKS_GUARD = threading.Lock()
_RUNTIME_THREAD_LOCKS: Dict[str, threading.Lock] = {}


def runtime_thread_lock(path: Path) -> threading.Lock:
    key = str(path)
    with _RUNTIME_THREAD_LOCKS_GUARD:
        lock = _RUNTIME_THREAD_LOCKS.get(key)
        if lock is None:
            lock = threading.Lock()
            _RUNTIME_THREAD_LOCKS[key] = lock
        return lock


def open_runtime_lock_fd(path: Path) -> int:
    if path.is_symlink():
        raise CompanionError(f"Refusing symlinked runtime lock: {path}")
    flags = os.O_RDWR | os.O_CREAT
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags, 0o600)
    except OSError as exc:
        raise CompanionError(f"Could not open runtime lock {path}: {exc}") from exc
    descriptor_stat = os.fstat(descriptor)
    if not stat_module.S_ISREG(descriptor_stat.st_mode):
        os.close(descriptor)
        raise CompanionError(f"Runtime lock is not a regular file: {path}")
    if os.name == "nt" and descriptor_stat.st_size == 0:
        os.write(descriptor, b"\0")
        os.fsync(descriptor)
    os.lseek(descriptor, 0, os.SEEK_SET)
    with contextlib.suppress(OSError, AttributeError):
        os.fchmod(descriptor, 0o600)
    return descriptor


def try_lock_descriptor(descriptor: int) -> bool:
    if os.name == "nt":
        import msvcrt

        os.lseek(descriptor, 0, os.SEEK_SET)
        locking = getattr(msvcrt, "locking")
        lock_nonblocking = getattr(msvcrt, "LK_NBLCK")
        try:
            locking(descriptor, lock_nonblocking, 1)
        except OSError as exc:
            if exc.errno in {errno.EACCES, errno.EAGAIN, errno.EDEADLK}:
                return False
            raise
        return True

    import fcntl

    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        return False
    except OSError as exc:
        if exc.errno in {errno.EACCES, errno.EAGAIN}:
            return False
        raise
    return True


def unlock_descriptor(descriptor: int) -> None:
    if os.name == "nt":
        import msvcrt

        os.lseek(descriptor, 0, os.SEEK_SET)
        locking = getattr(msvcrt, "locking")
        lock_unlock = getattr(msvcrt, "LK_UNLCK")
        locking(descriptor, lock_unlock, 1)
        return

    import fcntl

    fcntl.flock(descriptor, fcntl.LOCK_UN)


def runtime_lock_is_held(path: Path) -> bool:
    if runtime_thread_lock(path).locked():
        return True
    try:
        descriptor = open_runtime_lock_fd(path)
    except CompanionError:
        return False
    try:
        if not try_lock_descriptor(descriptor):
            return True
        unlock_descriptor(descriptor)
        return False
    finally:
        os.close(descriptor)


@dataclass
class RuntimeLock:
    path: Path
    token: str
    descriptor: Optional[int]
    thread_lock: threading.Lock
    released: bool = False
    release_guard: threading.Lock = field(default_factory=threading.Lock)

    def release(self) -> None:
        with self.release_guard:
            if self.released:
                return
            self.released = True
            descriptor = self.descriptor
            self.descriptor = None
            if descriptor is not None:
                with contextlib.suppress(OSError):
                    unlock_descriptor(descriptor)
                with contextlib.suppress(OSError):
                    os.close(descriptor)
            if self.thread_lock.locked():
                self.thread_lock.release()


def acquire_runtime_lock(
    project: Path,
    name: str,
    *,
    timeout: float,
) -> RuntimeLock:
    root = runtime_root(project)
    ensure_directory_without_symlink(root)
    ensure_runtime_ignore(root)
    lock_path = root / f".{name}.lock"
    token = secrets.token_urlsafe(18)
    deadline = time.monotonic() + max(timeout, 0.0)
    thread_lock = runtime_thread_lock(lock_path)
    while not thread_lock.acquire(blocking=False):
        if time.monotonic() >= deadline:
            raise CompanionError(f"Another {name} operation is already in progress")
        time.sleep(0.05)

    descriptor: Optional[int] = None
    descriptor_locked = False
    try:
        descriptor = open_runtime_lock_fd(lock_path)
        while not try_lock_descriptor(descriptor):
            if time.monotonic() >= deadline:
                raise CompanionError(f"Another {name} operation is already in progress")
            time.sleep(0.05)
        descriptor_locked = True

        payload = {
            "pid": os.getpid(),
            "token": token,
            "created_at": utc_now(),
        }
        encoded = (json_dumps(payload) + "\n").encode("utf-8")
        os.lseek(descriptor, 0, os.SEEK_SET)
        view = memoryview(encoded)
        while view:
            written = os.write(descriptor, view)
            if written <= 0:
                raise CompanionError("Runtime lock metadata write made no progress")
            view = view[written:]
        os.ftruncate(descriptor, len(encoded))
        os.fsync(descriptor)
        with contextlib.suppress(OSError, AttributeError):
            os.fchmod(descriptor, 0o600)
        return RuntimeLock(lock_path, token, descriptor, thread_lock)
    except Exception:
        if descriptor is not None:
            if descriptor_locked:
                with contextlib.suppress(OSError):
                    unlock_descriptor(descriptor)
            with contextlib.suppress(OSError):
                os.close(descriptor)
        thread_lock.release()
        raise


def validate_managed_launch(project: Path, token: str) -> None:
    lock_path = runtime_root(project) / ".launch.lock"
    if lock_path.is_symlink():
        raise CompanionError("Managed launch lock is unsafe")
    if not runtime_lock_is_held(lock_path):
        raise CompanionError("Managed launch requires an active parent launch lock")
    lock_info = read_json(lock_path)
    if not lock_info:
        raise CompanionError("Managed launch requires an active parent launch lock")
    lock_token = str(lock_info.get("token", ""))
    lock_pid = event_id(lock_info.get("pid"))
    if (
        not token
        or not secrets.compare_digest(token, lock_token)
        or not process_is_alive(lock_pid)
    ):
        raise CompanionError("Managed launch token is invalid or stale")


def requested_server_settings(
    args: argparse.Namespace,
) -> Tuple[str, str, int, bool, int]:
    host = normalize_host(args.host)
    allow_remote = bool(args.allow_remote)
    validate_bind_host(host, allow_remote)
    url_host = normalize_host(
        args.url_host or ("127.0.0.1" if host in {"0.0.0.0", "::"} else host)
    )
    validate_url_host(url_host, allow_remote)
    port = int(args.port)
    idle_timeout = int(args.idle_timeout)
    validate_port(port)
    validate_idle_timeout(idle_timeout)
    return host, url_host, port, allow_remote, idle_timeout


def existing_settings_match(
    info: Dict[str, Any],
    host: str,
    url_host: str,
    port: int,
    allow_remote: bool,
    idle_timeout: int,
) -> bool:
    if normalize_host(str(info.get("host", ""))) != host:
        return False
    if normalize_host(str(info.get("url_host", ""))) != url_host:
        return False
    if info.get("allow_remote") is not allow_remote:
        return False
    if event_id(info.get("idle_timeout_seconds")) != idle_timeout:
        return False
    if port and event_id(info.get("port")) != port:
        return False
    return True


def session_id() -> str:
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{stamp}-{os.getpid()}-{secrets.token_hex(3)}"


@dataclass(frozen=True)
class SessionPaths:
    project_dir: Path
    session_dir: Path
    content_dir: Path
    state_dir: Path
    key: str
    content_real: Path
    content_device: int
    content_inode: int
    state_real: Path
    state_device: int
    state_inode: int


def prepare_session(project: Path, requested: Optional[Path] = None) -> SessionPaths:
    project = resolve_project(project)
    root = runtime_root(project)
    ensure_directory_without_symlink(root)
    ensure_runtime_ignore(root)
    sessions_root = root / "sessions"
    ensure_directory_without_symlink(sessions_root)

    if requested is None:
        session = sessions_root / session_id()
    else:
        session = Path(os.path.abspath(requested.expanduser()))
        sessions_root_absolute = Path(os.path.abspath(sessions_root))
        try:
            session.relative_to(sessions_root_absolute)
        except ValueError as exc:
            raise CompanionError("Session directory must live under the project's runtime directory") from exc
        if path_has_symlink(sessions_root_absolute, session):
            raise CompanionError(f"Refusing symlinked session path: {session}")

    ensure_directory_without_symlink(session)
    if path_has_symlink(sessions_root, session):
        raise CompanionError(f"Refusing symlinked session path: {session}")
    try:
        session.resolve().relative_to(sessions_root.resolve())
    except (OSError, ValueError) as exc:
        raise CompanionError("Session directory resolved outside the project's runtime directory") from exc
    content = session / "content"
    state = session / "state"
    ensure_directory_without_symlink(content)
    ensure_directory_without_symlink(state)

    key_file = state / "session-key"
    if key_file.is_symlink():
        raise CompanionError(f"Refusing symlinked session key: {key_file}")
    if key_file.exists():
        try:
            key = key_file.read_text(encoding="utf-8").strip()
        except (OSError, UnicodeError) as exc:
            raise CompanionError(f"Session key is not readable UTF-8 text: {key_file}") from exc
        if not key:
            raise CompanionError(f"Session key is empty: {key_file}")
    else:
        key = secrets.token_urlsafe(32)
        atomic_write_text(key_file, key + "\n", mode=0o600)
    safe_chmod(state, 0o700)
    safe_chmod(session, 0o700)

    try:
        content_real = content.resolve(strict=True)
        content_stat = content.stat()
        state_real = state.resolve(strict=True)
        state_stat = state.stat()
    except OSError as exc:
        raise CompanionError(f"Session content directory is unavailable: {content}") from exc

    return SessionPaths(
        project,
        session,
        content,
        state,
        key,
        content_real,
        content_stat.st_dev,
        content_stat.st_ino,
        state_real,
        state_stat.st_dev,
        state_stat.st_ino,
    )


def content_root_is_valid(session: SessionPaths) -> bool:
    content = session.content_dir
    try:
        if content.is_symlink():
            return False
        resolved = content.resolve(strict=True)
        stat = content.stat()
    except OSError:
        return False
    return (
        resolved == session.content_real
        and stat.st_dev == session.content_device
        and stat.st_ino == session.content_inode
    )


def state_root_is_valid(session: SessionPaths) -> bool:
    state = session.state_dir
    try:
        if state.is_symlink():
            return False
        resolved = state.resolve(strict=True)
        stat = state.stat()
    except OSError:
        return False
    return (
        resolved == session.state_real
        and stat.st_dev == session.state_device
        and stat.st_ino == session.state_inode
    )


def open_session_state_fd(
    session: SessionPaths,
    name: str,
    flags: int,
    mode: int = 0o600,
) -> int:
    if not name or name in {".", ".."} or "/" in name or "\\" in name:
        raise CompanionError("Invalid session state file name")
    if not state_root_is_valid(session):
        raise CompanionError("Session state directory changed after startup")

    use_dir_fd = (
        os.name != "nt"
        and os.open in os.supports_dir_fd
        and hasattr(os, "O_DIRECTORY")
    )
    descriptor: Optional[int] = None
    if use_dir_fd:
        directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        if hasattr(os, "O_NOFOLLOW"):
            directory_flags |= os.O_NOFOLLOW
        try:
            directory_descriptor = os.open(session.state_dir, directory_flags)
        except OSError as exc:
            raise CompanionError(f"Session state directory is unavailable: {exc}") from exc
        try:
            directory_stat = os.fstat(directory_descriptor)
            if (
                not stat_module.S_ISDIR(directory_stat.st_mode)
                or directory_stat.st_dev != session.state_device
                or directory_stat.st_ino != session.state_inode
            ):
                raise CompanionError("Session state directory changed after startup")
            leaf_flags = flags
            if hasattr(os, "O_NOFOLLOW"):
                leaf_flags |= os.O_NOFOLLOW
            try:
                descriptor = os.open(
                    name,
                    leaf_flags,
                    mode,
                    dir_fd=directory_descriptor,
                )
            except FileNotFoundError:
                raise
            except OSError as exc:
                raise CompanionError(f"Session state file is unsafe: {name}: {exc}") from exc
        finally:
            os.close(directory_descriptor)
    else:
        path = session.state_dir / name
        if path.is_symlink():
            raise CompanionError(f"Session state file is symlinked: {name}")
        leaf_flags = flags
        if hasattr(os, "O_NOFOLLOW"):
            leaf_flags |= os.O_NOFOLLOW
        try:
            descriptor = os.open(path, leaf_flags, mode)
        except FileNotFoundError:
            raise
        except OSError as exc:
            raise CompanionError(f"Session state file is unsafe: {name}: {exc}") from exc
        if not state_root_is_valid(session):
            os.close(descriptor)
            raise CompanionError("Session state directory changed after startup")
        try:
            path_stat = path.lstat()
            descriptor_stat = os.fstat(descriptor)
        except OSError:
            os.close(descriptor)
            raise
        if (
            stat_module.S_ISLNK(path_stat.st_mode)
            or path_stat.st_dev != descriptor_stat.st_dev
            or path_stat.st_ino != descriptor_stat.st_ino
        ):
            os.close(descriptor)
            raise CompanionError(f"Session state file changed while opening: {name}")

    if descriptor is None:
        raise CompanionError(f"Session state file could not be opened: {name}")
    descriptor_stat = os.fstat(descriptor)
    if not stat_module.S_ISREG(descriptor_stat.st_mode):
        os.close(descriptor)
        raise CompanionError(f"Session state file is not regular: {name}")
    return descriptor


def single_url_key(raw: str, *, optional: bool = False) -> str:
    if not raw:
        if optional:
            return ""
        raise ValueError("missing key component")
    values = urllib.parse.parse_qs(raw, keep_blank_values=True)
    keys = values.get("key", [])
    if set(values) != {"key"} or len(keys) != 1 or not keys[0]:
        raise ValueError("invalid key component")
    return keys[0]


def current_info(project: Path) -> Optional[Dict[str, Any]]:
    project = project.expanduser().resolve()
    root = runtime_root(project)
    pointer = current_file(project)
    if root.is_symlink() or pointer.is_symlink():
        return None
    info = read_json(pointer)
    if not info:
        return None

    try:
        recorded_project = Path(str(info.get("project_dir", ""))).expanduser().resolve()
        session = Path(str(info.get("session_dir", ""))).expanduser().resolve()
        content = Path(
            os.path.abspath(Path(str(info.get("screen_dir", ""))).expanduser())
        )
        state = Path(
            os.path.abspath(Path(str(info.get("state_dir", ""))).expanduser())
        )
    except (OSError, RuntimeError):
        return None

    sessions_root = root / "sessions"
    if recorded_project != project:
        return None
    try:
        session.relative_to(sessions_root.resolve())
    except (OSError, ValueError):
        return None
    if content != session / "content" or state != session / "state":
        return None
    if path_has_symlink(root, session):
        return None

    control_url = str(info.get("control_url") or info.get("url") or "")
    browser_url = str(info.get("url") or "")
    try:
        control = urllib.parse.urlsplit(control_url)
        browser = urllib.parse.urlsplit(browser_url)
        control_key = single_url_key(control.query)
        browser_query_key = single_url_key(browser.query, optional=True)
        browser_fragment_key = single_url_key(browser.fragment, optional=True)
        if (
            browser_query_key
            and browser_fragment_key
            and not secrets.compare_digest(browser_query_key, browser_fragment_key)
        ):
            return None
        browser_key = browser_fragment_key or browser_query_key
        control_port = control.port
        browser_port = browser.port
    except (ValueError, UnicodeError):
        return None
    info_port = info.get("port")
    if type(info_port) is not int or not 1 <= info_port <= 65535:
        return None
    if (
        control.scheme != "http"
        or not control.hostname
        or not control_port
        or control.path not in {"", "/"}
        or control.fragment
        or control_port != info_port
    ):
        return None
    if control.username or control.password or not is_loopback_host(control.hostname):
        return None
    if (
        browser.scheme != "http"
        or not browser.hostname
        or not browser_port
        or browser.path not in {"", "/"}
        or browser_port != info_port
        or not browser_key
    ):
        return None
    if browser.username or browser.password:
        return None
    if normalize_host(browser.hostname) != normalize_host(str(info.get("url_host", ""))):
        return None
    allow_remote = info.get("allow_remote")
    if not isinstance(allow_remote, bool):
        return None
    try:
        validate_url_host(browser.hostname, allow_remote)
    except CompanionError:
        return None
    state_safe = not state.is_symlink() and not path_has_symlink(session, state)
    if state_safe:
        key_file = state / "session-key"
        if key_file.is_symlink():
            return None
        try:
            stored_key = key_file.read_text(encoding="utf-8").strip()
        except (OSError, UnicodeError):
            return None
        if not stored_key:
            return None
        if not secrets.compare_digest(control_key, stored_key) or not secrets.compare_digest(browser_key, stored_key):
            return None
    elif not control_key or not secrets.compare_digest(control_key, browser_key):
        return None

    sanitized = dict(info)
    sanitized["project_dir"] = str(project)
    sanitized["session_dir"] = str(session)
    sanitized["screen_dir"] = str(content)
    sanitized["state_dir"] = str(state)
    sanitized["control_url"] = control_url
    return sanitized


def endpoint_from_info(info: Dict[str, Any], path: str) -> str:
    raw_url = str(info.get("control_url") or info.get("url", ""))
    parsed = urllib.parse.urlsplit(raw_url)
    if parsed.scheme != "http" or not parsed.netloc or not parsed.hostname or not is_loopback_host(parsed.hostname):
        raise CompanionError("Current session has an invalid local control URL")
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, path, parsed.query, ""))


def http_json(
    url: str,
    *,
    method: str = "GET",
    payload: Optional[Dict[str, Any]] = None,
    timeout: float = 1.5,
) -> Dict[str, Any]:
    parsed = urllib.parse.urlsplit(url)
    if (
        parsed.scheme != "http"
        or not parsed.hostname
        or not parsed.port
        or parsed.username
        or parsed.password
        or not is_loopback_host(parsed.hostname)
    ):
        raise CompanionError("Control request URL must use a loopback HTTP endpoint")
    data: Optional[bytes] = None
    headers = {"X-VB-Client": "1"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    target = urllib.parse.urlunsplit(("", "", parsed.path or "/", parsed.query, ""))
    connection = http.client.HTTPConnection(parsed.hostname, parsed.port, timeout=timeout)
    try:
        connection.request(method, target, body=data, headers=headers)
        response = connection.getresponse()
        raw = response.read(MAX_REQUEST_BYTES + 1)
        if response.status < 200 or response.status >= 300:
            raise CompanionError(f"Control request failed with HTTP {response.status}")
        if len(raw) > MAX_REQUEST_BYTES:
            raise CompanionError("Control response is too large")
    finally:
        connection.close()
    result = json.loads(raw.decode("utf-8"))
    if not isinstance(result, dict):
        raise CompanionError("Server returned a non-object JSON response")
    return result


def server_health(
    info: Optional[Dict[str, Any]], timeout: float = 0.7
) -> Optional[Dict[str, Any]]:
    if not info:
        return None
    try:
        result = http_json(endpoint_from_info(info, "/api/health"), timeout=timeout)
    except (OSError, ValueError, CompanionError, http.client.HTTPException, json.JSONDecodeError):
        return None
    if result.get("ok") is not True:
        return None
    if event_id(result.get("pid")) != event_id(info.get("pid")):
        return None
    return result


def server_reachable(info: Optional[Dict[str, Any]], timeout: float = 0.7) -> bool:
    return server_health(info, timeout=timeout) is not None


def is_server_alive(info: Optional[Dict[str, Any]], timeout: float = 0.7) -> bool:
    health = server_health(info, timeout=timeout)
    return bool(health and health.get("version") == VERSION)


def latest_screen(content_dir: Path) -> Optional[Tuple[Path, os.stat_result]]:
    candidates: List[Tuple[int, str, Path, os.stat_result]] = []
    try:
        entries = list(content_dir.iterdir())
    except OSError:
        return None
    for path in entries:
        try:
            if path.name.startswith(".") or path.suffix.lower() not in {".html", ".htm"}:
                continue
            if path.is_symlink() or not path.is_file():
                continue
            stat = path.stat()
        except OSError:
            continue
        candidates.append((stat.st_mtime_ns, path.name, path, stat))
    if not candidates:
        return None
    _, _, path, stat = max(candidates, key=lambda item: (item[0], item[1]))
    return path, stat


def event_id(value: Any) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError, OverflowError):
        return 0
    return max(parsed, 0)


def read_descriptor_bytes(descriptor: int, limit: int) -> bytes:
    size = os.fstat(descriptor).st_size
    if size > limit:
        raise CompanionError(f"Session state file exceeds {limit} bytes")
    os.lseek(descriptor, 0, os.SEEK_SET)
    chunks: List[bytes] = []
    remaining = limit + 1
    while remaining > 0:
        chunk = os.read(descriptor, min(64 * 1024, remaining))
        if not chunk:
            break
        chunks.append(chunk)
        remaining -= len(chunk)
    data = b"".join(chunks)
    if len(data) > limit:
        raise CompanionError(f"Session state file exceeds {limit} bytes")
    return data


def parse_events_bytes(data: bytes, after: int = 0) -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []
    try:
        lines = data.decode("utf-8").splitlines()
    except UnicodeDecodeError:
        return events
    for line in lines:
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and event_id(value.get("id")) > after:
            events.append(value)
    return events


def read_session_events(session: SessionPaths, after: int = 0) -> List[Dict[str, Any]]:
    try:
        descriptor = open_session_state_fd(session, "events.jsonl", os.O_RDONLY)
    except FileNotFoundError:
        return []
    try:
        try:
            data = read_descriptor_bytes(descriptor, MAX_EVENTS_FILE_BYTES)
        except OSError as exc:
            raise CompanionError(f"Session event log is unreadable: {exc}") from exc
        return parse_events_bytes(data, after=after)
    finally:
        os.close(descriptor)


def last_existing_event_id(session: SessionPaths) -> int:
    return max(
        (event_id(event.get("id")) for event in read_session_events(session)),
        default=0,
    )


def bounded_text(value: Any, limit: int) -> str:
    if value is None:
        return ""
    return str(value).strip()[:limit]


def read_events(events_file: Path, after: int = 0) -> List[Dict[str, Any]]:
    if events_file.is_symlink():
        raise CompanionError(f"Session event log is symlinked: {events_file}")
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(events_file, flags)
    except FileNotFoundError:
        return []
    except OSError as exc:
        raise CompanionError(f"Session event log is unsafe: {events_file}: {exc}") from exc
    try:
        descriptor_stat = os.fstat(descriptor)
        if not stat_module.S_ISREG(descriptor_stat.st_mode):
            raise CompanionError(f"Session event log is not regular: {events_file}")
        try:
            path_stat = events_file.lstat()
        except OSError as exc:
            raise CompanionError(f"Session event log changed while opening: {events_file}") from exc
        if (
            stat_module.S_ISLNK(path_stat.st_mode)
            or path_stat.st_dev != descriptor_stat.st_dev
            or path_stat.st_ino != descriptor_stat.st_ino
        ):
            raise CompanionError(f"Session event log changed while opening: {events_file}")
        try:
            data = read_descriptor_bytes(descriptor, MAX_EVENTS_FILE_BYTES)
        except OSError as exc:
            raise CompanionError(f"Session event log is unreadable: {events_file}: {exc}") from exc
        return parse_events_bytes(data, after=after)
    finally:
        os.close(descriptor)


@dataclass
class ServerContext:
    session: SessionPaths
    host: str
    url_host: str
    port: int
    allow_remote: bool
    idle_timeout_seconds: int
    info: Dict[str, Any] = field(default_factory=dict)
    event_lock: threading.Lock = field(default_factory=threading.Lock)
    log_lock: threading.Lock = field(default_factory=threading.Lock)
    activity_lock: threading.Lock = field(default_factory=threading.Lock)
    event_counter: int = 0
    last_activity: float = field(default_factory=time.monotonic)

    def __post_init__(self) -> None:
        self.event_counter = last_existing_event_id(self.session)

    def touch(self) -> None:
        with self.activity_lock:
            self.last_activity = time.monotonic()

    def idle_for(self) -> float:
        with self.activity_lock:
            return max(0.0, time.monotonic() - self.last_activity)

    def screen_bridge(self, path: Path, stat: os.stat_result) -> str:
        payload = f"{path.name}:{stat.st_mtime_ns}:{stat.st_size}".encode("utf-8")
        return hmac.new(
            self.session.key.encode("utf-8"), payload, hashlib.sha256
        ).hexdigest()

    @property
    def allowed_hosts(self) -> set[str]:
        hosts = {"localhost", "127.0.0.1", "::1", normalize_host(self.url_host)}
        normalized_bind = normalize_host(self.host)
        if normalized_bind not in {"0.0.0.0", "::"}:
            hosts.add(normalized_bind)
        return {value for value in hosts if value}

    def log(self, message: str) -> None:
        with self.log_lock:
            append_bounded_log(self.session, message)

    def append_event(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        if not content_root_is_valid(self.session):
            raise CompanionError("Session content directory changed after startup")
        if not state_root_is_valid(self.session):
            raise CompanionError("Session state directory changed after startup")
        payload = raw.get("payload")
        if payload is not None:
            encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            if len(encoded) > MAX_PAYLOAD_BYTES:
                raise CompanionError("Event payload is too large")

        event_type = bounded_text(raw.get("type"), 40) or "choice"
        if event_type not in {"choice", "note", "action"}:
            event_type = "action"

        choice = bounded_text(raw.get("choice"), 200)
        note = bounded_text(raw.get("note"), 5000)
        if event_type == "choice" and not choice:
            raise CompanionError("Choice events require a non-empty choice ID")
        if event_type == "note" and not note:
            raise CompanionError("Note events require non-empty note text")

        current = latest_screen(self.session.content_dir)
        requested_screen = bounded_text(raw.get("screen"), 300)
        requested_path = safe_content_path(self.session.content_dir, requested_screen) if requested_screen else None
        if requested_path is not None and requested_path.suffix.lower() in {".html", ".htm"}:
            screen = requested_path.name
        elif current is not None:
            screen = current[0].name
        else:
            screen = ""

        with self.event_lock:
            if self.event_counter >= MAX_EVENTS_PER_SESSION:
                raise CompanionError("Session event limit reached")
            try:
                descriptor = open_session_state_fd(
                    self.session,
                    "events.jsonl",
                    os.O_RDWR | os.O_CREAT | os.O_APPEND,
                )
            except (CompanionError, OSError) as exc:
                raise CompanionError(f"Event log is not writable: {exc}") from exc
            try:
                existing_size = os.fstat(descriptor).st_size
                next_id = self.event_counter + 1
                event: Dict[str, Any] = {
                    "id": next_id,
                    "ts": utc_now(),
                    "type": event_type,
                    "choice": choice,
                    "label": bounded_text(raw.get("label"), 500),
                    "detail": bounded_text(raw.get("detail"), 500),
                    "note": note,
                    "screen": screen,
                }
                if payload is not None:
                    event["payload"] = payload
                event = {
                    key: value for key, value in event.items() if value not in ("", None)
                }
                encoded_event = (json_dumps(event) + "\n").encode("utf-8")
                if existing_size + len(encoded_event) > MAX_EVENTS_FILE_BYTES:
                    raise CompanionError("Session event log size limit reached")
                view = memoryview(encoded_event)
                while view:
                    written = os.write(descriptor, view)
                    if written <= 0:
                        raise CompanionError("Session event log write made no progress")
                    view = view[written:]
                os.fsync(descriptor)
                with contextlib.suppress(OSError, AttributeError):
                    os.fchmod(descriptor, 0o600)
                self.event_counter = next_id
            finally:
                os.close(descriptor)
        self.log(f"event id={event['id']} type={event.get('type')} screen={event.get('screen', '')}")
        return event


class CompanionHTTPServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address: Tuple[str, int], handler: Any, context: ServerContext):
        self.context = context
        self.request_semaphore = threading.BoundedSemaphore(MAX_HTTP_THREADS)
        self.address_family = socket.AF_INET6 if ":" in server_address[0] else socket.AF_INET
        super().__init__(server_address, handler)

    def process_request(self, request: Any, client_address: Any) -> None:
        if not self.request_semaphore.acquire(blocking=False):
            with contextlib.suppress(OSError):
                request.close()
            return
        try:
            super().process_request(request, client_address)
        except Exception:
            self.request_semaphore.release()
            raise

    def process_request_thread(self, request: Any, client_address: Any) -> None:
        try:
            super().process_request_thread(request, client_address)
        finally:
            self.request_semaphore.release()

    def handle_error(self, request: Any, client_address: Any) -> None:
        error_type = sys.exc_info()[0]
        error_name = error_type.__name__ if error_type is not None else "unknown"
        self.context.log(f"http handler error client={client_address[0]} type={error_name}")


def helper_markup(bridge_token: str) -> str:
    css = read_asset_text(HELPER_CSS_PATH)
    javascript = read_asset_text(HELPER_JS_PATH).replace(
        "__VB_BRIDGE_TOKEN__", bridge_token
    )
    return (
        '<style id="vb-injected-style">'
        + css
        + '</style><script id="vb-injected-helper">'
        + javascript
        + '</script>'
    )


def inject_helper(document: str, bridge_token: str) -> str:
    if 'id="vb-injected-helper"' in document or "id='vb-injected-helper'" in document:
        return document
    helper = helper_markup(bridge_token)
    matches = list(re.finditer(r"</body\s*>", document, flags=re.IGNORECASE))
    if matches:
        match = matches[-1]
        return document[: match.start()] + helper + document[match.start() :]
    return document + helper


def render_screen(raw: str, bridge_token: str) -> str:
    full_document = re.match(
        r"\s*(?:(?:<!--.*?-->)\s*)*(?:<!doctype\s+html|<html\b)",
        raw,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if full_document:
        return inject_helper(raw, bridge_token)
    css = read_asset_text(FRAME_CSS_PATH)
    return (
        '<!doctype html><html lang="zh-CN"><head>'
        '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Visual Brainstorming</title><style>'
        + css
        + '</style></head><body>'
        + raw
        + helper_markup(bridge_token)
        + '</body></html>'
    )


def shell_document() -> str:
    template = read_asset_text(SHELL_HTML_PATH)
    css = read_asset_text(SHELL_CSS_PATH)
    javascript = read_asset_text(SHELL_JS_PATH)
    return (
        template.replace("__SESSION_LABEL__", "本地")
        .replace("__SHELL_CSS__", css)
        .replace("__SHELL_JS__", javascript)
    )

def host_only(raw_host: str) -> str:
    raw = raw_host.strip()
    if not raw or any(char.isspace() for char in raw):
        return ""
    try:
        parsed = urllib.parse.urlsplit(f"http://{raw}")
        _ = parsed.port
    except ValueError:
        return ""
    if (
        parsed.scheme != "http"
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.path not in {"", "/"}
        or parsed.query
        or parsed.fragment
    ):
        return ""
    return normalize_host(parsed.hostname)


def split_browser_capability_path(raw_path: str) -> Tuple[str, str]:
    """Return the canonical route and an optional path-scoped session key."""

    if not raw_path.startswith(BROWSER_PATH_PREFIX):
        return raw_path, ""
    remainder = raw_path[len(BROWSER_PATH_PREFIX) :]
    raw_key, separator, route = remainder.partition("/")
    if not separator or not raw_key:
        return raw_path, ""
    key = urllib.parse.unquote(raw_key)
    if not key or "/" in key or "\\" in key:
        return raw_path, ""
    return f"/{route}", key


def safe_content_path(content_dir: Path, raw_path: str) -> Optional[Path]:
    if content_dir.is_symlink():
        return None
    decoded = urllib.parse.unquote(raw_path)
    pure = PurePosixPath(decoded)
    if pure.is_absolute() or not pure.parts:
        return None
    if any(part in {"", ".", ".."} or part.startswith(".") for part in pure.parts):
        return None
    current = content_dir
    for part in pure.parts:
        current = current / part
        if current.is_symlink():
            return None
    try:
        resolved = current.resolve(strict=True)
        resolved.relative_to(content_dir.resolve())
    except (FileNotFoundError, OSError, ValueError):
        return None
    if not resolved.is_file():
        return None
    return resolved


def session_usage(session_dir: Path) -> Tuple[int, int]:
    """Return non-symlink file bytes and the newest observed mtime in ns."""

    total = 0
    try:
        newest = session_dir.stat().st_mtime_ns
    except OSError:
        return 0, 0
    for root, directories, files in os.walk(session_dir, topdown=True, followlinks=False):
        root_path = Path(root)
        kept_directories: List[str] = []
        for name in directories:
            child = root_path / name
            if child.is_symlink():
                continue
            kept_directories.append(name)
            with contextlib.suppress(OSError):
                newest = max(newest, child.stat().st_mtime_ns)
        directories[:] = kept_directories
        for name in files:
            child = root_path / name
            try:
                if child.is_symlink() or not child.is_file():
                    continue
                stat = child.stat()
            except OSError:
                continue
            total += stat.st_size
            newest = max(newest, stat.st_mtime_ns)
    return total, newest


def prune_plan_token(
    project: Path,
    keep: int,
    older_than_days: int,
    candidates: List[Dict[str, Any]],
) -> str:
    material = {
        "version": PRUNE_PLAN_VERSION,
        "project_dir": str(project),
        "keep": keep,
        "older_than_days": older_than_days,
        "candidates": [
            {
                "session_dir": str(item["path"]),
                "bytes": item["bytes"],
                "modified_ns": item["modified_ns"],
                "device": item["device"],
                "inode": item["inode"],
            }
            for item in candidates
        ],
    }
    return hashlib.sha256(json_dumps(material).encode("utf-8")).hexdigest()


def prune_impl(
    project: Path,
    *,
    keep: int,
    older_than_days: int,
    apply: bool,
    plan: Optional[str] = None,
) -> Dict[str, Any]:
    project = resolve_project(project)
    if keep < 0:
        raise CompanionError("--keep must be zero or a positive integer")
    if older_than_days < 0:
        raise CompanionError("--older-than-days must be zero or a positive integer")
    if apply and not plan:
        raise CompanionError("--apply requires the exact --plan from a fresh dry-run")

    root = runtime_root(project)
    sessions_root = root / "sessions"
    if root.is_symlink() or sessions_root.is_symlink():
        raise CompanionError("Refusing to prune a symlinked runtime directory")
    empty_plan = prune_plan_token(project, keep, older_than_days, [])
    if not sessions_root.exists():
        if apply and not secrets.compare_digest(str(plan), empty_plan):
            raise CompanionError("Prune plan changed; run the dry-run again and use its exact plan")
        return {
            "type": "sessions-pruned",
            "project_dir": str(project),
            "dry_run": not apply,
            "keep": keep,
            "older_than_days": older_than_days,
            "candidates": [],
            "deleted": [],
            "reclaimable_bytes": 0,
            "plan": empty_plan,
            "remaining_sessions": 0,
        }

    try:
        sessions_root_resolved = sessions_root.resolve(strict=True)
        entries = list(sessions_root.iterdir())
    except OSError as exc:
        raise CompanionError(f"Could not inspect runtime sessions: {exc}") from exc

    current = current_info(project)
    pointer = current_file(project)
    if (pointer.exists() or pointer.is_symlink()) and current is None:
        raise CompanionError("Current session pointer is invalid; refusing to prune")
    current_session = (
        Path(str(current.get("session_dir", ""))).resolve()
        if current and current.get("session_dir")
        else None
    )
    inventory: List[Dict[str, Any]] = []
    for path in entries:
        if path.name.startswith(".") or path.is_symlink() or not path.is_dir():
            continue
        try:
            resolved = path.resolve(strict=True)
            resolved.relative_to(sessions_root_resolved)
            session_stat = resolved.stat()
        except (OSError, ValueError):
            continue
        state_dir = resolved / "state"
        if state_dir.is_symlink():
            continue
        size, modified_ns = session_usage(resolved)
        info = read_json(state_dir / "server-info.json")
        inventory.append(
            {
                "path": resolved,
                "bytes": size,
                "modified_ns": modified_ns,
                "device": session_stat.st_dev,
                "inode": session_stat.st_ino,
                "active": server_reachable(info, timeout=0.25),
            }
        )

    inventory.sort(key=lambda item: (item["modified_ns"], str(item["path"])), reverse=True)
    protected = {item["path"] for item in inventory[:keep]}
    if current_session is not None:
        protected.add(current_session)
    protected.update(item["path"] for item in inventory if item["active"])

    now_ns = time.time_ns()
    minimum_age_ns = older_than_days * 24 * 60 * 60 * 1_000_000_000
    candidates = [
        item
        for item in inventory
        if item["path"] not in protected
        and max(0, now_ns - item["modified_ns"]) >= minimum_age_ns
    ]
    computed_plan = prune_plan_token(project, keep, older_than_days, candidates)
    if apply and not secrets.compare_digest(str(plan), computed_plan):
        raise CompanionError("Prune plan changed; run the dry-run again and use its exact plan")

    if apply:
        refreshed_current = current_info(project)
        refreshed_current_session = (
            Path(str(refreshed_current.get("session_dir", ""))).resolve()
            if refreshed_current and refreshed_current.get("session_dir")
            else None
        )
        for item in candidates:
            path = item["path"]
            if path == refreshed_current_session:
                raise CompanionError("Prune plan became unsafe because the current session changed")
            info = read_json(path / "state" / "server-info.json")
            if server_reachable(info, timeout=0.25):
                raise CompanionError(f"Prune plan became unsafe because a session is active: {path}")
            current_bytes, current_modified_ns = session_usage(path)
            try:
                current_stat = path.stat()
            except OSError as exc:
                raise CompanionError(
                    "Prune plan changed; run the dry-run again and use its exact plan"
                ) from exc
            if (
                current_bytes != item["bytes"]
                or current_modified_ns != item["modified_ns"]
                or current_stat.st_dev != item["device"]
                or current_stat.st_ino != item["inode"]
            ):
                raise CompanionError("Prune plan changed; run the dry-run again and use its exact plan")
    selected: List[Dict[str, Any]] = []
    deleted: List[Dict[str, Any]] = []
    for item in candidates:
        path = item["path"]
        record = {
            "session_dir": str(path),
            "bytes": item["bytes"],
            "modified_at": dt.datetime.fromtimestamp(
                item["modified_ns"] / 1_000_000_000, tz=dt.timezone.utc
            )
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z"),
        }
        if apply:
            if path.is_symlink() or path_has_symlink(sessions_root_resolved, path):
                raise CompanionError(f"Refusing to prune symlinked session path: {path}")
            try:
                path.resolve(strict=True).relative_to(sessions_root_resolved)
            except (OSError, ValueError) as exc:
                raise CompanionError(f"Session resolved outside runtime root: {path}") from exc
            try:
                shutil.rmtree(path)
            except OSError as exc:
                raise CompanionError(f"Could not prune session {path}: {exc}") from exc
            deleted.append(record)
        selected.append(record)

    return {
        "type": "sessions-pruned",
        "project_dir": str(project),
        "dry_run": not apply,
        "keep": keep,
        "older_than_days": older_than_days,
        "candidates": selected if not apply else [],
        "deleted": deleted,
        "plan": computed_plan,
        "reclaimable_bytes": sum(item["bytes"] for item in candidates),
        "remaining_sessions": len(inventory) - (len(candidates) if apply else 0),
    }


class Handler(BaseHTTPRequestHandler):
    server_version = f"VisualBrainstorming/{VERSION}"

    def setup(self) -> None:
        super().setup()
        self.connection.settimeout(HTTP_CONNECTION_TIMEOUT_SECONDS)

    @property
    def context(self) -> ServerContext:
        return self.server.context  # type: ignore[attr-defined]

    def log_message(self, fmt: str, *args: Any) -> None:
        # Routine access logging is intentionally disabled. Request targets may
        # contain the session key, and polling would otherwise grow logs forever.
        return

    def _query(self) -> Dict[str, List[str]]:
        return urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query, keep_blank_values=True)

    def _provided_key(self, path_key: str, *, allow_referer: bool = False) -> str:
        if path_key:
            return path_key
        query_keys = self._query().get("key", [])
        if len(query_keys) == 1 and query_keys[0]:
            return query_keys[0]
        if allow_referer:
            return self._referer_key()
        return ""

    def _referer_key(self) -> str:
        raw = self.headers.get("Referer", "")
        host = self.headers.get("Host", "")
        if not raw or not host:
            return ""
        try:
            parsed = urllib.parse.urlsplit(raw)
        except ValueError:
            return ""
        if (
            parsed.scheme != "http"
            or parsed.netloc.lower() != host.lower()
            or parsed.username
            or parsed.password
        ):
            return ""
        route, key = split_browser_capability_path(parsed.path)
        if not route.startswith("/screen/"):
            return ""
        return key

    def _host_allowed(self) -> bool:
        raw = self.headers.get("Host", "")
        if not raw:
            return False
        return host_only(raw) in self.context.allowed_hosts

    def _authenticate(self, path_key: str, *, allow_referer: bool = False) -> bool:
        if not self._host_allowed():
            return False
        provided = self._provided_key(path_key, allow_referer=allow_referer)
        return secrets.compare_digest(provided, self.context.session.key)

    def _base_headers(
        self,
        content_type: str,
        length: int,
        *,
        referrer_policy: str = "no-referrer",
    ) -> None:
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(length))
        self.send_header("Cache-Control", "no-store, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", referrer_policy)
        self.send_header("X-Frame-Options", "SAMEORIGIN")

    def _send_bytes(
        self,
        status: int,
        data: bytes,
        content_type: str,
        *,
        csp: Optional[str] = None,
        referrer_policy: str = "no-referrer",
    ) -> None:
        self.send_response(status)
        self._base_headers(
            content_type,
            len(data),
            referrer_policy=referrer_policy,
        )
        if csp:
            self.send_header("Content-Security-Policy", csp)
        self.end_headers()
        self.wfile.write(data)

    def _send_json(self, status: int, value: Any) -> None:
        self._send_bytes(
            status,
            (json_dumps(value) + "\n").encode("utf-8"),
            "application/json; charset=utf-8",
            csp="default-src 'none'; frame-ancestors 'none'",
        )

    def _reject(self, status: int, message: str) -> None:
        self._send_json(status, {"ok": False, "error": message})

    def _require_auth(self, path_key: str, *, allow_referer: bool = False) -> bool:
        if not self._authenticate(path_key, allow_referer=allow_referer):
            self._reject(403, "invalid session key or host")
            return False
        return True

    def _origin_allowed(self) -> bool:
        origin = self.headers.get("Origin")
        if not origin:
            return True
        host = self.headers.get("Host", "")
        return origin == f"http://{host}"

    def _require_content_root(self) -> bool:
        if content_root_is_valid(self.context.session):
            return True
        self._reject(409, "session content directory changed after startup")
        return False

    def _require_state_root(self) -> bool:
        if state_root_is_valid(self.context.session):
            return True
        self._reject(409, "session state directory changed after startup")
        return False

    def do_GET(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlsplit(self.path)
        route, path_key = split_browser_capability_path(parsed.path)
        if not self._host_allowed():
            self._reject(403, "invalid session key or host")
            return

        if route == "/":
            try:
                body = shell_document().encode("utf-8")
            except CompanionError as exc:
                self._reject(500, str(exc))
                return
            self._send_bytes(
                200,
                body,
                "text/html; charset=utf-8",
                csp=(
                    "default-src 'self'; script-src 'self' 'unsafe-inline'; "
                    "style-src 'self' 'unsafe-inline'; img-src 'self' data:; "
                    "frame-src 'self'; connect-src 'self'; frame-ancestors 'self'; "
                    "object-src 'none'; base-uri 'none'; form-action 'none'"
                ),
            )
            return

        if route in {"/favicon.svg", "/favicon.ico"}:
            try:
                body = ICON_PATH.read_bytes()
            except OSError as exc:
                self._reject(500, f"favicon unavailable: {exc}")
                return
            self._send_bytes(
                200,
                body,
                "image/svg+xml; charset=utf-8",
                csp=(
                    "default-src 'none'; script-src 'none'; object-src 'none'; "
                    "base-uri 'none'; frame-ancestors 'none'; sandbox"
                ),
            )
            return

        if not self._require_auth(
            path_key,
            allow_referer=route.startswith("/files/"),
        ):
            return

        if route == "/api/health":
            self._send_json(200, {"ok": True, "version": VERSION, "pid": os.getpid()})
            return

        if route == "/api/latest":
            if not self._require_content_root():
                return
            latest = latest_screen(self.context.session.content_dir)
            if latest is None:
                self._send_json(200, {"available": False})
                return
            path, stat = latest
            if stat.st_size > MAX_SCREEN_BYTES:
                self._send_json(
                    200,
                    {
                        "available": False,
                        "error": "最新画面超过 5 MiB，未加载",
                        "name": path.name,
                        "size": stat.st_size,
                    },
                )
                return
            version = f"{stat.st_mtime_ns:x}-{stat.st_size:x}"
            self._send_json(
                200,
                {
                    "available": True,
                    "name": path.name,
                    "version": version,
                    "bridge": self.context.screen_bridge(path, stat),
                    "size": stat.st_size,
                    "modified_ns": stat.st_mtime_ns,
                },
            )
            return

        if route == "/api/events":
            if not self._require_state_root():
                return
            try:
                after = int((self._query().get("after") or ["0"])[0])
            except ValueError:
                after = 0
            try:
                events = read_session_events(
                    self.context.session,
                    after=max(after, 0),
                )
            except CompanionError as exc:
                self._reject(409, str(exc))
                return
            self._send_json(200, {"events": events})
            return

        if route == "/api/session":
            allowed = {
                "type",
                "version",
                "pid",
                "host",
                "url_host",
                "port",
                "allow_remote",
                "idle_timeout_seconds",
                "started_at",
            }
            public = {key: value for key, value in self.context.info.items() if key in allowed}
            public["url"] = "/"
            self._send_json(200, public)
            return

        if route.startswith("/screen/"):
            if not self._require_content_root():
                return
            name = route[len("/screen/") :]
            screen_path = safe_content_path(self.context.session.content_dir, name)
            if screen_path is None or screen_path.suffix.lower() not in {".html", ".htm"}:
                self._reject(404, "screen not found")
                return
            try:
                screen_stat = screen_path.stat()
                if screen_stat.st_size > MAX_SCREEN_BYTES:
                    self._reject(413, "screen exceeds 5 MiB")
                    return
            except OSError:
                self._reject(404, "screen not readable")
                return
            try:
                raw = screen_path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                self._reject(422, "screen must be readable UTF-8 HTML")
                return
            try:
                body = render_screen(
                    raw, self.context.screen_bridge(screen_path, screen_stat)
                ).encode("utf-8")
            except CompanionError as exc:
                self._reject(500, str(exc))
                return
            self.context.touch()
            self._send_bytes(
                200,
                body,
                "text/html; charset=utf-8",
                csp=(
                    "default-src 'self' data: blob:; script-src 'self' 'unsafe-inline'; "
                    "style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; "
                    "font-src 'self' data:; connect-src 'none'; frame-ancestors 'self'; "
                    "frame-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'"
                ),
                referrer_policy="same-origin",
            )
            return

        if route.startswith("/files/"):
            if not self._require_content_root():
                return
            relative = route[len("/files/") :]
            file_path = safe_content_path(self.context.session.content_dir, relative)
            if file_path is None or file_path.suffix.lower() in {".html", ".htm"}:
                self._reject(404, "file not found")
                return
            try:
                if file_path.stat().st_size > MAX_ASSET_BYTES:
                    self._reject(413, "file exceeds 10 MiB")
                    return
            except OSError:
                self._reject(404, "file not readable")
                return
            try:
                data = file_path.read_bytes()
            except OSError:
                self._reject(404, "file not readable")
                return
            guessed, _ = mimetypes.guess_type(file_path.name)
            content_type = guessed or "application/octet-stream"
            if content_type.startswith("text/") or content_type in {"application/javascript", "application/json", "image/svg+xml"}:
                content_type += "; charset=utf-8"
            self.context.touch()
            self._send_bytes(
                200,
                data,
                content_type,
                csp=(
                    "default-src 'none'; script-src 'none'; object-src 'none'; "
                    "base-uri 'none'; frame-ancestors 'none'; sandbox"
                ),
            )
            return

        self._reject(404, "not found")

    def do_POST(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlsplit(self.path)
        route, path_key = split_browser_capability_path(parsed.path)
        if not self._require_auth(path_key):
            return
        if not self._origin_allowed():
            self._reject(403, "origin rejected")
            return
        if self.headers.get("X-VB-Client") != "1":
            self._reject(403, "missing client marker")
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length < 0 or length > MAX_REQUEST_BYTES:
            self._reject(413, "request body is too large")
            return
        raw_body = self.rfile.read(length) if length else b"{}"
        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._reject(400, "invalid JSON")
            return
        if not isinstance(payload, dict):
            self._reject(400, "JSON body must be an object")
            return

        if route == "/api/events":
            if not self._require_state_root():
                return
            try:
                event = self.context.append_event(payload)
            except CompanionError as exc:
                self._reject(422, str(exc))
                return
            self.context.touch()
            self._send_json(201, {"ok": True, "event": event})
            return

        if route == "/api/shutdown":
            self._send_json(200, {"ok": True, "stopping": True})
            threading.Thread(target=self.server.shutdown, daemon=True).start()
            return

        self._reject(404, "not found")


def build_info(
    session: SessionPaths,
    host: str,
    url_host: str,
    port: int,
    allow_remote: bool,
    idle_timeout_seconds: int,
) -> Dict[str, Any]:
    url_host_formatted = f"[{url_host}]" if ":" in url_host and not url_host.startswith("[") else url_host
    control_host = "::1" if host == "::" else ("127.0.0.1" if host == "0.0.0.0" else host)
    control_host_formatted = f"[{control_host}]" if ":" in control_host and not control_host.startswith("[") else control_host
    quoted_key = urllib.parse.quote(session.key, safe="")
    url = f"http://{url_host_formatted}:{port}/#key={quoted_key}"
    control_url = f"http://{control_host_formatted}:{port}/?key={quoted_key}"
    return {
        "type": "server-started",
        "version": VERSION,
        "pid": os.getpid(),
        "host": host,
        "url_host": url_host,
        "port": port,
        "url": url,
        "control_url": control_url,
        "allow_remote": allow_remote,
        "idle_timeout_seconds": idle_timeout_seconds,
        "project_dir": str(session.project_dir),
        "session_dir": str(session.session_dir),
        "screen_dir": str(session.content_dir),
        "state_dir": str(session.state_dir),
        "started_at": utc_now(),
    }


def install_signal_handlers(server: CompanionHTTPServer) -> None:
    def request_shutdown(signum: int, _frame: Any) -> None:
        server.context.log(f"received signal {signum}; shutting down")
        threading.Thread(target=server.shutdown, daemon=True).start()

    for signum in (signal.SIGTERM, signal.SIGINT):
        with contextlib.suppress(ValueError, OSError):
            signal.signal(signum, request_shutdown)


def start_idle_watchdog(server: CompanionHTTPServer) -> Optional[threading.Thread]:
    timeout = server.context.idle_timeout_seconds
    if timeout <= 0:
        return None

    interval = min(30.0, max(0.25, timeout / 4.0))

    def monitor() -> None:
        while True:
            time.sleep(interval)
            idle_for = server.context.idle_for()
            if idle_for < timeout:
                continue
            server.context.log(
                f"idle timeout reached after {idle_for:.1f}s; shutting down"
            )
            server.shutdown()
            return

    thread = threading.Thread(
        target=monitor,
        name="visual-brainstorming-idle-watchdog",
        daemon=True,
    )
    thread.start()
    return thread


def serve_impl(args: argparse.Namespace) -> int:
    project = resolve_project(args.project_dir)
    try:
        if args.launch_managed:
            validate_managed_launch(project, str(args.launch_managed))
            launch_lock = None
        else:
            launch_lock = acquire_runtime_lock(project, "launch", timeout=12.0)
        try:
            server_lock = acquire_runtime_lock(project, "server", timeout=0.1)
            try:
                return serve_locked_impl(args, project, launch_lock)
            finally:
                server_lock.release()
        finally:
            if launch_lock is not None:
                launch_lock.release()
    except Exception as exc:
        if args.launch_managed and args.session_dir:
            record_launch_error(project, args.session_dir, exc)
        raise


def record_launch_error(project: Path, requested: Path, exc: Exception) -> None:
    sessions_root = runtime_root(project) / "sessions"
    requested_path = Path(os.path.abspath(requested.expanduser()))
    try:
        requested_path.relative_to(Path(os.path.abspath(sessions_root)))
    except ValueError:
        return
    if sessions_root.is_symlink() or path_has_symlink(sessions_root, requested_path):
        return
    state_dir = requested_path / "state"
    if state_dir.is_symlink() or not state_dir.is_dir():
        return
    secret = ""
    key_file = state_dir / "session-key"
    if not key_file.is_symlink():
        with contextlib.suppress(OSError, UnicodeError):
            secret = key_file.read_text(encoding="utf-8").strip()
    message = sanitized_log_message(str(exc), secret)
    with contextlib.suppress(OSError):
        write_json(
            state_dir / "launch-error.json",
            {"type": "launch-error", "message": message, "recorded_at": utc_now()},
            mode=0o600,
        )


def serve_locked_impl(
    args: argparse.Namespace,
    project: Path,
    startup_lock: Optional[RuntimeLock],
) -> int:
    host, url_host, port, allow_remote, idle_timeout = requested_server_settings(args)
    session = prepare_session(project, args.session_dir)

    context = ServerContext(
        session=session,
        host=host,
        url_host=url_host,
        port=port,
        allow_remote=allow_remote,
        idle_timeout_seconds=idle_timeout,
    )
    try:
        server = CompanionHTTPServer((host, port), Handler, context)
    except OSError as exc:
        raise CompanionError(f"Could not bind local server on {host}:{port}: {exc}") from exc
    actual_port = int(server.server_address[1])
    context.port = actual_port
    info = build_info(
        session,
        host,
        url_host,
        actual_port,
        allow_remote,
        idle_timeout,
    )
    context.info = info

    write_json(session.state_dir / "server-info.json", info, mode=0o600)
    write_json(current_file(project), info, mode=0o600)
    if startup_lock is not None:
        startup_lock.release()
    stopped_file = session.state_dir / "server-stopped.json"
    with contextlib.suppress(FileNotFoundError):
        stopped_file.unlink()

    install_signal_handlers(server)
    start_idle_watchdog(server)
    if not args.launch_managed:
        print(json_dumps(info), flush=True)
    context.log(f"server started pid={os.getpid()} url_host={url_host} port={actual_port}")

    if args.open:
        browser_timer = threading.Timer(0.25, lambda: webbrowser.open(info["url"]))
        browser_timer.daemon = True
        browser_timer.start()

    try:
        server.serve_forever(poll_interval=0.35)
    finally:
        server.server_close()
        if state_root_is_valid(session):
            write_json(
                stopped_file,
                {"type": "server-stopped", "pid": os.getpid(), "stopped_at": utc_now()},
                mode=0o600,
            )
        context.log("server stopped")
    return 0


def stop_info(info: Dict[str, Any], timeout: float = 3.0) -> bool:
    try:
        result = http_json(endpoint_from_info(info, "/api/shutdown"), method="POST", payload={}, timeout=timeout)
    except (OSError, ValueError, CompanionError, http.client.HTTPException, json.JSONDecodeError):
        return False
    return result.get("ok") is True


def start_impl(args: argparse.Namespace) -> Dict[str, Any]:
    project = resolve_project(args.project_dir)
    settings = requested_server_settings(args)
    launch_lock = acquire_runtime_lock(project, "launch", timeout=12.0)
    try:
        return start_locked_impl(args, project, settings, launch_lock)
    finally:
        launch_lock.release()


def start_locked_impl(
    args: argparse.Namespace,
    project: Path,
    settings: Tuple[str, str, int, bool, int],
    launch_lock: RuntimeLock,
) -> Dict[str, Any]:
    host, url_host, port, allow_remote, idle_timeout = settings
    existing = current_info(project)
    existing_health = server_health(existing)
    if existing and existing_health:
        compatible = existing_health.get("version") == VERSION
        if args.new:
            stop_info(existing)
            deadline = time.time() + 3.0
            while time.time() < deadline and server_reachable(existing, timeout=0.25):
                time.sleep(0.08)
            if server_reachable(existing, timeout=0.25):
                raise CompanionError("Current server did not stop; refusing to start a second session")
        else:
            if not compatible:
                raise CompanionError(
                    "Current server uses a different companion version; use --new to replace it"
                )
            if not existing_settings_match(
                existing,
                host,
                url_host,
                port,
                allow_remote,
                idle_timeout,
            ):
                raise CompanionError(
                    "Current server settings differ from this request; use --new to replace it"
                )
            if args.open:
                webbrowser.open(str(existing.get("url", "")))
            result = dict(existing)
            result["_started_new"] = False
            return result

    session = prepare_session(project)
    launch_error_path = session.state_dir / "launch-error.json"

    command = [
        sys.executable,
        "-I",
        "-S",
        str(Path(__file__).resolve()),
        "serve",
        "--project-dir",
        str(project),
        "--session-dir",
        str(session.session_dir),
        "--host",
        host,
        "--port",
        str(port),
        "--url-host",
        url_host,
        "--idle-timeout",
        str(idle_timeout),
        f"--launch-managed={launch_lock.token}",
    ]
    if allow_remote:
        command.append("--allow-remote")
    if args.open:
        command.append("--open")

    popen_kwargs: Dict[str, Any] = {
        "cwd": str(project),
        "stdin": subprocess.DEVNULL,
    }
    if os.name == "nt":
        detached = getattr(subprocess, "DETACHED_PROCESS", 0x00000008)
        new_group = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0x00000200)
        popen_kwargs["creationflags"] = detached | new_group
    else:
        popen_kwargs["start_new_session"] = True

    popen_kwargs["stdout"] = subprocess.DEVNULL
    popen_kwargs["stderr"] = subprocess.DEVNULL
    process = subprocess.Popen(command, **popen_kwargs)

    write_json(
        session.state_dir / "launcher.json",
        {"pid": process.pid, "command": command, "launched_at": utc_now()},
        mode=0o600,
    )

    info_path = session.state_dir / "server-info.json"
    deadline = time.time() + 10.0
    while time.time() < deadline:
        info = read_json(info_path)
        if info and is_server_alive(info, timeout=0.4):
            result = dict(info)
            result["_started_new"] = True
            return result
        if process.poll() is not None:
            break
        time.sleep(0.1)

    if process.poll() is None:
        with contextlib.suppress(OSError):
            process.terminate()
        try:
            process.wait(timeout=2.0)
        except subprocess.TimeoutExpired:
            with contextlib.suppress(OSError):
                process.kill()
            with contextlib.suppress(subprocess.TimeoutExpired):
                process.wait(timeout=2.0)

    launch_error = read_json(launch_error_path)
    detail = str(launch_error.get("message", "")) if launch_error else ""
    suffix = f" Detail: {detail}" if detail else ""
    raise CompanionError(f"Server did not start.{suffix}")


def validated_html_source(source: Path) -> Tuple[Path, bytes]:
    source_path = source.expanduser().resolve()
    if not source_path.is_file():
        raise CompanionError(f"Source HTML does not exist: {source_path}")
    if source_path.suffix.lower() not in {".html", ".htm"}:
        raise CompanionError("Source must use .html or .htm")
    data = source_path.read_bytes()
    if len(data) > MAX_SCREEN_BYTES:
        raise CompanionError(f"Screen exceeds {MAX_SCREEN_BYTES} bytes")
    try:
        data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CompanionError("Screen must be UTF-8") from exc
    return source_path, data


def publish_impl(
    project: Path,
    source: Path,
    name: Optional[str],
    *,
    expected_session: Optional[Path] = None,
) -> Dict[str, Any]:
    project = resolve_project(project)
    info = current_info(project)
    if not info:
        raise CompanionError("No current session. Run start or serve first.")
    if not is_server_alive(info):
        raise CompanionError("Current server is not running. Run start or serve first.")
    session_dir = Path(str(info.get("session_dir", ""))).resolve()
    if expected_session is not None and session_dir != expected_session.resolve():
        raise CompanionError("Current session changed before the screen was published")
    content_dir = Path(os.path.abspath(str(info.get("screen_dir", ""))))
    if (
        content_dir != session_dir / "content"
        or content_dir.is_symlink()
        or path_has_symlink(session_dir, content_dir)
        or not content_dir.is_dir()
    ):
        raise CompanionError(f"Current screen directory is missing: {content_dir}")
    try:
        http_json(endpoint_from_info(info, "/api/latest"), timeout=1.0)
    except (
        OSError,
        ValueError,
        CompanionError,
        http.client.HTTPException,
        json.JSONDecodeError,
    ) as exc:
        raise CompanionError("Current server rejected its content directory") from exc

    source_path, data = validated_html_source(source)

    raw_slug = name or source_path.stem or "screen"
    slug = re.sub(r"[^\w-]+", "-", raw_slug, flags=re.UNICODE).strip("-_")[:64] or "screen"
    now = dt.datetime.now()
    millis = now.microsecond // 1000
    filename = f"{now:%Y%m%d-%H%M%S}-{millis:03d}-{secrets.token_hex(2)}-{slug}.html"
    target = content_dir / filename
    atomic_write_bytes(target, data, mode=0o600)
    try:
        current_after = current_info(project)
        if not current_after:
            raise CompanionError("Current session changed before the screen was published")
        current_after_session = Path(str(current_after.get("session_dir", ""))).resolve()
        if current_after_session != session_dir:
            raise CompanionError("Current session changed before the screen was published")
        latest = http_json(endpoint_from_info(current_after, "/api/latest"), timeout=1.0)
        if latest.get("available") is not True or latest.get("name") != target.name:
            raise CompanionError("Current server did not acknowledge the published screen")
        stat = target.stat()
    except Exception:
        # Do not unlink through a path that may have been swapped after write.
        # Failed publications remain inside the ignored session for inspection.
        raise
    return {
        "type": "screen-published",
        "name": target.name,
        "path": str(target),
        "size": stat.st_size,
        "version": f"{stat.st_mtime_ns:x}-{stat.st_size:x}",
        "published_at": utc_now(),
    }


def print_result(value: Any) -> None:
    print(json_dumps(value, pretty=True))


def cmd_start(args: argparse.Namespace) -> int:
    result = start_impl(args)
    result.pop("_started_new", None)
    print_result(result)
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    project = resolve_project(args.project_dir)
    info = current_info(project)
    health = server_health(info)
    running = health is not None
    compatible = bool(health and health.get("version") == VERSION)
    result: Dict[str, Any] = {
        "running": running,
        "compatible": compatible,
        "project_dir": str(project),
    }
    if info:
        result.update(
            {
                "url": info.get("url"),
                "pid": info.get("pid"),
                "session_dir": info.get("session_dir"),
                "screen_dir": info.get("screen_dir"),
                "state_dir": info.get("state_dir"),
                "server_version": health.get("version") if health else None,
            }
        )
    print_result(result)
    return 0


def cmd_paths(args: argparse.Namespace) -> int:
    project = resolve_project(args.project_dir)
    info = current_info(project)
    if not info:
        raise CompanionError("No current session")
    print_result(
        {
            "project_dir": str(project),
            "session_dir": info.get("session_dir"),
            "screen_dir": info.get("screen_dir"),
            "state_dir": info.get("state_dir"),
            "url": info.get("url"),
        }
    )
    return 0


def cmd_publish(args: argparse.Namespace) -> int:
    project = resolve_project(args.project_dir)
    launch_lock = acquire_runtime_lock(project, "launch", timeout=12.0)
    try:
        print_result(publish_impl(project, args.source, args.name))
    finally:
        launch_lock.release()
    return 0


def show_impl(args: argparse.Namespace, source: Path, name: Optional[str]) -> Dict[str, Any]:
    """Start or reuse the server, publish one screen, then optionally open it."""

    validated_html_source(source)
    open_requested = bool(args.open)
    start_args = argparse.Namespace(**vars(args))
    start_args.open = False
    project = resolve_project(args.project_dir)
    settings = requested_server_settings(start_args)
    launch_lock = acquire_runtime_lock(project, "launch", timeout=12.0)
    try:
        info = start_locked_impl(start_args, project, settings, launch_lock)
        started_new = bool(info.pop("_started_new", False))
        expected_session = Path(str(info.get("session_dir", "")))
        try:
            published = publish_impl(
                project,
                source,
                name,
                expected_session=expected_session,
            )
        except Exception:
            if started_new:
                stop_info(info)
            raise
        if open_requested:
            webbrowser.open(str(info.get("url", "")))
    finally:
        launch_lock.release()
    return {
        "type": "screen-shown",
        "running": True,
        "url": info.get("url"),
        "pid": info.get("pid"),
        "host": info.get("host"),
        "url_host": info.get("url_host"),
        "allow_remote": info.get("allow_remote"),
        "session_dir": info.get("session_dir"),
        "screen": published,
        "browser_open_requested": open_requested,
    }


def cmd_show(args: argparse.Namespace) -> int:
    print_result(show_impl(args, args.source, args.name))
    return 0


def cmd_events(args: argparse.Namespace) -> int:
    project = resolve_project(args.project_dir)
    info = current_info(project)
    if not info:
        raise CompanionError("No current session")
    session_dir = Path(str(info.get("session_dir", ""))).resolve()
    state_dir = Path(os.path.abspath(str(info.get("state_dir", ""))))
    if (
        state_dir != session_dir / "state"
        or state_dir.is_symlink()
        or path_has_symlink(session_dir, state_dir)
    ):
        raise CompanionError("Current session state directory is unsafe")
    events = read_events(state_dir / "events.jsonl", after=max(args.after, 0))
    if args.latest and args.tail is not None:
        raise CompanionError("Use either --latest or --tail, not both")
    if args.latest:
        print_result(events[-1] if events else {})
    elif args.tail is not None:
        if args.tail < 0 or args.tail > 200:
            raise CompanionError("--tail must be between 0 and 200")
        print_result(events[-args.tail :] if args.tail else [])
    else:
        print_result(events)
    return 0


def cmd_stop(args: argparse.Namespace) -> int:
    project = resolve_project(args.project_dir)
    launch_lock = acquire_runtime_lock(project, "launch", timeout=12.0)
    try:
        info = current_info(project)
        if not info:
            print_result({"stopped": False, "reason": "no current session"})
            return 0
        if not server_reachable(info):
            print_result({"stopped": False, "reason": "server is not running", "session_dir": info.get("session_dir")})
            return 0
        accepted = stop_info(info)
        if accepted:
            deadline = time.time() + 4.0
            while time.time() < deadline and server_reachable(info, timeout=0.25):
                time.sleep(0.1)
        print_result({"stopped": not server_reachable(info, timeout=0.25), "session_dir": info.get("session_dir")})
    finally:
        launch_lock.release()
    return 0


def cmd_prune(args: argparse.Namespace) -> int:
    project = resolve_project(args.project_dir)
    launch_lock = acquire_runtime_lock(project, "launch", timeout=12.0)
    try:
        print_result(
            prune_impl(
                project,
                keep=int(args.keep),
                older_than_days=int(args.older_than_days),
                apply=bool(args.apply),
                plan=args.plan,
            )
        )
    finally:
        launch_lock.release()
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    print_result(show_impl(args, DEMO_PATH, "model-routing-demo"))
    return 0


def add_common_start_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--project-dir", type=Path, default=Path.cwd(), help="Project root")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host; loopback by default")
    parser.add_argument("--port", type=int, default=0, help="Port; 0 selects a free port")
    parser.add_argument(
        "--url-host",
        help="Host placed in the browser URL; remote mode requires a local literal IP",
    )
    parser.add_argument("--allow-remote", action="store_true", help="Allow non-loopback binding")
    parser.add_argument(
        "--idle-timeout",
        type=int,
        default=DEFAULT_IDLE_TIMEOUT_SECONDS,
        help="Stop after this many idle seconds; 0 disables the timeout",
    )
    parser.add_argument("--open", action="store_true", help="Open the browser")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    start = subparsers.add_parser("start", help="Start or reuse a detached local server")
    add_common_start_arguments(start)
    start.add_argument("--new", action="store_true", help="Stop the current server and start a new session")
    start.set_defaults(func=cmd_start)

    serve = subparsers.add_parser("serve", help="Run the local server in the foreground")
    add_common_start_arguments(serve)
    serve.add_argument("--session-dir", type=Path, help=argparse.SUPPRESS)
    serve.add_argument("--launch-managed", help=argparse.SUPPRESS)
    serve.set_defaults(func=serve_impl)

    status = subparsers.add_parser("status", help="Check the current project session")
    status.add_argument("--project-dir", type=Path, default=Path.cwd())
    status.set_defaults(func=cmd_status)

    paths = subparsers.add_parser("paths", help="Print current session paths")
    paths.add_argument("--project-dir", type=Path, default=Path.cwd())
    paths.set_defaults(func=cmd_paths)

    publish = subparsers.add_parser("publish", help="Atomically publish a UTF-8 HTML screen")
    publish.add_argument("--project-dir", type=Path, default=Path.cwd())
    publish.add_argument("--source", type=Path, required=True)
    publish.add_argument("--name")
    publish.set_defaults(func=cmd_publish)

    show = subparsers.add_parser("show", help="Start or reuse the server and publish one screen")
    add_common_start_arguments(show)
    show.add_argument("--source", type=Path, required=True)
    show.add_argument("--name")
    show.add_argument("--new", action="store_true", help="Stop the current server and start a new session")
    show.set_defaults(func=cmd_show)

    events = subparsers.add_parser("events", help="Read recorded browser events")
    events.add_argument("--project-dir", type=Path, default=Path.cwd())
    events.add_argument("--latest", action="store_true")
    events.add_argument("--tail", type=int, help="Return only the last N matching events (0-200)")
    events.add_argument("--after", type=int, default=0)
    events.set_defaults(func=cmd_events)

    stop = subparsers.add_parser("stop", help="Stop the current project server")
    stop.add_argument("--project-dir", type=Path, default=Path.cwd())
    stop.set_defaults(func=cmd_stop)

    prune = subparsers.add_parser(
        "prune", help="List or remove old stopped project sessions"
    )
    prune.add_argument("--project-dir", type=Path, default=Path.cwd())
    prune.add_argument(
        "--keep",
        type=int,
        default=DEFAULT_PRUNE_KEEP,
        help="Always keep this many newest sessions in addition to the current or active session",
    )
    prune.add_argument(
        "--older-than-days",
        type=int,
        default=DEFAULT_PRUNE_OLDER_THAN_DAYS,
        help="Only select sessions at least this many days old",
    )
    prune.add_argument(
        "--apply",
        action="store_true",
        help="Delete exactly the sessions bound to --plan; dry-run by default",
    )
    prune.add_argument(
        "--plan",
        help="Exact plan token returned by a fresh dry-run; required with --apply",
    )
    prune.set_defaults(func=cmd_prune)

    demo = subparsers.add_parser("demo", help="Start the server and publish the built-in demo")
    add_common_start_arguments(demo)
    demo.add_argument("--new", action="store_true", help="Stop the current server and start a new session")
    demo.set_defaults(func=cmd_demo)

    return parser


def main() -> int:
    if sys.version_info < (3, 9):
        print("Python 3.9 or newer is required", file=sys.stderr)
        return 2
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except CompanionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
