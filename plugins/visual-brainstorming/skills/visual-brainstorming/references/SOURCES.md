# 参考对象、来源与独立实现边界

## 结论

本 Skill 的核心概念参考对象是：

> `obra/superpowers` 项目中的 **Visual Companion / Visual Brainstorming** 工作流。

参考的是“Agent 生成视觉页面 → 本地浏览器展示 → 用户选择回传 → Agent 继续收敛”的交互抽象，不是其品牌或源代码。

入口声明见 `NOTICE.md`；本文件记录具体来源与设计取舍。

## 1. Superpowers Visual Companion

主要参考：

- https://github.com/obra/superpowers/blob/main/skills/brainstorming/visual-companion.md
- https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md
- https://github.com/obra/superpowers/blob/main/RELEASE-NOTES.md

从这些资料中学习的概念：

- 按具体问题、而不是按整场会话决定是否打开浏览器；
- 视觉页面由 Agent 写入文件；
- 本地服务展示页面；
- 浏览器选择被记录并供下一轮读取；
- mockup、架构图、流程图和并排比较适合该媒介；
- 不把浏览器内容描述为模型内部思维展示。

没有直接搬入：

- 第三方服务端实现；
- 第三方品牌、Logo 和视觉样式；
- 长段技能文案；
- 与本 Skill 工具链不匹配的进程或通信实现。

Superpowers 项目采用 MIT License；其具体授权范围以原仓库为准。

## 2. OpenAI Codex Skills 与插件结构

主要参考：

- https://developers.openai.com/codex/skills
- https://developers.openai.com/codex/plugins/build

从中采用的结构原则：

- Skill 是以 `SKILL.md` 为入口的独立目录；
- `scripts/`、`references/`、`assets/` 和 `agents/openai.yaml` 是 Skill 内的可选组成；
- 触发描述应前置、清晰；
- 执行必需规则放在 `SKILL.md`，长背景按需放进 `references/`；
- 插件是分发容器，一个现有插件可以包含多个 Skill；
- 嵌入现有插件的 Skill 不应再携带第二个插件 manifest。

因此，本包只交付一个顶层目录：

```text
visual-brainstorming/
```

## 3. Agent Skills 规范

主要参考：

- https://agentskills.io/specification
- https://agentskills.io/skill-creation/best-practices

采用的原则包括：

- 目录名与 frontmatter `name` 一致；
- `description` 同时说明能力和触发边界；
- 主说明保持聚焦；
- 确定性工作交给脚本；
- 模板、案例和参考文档分层存放。

## 4. Web 与 Python 标准库机制

实现使用：

- Python `ThreadingHTTPServer`；
- `secrets.token_urlsafe` 会话 key；
- `pathlib` 路径边界与符号链接拒绝；
- 临时文件加 `os.replace` 的原子发布；
- JSONL 事件日志；
- sandbox iframe；
- `window.postMessage`；
- URL fragment、origin-scoped `sessionStorage` 与 path capability；
- Content Security Policy；
- HTTP 短轮询与空闲自动关闭。

这些是浏览器和 Python 标准库的通用机制，不依赖远程前端框架。

## 5. 本 Skill 的独立实现选择

| 维度 | 本 Skill |
|---|---|
| 服务 | Python 标准库 |
| 页面更新 | 前台约 1 秒、后台约 5 秒的 HTTP 轮询 |
| 页面隔离 | sandbox iframe + 受控 `postMessage` |
| 事件 | JSONL + 单调递增 ID |
| 发布 | 唯一文件名 + 原子替换 |
| 默认网络 | `127.0.0.1` |
| 会话 | 随机 key + fragment bootstrap + `sessionStorage` + path capability |
| 生命周期 | 默认 2 小时无有效交互自动停止；轮询不保活 |
| 视觉资产 | 自有 CSS、SVG、外壳、模板和案例 |
| 包装 | 独立 Plugin，内含单一 Skill |

## 6. 可借鉴与不可照搬

可以继续借鉴：

- “看图是否显著优于读文字”的触发判断；
- 每屏只解决一个视觉决策；
- 本地页面与结构化反馈闭环；
- 渐进加载文档；
- 会话级 key 和受限文件路径。

不应照搬：

- 第三方品牌、完整措辞和源代码；
- 每次 brainstorm 都自动启动浏览器；
- 未经验证的性能、成本和模型数据；
- 公网暴露本地会话；
- 将视觉页面包装成“模型思维直播”。

最后查阅：2026-07-12。
