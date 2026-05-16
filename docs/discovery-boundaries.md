# Codex Discovery Boundaries / Codex 发现边界

This document summarizes the public-safe conclusions from local Codex skill and
custom-agent discovery experiments. It intentionally omits machine-specific lab
paths, run IDs, and generated result files.

本文总结本地 Codex skill 与 custom agent discovery 实验得到的公开安全结论。这里刻意
省略本机实验路径、run ID 和生成结果文件。

## Summary / 摘要

```text
With a git root:
  Codex scans repo-level entries only along git root -> CWD.

有 git root：
  Codex 只扫描 git root -> CWD 路径链上的 repo-level entries。

Without a git root:
  Codex scans only the current working directory.

无 git root：
  Codex 只扫描当前工作目录。
```

Consequences:

结论：

- A parent workspace `.codex` is not automatically inherited by child git repos.
- Codex does not recursively scan the whole repository.
- Sibling subtrees are not scanned.
- Nested git repositories block outer repo-level discovery.
- Repo-local skills can be exposed through `.agents/skills/<skill>` and legacy `.codex/skills/<skill>`.
- Repo-local custom agents are discovered from `.codex/agents/*.toml`.
- `.agents/agents` and `.agents/*.toml` are not repo-local custom-agent discovery paths.

## Matrix / 矩阵

| Situation | Expected Discovery |
|---|---|
| CWD has `.agents/skills/<skill>` | Found |
| CWD has `.codex/skills/<skill>` | Found, legacy path |
| Git repo root has `.agents/skills/<skill>` and CWD is below it | Found |
| Git repo root has `.codex/agents/<agent>.toml` and CWD is below it | Found |
| Parent directory above git root has `.codex` | Not found |
| Sibling subtree inside same repo has `.agents/skills` | Not found |
| Outer repo has entries, inner nested git repo is CWD root | Outer entries not found |
| No git root, parent directory has entries | Parent entries not found |

## Practical Pattern / 实用模式

Use a workspace aggregate as a symlink target, not as an inherited parent:

把工作区聚合层当成 symlink target，而不是继承式父目录：

```text
<workspace>/.codex/agents
<workspace>/.codex/skills

<repo>/.codex/agents/<agent>.toml -> <workspace>/.codex/agents/<agent>.toml
<repo>/.codex/skills/<skill>      -> <workspace>/.codex/skills/<skill>
```

The helper script automates this explicit opt-in:

同步脚本用于自动化这种显式 opt-in：

```bash
python3 scripts/sync_codex_entrypoints.py sync \
  --workspace /path/to/workspace \
  --source-root /path/to/workspace/.codex \
  --apply
```

## Local Notes / 本机记录

Detailed local experiment logs can live under `local/`, but that directory is
ignored because it may contain machine-specific paths and generated result
locations.

详细本机实验记录可以放在 `local/`，但该目录被 Git 忽略，因为它可能包含本机路径和
生成结果位置。
