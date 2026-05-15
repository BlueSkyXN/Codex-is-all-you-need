# 仓库指南

[English](AGENTS.md) | 中文

## 项目结构与模块组织

本仓库用于发布可公开的 Codex preset 文档、示例和只读 dashboard。

- `README.md` 与 `README_CN.md`：英文和中文项目入口说明。
- `docs/`：架构、agent 设计、skill 设计、迁移策略、公开/私有分层说明。
- `examples/catalog/`：脱敏后的 preset catalog，按 `common`、`dev`、`data`、`office`、`research` 分组；agent 位于 `agents/*.toml`，skill 位于 `skills/<skill-name>/SKILL.md`。
- `examples/runtime/` 与 `examples/suites/`：runtime 和 suite 布局示例。
- `dashboard/`：Python 静态 dashboard 生成器、HTML 模板和示例配置。

## 构建、测试与开发命令

- `python3 dashboard/build_dashboard.py --config ~/.codex/dashboard/config.toml`：使用仓库外的本地配置生成 dashboard JSON 和 HTML。
- `python3 dashboard/build_dashboard.py --config ~/.codex/dashboard/config.toml --json-only`：只生成 JSON，用于快速验证扫描结果。
- `open ~/.codex/dashboard/index.html`：本地预览生成后的 dashboard。

首次配置示例：

```bash
mkdir -p ~/.codex/dashboard
cp dashboard/examples/config.example.toml ~/.codex/dashboard/config.toml
```

不要提交真实 runtime 配置或生成出的 dashboard 文件。

## 代码风格与命名约定

Python 代码应延续 `dashboard/build_dashboard.py` 的 stdlib-first 风格：函数边界清晰，必要时添加 type hints，文件系统逻辑优先使用 `pathlib.Path`，只在非显而易见处写简短注释。Python 使用 4 空格缩进。Markdown 保持简洁；只有上下文已经是双语文档时才继续中英双语。

Agent 文件使用 snake_case，例如 `dev_python_engineer.toml`。Skill 目录使用 kebab-case，例如 `python-quality/`，入口文件固定为 `SKILL.md`。

## 测试指南

当前仓库尚未提交测试框架。修改 dashboard 后，至少使用本地配置跑一次最小 smoke check：

```bash
python3 dashboard/build_dashboard.py --config ~/.codex/dashboard/config.toml --json-only
```

修改文档或 catalog 时，手动检查链接、标题层级、TOML 语法和 public-safe 表述。没有新增并运行真实测试时，不要声称已有 coverage。

## Commit 与 Pull Request 规范

近期提交历史使用简短、祈使句风格的 Conventional-style message，以 `docs:` 为主；例如 `docs: add public Codex preset catalog` 和 `docs: split README translations`。根据修改范围优先使用 `docs:`、`dashboard:` 或 `examples:`。

PR 应说明修改了哪些文件、为什么这些内容可公开，以及执行过哪些验证。只有 dashboard UI 变更需要附截图。

## 安全与配置提示

不要把私有 skills、runtime 路径、生成的扫描结果、机器特定 symlink 状态，以及真实的 `~/.codex/dashboard/config.toml` 值提交到仓库。Dashboard 应保持只读；除非任务明确要求，否则不要创建、删除或重写 `.codex`、`.agents`、suite symlink 或 source catalog 文件。
