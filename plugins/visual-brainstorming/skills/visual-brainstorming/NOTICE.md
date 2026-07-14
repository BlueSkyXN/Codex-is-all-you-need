# Reference and Implementation Notice

## 参考对象

本 Skill 的**概念参考对象**是 `obra/superpowers` 项目中的 **Visual Companion / Visual Brainstorming** 工作流，主要参考：

- `skills/brainstorming/visual-companion.md`
- `skills/brainstorming/SKILL.md`
- `RELEASE-NOTES.md`

公开地址：

- https://github.com/obra/superpowers/blob/main/skills/brainstorming/visual-companion.md
- https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md
- https://github.com/obra/superpowers/blob/main/RELEASE-NOTES.md

借鉴的是以下交互抽象：

1. 只在具体问题确实适合视觉表达时启用浏览器；
2. Agent 生成 HTML 视觉页面；
3. 本地服务展示最新页面；
4. 用户在浏览器中选择或提交反馈；
5. Agent 读取结构化事件并继续收敛方案。

## 独立实现声明

本 Skill 不是 Superpowers 的分支、官方移植或兼容层，也不代表与其作者存在隶属或背书关系。

本目录中的 Python 服务、HTTP 接口、事件格式、浏览器外壳、CSS、SVG、模板、案例和中文技能说明均为独立实现。实现采用：

- Python 标准库 HTTP 服务；
- HTTP 短轮询；
- sandbox iframe 与受控 `postMessage`；
- JSONL 事件；
- 原子页面发布；
- 自有视觉样式与示例。

没有把第三方的服务端源代码、品牌视觉或长段技能文案直接复制进本 Skill。Superpowers 项目本身采用 MIT License；其具体授权范围以原项目仓库为准。

## Skill 结构参考

目录结构与元数据设计参考 OpenAI Codex Skills 文档和 Agent Skills 规范：

- https://developers.openai.com/codex/skills
- https://developers.openai.com/codex/plugins/build
- https://agentskills.io/specification
- https://agentskills.io/skill-creation/best-practices

完整来源分类与设计取舍见 `references/SOURCES.md`。

最后查阅：2026-07-12。
