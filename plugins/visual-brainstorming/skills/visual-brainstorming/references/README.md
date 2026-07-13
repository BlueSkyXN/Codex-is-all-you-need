# Reference Guide

`SKILL.md` 已包含正常执行所需的全部快路径。不要在每次调用时加载本目录；只在出现对应问题时读取一份资料。

## 按任务读取

| 当前任务 | 建议读取 |
|---|---|
| 判断这个功能是否值得使用 | `BACKGROUND.md` |
| 复杂会话或多轮收敛 | `WORKFLOW.md` |
| 编写定制 HTML、CSS、SVG | `VISUAL_AUTHORING.md` |
| 理解服务、iframe 和事件桥 | `ARCHITECTURE.md` |
| 查询高级 CLI、HTTP 和 JSONL | `PROTOCOL.md` |
| 放入现有插件、改名或裁剪 | `ADAPTATION.md` |
| 查看典型输入与反例 | `EXAMPLES.md` |
| 评估触发范围和交付质量 | `EVALUATION.md` |
| 处理端口、刷新和事件问题 | `TROUBLESHOOTING.md` |
| 系统学习整个实现 | `LEARNING_GUIDE.md` |
| 查看公开来源和实现边界 | `SOURCES.md`、`../NOTICE.md` |

## 阅读原则

- 正常使用：`SKILL.md` + 一个 `assets/templates/*.html`；
- 视觉定制：再读 `VISUAL_AUTHORING.md`；
- 运行失败：再读 `TROUBLESHOOTING.md`；
- 维护实现：按需读架构、协议和评估；
- 不在文件之间形成连续深层引用链。
