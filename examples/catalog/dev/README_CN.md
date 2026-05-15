# Development Catalog / 开发目录

[English](README.md) | 中文

这里存放软件工程相关 agents 与 skills，覆盖仓库探索、实现、审查、测试、安全、文档、API 设计、前端、后端、性能、发布和 Git 工作流。

## 内容清单

```text
agents/   14 个开发 agents
skills/   19 个公开 skills
```

## Agent 分组

- 结构梳理与规划：`dev_code_mapper`、`dev_architect_reviewer`、`dev_docs_researcher`。
- 代码实现：`dev_implementer`、`dev_backend_engineer`、`dev_frontend_engineer`、`dev_python_engineer`、`dev_cli_engineer`。
- 审查与验证：`dev_code_reviewer`、`dev_security_reviewer`、`dev_test_runner`、`dev_performance_engineer`。
- 设计与文档：`dev_api_designer`、`dev_docs_engineer`。

## Skills

```text
accessibility-audit      api-contract-review      bugfix
build-optimization       cli-tooling-workflow     dependency-upgrade
frontend-ui-implementation
fullstack-feature        git-workflow             migration-plan
performance-diagnosis    pr-review                prompt-evaluation
python-quality           refactor-plan            release-check
repo-onboarding          security-review          test-strategy
```

## 使用说明

当任务涉及代码仓库、构建系统、API、UI、测试、安全面或发布流程时，优先使用本 catalog。大范围实现前，优先使用只读的 mapper/reviewer agents。除非某个 skill 明确面向特定工具族，否则示例和说明应保持框架中立。

## 维护说明

不要加入项目私有架构、秘密 workflow 名称、内部 endpoint 或公司特定发布规则。新增开发类 skill 时，应说明触发条件、工作步骤、验证预期、输出格式和明确边界。
