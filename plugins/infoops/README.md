# InfoOps

InfoOps is an installable Codex plugin and OpenClaw-compatible standalone skill
for turning workstream signals into structured operational awareness and action
priorities.

It packages the `infoops` skill as a standalone marketplace plugin. It is not
installed into a production runtime by this repository change, and it is not
merged into the Codex Next all-in-one plugin.

## Compatibility

- Codex: install through this repository marketplace and load the bundled
  `skills/infoops/` directory from `.codex-plugin/plugin.json`.
- OpenClaw bundle: install `plugins/infoops/` as a Codex-compatible bundle.
  OpenClaw detects `.codex-plugin/plugin.json` and maps the bundled `skills/`
  content into normal OpenClaw skills.
- OpenClaw standalone skill: use `plugins/infoops/skills/infoops/` directly.
  The standalone skill surface is `SKILL.md` plus `references/`.
- Runtime files such as `workspace/infoops/` are created only when the skill is
  invoked; they are not shipped as plugin state.

## Prerequisites

- `lark-cli` is required only for Feishu/Lark data collection.
- Before running Feishu/Lark collection, use `lark-cli skills read lark-shared`
  and the relevant embedded `lark-cli` skill guide.
- These requirements are documented in the skill body instead of declared in
  `plugin.json`, because the Codex plugin manifest schema does not accept
  external dependency declarations.

## Included Skill

- `infoops`: maintain a `workspace/infoops/` operating system for signal
  collection, source profiles, thread tracking, PULSE refreshes, and action
  prioritization.

## Install

This plugin is published through the repository marketplace:

```bash
codex plugin marketplace add /path/to/Codex-is-all-you-need
codex plugin add infoops@codex-is-all-you-need
```

After installation, invoke:

```text
$infoops:infoops
```

For OpenClaw-style use, copy or reference:

```text
plugins/infoops/skills/infoops/
```

Or install the plugin directory as an OpenClaw-compatible Codex bundle:

```bash
openclaw plugins install ./plugins/infoops
```

## Validate

From the repository root:

```bash
python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py \
  plugins/infoops
```
