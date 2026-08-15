# Codex permissions and sandbox reference

Use this reference when an authenticated CLI behaves differently inside Codex,
when selecting a comparator, or when proposing a persistent permission repair.
The facts below were checked against official OpenAI documentation on
2026-08-15; re-check current docs and runtime help before writing config because
permission profiles are beta.

## Contents

1. [Control layers](#control-layers)
2. [Two non-composable configuration systems](#two-non-composable-configuration-systems)
3. [Legacy sandbox settings](#legacy-sandbox-settings)
4. [Permission profiles](#permission-profiles)
5. [Credential-path and socket decisions](#credential-path-and-socket-decisions)
6. [Platform enforcement](#platform-enforcement)
7. [Diagnostic and repair protocol](#diagnostic-and-repair-protocol)
8. [Official sources](#official-sources)

## Control layers

Treat these controls as independent:

| Layer | Controls | Does not grant or prove |
| --- | --- | --- |
| Filesystem sandbox/profile | Which paths commands can read, write, or not access | Network, Keychain, Credential Manager, DPAPI, GUI, or remote scopes |
| Command network | Whether spawned commands can connect | App, MCP, hosted search, browser, or service authorization |
| Network proxy policy | Which destinations enabled command traffic may reach | Network access unless network is enabled separately |
| Unix-socket policy | Which local sockets commands may reach | That granting the socket is narrow or safe |
| Approval policy | When eligible boundary crossings prompt, auto-reject, or run without a prompt | A broader sandbox boundary |
| Approval reviewer | User or automatic reviewer for eligible approvals | New filesystem or network capabilities |
| Command rules | Allow, prompt, or forbid matching command prefixes | That every subcommand has the same side effects |
| Tool policy | Apps, connectors, MCP, browser, and Computer Use | Spawned shell-command access |
| Managed requirements | Organization-enforced upper bounds | Remote account scopes or resource ACLs |

The sandbox applies to spawned commands, including `git`, package managers,
credential helpers, and test runners. A CLI helper process inherits the same
technical boundary.

The active session or harness policy is authoritative. A user config file may
be overridden by CLI flags, named config profiles, managed requirements, the
desktop permissions selector, or a session that started before a config change.

## Two non-composable configuration systems

Codex currently exposes two local permission systems:

1. Legacy `sandbox_mode` plus `[sandbox_workspace_write]`.
2. Beta `default_permissions` plus `[permissions.<name>]`.

Do not combine them. If `sandbox_mode` appears in a loaded config layer, the
user passes `--sandbox`, or a selected Codex config profile sets
`sandbox_mode`, Codex uses the legacy system instead of
`default_permissions`. Remove older settings before expecting a permission
profile to control the run.

`approval_policy` is orthogonal and can accompany either system. In particular:

```text
restrictive sandbox + never = fail without prompting
full access + never         = broad access without prompting
```

Never describe `never` by itself as full access.

## Legacy sandbox settings

Common modes:

| Mode | Local behavior |
| --- | --- |
| `read-only` | Inspect files; edits and command execution require approval or fail under non-interactive policy |
| `workspace-write` | Read and write normal workspace paths; network is off unless enabled; protected subpaths remain read-only |
| `danger-full-access` | Removes local sandbox restrictions; use only when that broad boundary is intentional |

The relevant legacy shape is:

```toml
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
network_access = true
writable_roots = ["/path/to/reviewed-cli-state"]
```

Use `writable_roots` only when the CLI must refresh or atomically replace local
state. If the CLI only reads a fixed credential, a persistent write grant is
broader than necessary; prefer an exact command escalation or the newer profile
system when available.

In default `workspace-write`, these paths remain recursively protected as
read-only inside each writable root:

- `.git`, including the resolved Git directory when `.git` is a pointer file;
- `.agents`;
- `.codex`.

Therefore, “the repository is writable” does not prove Git metadata, local
agent config, or Codex config is writable.

## Permission profiles

Permission profiles are beta and support explicit filesystem, network, domain,
and Unix-socket policy. Built-ins include `:read-only`, `:workspace`, and
`:danger-full-access`. A custom profile can extend `:read-only`, `:workspace`,
or another custom profile; it cannot extend `:danger-full-access`.

A narrowly scoped authenticated-CLI profile can look like this:

```toml
approval_policy = "on-request"
default_permissions = "auth-cli"

[features]
network_proxy = true

[permissions.auth-cli]
description = "Workspace editing plus reviewed CLI state and service access."
extends = ":workspace"

[permissions.auth-cli.filesystem]
"/path/to/reviewed-cli-state" = "write"

[permissions.auth-cli.filesystem.":workspace_roots"]
"**/*.env" = "deny"

[permissions.auth-cli.network]
enabled = true

[permissions.auth-cli.network.domains]
"api.example.com" = "allow"
```

Important semantics:

- `read`, `write`, and `deny` control filesystem access. A more specific rule
  can narrow a broader one; use deny rules for credential-bearing workspace
  files that commands should not read.
- `network.enabled = true` grants command network access but does not activate
  destination filtering.
- `features.network_proxy = true` activates enforcement of profile domain
  rules. Network on with proxy off means direct, unrestricted outbound access.
- With the proxy active and at least one allow rule, use exact service hosts or
  carefully reviewed wildcard domains. Deny rules override allow rules.
- `network.allow_local_binding` is separate. Browser callback flows that bind
  localhost may fail even when outbound service domains are allowed.
- `network.unix_sockets` is an explicit allowlist for supported local
  integrations. A socket grant can be far broader than a domain grant.

## Credential-path and socket decisions

Classify the CLI's state before writing a profile:

| Dependency | Typical minimum | Caveat |
| --- | --- | --- |
| Fixed token/config file | `read` on the exact file or narrow parent | Parent traversal and helper files may still be needed |
| OAuth refresh with atomic replace | `write` on the containing directory | Write allows creation, rename, replacement, and deletion inside that subtree |
| Cache that is optional | No grant, or redirect cache to a reviewed temporary root | Do not confuse cache failure with credential failure |
| macOS Keychain / Windows Credential Manager | Not representable as a normal file rule | Requires OS service access, supported CLI fallback, or a comparator outside the sandbox |
| SSH/GPG agent | Exact socket plus any required public config reads | Agent socket use can authorize signatures without exposing the private key |
| Docker daemon | Exact socket where supported | Docker documents daemon control as trusted-user, potentially privileged access |
| Browser/device OAuth | Outbound domains; local binding only if the flow needs it | Device-code flows often avoid local callback binding |

Do not add a broad credential directory merely because its path is known. First
prove whether the failing operation needs read, write, helper execution, OS
service IPC, or network.

## Platform enforcement

### macOS

Codex uses the built-in Seatbelt framework. Filesystem permission alone does
not imply access to Keychain services, GUI prompts, desktop-app IPC, or every
Unix socket. Use the macOS branch in
[platform-credential-backends.md](platform-credential-backends.md).

### Native Windows

Codex provides:

- preferred `elevated` sandbox: dedicated lower-privilege sandbox users,
  filesystem boundaries, firewall rules, and local policy;
- fallback `unelevated` sandbox: restricted token, ACL-based filesystem
  boundaries, and weaker environment-level network isolation.

The current-session `/sandbox-add-read-dir C:\absolute\path` command adds read
access only. It does not add write access for token refresh, grant Credential
Manager/DPAPI access, or allow named pipes.

### Linux and WSL2

Codex uses the Linux sandbox implementation and currently documents
`bubblewrap` as a prerequisite. Secret Service, D-Bus, agent sockets, XDG
config roots, and WSL-to-Windows credential boundaries remain separate
dependencies.

## Diagnostic and repair protocol

1. Record the active runtime permission boundary; do not infer it solely from
   `~/.codex/config.toml`.
2. Run the same non-mutating CLI command under the restrictive boundary and one
   approved comparator.
3. Change one dimension: filesystem, network, local binding, OS credential
   service, or socket.
4. Prefer one exact approval for a one-off command.
5. Use a named permission profile only for a repeated, stable workflow whose
   paths and destinations are understood.
6. Treat `danger-full-access` as a deliberate broad trust choice, not a generic
   auth fix.
7. Restart or create a new session when the runtime does not hot-apply config;
   then re-read the active boundary rather than assuming the file was consumed.
8. Re-run the original command and an identity readback. Exercise refresh
   persistence only when authorized and necessary.

## Official sources

- <https://learn.chatgpt.com/codex/sandboxing>
- <https://learn.chatgpt.com/codex/agent-approvals-security>
- <https://learn.chatgpt.com/codex/permissions>
- <https://learn.chatgpt.com/docs/config-file/config-reference>
- <https://learn.chatgpt.com/codex/windows/windows-sandbox>

Do not freeze current beta syntax into a repair without re-reading these pages
and the installed Codex runtime help.
