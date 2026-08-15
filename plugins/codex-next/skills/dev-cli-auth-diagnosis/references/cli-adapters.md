# Authenticated CLI practical adapters

Use this reference for `gh`, `hf`, and `lark-cli`. It captures the practical
differences that a generic “set a token variable” rule would erase. Commands
were checked against locally installed versions and official documentation on
2026-08-15; always re-read current `--help` before execution.

## Contents

1. [Adapter contract](#adapter-contract)
2. [GitHub CLI](#github-cli-gh)
3. [Hugging Face CLI](#hugging-face-cli-hf)
4. [Lark and Feishu CLI](#lark-and-feishu-cli-lark-cli)
5. [Transfer to other CLIs](#transfer-to-other-clis)
6. [Official sources](#official-sources)

## Adapter contract

For each CLI, determine:

1. current binary and command surface;
2. config root and selected profile/host/account/app/identity;
3. credential-source precedence;
4. local retrieval probe that does not print the credential;
5. online identity probe;
6. whether ordinary reads can refresh or persist state;
7. official headless, device-code, config-redirection, helper, or fallback
   mechanisms;
8. which mechanisms are mutations or security downgrades.

Never assume that two CLIs on the same service share credentials. Never assume
that a CLI's API authentication also configures Git HTTPS, Git SSH, package
registry, or browser authentication.

## GitHub CLI (`gh`)

### Credential model

`gh auth login` prefers the system credential store. Official help states that
if no credential store is found or it cannot be used, `gh` can fall back to a
plain-text config file. That fallback is supported, but it is a security
downgrade rather than the default repair.

For `github.com`, environment precedence includes `GH_TOKEN` before
`GITHUB_TOKEN`. Enterprise hosts use the corresponding enterprise variables.
`GH_CONFIG_DIR` redirects GitHub CLI configuration files. Environment tokens
are intended for headless automation, but every child process that inherits the
variable can potentially read it.

Git operations are separate:

- `gh api` uses GitHub CLI authentication;
- Git HTTPS uses a Git credential helper;
- Git SSH uses an SSH key or `ssh-agent`;
- `gh auth setup-git` mutates Git config so Git HTTPS can use `gh` as a helper.

Do not treat `gh auth status` success as proof that `git push` over SSH works.

### Safe probe sequence

For an already selected host:

```bash
gh --version
gh auth token --hostname <host> >/dev/null
gh auth status --active --hostname <host>
gh api --hostname <host> user --jq .login
```

Interpret each step separately:

- `gh auth token ... >/dev/null` tests local credential retrieval. Without the
  redirection it prints the token and must not be run in an agent-visible log.
- `gh auth status` verifies authentication state online. It is not a purely
  local credential probe.
- Current `gh` help states that `auth status --json` exits zero even when an
  account has authentication issues unless there is a fatal error. Inspect the
  structured status rather than trusting only the exit code.
- `gh api ... user` verifies the selected remote identity and adds network and
  service acceptance to the evidence.

### Repairs and authorization boundaries

| Mechanism | Appropriate use | Boundary |
| --- | --- | --- |
| Exact command approval | One-off access to an existing system credential | No persistent auth mutation |
| Per-command `GH_TOKEN` | Controlled headless operation with a scoped token | Do not export globally or log the value |
| `GH_CONFIG_DIR` | Isolate or redirect CLI config to a reviewed private root | Does not make Keychain work and may create a second login context |
| `gh auth login --with-token` | Explicitly authorized login from stdin | Writes authentication state |
| `gh auth setup-git` | Explicitly authorize Git config to use `gh` as helper | Changes Git credential behavior |
| `--insecure-storage` | User explicitly accepts plain-text storage | Never recommend as the default sandbox fix |

Do not run `auth logout`, switch active accounts, overwrite config roots, or
re-login until the target host and account are anchored and the user authorizes
the mutation.

## Hugging Face CLI (`hf`)

### Credential model

Hugging Face uses file-based state rather than requiring the macOS Keychain by
default:

- `HF_TOKEN` overrides the token stored on the machine;
- `HF_HOME` redirects Hugging Face local state and caches;
- `HF_TOKEN_PATH` selects the token file, defaulting under `HF_HOME`;
- `hf auth login --add-to-git-credential` optionally adds Git credential-helper
  state for direct Git operations.

Do not assume a Hugging Face user access token has OAuth refresh semantics. A
failure to update a cache is not automatically token-refresh failure. Likewise,
a private or gated model/repository denial can be a resource ACL or terms-
acceptance issue even when `whoami` succeeds.

### Safe probe sequence

```bash
hf --version
hf auth --help
hf auth token >/dev/null
hf auth whoami --format json
```

Interpretation:

- `hf auth token >/dev/null` tests whether the currently selected token can be
  retrieved locally without disclosing it.
- `hf auth whoami` adds network and service identity verification.
- Check only whether `HF_TOKEN`, `HF_HOME`, and `HF_TOKEN_PATH` are present or
  selected. Never print their values or dump the Hugging Face environment.
- Separate Hub authentication from Git credential-helper configuration and
  from local model/cache writes.

### Repairs and authorization boundaries

| Mechanism | Appropriate use | Boundary |
| --- | --- | --- |
| Exact path read | Existing token file is outside the sandbox | Read does not allow login/switch/logout persistence |
| Reviewed `HF_HOME` or `HF_TOKEN_PATH` | Deliberately isolate state for a workflow | Avoid putting token files in a public or repository-controlled path |
| Per-command `HF_TOKEN` | Controlled headless operation | Package scripts and other children can inherit it |
| `hf auth login --token` | Explicitly authorized login | Writes token state; pass securely, not as a logged literal |
| `--add-to-git-credential` | Direct Git use is explicitly required | Mutates a second credential system |

Do not copy a token into the workspace to make sandbox access easy. A readable
workspace secret is visible to every command allowed to read that workspace.

## Lark and Feishu CLI (`lark-cli`)

### Credential and execution model

`lark-cli` has more routing dimensions than a single-account token CLI:

- config root;
- named profile;
- bound App;
- user versus bot identity selected with `--as`;
- local credential/master-key backend;
- user OAuth or bot token validity and scope;
- resource sharing/ACL.

The same binary and profile name can still resolve a different App or identity
when the config root differs. `--profile` selects a profile inside the current
config root; it does not switch the App across config roots. Keep `--as
user|bot` explicit across a workflow.

### Safe probe sequence

Start from current help:

```bash
lark-cli --version
lark-cli profile list
lark-cli --profile <profile> doctor --offline
lark-cli --profile <profile> whoami --as <user|bot>
lark-cli --profile <profile> auth status --json --verify
```

Current locally checked `lark-cli 1.0.86` behavior matters:

- `doctor --offline` checks local config/auth shape without network;
- `whoami` already reports JSON and does not expose a `--json` flag in its
  current help;
- `auth status --verify` performs an online token verification;
- command help labels risk as `read`, `write`, or `high-risk-write`.

Re-check help before copying these flags to another version. Do not treat
`doctor --offline` as online identity proof or `auth status --verify` as proof
that a particular document/Base/chat is shared with that identity.

### macOS Keychain fallback

When direct evidence shows the macOS system Keychain is blocked, inspect:

```bash
lark-cli config keychain-downgrade --help
```

The current official CLI help states that this command:

- is the supported fix for environments such as the Codex sandbox;
- must be run once from an interactive macOS Terminal where Keychain is
  reachable;
- materializes the master key into a local fallback file and pins subsequent
  reads to it;
- preserves the Keychain entry as a cold backup;
- is idempotent;
- is expected to fail if run from inside the Keychain-blocked sandbox.

Do not run it automatically. The command intentionally changes the credential
storage boundary from an OS service to a file. It solves master-key retrieval,
not command network, App/profile/identity mismatch, OAuth scope, resource ACL,
or every refresh/config write.

### Failure interpretation

| Observation | Primary candidate |
| --- | --- |
| Offline doctor fails only in sandbox | Config path, master-key backend, file permission, or local helper |
| Offline doctor passes; verify cannot connect | Command network, DNS, proxy, or domain policy |
| Verify rejects intended user token | Authentication or refresh state |
| Bot works but user fails | Identity selector or user OAuth scope/token |
| User works but bot fails | App bot scope, bot enablement, or tenant policy |
| Identity succeeds but resource call is denied | API scope or resource ACL |
| Refresh succeeds remotely but later login disappears | Credential persistence or atomic-write failure |

Do not repair one row with another row's action. In particular, re-login does
not fix a wrong App/config root, and broader API scope does not share a resource.

## Transfer to other CLIs

The three primary adapters expose reusable patterns:

- `gh` pattern: OS credential store plus environment override plus separate Git
  transport credentials. `glab` and some registry CLIs are similar.
- `hf` pattern: file token plus configurable home/path plus optional Git helper.
  Package and model registries often resemble this.
- `lark-cli` pattern: encrypted local state plus App/profile/identity routing,
  refresh persistence, and resource ACL. Enterprise SaaS and cloud CLIs often
  resemble this.

For Docker, cloud providers, Kubernetes, password managers, or package
managers, use current official help to instantiate the same adapter contract;
do not expand this reference into an unverified command encyclopedia.

## Official sources

### GitHub CLI

- <https://cli.github.com/manual/gh_auth_login>
- <https://cli.github.com/manual/gh_auth_status>
- <https://cli.github.com/manual/gh_auth_setup-git>
- <https://cli.github.com/manual/gh_help_environment>

### Hugging Face

- <https://huggingface.co/docs/huggingface_hub/en/guides/cli>
- <https://huggingface.co/docs/huggingface_hub/en/package_reference/environment_variables>

### Lark/Feishu

Use the installed runtime's `--help` and embedded skills as the current
contract. In particular, inspect `config keychain-downgrade --help`, `whoami
--help`, `auth status --help`, and `doctor --help` before acting.
