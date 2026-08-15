---
name: dev-cli-auth-diagnosis
description: Use when gh, hf, lark-cli, Git/SSH, or another authenticated CLI works in one shell or host but reports missing credentials, cannot refresh or persist authentication, cannot reach its service, or behaves differently inside Codex or across permission profiles, macOS, Windows, WSL, containers, or CI. Diagnose sandbox, OS credential backend, persistence, network, execution-context, authentication, scope, and resource-ACL failures before login or credential changes; do not use for routine first-time login with no environment discrepancy.
metadata:
  version: "0.1"
  updated: "2026-08-15"
---

# CLI authentication diagnosis

Diagnose the failing boundary before changing credentials. Keep the investigation
read-only unless the user separately authorizes an authentication, storage, or
remote-state mutation.

Always read
[references/authenticated-cli-sandbox-guide.md](references/authenticated-cli-sandbox-guide.md)
before selecting probes, assigning a failure class, or proposing a repair.
Then load only the reference needed for the current branch:

- Read
  [references/codex-permissions-and-sandbox.md](references/codex-permissions-and-sandbox.md)
  when the task involves Codex permissions, sandbox modes, approval behavior,
  filesystem roots, network policy, or Unix sockets.
- Read [references/cli-adapters.md](references/cli-adapters.md) for `gh`, `hf`,
  `lark-cli`, or when transferring their credential patterns to another CLI.
- Read
  [references/platform-credential-backends.md](references/platform-credential-backends.md)
  for macOS Keychain, Windows Credential Manager or DPAPI, named pipes, agent
  sockets, WSL separation, browser/device login, or cross-platform differences.

## Workflow

1. Freeze the comparison.
   - Record the CLI, host or service, working directory, active Codex permission
     boundary, operating system, and the exact non-mutating command that succeeds
     and fails.
   - Preserve explicit profile, account, tenant, app, and identity selectors.
   - Do not translate a context mismatch into a request to log in again.

2. Route to the relevant knowledge branch.
   - Use the practical adapter for `gh`, `hf`, or `lark-cli`; do not flatten
     their different credential models into one generic token recipe.
   - Use the Codex reference for permission-system selection and the platform
     reference for OS credential services. A filesystem rule is not a Keychain,
     Credential Manager, DPAPI, GUI, or socket grant.

3. Establish the local execution boundary.
   - Distinguish filesystem access, command network access, approval policy,
     approval reviewer, command rules, and tool-specific controls.
   - Treat the current harness or session policy as authoritative for the run;
     local `config.toml` is only one input.
   - Check current CLI help before relying on a remembered flag or storage path.

4. Map the credential chain without exposing it.
   - Identify environment overrides, OS keyrings, credential helpers, token
     files, agent or daemon sockets, config roots, caches, and refresh storage.
   - Report only presence, source kind, ownership, and permissions needed for
     diagnosis. Never print token, cookie, private key, refresh token, or secret
     content.

5. Separate safe probes.
   - Test binary discovery and version first.
   - Test local credential retrieval without network and redirect secret-bearing
     stdout to a sink.
   - Test service reachability separately from authenticated identity.
   - Account for read-oriented remote commands that may still refresh tokens or
     write local caches.

6. Use a controlled comparator only when needed.
   - Repeat the same non-mutating command under the restrictive profile and one
     user-approved escalation or unrestricted comparator.
   - Change one boundary at a time. Do not combine re-login, network changes,
     profile switching, and full access in one experiment.
   - Do not use a destructive or externally visible command as an auth probe.

7. Assign one primary failure class from the reference guide.
   - Keep local credential access, credential persistence, network, execution
     context, authentication, authorization, and resource ACL distinct.
   - If the evidence supports more than one layer, name the first blocking layer
     and list the later layers as unverified.

8. Recommend the least-broad repair.
   - Prefer an exact command escalation, a tool-supported credential backend,
     or a narrowly scoped permission/profile correction.
   - Treat login, logout, token rotation, credential-store migration, permanent
     writable roots, and organization permission changes as separate mutations
     requiring explicit authorization.
   - Do not prescribe permanent full access merely because it makes the probe
     pass.

9. Verify with independent readback.
   - Re-run the original failing command under the intended final boundary.
   - Verify the remote identity when network access is expected.
   - Confirm refresh or cache persistence only when that path was exercised.
   - State which layers remain untested.

## Stop conditions

Stop and ask for a bounded decision when:

- the next probe may print or export a secret;
- the selected profile, account, app, tenant, or user/bot identity is ambiguous;
- the next step changes login state, credential storage, scopes, permissions, or
  remote data;
- only a broad permanent exception appears possible and a narrower comparator
  has not been tried;
- the live environment is production and the requested action is not an
  explicitly authorized read.

## Output

Return:

1. observed sandbox and approval boundary;
2. CLI and credential-source chain, with all values redacted;
3. probes run and their sandboxed versus comparator results;
4. primary failure class and supporting evidence;
5. minimal repair, authorization needed, and tradeoff;
6. verification performed and remaining uncertainty.

## Completion criteria

Complete only when the failure is classified with direct evidence and the
original command either succeeds under the intended boundary or is left with a
specific, user-owned authorization or external-state requirement. A successful
version command, readable config file, or unrestricted comparator alone is not
end-to-end authentication proof.
