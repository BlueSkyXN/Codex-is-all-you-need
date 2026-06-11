---
name: meeting-summary
description: Use when converting meeting notes, transcripts, or chat logs into minutes, decisions, action items, and open questions.
---


## Purpose

Produce concise meeting minutes that preserve decisions and follow-ups.

## Inputs

Use provided materials, such as:

- meeting transcripts
- notes
- chat logs
- agenda documents
- audio/video summaries already transcribed by the user

## Process

1. Identify meeting topic, date, participants, and agenda when available.
2. Extract key discussion points.
3. Distinguish decisions from discussion.
4. Extract action items with owner, deadline, and dependency when available.
5. List open questions, risks, and missing information.
6. Preserve source references when useful.

## Recommended structure

```text
1. Meeting summary
2. Key discussion points
3. Decisions
4. Action items
5. Open questions
6. Risks / blockers
7. Missing information
```

## Rules

- Do not invent decisions, owners, deadlines, or commitments.
- If owner or deadline is unclear, mark it as unspecified.
- Do not hide disagreements or unresolved items.
- Keep minutes action-oriented.

## Output

Return:

1. Meeting purpose
2. Decisions
3. Action items
4. Open questions
5. Missing information
