# Skill Versioning / Skill 版本治理

This repository gives every published skill an independent lifecycle version in
its `SKILL.md` frontmatter. Skill versions describe workflow behavior; plugin
manifest versions describe installable packages. They are related only when a
plugin release contains a real change to that skill.

本仓库为每个公开 skill 在 `SKILL.md` frontmatter 中维护独立生命周期版本。
Skill 版本描述工作流行为，plugin manifest 版本描述可安装软件包；只有某次插件
发布确实改变了该 skill 时，两者才会同时变化。

```yaml
metadata:
  version: "0.4"
  updated: "2026-07-12"
```

## Version Contract / 版本契约

- The first substantive state is `0.1`.
- A backward-compatible substantive change increments the second component by
  one: `0.9 -> 0.10`, `1.0 -> 1.1`.
- A breaking change increments the first component and resets the second:
  `0.10 -> 1.0`, `1.4 -> 2.0`.
- Two-component versions are strings, not decimal numbers.
- `updated` is a quoted `YYYY-MM-DD` string derived from the Git committer date
  of the latest substantive state.

- 第一个实质状态使用 `0.1`。
- 向后兼容的实质变化将第二段加一，例如 `0.9 -> 0.10`、`1.0 -> 1.1`。
- 破坏性变化将第一段加一并把第二段归零，例如 `0.10 -> 1.0`、
  `1.4 -> 2.0`。
- 两段式版本是字符串序列，不是十进制数。
- `updated` 是带引号的 `YYYY-MM-DD` 字符串，取最后一个实质状态对应的
  Git committer date。

A major bump is required when a change breaks a public invocation name,
required input/output contract, artifact schema, bundled script CLI, core
default workflow, or a contract consumed by another skill. Compatible workflow
additions, corrections, validation improvements, and output improvements use a
minor bump.

公开调用名称、必需输入输出、artifact schema、附带脚本 CLI、核心默认流程，
或其他 skill 消费的契约发生不兼容变化时必须升级大版本。兼容性的工作流增补、
规则修正、验证增强和输出改进使用小版本。

## Substantive Content / 实质内容

The version fingerprint includes:

- `SKILL.md`, excluding `metadata.version` and `metadata.updated`
- `agents/openai.yaml`
- `references/`, `scripts/`, `assets/`, and `examples/`

It excludes `README*`, `LICENSE*`, `NOTICE*`, OS junk, generated caches,
metadata-only edits, identical catalog/plugin copies, and content-identical
moves. One commit that changes several behavior files is one skill revision.

版本指纹包含 `SKILL.md`（忽略 `metadata.version` / `metadata.updated`）、
`agents/openai.yaml`、`references/`、`scripts/`、`assets/` 和 `examples/`。
它排除 `README*`、`LICENSE*`、`NOTICE*`、系统垃圾文件、生成缓存、纯元信息
修改、相同 catalog/plugin 镜像和内容未变的移动。同一提交改动多个行为文件时，
只计算一次 skill revision。

## Source And Package Rules / 源与软件包规则

- `plugins/*/skills/*/SKILL.md` is the canonical published skill surface.
- The 58 Codex Next catalog skills must remain byte-identical to their packaged
  copies. `core-router` is the only plugin-only Codex Next skill.
- `local/`, runtime `.codex`, generated output, and private skills are outside
  this policy.
- Plugin package SemVer remains in `.codex-plugin/plugin.json`, mirrored to the
  Claude compatibility manifest when present. Marketplace entries do not copy
  package versions.

- `plugins/*/skills/*/SKILL.md` 是公开 skill 的 canonical surface。
- Codex Next 的 58 个 catalog skill 必须与 package 副本逐字节一致；
  `core-router` 是唯一 plugin-only 例外。
- `local/`、runtime `.codex`、生成产物和私有 skill 不属于本规则范围。
- Plugin package SemVer 继续由 `.codex-plugin/plugin.json` 管理；存在 Claude
  compatibility manifest 时必须保持版本一致。Marketplace entry 不复制版本。

## Commands / 命令

```bash
python3 scripts/check_skill_metadata.py audit --history-ref HEAD
python3 scripts/check_skill_metadata.py backfill --history-ref HEAD
python3 scripts/check_skill_metadata.py backfill --history-ref HEAD --apply
python3 scripts/check_skill_metadata.py check --base-ref origin/main
```

`audit` and the default `backfill` mode are read-only. `backfill --apply` is the
only mode that writes `SKILL.md`, and it fills only missing or invalid metadata;
it never resets an already valid independent version. `check` validates schema,
mirror parity, and version transitions relative to the selected base ref.

`audit` 和默认的 `backfill` 都是只读模式。只有 `backfill --apply` 会写入
`SKILL.md`，且只补齐缺失或非法的元信息，不会重置已经合法的独立版本。
`check` 会相对指定 base ref 校验 schema、镜像一致性和版本转换。
