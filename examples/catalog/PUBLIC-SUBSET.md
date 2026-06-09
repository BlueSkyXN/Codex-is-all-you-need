# Public Subset / 公开子集

This catalog is a sanitized public subset derived from a private production
Codex preset catalog.

本目录是从私有生产 Codex preset catalog 抽取并脱敏后的公开子集。

## Included / 已包含

```text
Agents:
  common                 6
  sdlc-manager          7
  dev                   14
  data                   5
  office                 5
  research               4

Skills:
  common                 1
  sdlc-manager          19
  dev                   20
  data                   4
  office                 5
  research               3
```

The included agents and skills are generic workflows for planning, Codex project
instructions, Architecture-first SDLC management, software development, data
analysis, office reporting, and research synthesis.

已包含内容都是通用工作流，覆盖任务规划、Codex 项目指令、架构先行 SDLC 管理、软件开发、数据分析、办公报告和研究综合。

## Excluded / 已排除

- Private symlinked skills.
- Machine-specific paths.
- Generated dashboard state.
- Local suite symlink state.
- Private templates, examples, scripts, or business process.
- Unpublished skill names used only in the private production catalog.

## Sanitization Rules / 脱敏规则

- Copy only real public-safe skill folders that contain `SKILL.md`.
- Do not copy skill directories that are symlinks to a private skill library.
- Keep agent roles when they are generic and reusable.
- Remove `Recommended skills` references to unpublished private skills.
- Omit model policy overrides by default so public examples inherit runtime configuration.
- Keep one `nickname_candidates` entry per agent.

## Maintenance / 维护

When refreshing this public subset, compare it against the private production
catalog, then run:

```bash
git diff --check
python3 - <<'PY'
from pathlib import Path
import tomllib
import yaml

root = Path("examples/catalog")
for path in root.glob("*/agents/*.toml"):
    tomllib.loads(path.read_text())
for path in root.glob("*/skills/*/SKILL.md"):
    text = path.read_text()
    if text.startswith("---"):
        _, frontmatter, _ = text.split("---", 2)
        yaml.safe_load(frontmatter)
print("public catalog ok")
PY
```
