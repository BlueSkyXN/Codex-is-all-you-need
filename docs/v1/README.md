# V1 Legacy Docs / V1 旧方案文档

V1 is the old suite/composition model. Keep these docs for migration,
compatibility, and local-development experiments only.

V1 是旧的 suite / composition 模型。本目录只保留迁移、兼容和 local-development
实验所需资料。

## Current State / 当前状态

The repository's current public model is V2:

本仓库当前公开模型是 V2：

```text
source catalog -> plugin package -> marketplace install
```

In V2, production shared skills are distributed by the Codex Next plugin.
Machine-local suite symlinks are not the production path.

在 V2 中，生产态共享 skills 通过 Codex Next 插件分发。本机 suite symlink
不再是生产路径。

## V1 Materials / V1 资料

- [Suite Composition](suite-composition.md): old suite symlink pattern and runtime entrypoints.
- [V1 To V2 Migration](suite-to-plugin-migration.md): cleanup path from V1 suite exposure to V2 plugin-first usage.

## Boundary / 边界

Use V1 docs only when:

- Migrating an existing machine that still exposes shared skills through
  `~/.codex/suites` or repo-local `.codex/skills` links.
- Maintaining a local-development experiment that intentionally uses runtime
  symlink entrypoints.
- Debugging dashboard reports for V1 legacy/local-dev suite visibility.

Do not use V1 docs as the default onboarding path for new users. New usage
should start from the V2 plugin-first docs in `README.md`, `docs/usage-guide.md`,
and `plugins/codex-next/README.md`.
