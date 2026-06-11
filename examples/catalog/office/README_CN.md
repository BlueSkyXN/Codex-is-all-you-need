# Office Catalog / 办公目录

[English](README.md) | 中文

这里存放结构化办公任务相关 agents 与 skills，覆盖会议纪要、周报、项目报告、产品规划、简报和演示大纲。

## 内容清单

```text
agents/   5 个办公 agents
skills/   5 个公开 skills
```

## Agent 角色

- `office_meeting_summarizer`：将会议记录、转写或聊天记录整理为纪要、决策、行动项、负责人和开放问题。
- `office_weekly_summarizer`：提取周进展、阻塞、风险、下一步、负责人和缺失信息。
- `office_report_writer`：基于素材起草日报、周报、月报、项目报告或状态报告。
- `office_product_planner`：整理需求、PRD、路线图、干系人对齐记录和成功指标。
- `office_slide_planner`：规划演示叙事、PPT 大纲、speaker notes 和分享结构。

## Skills

- `office-meeting-summary`：将会议材料转成纪要、决策、行动项和开放问题。
- `office-weekly-report`：基于进展记录和素材起草或复核周报。
- `office-project-report`：起草项目状态、里程碑、风险或管理汇报。
- `office-briefing-note`：生成简洁、可用于决策的 briefing note。
- `office-ppt-outline`：将素材整理为演示叙事、大纲或 speaker notes。

## 维护说明

业务细节应保持通用。不要加入私有会议内容、人员姓名、客户信息、路线图承诺或内部汇报模板。输出应保留不确定性，列明缺失信息，不要编造细节。
