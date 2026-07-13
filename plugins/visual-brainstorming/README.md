# Visual Brainstorming

Visual Brainstorming is an installable Codex plugin for comparing genuinely
different visual alternatives in a local browser and recording the user's
selection as structured project-local events.

It is intentionally distributed as a standalone plugin rather than bundled
into Codex Next. Installing it is an explicit opt-in to a workflow that starts
a local HTTP companion, opens a browser, and writes temporary session data
under the current project.

## Included Skill

- `visual-brainstorming`: compare two to four UI, layout, architecture,
  data-flow, process, state, or model-routing alternatives when seeing the
  options materially reduces ambiguity.

The skill asks for consent before an implicit invocation opens a browser. It
falls back to Mermaid, ASCII, a static image, or structured text when the local
browser cannot reach the companion.

The packaged release is `2.4.0`. It is not only a directory move: the release
adds the standalone marketplace surface plus runtime locking, version-aware
reuse, bounded events and logs, per-screen bridge binding, exact-plan pruning,
remote URL validation, and live runtime path checks.

## Runtime and Security Boundary

- Python 3.9 or newer; standard library only.
- Binds to `127.0.0.1` by default.
- Uses a random session key carried in the initial URL fragment, origin-scoped
  `sessionStorage`, path capabilities, Host and Origin checks, CSP, a sandboxed
  iframe, bounded requests, and symlink/path traversal rejection. Cookies are
  not accepted as session credentials.
- Writes runtime state to `<project>/.visual-brainstorming/`; this directory
  receives its own deny-all `.gitignore` and should stay untracked.
- Routine HTTP access logs are disabled so control-query and capability keys
  are not persisted; diagnostic logging is redacted, mode `0600` where
  supported, and capped at 256 KiB per session.
- Remote binding is an expert-only escape hatch. It uses plain HTTP and must
  not be enabled automatically or exposed to an untrusted network. Prefer a
  trusted tunnel or local execution. A remote browser URL must use a literal
  loopback/private/link-local address actually assigned to the Agent host.

## Install

Add this repository marketplace, then install the standalone plugin:

```bash
codex plugin marketplace add https://github.com/BlueSkyXN/Codex-is-all-you-need.git
codex plugin add visual-brainstorming@codex-is-all-you-need
```

### Existing sparse marketplace installs

Codex Git marketplaces use a persistent sparse checkout. If this marketplace
was already added with an explicit sparse path list, `marketplace upgrade`
does not add a newly published plugin directory to that list. Remove and
re-add the marketplace while preserving every path you still use:

```bash
codex plugin marketplace remove codex-is-all-you-need
codex plugin marketplace add https://github.com/BlueSkyXN/Codex-is-all-you-need.git \
  --sparse .agents/plugins \
  --sparse plugins/codex-next \
  --sparse plugins/github-publish-zip \
  --sparse plugins/infoops \
  --sparse plugins/expression-fixer \
  --sparse plugins/visual-brainstorming
codex plugin add visual-brainstorming@codex-is-all-you-need
```

Omit plugin paths that were not part of the previous installation; the
important requirement is to preserve the existing sparse set and add
`plugins/visual-brainstorming`.

Claude Code Git marketplaces can also use persistent sparse checkout. Re-add
the marketplace at the same scope while preserving its existing paths and
adding the new plugin directory (`user` is only the example scope below):

```bash
claude plugin marketplace remove codex-is-all-you-need --scope user
claude plugin marketplace add https://github.com/BlueSkyXN/Codex-is-all-you-need.git \
  --scope user \
  --sparse .claude-plugin \
    plugins/codex-next \
    plugins/github-publish-zip \
    plugins/infoops \
    plugins/expression-fixer \
    plugins/visual-brainstorming
claude plugin install visual-brainstorming@codex-is-all-you-need --scope user
```

For local development, add the checked-out repository root instead:

```bash
codex plugin marketplace add /path/to/Codex-is-all-you-need
```

Invoke the skill explicitly with:

```text
$visual-brainstorming:visual-brainstorming
```

For Claude Code, add the repository marketplace and install the same standalone
plugin:

```bash
claude plugin marketplace add https://github.com/BlueSkyXN/Codex-is-all-you-need.git
claude plugin install visual-brainstorming@codex-is-all-you-need
```

## Validate

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_visual_brainstorming -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  plugins/visual-brainstorming/skills/visual-brainstorming
python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py \
  plugins/visual-brainstorming
claude plugin validate --strict plugins/visual-brainstorming
claude plugin validate --strict .
node --check plugins/visual-brainstorming/skills/visual-brainstorming/assets/browser-shell.js
node --check plugins/visual-brainstorming/skills/visual-brainstorming/assets/injected-helper.js
git diff --check -- plugins/visual-brainstorming \
  .agents/plugins/marketplace.json .claude-plugin/marketplace.json \
  tests/test_visual_brainstorming.py
```

The browser acceptance checklist lives in
`skills/visual-brainstorming/references/EVALUATION.md`.

## License and Attribution

This plugin is distributed under the MIT License. The implementation is
independent; its conceptual references and attribution boundary are documented
in `NOTICE.md` and the bundled skill's `references/SOURCES.md`.
