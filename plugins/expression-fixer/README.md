# Expression Fixer

Expression Fixer is an installable Codex plugin for reviewing Chinese workplace
documents and making the wording sound natural, accurate, and presentation-safe.

It focuses on practical writing issues in weekly reports, project updates,
summaries, and work emails:

- meta-language leakage
- exposed source references
- awkward verb-object collocations
- repetitive sentence patterns
- unsuitable tone
- overloaded sentences
- overconfident claims

## Included Skill

- `expression-fixer`: review Chinese workplace writing, list expression issues,
  and return a minimally edited full version.

## Install

This plugin is published through the repository marketplace:

```bash
codex plugin marketplace add /path/to/Codex-is-all-you-need
codex plugin add expression-fixer@codex-is-all-you-need
```

After installation, invoke:

```text
$expression-fixer:expression-fixer
```

## Validate

From the repository root:

```bash
python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py \
  plugins/expression-fixer
```
