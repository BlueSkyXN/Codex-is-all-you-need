# Example Catalog / 示例素材目录

This is a sanitized source catalog derived from a real Codex preset catalog.

这是一个从真实 Codex preset catalog 抽取并脱敏后的 source catalog，结构与生产素材目录一致。

```text
common/
  agents/
  skills/
sdlc-manager/
  agents/
  skills/
dev/
  agents/
  skills/
data/
  agents/
  skills/
office/
  agents/
  skills/
research/
  agents/
  skills/
```

The dashboard can scan this directory as `source.codex_root` when paired with a local `suites_root`.

配合本机 `suites_root` 时，dashboard 可以把本目录作为 `source.codex_root` 扫描。

Current public subset:

当前公开子集：

```text
common/                 6 agents, 1 public skill
sdlc-manager/           7 agents, 19 public skills
dev/                   14 agents, 20 public skills
data/                   5 agents, 4 public skills
office/                 5 agents, 5 public skills
research/               4 agents, 3 public skills
```

Private symlinked skills are intentionally excluded. Agent `Recommended skills`
hints are sanitized so they only name public skills or generic runtime-provided
workflows.

私有 symlink skills 已被刻意排除。agent 中的 `Recommended skills` 提示也已脱敏，
只会指向公开 skill，或使用“当前 runtime 可见的通用 workflow”这类泛化说法。

See `PUBLIC-SUBSET.md` for the publication boundary.

发布边界见 `PUBLIC-SUBSET.md`。
