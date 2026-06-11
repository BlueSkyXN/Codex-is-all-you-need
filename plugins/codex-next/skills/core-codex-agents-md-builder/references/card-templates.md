# 三类 AGENTS.md 模板

本文件给出 Root router / Domain card / Guardrail card 的完整结构和示例。
SKILL.md 已经讲清"什么时候用哪种"，本文件只讲"怎么写"。

## 通用要求（三类都适用）

- 简洁、准确、可执行
- 不重复上级 AGENTS.md 已覆盖的规则
- 不写无法验证的主观要求（"遵循最佳实践"等空话——除非后面跟具体标准）
- 不复制 README 大段
- 不写过长背景介绍——只写未来修改必须遵守的不变量
- 不泄露 secret / token / credentials / PII
- 不创建空文件（标题下没内容就删掉整段）
- 语言优先沿用仓库现有文档主语言

---

## Root router 模板（仓库根 AGENTS.md）

**必须创建**。从仓库根目录启动 Codex 时，这是 repo-local 启动上下文中的主项目指令。

### 推荐结构

```md
# Repository agent instructions

## Purpose

<一句话说明仓库用途。>

## Codex startup behavior

- Codex 通常从仓库根目录启动
- 本文件是启动期主规则
- 子目录 AGENTS.md 是按需导航卡片
- 修改有本地 AGENTS.md 的目录前必须先 cat 对应文件
- 如果从子目录启动，Codex 也可能自动加载路径链上的本地 AGENTS.md；仍以本文件的目录地图作为根启动 workflow 的 router

## Directory map

| Path | Responsibility | Local AGENTS.md | Read when |
|---|---|---:|---|
| `apps/web/` | Next.js frontend | No | — |
| `services/payments/` | 支付处理服务 | Yes | 修改 webhook、refund、provider 代码前 |
| `packages/ui/` | 共享 UI 组件库 | Yes | 修改导出组件、design tokens、public props 前 |
| `infra/terraform/` | 生产环境基础设施 | Yes | 任何 .tf 修改前 |
| `migrations/` | 数据库迁移 | Yes | 新增 / 修改 / 回滚 migration 前 |
| `docs/` | 用户文档 | No | — |

## On-demand cat protocol

Before editing files under a directory that has a local AGENTS.md,
read that file first using `cat <path>/AGENTS.md`.
If multiple nested AGENTS.md exist on the path to the target file,
read them from shallow to deep before making changes.

## Commands

| Command | Purpose | Scope | Sandbox notes |
|---|---|---|---|
| `pnpm install` | install deps | repo | OK |
| `pnpm build` | build all packages | repo | OK |
| `pnpm test` | run unit tests | repo | OK |
| `pnpm lint` | run ESLint | repo | OK |
| `pnpm typecheck` | run TypeScript check | repo | OK |
| `pnpm db:migrate` | run migrations | services/* | 需要 PostgreSQL 可用 |
| `pnpm e2e` | end-to-end tests | repo | 需要本地服务启动 |

## Global rules

- 包管理器：pnpm（不要用 npm / yarn）
- 不要手动改 `pnpm-lock.yaml`，通过 `pnpm install` 重生成
- 新增依赖前确认是否已存在等价能力（先 grep）
- TypeScript strict 模式开启，不要用 `any` 兜底
- 测试覆盖率要求：services/ 下新增代码必须有单元测试

## Do not

- 不要提交 `.env*` 文件或任何凭据
- 不要手动改 `**/generated/**` 下的文件
- 不要执行 `pnpm publish` 或任何发布命令
- 不要跳过 pre-commit hook（除非用户明确要求）

## Validation

完成任意修改后默认验证流程：

1. `pnpm typecheck` 必须通过
2. `pnpm lint` 必须通过
3. `pnpm test` 相关测试必须通过

涉及数据库 / e2e 的修改在受限沙箱无法完整验证时，在最终汇报中明确说明哪些步骤被跳过。

## Notes for future agents

- `services/payments/` 与 `services/billing/` 经常需要协同修改，注意检查
- `packages/ui/` 的 public props 变更会影响所有 apps，谨慎设计
```

### Directory map 必含元素

1. **必须有 Local AGENTS.md 列**——告诉 agent 哪些子目录需要 cat
2. **必须有 Read when 列**——具体场景，不要只写 "when relevant"
3. 至少覆盖所有一级目录
4. 有本地 AGENTS.md 的子目录必须出现在表中

### Commands 必含元素

1. **复述实际命令**——从 package.json scripts / Makefile / CI / pyproject.toml 确认
2. **Sandbox notes 标注网络/Docker/数据库/sudo/凭据依赖**
3. 不要写 "see README"

### 禁止事项

- 写某个服务的详细业务状态机（属于该服务的 Domain card）
- 写某个包的所有导出清单（属于该包的 Domain card）
- 写某个部署环境的完整说明（属于 infra 的 Guardrail card）
- 大段复制 README
- 泛泛的"写高质量代码"

---

## Domain card 模板（业务模块子目录）

**适用于**：应用目录、服务目录、共享库、有独立职责边界的业务模块。

**只在满足以下任一条件时创建**：

- 独立职责边界
- 特殊业务不变量
- 专属验证命令
- 经常被 agent 误改
- 与上级规则有明显差异
- public API / 依赖边界 / 导出规则需要保护

### 推荐结构

```md
# services/payments navigation card

支付处理服务，对接 Stripe / Adyen，处理 charge / refund / webhook。
Read this card before modifying webhook handlers, refund logic, or provider integration.
Key files: `src/webhook.ts`, `src/providers/`, `src/state-machine.ts`.

## Local invariants

- charge 状态机只能按 `pending → authorized → captured → settled` 流转
- refund 必须在 capture 后 90 天内发起
- 所有 webhook 必须验证签名（`verifyWebhookSignature` 已封装）
- 金额单位永远是最小货币单位（cents），不要在本服务内做 100 倍换算

## Local rules

- 新增 provider 必须实现 `PaymentProvider` interface 完整契约
- webhook 事件必须先 ack 再处理，避免超时
- 失败重试用 `services/queue/` 的标准 backoff，不要自己实现

## Do not

- 不要在本服务内直接读用户表，通过 `services/users/` 的 API
- 不要把 provider 的原始 webhook payload 落库（含 PII），只存提取后的字段

## Validation

- `pnpm --filter @repo/payments test` — 单元测试
- `pnpm --filter @repo/payments test:integration` — 集成测试，**需要本地 PostgreSQL**
```

### Domain card 规则

- 前 3 行必须说明：目录是什么、修改前最该看哪些文件、卡片何时值得读
- 只写本目录特有内容
- 没有 Do not 内容就删掉 Do not 段——不写空标题
- 没有专属验证命令就写 "Use root validation commands."；如果根命令已经足够明确，也可以删除整个 Validation 段
- 长度控制在 0.5–2 KiB

### 禁止事项

- 重复根 AGENTS.md 的规则
- 写长背景介绍（动机、历史、设计哲学）
- 写无法验证的主观要求
- 机械套模板（如本目录无 invariant 内容，删掉整段）

---

## Guardrail card 模板（高风险或只读目录）

**适用于**：infra / deploy / terraform / helm / k8s / migrations / database / auth / security / payments / billing / generated / codegen / vendor / third_party / secrets / credentials。

**目标**：降低破坏性改动风险，明确禁止事项和必须的前置检查。

### 推荐结构（高风险目录）

```md
# infra/terraform navigation card

Production infrastructure as code. Changes here affect live systems.
Read this card before any .tf modification, even one-line changes.
Key files: `main.tf`, `variables.tf`, `environments/prod/`.

## Why this is high-risk

- Apply 操作直接影响生产环境
- State 文件存放在远端 S3，并发 apply 会损坏 state
- 部分资源（RDS、VPC）删除不可逆

## Required before changes

- 读取 `environments/<target>/README.md` 确认变更目标环境
- 确认当前 state 已 lock-free（`terraform state list` 可运行）
- 用户已明确授权变更范围

## Do not

- 不要执行 `terraform apply`（必须用户手动执行）
- 不要执行 `terraform destroy` 在任何 prod 资源上
- 不要修改 `environments/prod/` 下的文件而不显式标注影响
- 不要在 .tf 中硬编码凭据，使用 AWS SSM / Vault

## Validation

- `terraform fmt -check` — 格式检查，OK in sandbox
- `terraform validate` — 语法检查，OK in sandbox
- `terraform plan -out=tfplan` — 变更预览，**需要 AWS 凭据**
- 不要在 PR 流程外运行 `terraform apply`
```

### 推荐结构（Generated / 只读目录最短形式）

```md
# generated navigation card

This directory contains generated files.
Do not edit files here manually.
Change the source schema / IDL / OpenAPI spec / protobuf / generator instead.
Use root validation commands unless a regeneration command is listed there.
```

### Guardrail card 规则

- 必须明确"为什么高风险或只读"
- 必须列出修改前的前置检查
- Do not 列表要具体，不要泛泛
- 需要凭据 / 网络 / Docker / 外部服务的命令必须标注
- 生成 / 只读目录的卡片应非常短（< 0.5 KiB）

### 禁止事项

- 把 Guardrail card 写成 Domain card（业务细节）
- 把 Guardrail card 写成警告堆砌（"危险！谨慎！"——没有具体动作）
- 让 agent 在受限沙箱里运行需要凭据的命令而不标注

---

## 三类卡片选哪个：决策快查

| 目录特征 | 选 |
|---|---|
| 仓库根 | Root router |
| 有独立产品 / 服务边界 | Domain card |
| 有 public API 或导出契约 | Domain card |
| 有专属业务状态机 / 不变量 | Domain card |
| 影响生产环境的配置 | Guardrail card |
| 数据库 schema / migrations | Guardrail card |
| auth / payments / secrets | Guardrail card |
| 生成代码 / vendor / 第三方 | Guardrail card |
| 纯组织目录、无规则、无验证 | 不创建 |

如果同时满足 Domain card 和 Guardrail card 条件（如 `services/payments/`），优先用 Domain card 结构，但把 guardrail 内容融入 Do not 和 Local invariants。
