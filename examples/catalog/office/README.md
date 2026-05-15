# Office Catalog

[中文](README_CN.md) | English

Agents and skills for structured office work: meeting minutes, weekly reports, project reports, product planning, briefing notes, and presentation outlines.

## Contents

```text
agents/   5 office agents
skills/   5 public skills
```

## Agent Roles

- `office_meeting_summarizer`: turn notes, transcripts, or chats into minutes, decisions, actions, owners, and open questions.
- `office_weekly_summarizer`: extract weekly progress, blockers, risks, next steps, owners, and missing information.
- `office_report_writer`: draft daily, weekly, monthly, project, or status reports from provided materials.
- `office_product_planner`: consolidate requirements, PRDs, roadmap notes, stakeholder alignment, and success metrics.
- `office_slide_planner`: plan deck storylines, slide outlines, speaker notes, and sharing-session structures.

## Skills

- `meeting-summary`: convert meeting materials into minutes, decisions, actions, and open questions.
- `weekly-report`: draft or review weekly reports from progress logs and source materials.
- `project-report`: draft project status, milestone, risk, or management updates.
- `briefing-note`: produce concise decision-ready briefing notes.
- `ppt-outline`: turn materials into a presentation storyline, outline, or speaker notes.

## Maintenance Notes

Keep business details generic. Do not include private meeting content, names, customer information, roadmap commitments, or internal reporting templates. Outputs should preserve uncertainty and list missing information instead of inventing details.
