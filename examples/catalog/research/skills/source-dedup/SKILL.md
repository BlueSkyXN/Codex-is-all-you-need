---
name: source-dedup
description: Use when deduplicating overlapping research materials, AI notes, excerpts, transcripts, and source packs.
---

# Source deduplication workflow

Use this skill when multiple materials may overlap, repeat the same source, summarize the same source differently, or contain duplicated excerpts.

## Steps

1. Inventory all materials and assign stable source identifiers.
2. Group likely duplicates and near-duplicates by title, URL, author, date, filename, excerpt overlap, and topic.
3. Identify canonical sources when possible.
4. Separate primary sources from summaries, AI-generated notes, commentary, and derivative materials.
5. Preserve unique details even when sources overlap.
6. Flag materials with missing metadata.
7. Return a deduplication map before synthesis.

## Do not

- Delete or overwrite original materials.
- Treat a summary as a primary source when the primary source exists.
- Merge conflicting versions without noting the conflict.
- Invent missing metadata.

## Output

Return:

1. Source inventory
2. Duplicate groups
3. Canonical source candidates
4. Unique materials
5. Missing metadata
6. Recommended source set for synthesis
