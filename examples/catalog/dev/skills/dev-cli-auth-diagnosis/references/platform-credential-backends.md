# Platform credential backend reference

Use this reference when the same CLI behaves differently across macOS,
Windows, WSL, Linux, Terminal/PowerShell, Codex, a container, or CI. Platform
knowledge narrows the probe; it does not authorize credential migration,
password-manager unlock, or permission changes.

## Contents

1. [Dependency model](#dependency-model)
2. [macOS](#macos)
3. [Native Windows](#native-windows)
4. [WSL and Linux](#wsl-and-linux)
5. [Containers and CI](#containers-and-ci)
6. [Cross-platform comparison protocol](#cross-platform-comparison-protocol)
7. [Official sources](#official-sources)

## Dependency model

An OS-backed credential may require more than a readable config file:

| Dependency | macOS examples | Windows examples |
| --- | --- | --- |
| User credential service | Keychain | Credential Manager |
| User-bound encryption | Keychain access controls | DPAPI bound to user logon or, when selected, machine |
| Local IPC | Unix socket, XPC, helper process | Named pipe, COM, helper process |
| Interactive approval | Keychain prompt, Touch ID, hardware key | Credential UI, Windows Hello, WAM, hardware key |
| User state path | `~/Library/Application Support`, `~/.config`, tool-specific home | `%APPDATA%`, `%LOCALAPPDATA%`, `%USERPROFILE%`, tool-specific home |
| Network callback | Browser plus optional localhost listener | Browser/WAM plus optional localhost listener |

A filesystem grant can solve only the file-path portions. It does not imply OS
service, UI, user-logon, named-pipe, or agent-socket access.

## macOS

### Keychain is an OS service, not an ordinary file

Keychain stores passwords, keys, certificates, and other confidential items
under OS-managed access controls. A CLI normally reaches it through Security
framework APIs or a credential-helper process. Granting read access to a config
directory does not grant Keychain service access or approve a Keychain/Touch ID
prompt.

Codex local sandboxing uses Seatbelt. A CLI can therefore exhibit these
different outcomes:

| Result | Interpretation |
| --- | --- |
| Config file readable; Keychain lookup denied | `credential_source_unreachable`, not missing file |
| Keychain lookup works; token refresh cannot rename config | `credential_persistence_blocked` |
| Interactive Terminal works; Codex fails with same user/config | Boundary dependency proven; isolate service, file, network, or socket next |
| File fallback works | Keychain dependency bypassed; security boundary changed |

Do not use `security ... -w`, credential-helper `get`, or equivalent commands
that print passwords/tokens. If a retrieval command is necessary, redirect its
secret-bearing stdout to `/dev/null` and retain only exit status and non-secret
error class.

### Application state and atomic persistence

macOS CLIs often store configuration under `~/Library/Application Support`,
`~/.config`, a dot-directory, or a tool-specific environment-selected root.
OAuth refresh may use:

1. temporary file creation in the same parent directory;
2. restrictive file mode;
3. fsync or lock;
4. atomic rename over the previous file;
5. cache or profile metadata update.

Reading the existing file is insufficient. When refresh persistence is proven
necessary, the containing directory—not only the final file—usually needs the
reviewed write boundary.

### Helpers, agents, and sockets

Git credential helpers, `ssh-agent`, `gpg-agent`, Docker Desktop, password
managers, and desktop integrations can use executable helpers or Unix sockets.
Check only helper selection and socket reachability; do not request key export
or signing merely as a diagnostic probe.

An agent socket protects the private key from direct export, but socket access
can still authorize authentication or signatures. Treat it as a capability,
not a harmless file read.

### Browser and device flows

Separate these requirements:

- outbound access to the authorization and token hosts;
- launching or showing a browser/UI;
- binding a localhost callback;
- receiving a device code without local binding;
- persisting the resulting credential.

A device-code flow can avoid local callback binding but still changes login
state and requires user authorization.

## Native Windows

### Credential Manager and DPAPI are identity-bound services

Windows Credential Management APIs store and retrieve credentials in the
user's credential store. DPAPI commonly encrypts data so that only the same
user logon credential on the same computer can decrypt it; machine-bound mode
has different and broader semantics.

Consequences for diagnosis:

- a sandbox process with a different or restricted user token may not see the
  same credential state as the interactive user;
- copying a DPAPI-protected blob into an accessible folder does not make it
  decryptable in another user/machine context;
- “file exists” is not evidence that Credential Manager or DPAPI decryption is
  available;
- changing a CLI from Credential Manager/DPAPI to plaintext is a security
  migration requiring explicit authorization.

Do not enumerate all Credential Manager entries merely to prove the service
exists. Target the selected CLI/host through its own safe status or retrieval
probe.

### Named pipes and desktop integrations

Windows helpers and daemon-backed CLIs may use named pipes. Pipe access is
controlled by a security descriptor and an access check against the calling
thread's token. A readable executable and writable config directory do not
prove pipe access.

Treat a named pipe like a Unix socket:

- identify the exact pipe and owner without dumping messages;
- determine whether it grants narrow credential lookup or broad daemon control;
- compare the same non-mutating command under the same Windows identity;
- do not broaden pipe ACLs as a diagnostic shortcut.

### Codex elevated and unelevated sandboxes

The native Codex Windows sandbox currently has two implementations:

- `elevated`: preferred; dedicated lower-privilege sandbox users, filesystem
  permission boundaries, firewall rules, and local policy;
- `unelevated`: fallback; restricted token derived from the current user,
  ACL-based filesystem boundaries, and weaker environment-level network
  isolation.

Record which implementation is active. A result from one does not automatically
generalize to the other.

`/sandbox-add-read-dir C:\absolute\path` adds an existing directory as read-only
for the current session. It does not provide refresh writes, Credential Manager
access, DPAPI identity equivalence, named-pipe access, or network.

### Safe PowerShell probes

Use presence checks that do not print values:

```powershell
Get-Command <cli>
<cli> --version
Test-Path Env:<TOKEN_VARIABLE>
Test-Path "$env:APPDATA\<cli>"
```

Avoid `Get-ChildItem Env:`, `$env:<TOKEN_VARIABLE>`, verbose config dumps,
command-line secrets, broad credential enumeration, and unverified generic pipe
enumeration. Use the target CLI's own non-secret connectivity probe for a named
pipe. Quote paths and keep PowerShell, `cmd.exe`, Git Bash, native Windows, and
WSL path semantics separate.

## WSL and Linux

WSL is a Linux environment with different homes, config roots, sockets, and
credential services from native Windows. A Windows Credential Manager login is
not automatically present in WSL; a WSL token file or agent is not
automatically present in native PowerShell.

Common Linux dependencies include:

- XDG config/cache roots;
- Secret Service or `libsecret` over D-Bus;
- `ssh-agent` and `gpg-agent` Unix sockets;
- browser/device authorization;
- container or desktop integration sockets;
- writable home/cache directories.

Do not “fix” WSL by copying native Windows credential files across the boundary.
Use a supported helper, device flow, workload identity, or deliberately
provisioned credential inside the intended boundary.

## Containers and CI

When a container, remote workspace, or CI runner is the intended outer security
boundary, provision credentials deliberately inside it. A working host login
does not prove that the container should inherit the host credential store or
agent socket.

Prefer, in order appropriate to the provider:

1. workload identity, managed identity, CI job token, or short-lived federation;
2. device/SSO flow with a bounded persisted cache when interactive approval is
   intended;
3. per-command environment injection scoped to one trusted process tree;
4. reviewed credential file or helper mounted read-only when no refresh write is
   required.

Avoid mounting an entire home directory, Docker socket, password-manager
socket, or long-lived user credential merely because it makes the CLI work.
Full access inside a container exposes every secret mounted into that container.

## Cross-platform comparison protocol

Keep this matrix for the same CLI, host, and identity:

| Dimension | Restricted run | Comparator | Interpretation |
| --- | --- | --- | --- |
| Binary/version | Same/different | Same/different | Resolve runtime mismatch first |
| Config root | Same/different | Same/different | Different roots are different auth contexts |
| Credential backend | Keychain/Credential Manager/file/helper | Same/different | A backend change is not a pure sandbox comparator |
| Local retrieval | Pass/fail | Pass/fail | Isolates credential-source access |
| Network identity | Pass/fail | Pass/fail | Adds service reachability and authentication |
| Refresh persistence | Exercised/not exercised | Exercised/not exercised | Required before claiming durable repair |
| Remote scope/ACL | Pass/fail | Pass/fail | Independent of local OS backend |

Change one dimension at a time. If the comparator also changes OS, shell,
config root, profile, token source, and network, it cannot identify a primary
cause.

## Official sources

- Apple Keychain Access overview:
  <https://support.apple.com/guide/keychain-access/what-is-keychain-access-kyca1083/mac>
- Apple Keychain Services:
  <https://developer.apple.com/documentation/security/keychain-services>
- Microsoft Credentials Management:
  <https://learn.microsoft.com/en-us/windows/win32/secauthn/credentials-management>
- Microsoft DPAPI `CryptProtectData`:
  <https://learn.microsoft.com/en-us/windows/win32/api/dpapi/nf-dpapi-cryptprotectdata>
- Microsoft named-pipe security:
  <https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipe-security-and-access-rights>
- OpenAI Windows sandbox:
  <https://learn.chatgpt.com/codex/windows/windows-sandbox>
- OpenAI sandbox overview:
  <https://learn.chatgpt.com/codex/sandboxing>
