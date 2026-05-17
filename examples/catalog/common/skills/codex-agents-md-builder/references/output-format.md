# 探索清单、自检、最终汇报格式

本文件覆盖 Step 1（探索）和 Step 5（自检与汇报）需要的所有详细 checklist。

---

## 1. 探索清单（Step 1 用）

### 必查项

**仓库结构**
- 顶层目录结构（`find . -maxdepth 3 -type d`）
- package manager / 主要语言 / 框架 / 构建系统

**配置文件（任选适用的检查）**
- JavaScript/TypeScript: `package.json` / `pnpm-workspace.yaml` / `yarn.lock` / `package-lock.json` / `bun.lock` / `turbo.json` / `nx.json`
- Python: `pyproject.toml` / `requirements.txt` / `uv.lock` / `Pipfile`
- Go: `go.mod`
- Rust: `Cargo.toml`
- Java/Kotlin: `pom.xml` / `build.gradle`
- 通用: `Makefile` / `Justfile` / `Taskfile.yml`
- 容器: `Dockerfile` / `docker-compose.yml`
- IaC: Terraform (`*.tf`) / Helm (`Chart.yaml`) / Kubernetes manifests
- CI: `.github/workflows/` / `.gitlab-ci.yml` / `Jenkinsfile` / `.circleci/`

**已有文档**
- `README` / `README.md` / `CONTRIBUTING.md` / `docs/`
- 已有 `AGENTS.md` / `AGENTS.override.md`（任意层级）
- Architecture / RFC / ADR 文档
- 如果目标目录已有 `AGENTS.override.md`，暂停并让用户决定 override 策略；不要继续写会被同目录 override 屏蔽的普通 `AGENTS.md`

**命令源**
- `package.json` 的 `scripts` 字段
- `Makefile` 的 target
- `pyproject.toml` 的 `[tool.poetry.scripts]` / `[project.scripts]`
- CI workflow 里的实际命令
- 文档里说明的命令

**目录分类**

按风险/职责扫描：

| 类型 | 关键词 |
|---|---|
| 高风险 | `auth` `authentication` `security` `payments` `billing` `database` `migrations` `infra` `deploy` `terraform` `helm` `k8s` `secrets` `credentials` |
| 生成 / 只读 | `generated` `gen` `__generated__` `codegen` `vendor` `third_party` `dist` `build` |
| 共享 | `packages` `libs` `common` `shared` `ui` `api-client` `sdk` |
| 应用 / 服务 | `apps` `services` `frontend` `backend` `web` `mobile` `cmd` |
| 工程辅助 | `scripts` `tools` `ci` `.github` |
| 文档 / 测试 / 示例 | `docs` `tests` `__tests__` `examples` `e2e` |

**生成源线索**
- 文件头 `DO NOT EDIT` / `@generated`
- OpenAPI / Swagger spec
- protobuf `.proto`
- GraphQL schema
- Database migrations 目录

### 推荐命令

以下命令只用于只读探索。Git 操作仍只允许 `status` / `diff` / `ls-files` / `rev-parse` / `log`。

```bash
# 仓库定位
pwd
git rev-parse --show-toplevel

# 结构
find . -maxdepth 3 -type d \
  -not -path './.git*' -not -path '*/node_modules*' \
  -not -path '*/.venv*' -not -path '*/dist*'

# 文件清单
git ls-files | head -200
git ls-files | wc -l

# 关键关键词扫描
rg -n "test|lint|typecheck|build|format|migrate|migration|codegen|generated|DO NOT EDIT|OpenAPI|protobuf|GraphQL" \
  --type-not lock --type-not log -g '!node_modules' -g '!dist' -g '!.git'

# 读关键配置
cat package.json
cat pnpm-workspace.yaml 2>/dev/null
cat turbo.json 2>/dev/null
cat Makefile 2>/dev/null
cat pyproject.toml 2>/dev/null
cat go.mod 2>/dev/null
cat Cargo.toml 2>/dev/null

# 已有 AGENTS.md
find . -name 'AGENTS.md' -not -path '*/node_modules/*'
find . -name 'AGENTS.override.md' -not -path '*/node_modules/*'

# Git 状态（只读）
git status
git log --oneline -10
```

### 探索预算

- 总 tool 调用 **≤ 30 次**
- 不需要穷尽每个文件
- 30 次后仍不确定 → 标记"未确认"并进入 Step 2
- monorepo 不要无限递归——一级 + 关键二级目录足够

### 探索忽略目录

不要进入这些目录扫描：

`.git` / `node_modules` / `dist` / `build` / `coverage` / `.next` / `.nuxt` / `.turbo` / `.cache` / `target` / `out` / `vendor/cache` / `__pycache__` / `.venv` / `venv` / `.idea` / `.vscode` / `.pytest_cache` / `.mypy_cache`

---

## 2. 自检清单（Step 5 用）

写完所有 AGENTS.md 后，逐项确认：

### 文件层面

- [ ] 只有 AGENTS.md 文件被改（`git status` / `git diff` 确认）
- [ ] 未执行 `git add` / `git commit` / `git reset` / `git checkout` / `git clean` / `git stash`
- [ ] 没创建 `AGENTS.override.md`（除非用户明确同意）
- [ ] 未在存在同目录 `AGENTS.override.md` 的位置写入会被屏蔽的普通 `AGENTS.md`
- [ ] 所有写入文件大小合理（根 8–16 KiB、子卡 0.5–2 KiB）

