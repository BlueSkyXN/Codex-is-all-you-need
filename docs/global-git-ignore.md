# Global Git Ignore Profile / 用户级 Git Ignore 配置

This note documents a user-level Git ignore profile for machine-local Codex,
agent, secret-scan, and scratch-work files. It is intended for private developer
machines, not for repository-specific build outputs.

本文档记录用户级 Git ignore 的部署原则，适用于本机 Codex、agent、secret
扫描和临时工作文件。它不是项目构建产物的 `.gitignore` 模板。

## Standard Location / 标准位置

Use Git's default XDG user-level ignore file:

使用 Git 默认的 XDG 用户级 ignore 文件：

```text
~/.config/git/ignore
```

On this machine, that resolves to:

在这台机器上，它对应：

```text
/Users/sky/.config/git/ignore
```

Keep global `core.excludesfile` unset unless there is a deliberate reason to
override Git's default discovery path:

除非有明确原因覆盖 Git 默认发现路径，否则保持全局 `core.excludesfile` 未设置：

```bash
git config --global --get-all core.excludesfile
```

Expected output is empty. When `XDG_CONFIG_HOME` is unset, Git reads
`$HOME/.config/git/ignore`.

预期输出为空。当 `XDG_CONFIG_HOME` 未设置时，Git 会读取
`$HOME/.config/git/ignore`。

## What Belongs Here / 适合放什么

User-level ignore rules are for files that should stay private or local across
many repositories:

用户级 ignore 适合跨仓库都应保持本机私有的内容：

- machine-local work folders such as `local/`;
- local environment and secret-bearing files;
- private key and certificate material;
- macOS noise files;
- agent runtime folders and local assistant configuration;
- raw secret-scan output that may contain sensitive paths or findings.

Do not use the user-level file for project-specific build outputs, framework
caches, generated SDKs, or business directories. Those belong in the project's
tracked `.gitignore`.

不要把用户级 ignore 当成项目规则仓库。具体项目的构建产物、框架缓存、生成
SDK 或业务目录，应写进该项目自己的 `.gitignore`。

## Recommended Rules / 推荐规则

```gitignore
# Local private work areas
local/
**/local/

# Local environment and secret-bearing files
.env.local
*.secret
*.key
*.pem

# Machine and OS noise
.DS_Store

# Local agent and assistant runtime/config directories
.codex/
.claude/
.agent/
.agents/

# Local secret-scan output
secret-audit-reports/
secret-audit-reports/private-raw/
*.trufflehog.raw.jsonl
```

Notes:

- `local/` already matches directories named `local` below a repository root in
  normal Git ignore semantics; `**/local/` is mostly redundant, but harmless.
- `.codex/`, `.claude/`, `.agent/`, and `.agents/` are treated here as
  machine-local runtime/config directories. If a specific public project wants
  to track one of these directories intentionally, review that project before
  force-adding files.
- `secret-audit-reports/private-raw/` is covered by `secret-audit-reports/`, but
  keeping it documents the sensitive subdirectory explicitly.

说明：

- `local/` 在 Git ignore 语义里已经可以匹配 repo 下任意层级名为 `local`
  的目录；`**/local/` 基本冗余，但无害。
- `.codex/`、`.claude/`、`.agent/`、`.agents/` 在这里被视为本机 runtime
  或配置目录。如果某个公开项目确实要跟踪这些目录，应先审查该项目规则，再决定
  是否 `git add -f`。
- `secret-audit-reports/private-raw/` 已被 `secret-audit-reports/` 覆盖，
  保留它是为了显式标记敏感原始输出目录。

## Deployment / 部署

```bash
mkdir -p ~/.config/git
$EDITOR ~/.config/git/ignore
git config --global --unset-all core.excludesfile || true
```

Verify Git is using the default path:

验证 Git 使用默认路径：

```bash
git config --show-origin --get-all core.excludesfile
git check-ignore -v local/test.txt .codex/config.toml .claude/settings.local.json
```

The first command should print nothing. The second command should cite
`~/.config/git/ignore`.

第一条命令应无输出。第二条命令应显示命中 `~/.config/git/ignore`。

## Interaction With Repository Rules / 和仓库规则的关系

Git ignore rules only affect untracked files. If a file is already tracked,
adding it to the user-level ignore file will not remove it from Git history or
from the index.

Git ignore 只影响未被跟踪的文件。已经被 Git 跟踪的文件，不会因为加入用户级
ignore 自动从 index 或历史里消失。

Use the right layer:

按语义选择层级：

```text
~/.config/git/ignore      user-level private defaults; not committed
<repo>/.gitignore         project-wide shared rules; committed
<repo>/.git/info/exclude  repo-local private rules; not committed
```

For machine-local Codex entrypoint symlinks created by
`scripts/sync_codex_entrypoints.py`, either the user-level ignore file or the
repo-local `.git/info/exclude` may ignore `.codex/` and `.agents/`. The helper
uses `.git/info/exclude` so each target repository stays clean even when the
user-level file is not configured.

对于 `scripts/sync_codex_entrypoints.py` 创建的本机 Codex entrypoint
symlink，用户级 ignore 或 repo-local `.git/info/exclude` 都可以忽略
`.codex/` 和 `.agents/`。该 helper 使用 `.git/info/exclude`，这样即使用户级
ignore 未配置，目标 repo 也能保持干净。
