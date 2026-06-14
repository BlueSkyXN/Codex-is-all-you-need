# V1 Suite Examples / V1 Suite 示例

This directory is a legacy fixture for the old suite/composition model. It does
not create real symlinks, and it is not the V2 production path.

本目录是旧 suite / composition 模型的 legacy 示例，不创建真实 symlink，也不是
V2 生产路径。

Current V2 usage is plugin-first:

当前 V2 使用方式是 plugin-first：

```text
source catalog -> plugin package -> marketplace install
```

Use these examples only when maintaining or migrating a V1-style local runtime:

- Suite composition pattern: [docs/v1/suite-composition.md](../../docs/v1/suite-composition.md)
- V1 to V2 migration: [docs/v1/suite-to-plugin-migration.md](../../docs/v1/suite-to-plugin-migration.md)

Production shared skills should come from the Codex Next plugin. Runtime suite
links are only for legacy migration, local-development experiments, or explicit
custom-agent exposure.
