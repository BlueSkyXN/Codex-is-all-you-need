# Authenticated CLI diagnosis guide

Use this core reference for every diagnosis. It defines the failure model,
evidence protocol, and repair boundary. Load the sibling references only for the
relevant CLI, Codex permission system, or operating system.

## Contents

1. [Failure model](#failure-model)
2. [Failure classes](#failure-classes)
3. [Evidence protocol](#evidence-protocol)
4. [Controlled comparator](#controlled-comparator)
5. [Repair selection](#repair-selection)
6. [Transfer patterns](#transfer-patterns)
7. [Reporting template](#reporting-template)

## Failure model

An authenticated CLI is usable only when every required gate is open:

```text
binary and runtime available
  -> intended config root and profile selected
  -> credential source readable
  -> refreshed or rotated state persistable
  -> service network reachable
  -> intended account/app/tenant/identity selected
  -> authentication accepted
  -> remote scope and resource ACL sufficient
```

The first failed gate is the primary diagnosis. Do not skip ahead to login or
permission changes.

Keep four meanings of “read-only” separate:

- A remote read can refresh a token or update a local cache, SQLite DB, lock,
  last-used profile, or credential file.
- A local status command can read sensitive credential material without making
  a remote change.
- A CLI can read an existing token but fail when refresh requires an atomic
  temporary-file write and rename in the parent directory.
- A successful identity read proves the current credential, network, and remote
  acceptance for that call; it does not prove future refresh persistence.

## Failure classes

Assign one primary class and preserve untested later gates.

| Class | Direct evidence | Do not misclassify as |
| --- | --- | --- |
| `binary_unavailable` | Executable or required runtime is absent from the active `PATH` | Authentication failure |
| `config_context_mismatch` | A different config root, host, profile, account, app, tenant, or user/bot identity is selected | Missing login |
| `credential_source_unreachable` | Keyring, helper, token file, agent, named pipe, or socket works in the comparator but cannot be read in the target boundary | Invalid token |
| `credential_persistence_blocked` | Refresh or login obtains state but cannot create, lock, replace, rename, or update its store | OAuth rejection |
| `network_unreachable` | DNS, proxy, TLS, domain policy, local binding, named pipe, or Unix socket fails before an authenticated response | Invalid credentials |
| `authentication_invalid` | The intended service rejects the intended credential during online verification | Sandbox failure |
| `authorization_missing` | Authentication succeeds but the required remote scope, role, or API permission is absent | Credential corruption |
| `resource_acl_missing` | Identity and scope are valid but the specific repository, model, document, project, or resource is not shared | Missing global scope |
| `capability_unavailable` | The installed CLI version or distribution lacks the requested command or backend | Permission failure |

Timeouts and generic connection errors are not authentication evidence. A
successful unrestricted comparator proves a boundary dependency, but does not
identify whether the missing capability was keyring, filesystem, network,
local binding, named pipe, or socket access.

## Evidence protocol

### 1. Freeze the target

Record without secrets:

- exact executable and version;
- operating system and shell/runtime boundary;
- service host and working directory;
- current permission profile or sandbox mode;
- account/profile/app/tenant/identity selector;
- exact command whose results differ;
- whether the command is local-only, remote read, remote write, or may refresh
  local state.

Do not silently change any selector between probes.

### 2. Inspect current help

Prefer current runtime truth over remembered syntax:

```bash
command -v <cli>
<cli> --version
<cli> auth --help
```

Use the CLI's actual equivalent if it has no `auth` command. Do not install,
upgrade, reconfigure `PATH`, or start a login shell merely to make the binary
appear unless the user authorizes that mutation.

### 3. Map the credential source without content

Safe evidence includes:

- whether a credential environment variable is set, never its value;
- whether an OS keyring, credential helper, or password-manager integration is
  selected;
- whether a credential file exists, plus ownership and mode when relevant;
- whether a required agent, daemon, Unix socket, or named pipe is reachable;
- whether the containing config directory is writable when refresh persistence
  is expected.

Avoid:

- `env`, `set`, PowerShell environment enumeration, or shell tracing;
- `--show-token`, token-list output, or config dumps that may contain secrets;
- hashes or token prefixes that are unnecessary for classification;
- copying credentials into a repository or workspace for testing;
- placing a token in command arguments, where process listings or logs may
  retain it.

If a command returns a credential on stdout, redirect it to a sink and report
only the exit code:

```bash
<credential-retrieval-command> >/dev/null
```

### 4. Split combined status checks

Use distinct probes for:

1. binary and config-context selection;
2. local credential retrieval without network;
3. low-risk service reachability;
4. authenticated identity readback;
5. refresh or cache persistence, only when naturally exercised or explicitly
   approved.

Do not infer all five results from a single `status` command. Some CLIs label a
command “status” even though it verifies credentials online or updates local
state.

### 5. Keep logs redacted

Capture command, exit code, error class, and the minimum non-secret stderr.
Remove credentials, authorization headers, cookies, OAuth codes, signed URLs,
private repository names, personal identities, and internal hosts before using
logs as durable evidence.

## Controlled comparator

When the restrictive run is inconclusive, repeat the same non-mutating command
with one changed boundary:

- a different built-in Codex permission profile;
- one exact sandbox escalation;
- an interactive Terminal or PowerShell session under the same user;
- an externally isolated container chosen as the outer security boundary.

Keep the executable, arguments, environment selectors, host, and identity the
same. Never use login, logout, token creation, repository push, message send,
document update, deployment, or resource deletion as the comparator.

Interpret `approval_policy = "never"` correctly: it disables approval prompts;
it does not make a restrictive sandbox permissive. Full access is a separate
boundary decision. Read
[codex-permissions-and-sandbox.md](codex-permissions-and-sandbox.md) before
changing either system.

## Repair selection

| Primary class | Least-broad repair | Separate authorization |
| --- | --- | --- |
| `binary_unavailable` | Use the intended non-interactive `PATH` or explicit executable | Install, upgrade, or runtime ownership change |
| `config_context_mismatch` | Re-select the already intended config root/profile/account/app/identity | Create profile, change default, or bind a new account |
| `credential_source_unreachable` | Exact command escalation or supported backend for that CLI and OS | Keyring-to-file migration, password-manager unlock, or socket grant |
| `credential_persistence_blocked` | Exact refresh/login escalation or narrowly reviewed directory write | Permanent writable credential root or storage redesign |
| `network_unreachable` | Enable command network or allow exact service destinations through the active proxy | Broad internet, private-network, local-binding, or daemon-socket access |
| `authentication_invalid` | Re-authenticate with the current official flow | Logout, token rotation, revocation, or new scopes |
| `authorization_missing` | Grant the narrow required remote scope or role | Organization or administrator change |
| `resource_acl_missing` | Share only the intended resource with the intended identity | Bulk or inherited permission change |
| `capability_unavailable` | Use a supported version or documented alternate command | Upgrade, install, or browser/UI fallback |

Do not make permanent full access the default repair. Do not inject a long-lived
token into the whole Codex environment merely to bypass a keyring. Do not make
an entire credential directory writable without explaining that every command
inside that sandbox can then modify its contents.

A tool-supported credential backend can be appropriate, but changing from an
OS keyring to a local file is a security and persistence decision. Read current
help, report path and rollback semantics without secret values, and obtain
explicit authorization before running the migration.

## Transfer patterns

Use these patterns only after loading the primary adapter or platform reference:

| CLI family | Extra dependency to isolate |
| --- | --- |
| Git over HTTPS | Git credential helper may be separate from a service CLI's API authentication |
| Git over SSH | `SSH_AUTH_SOCK`, private-key paths, hardware-key confirmation, and `known_hosts` writes |
| Package managers | Project-controlled config, registry network, environment-token inheritance, and lifecycle scripts |
| Cloud CLIs | SSO/device login, token caches, workload identity, selected account/project/subscription, and remote IAM |
| Daemon-backed CLIs | Unix socket or Windows named pipe may confer broader host control than the CLI operation suggests |
| Password managers | Desktop IPC, biometric/UI prompt, session token, and vault ACL are separate gates |

## Reporting template

```markdown
## CLI authentication diagnosis

- CLI/runtime: <binary and version>
- Platform: <macOS/Windows/WSL/Linux/CI>
- Target context: <host/profile/account/app/identity, redacted>
- Active boundary: <filesystem, network, approval, reviewer>
- Credential source: <environment/keyring/file/helper/agent, values omitted>
- Restricted result: <command and outcome>
- Comparator result: <same command and one changed boundary>
- Primary class: <failure_class>
- Evidence: <direct observations>
- Minimal repair: <narrowest change>
- Authorization needed: <none or exact mutation>
- Verification: <original command and identity readback>
- Remaining uncertainty: <untested layers>
```

Complete only when the primary failure is supported by direct evidence. A
successful version command, readable config file, local token retrieval, or
unrestricted comparator alone is not end-to-end authentication proof.