### 根 AGENTS.md 内容

- [ ] 包含仓库 Purpose
- [ ] 包含 Codex startup behavior 说明
- [ ] 包含 Directory map，有 Local AGENTS.md 列和 Read when 列
- [ ] 包含 On-demand cat protocol
- [ ] 关键命令复述（install/build/test/lint/typecheck/format/codegen/migration 中实际存在的）
- [ ] 每条命令标注 Sandbox notes（需要网络/Docker/数据库/sudo/凭据的明确标注）
- [ ] 包含 Global rules / Do not / Validation

### 子目录 AGENTS.md 内容

- [ ] 每个子卡片前 3 行说明：目录是什么、修改前最该看哪些文件、何时值得读
- [ ] 不重复根 AGENTS.md 已有规则
- [ ] 没有空段落（标题下没内容就删整段）
- [ ] 高风险目录有 Do not 和 Required before changes
- [ ] Generated / 只读目录卡片足够短（< 0.5 KiB）

### 命令真实性

- [ ] 每条命令都从仓库实际配置（package.json / Makefile / CI / pyproject.toml / 文档）确认存在
- [ ] 没有编造命令
- [ ] 不确定的命令明确标注"不确定"或指回根命令

### 冲突处理

- [ ] 根与子目录规则无冲突，或冲突已按"子目录优先"原则处理
- [ ] 删除/压缩/改写已有 AGENTS.md 内容的部分有记录，准备在最终汇报中说明

---

## 3. 最终汇报格式（中文，给用户看）

汇报必须严格按以下结构。

### 仓库判断

- **仓库类型**：（如 monorepo / 单体服务 / SDK / prompts 仓库 / IaC 仓库）
- **主要技术栈**：（如 TypeScript + React + Node.js / Python + FastAPI / Go）
- **包管理器**：（如 pnpm / npm / poetry / uv / go mod / cargo）
- **构建/测试系统**：（如 turbo + vitest / pytest + tox / go test）
- **高风险目录**：（列出实际识别到的）

### AGENTS.md 分层策略

简述本仓库 Root router / Domain card / Guardrail card 的使用方式。例如：

> 根 AGENTS.md 作为 router 提供目录地图和命令索引；services/payments/、packages/ui/ 各有 Domain card；infra/terraform/、migrations/ 各有 Guardrail card；apps/* 和 docs/ 不创建本地卡片（无独立规则）。

### 新增或更新文件

| Path | Type | Purpose | Notes |
|---|---|---|---|
| `AGENTS.md` | Root router | 启动期主规则、目录地图、命令索引 | 新建 / 更新 |
| `services/payments/AGENTS.md` | Domain card | 支付服务状态机和不变量 | 新建 |
| `infra/terraform/AGENTS.md` | Guardrail card | 生产基础设施变更约束 | 新建 |

### 根 AGENTS.md 覆盖内容

明确说明根文件是否包含：
- 目录地图（含 Local AGENTS.md 列） ✓ / ✗
- 按需 cat 协议 ✓ / ✗
- 关键命令复述 ✓ / ✗
- 全局规则 ✓ / ✗
- 验证标准 ✓ / ✗

### 未创建 AGENTS.md 的重要目录

| Path | Reason |
|---|---|
| `apps/web/` | 无独立规则，根 AGENTS.md 已覆盖 |
| `docs/` | 用户文档，agent 不修改 |
| `tests/` | 测试目录，跟随被测代码规则即可 |

### 验证与限制

- **已检查的命令来源**：package.json scripts / Makefile / `.github/workflows/ci.yml`
- **默认沙箱可运行**：`pnpm install` / `pnpm build` / `pnpm test` / `pnpm lint` / `pnpm typecheck`
- **需要外部依赖**：
  - `pnpm db:migrate` — 需要本地 PostgreSQL
  - `pnpm e2e` — 需要本地服务启动
  - `terraform plan` — 需要 AWS 凭据
- **未运行或无法确认的命令**：（如有，列出并说明原因）

### 冲突与保留内容

- 是否发现根与子目录规则冲突：（是/否，简述）
- 是否发现 `AGENTS.override.md` 影响普通 `AGENTS.md`：（是/否，简述）
- 是否删除 / 压缩 / 改写已有 AGENTS.md 重要内容：（是/否）
- 如果是，列出摘要：
  - 删除了 `services/legacy/AGENTS.md` 的"FIXME 由 X 接手"段（看起来是历史遗留，X 已离职）
  - 压缩了根 AGENTS.md 的某节大段背景介绍（保留事实结论）
- 处理理由：（简述）

### Git diff 摘要

- 只修改了以下 AGENTS.md：
  - `AGENTS.md`（新建 / 更新）
  - `services/payments/AGENTS.md`（新建）
  - `infra/terraform/AGENTS.md`（新建）
- 确认未执行 `git add` / `git commit` / `git reset` / `git checkout` / `git clean` / `git stash`
- 如果不小心改了非 AGENTS.md 文件，**必须**在此处明确指出并说明原因

---

## 收尾追问

如果在执行过程中本 skill 没有命中暂停条件，最终汇报后用一次性追问收尾：

> 还有没有补充要做的事情？请一次性列出，我将继续在本轮内处理。

不要反复追问，不要在没有完成自检前追问。
