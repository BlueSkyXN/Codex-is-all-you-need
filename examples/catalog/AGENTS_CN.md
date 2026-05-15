# Catalog 目录指南

[English](AGENTS.md) | 中文

这些规则适用于 `examples/catalog/` 及其所有下级 catalog 分组。

## 目录用途

本目录是从私有 Codex preset catalog 抽取并脱敏后的公开安全 source catalog。内容应保持通用、可复用，不包含机器特定信息或业务私有细节。

## 目录结构

每个分组都遵循同一结构：

```text
<group>/
  agents/*.toml
  skills/<skill-name>/SKILL.md
```

当前分组包括 `common`、`product-engineering`、`dev`、`data`、`office`、`research`。Agent 文件使用 snake_case，例如 `dev_python_engineer.toml`。Skill 目录使用 kebab-case，例如 `python-quality/`。

## Agent TOML 规则

- Agent 角色应保持通用和可复用。
- `description`、`developer_instructions`、`nickname_candidates` 只能包含可公开内容。
- 默认不设置模型策略字段；agent 应继承 runtime 配置，除非有明确理由单独覆盖。
- `nickname_candidates` 最多保留一个候选名。
- Recommended skills 只能引用本 catalog 中的公开 skill，或描述为当前 runtime 可见的通用 workflow。

## Skill 规则

- 每个 skill 目录必须包含 `SKILL.md`。
- 如有 frontmatter，应保持简洁，并包含 `name` 和 `description`。
- 不要加入私有脚本、专有模板、私有示例，或指向私有 skill library 的 symlink。
- 示例内容应保持抽象，除非确认可以公开。

## 验证方式

修改 catalog 后，至少运行：

```bash
python3 - <<'PY'
from pathlib import Path
import tomllib

root = Path("examples/catalog")
for path in root.glob("*/agents/*.toml"):
    tomllib.loads(path.read_text())
for path in root.glob("*/skills/*"):
    if path.name.startswith("."):
        continue
    if not (path / "SKILL.md").is_file():
        raise SystemExit(f"missing SKILL.md: {path}")
print("catalog structure ok")
PY
git diff --check -- examples/catalog
```

发布边界变更需对照 `PUBLIC-SUBSET.md`。

## 公开安全边界

不要提交私有 symlink skills、机器路径、生成的 dashboard 状态、本地 suite 状态、未公开的私有 skill 名称、凭证，或业务特定流程细节。
