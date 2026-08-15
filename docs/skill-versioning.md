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
  version: "0.2"
  updated: "2026-07-12"
  maintainer: "Alice"
  updated_by: "Alice, Bob"
```

`maintainer` names the current human owner or stable team. `updated_by` names
the humans responsible for the current substantive state. Separate multiple
names with an English comma and one space. Do not list AI, formatters, CI, or
automatic mirrors; Git history and pull requests retain original authorship and
the full contributor record.

`maintainer` 表示当前人类负责人或稳定团队，`updated_by` 表示对当前实质状态负责
的人类修改人；多人用英文逗号加一个空格分隔。不记录 AI、formatter、CI 或自动镜像；
原始作者和完整贡献记录由 Git history / PR 保留。

## Version Contract / 版本契约

- The first substantive state is `0.1`.
- While the major component is `0`, the skill is in initial development and
  each new substantive state increments the second component, for example
  `0.1 -> 0.2` or `0.9 -> 0.10`; an incompatible change does not automatically
  declare `1.0`.
- `1.0` is an explicit declaration of the first stable public contract, not a
  measure of how large an improvement was. After stability is declared,
  compatible changes increment the second component (`1.0 -> 1.1`) and
  breaking public-contract changes increment the first component and reset the
  second (`1.4 -> 2.0`).
- One unpublished change batch gets one version bump. Consecutive edits, review
  rounds, and multiple commits in the same task or PR are one substantive state
  until they are published or accepted as a release baseline.
- Do not stack version bumps merely because several edits happened in a short
  period. A new bump begins only after the previous state was published,
  adopted as a baseline, or consumed externally and a new substantive change
  starts.
- Two-component versions are strings, not decimal numbers.
- `updated` is a quoted `YYYY-MM-DD` string derived from the Git committer date
  of the latest substantive state. For an uncommitted current substantive
  fingerprint, use the current calendar date; commit it before treating that
  date as historical evidence.

- 第一个实质状态使用 `0.1`。
- 主段为 `0` 时表示 Skill 处于初始开发；每个新的实质状态递增第二段，例如 `0.1 -> 0.2`、`0.9 -> 0.10`，不兼容变化也不自动声明 `1.0`。
- `1.0` 是负责人对首个稳定公开契约的明确声明，不表示改动幅度或质量提升大小。进入稳定阶段后，兼容变化递增第二段（`1.0 -> 1.1`），破坏公开契约才递增第一段并把第二段归零（`1.4 -> 2.0`）。
- 同一未发布修改批次只升版一次；同一任务、同一 PR、连续 review 和多个 commit 在发布或成为正式基线前都属于一个实质状态。
- 禁止因短时间发生多次编辑就叠加版本号。只有前一状态已发布、成为正式基线或被外部消费后，新的实质变化才开始下一次升版。
- 两段式版本是字符串序列，不是十进制数。
- `updated` 是带引号的 `YYYY-MM-DD` 字符串，取最后一个实质状态对应的
  Git committer date；若当前实质 fingerprint 尚未提交，则使用当天日期，并在
  提交后才将该日期视为历史证据。

After a skill has declared a stable `1.x` contract, a major bump is required
when a change breaks a public invocation name, required input/output contract,
artifact schema, bundled script CLI, core default workflow, or a contract
consumed by another skill. Before that declaration, `0.x` initial-development
states continue by incrementing the second component.

Skill 已声明稳定的 `1.x` 契约后，公开调用名称、必需输入输出、artifact schema、
附带脚本 CLI、核心默认流程或其他 Skill 消费的契约发生不兼容变化时必须升级主段；
在稳定声明之前，`0.x` 初始开发状态继续递增第二段。

## Substantive Content / 实质内容

The version fingerprint includes:

- `SKILL.md`, excluding governance-only metadata and WorkBuddy's UI-only
  `display_name`
- behavior-affecting adapter settings, including invocation policy, tool
  dependencies, and `default_prompt`
- `references/`, `scripts/`, `assets/`, and `examples/`

It excludes `skill-manifest.json`, `README*`, `LICENSE*`, `NOTICE*`, OS junk,
generated caches, metadata-only edits, WorkBuddy `display_name`, OpenAI
presentation-only fields such as `interface.display_name`,
`interface.short_description`, icons, and brand color, identical catalog/plugin
copies, and content-identical moves. One coherent unpublished change batch is
one skill revision even when it spans several edits, review rounds, or commits.

版本指纹包含 `SKILL.md`（忽略纯治理和纯 UI metadata）、`references/`、`scripts/`、
`assets/`、`examples/`，以及会改变调用策略、工具依赖、`default_prompt` 或执行行为的
平台 adapter 字段。它排除 `skill-manifest.json`、`README*`、`LICENSE*`、`NOTICE*`、
系统垃圾、生成缓存、WorkBuddy `display_name`、OpenAI `interface.display_name` /
`interface.short_description` / 图标 / 品牌色等纯展示字段、相同 catalog/plugin 镜像和
内容未变的移动。同一未发布修改批次即使跨越多次编辑、review 或 commit，也只计算
一次 skill revision。

## Source And Package Rules / 源与软件包规则

- `plugins/*/skills/*/SKILL.md` is the canonical published skill surface.
- The 59 Codex Next catalog skills must remain byte-identical to their packaged
  copies. `core-router` is the only plugin-only Codex Next skill.
- `local/`, runtime `.codex`, generated output, and private skills are outside
  this policy.
- Plugin package SemVer remains in `.codex-plugin/plugin.json`, mirrored to the
  Claude compatibility manifest when present. Marketplace entries do not copy
  package versions.

- `plugins/*/skills/*/SKILL.md` 是公开 skill 的 canonical surface。
- Codex Next 的 59 个 catalog skill 必须与 package 副本逐字节一致；
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

These commands intentionally have two different evidence models:

- `check --base-ref <base>` evaluates the current checkout as one unpublished
  delivery batch relative to `<base>`. All behavior changes in that batch require
  one version step, rather than one step per local edit or commit. A canonical
  skill absent from `<base>` must start at `0.1`; its `updated` must equal the
  latest substantive fingerprint date (the committer date when present in
  `HEAD`, otherwise today's date for an uncommitted current fingerprint).
- `audit` and `backfill --history-ref <ref>` walk committed trees and deduplicate
  adjacent identical behavior fingerprints as historical evidence. Without
  release, accepted-baseline, or PR boundaries, that is only a committed-history
  proxy: they must not claim to infer that separate commits belonged to one PR
  or one unpublished delivery batch.

The CLI deliberately does not add release or baseline flags. Choose
`check --base-ref` when validating the current delivery boundary; use
`audit`/`backfill` only to inspect or repair metadata from the available commit
history.

`audit` 和默认的 `backfill` 都是只读模式。只有 `backfill --apply` 会写入
`SKILL.md`，且只补齐缺失或非法的元信息，不会重置已经合法的独立版本。
`check` 会相对指定 base ref 校验 schema、镜像一致性和版本转换。

这些命令刻意采用两层不同的证据语义：

- `check --base-ref <base>` 将当前 checkout 相对 `<base>` 视为一个未发布的
  交付批次。该批次内的所有行为改动只要求一次 version step，不会按本地编辑或
  commit 次数累计。canonical skill 若在 `<base>` 中不存在，必须从 `0.1` 开始；
  `updated` 必须等于最新实质 fingerprint 的日期（已存在于 `HEAD` 时为 committer
  date，当前 fingerprint 未提交时为当天日期）。
- `audit` 和 `backfill --history-ref <ref>` 会逐个查看已提交 tree，并把相邻且行为
  fingerprint 相同的状态去重，作为历史证据。缺少 release、已接受 baseline 或 PR
  边界时，这只能是 committed-history proxy；它们不能声称推断出多个 commit 属于
  同一个 PR 或同一个未发布交付批次。

CLI 刻意不新增 release 或 baseline flag。验证当前交付边界时使用
`check --base-ref`；只在根据可用 commit history 检查或补齐 metadata 时使用
`audit` / `backfill`。
