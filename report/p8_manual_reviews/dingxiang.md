# dingxiang 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/dingxiang.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 94 行
- **条目：** 丁香

## P26 问题段

P26 quote 实际在讲桂枝，旁及“豆蔻、大茴小茴香、丁香、肉桂”等香料产地，随后继续桂枝主治。该段不支撑丁香药材条目。

## 来源与 FTS 摘要

- 当前正文 frontmatter 使用桂枝讲解段，属于相邻/旁及污染。
- `data/herb_sources.jsonl` 显示 `source_hit_count=2`，本轮摘要未输出非空 top quote；未见丁香独立讲解证据。
- `data/herb_index.jsonl` 为 `verified_direct`，P26 标为 `dirty_quote`。
- `data/source_fts.sqlite` exact MATCH `丁香` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。
- **registry 后续修复：** 建议降级或重查丁香直接来源；现有桂枝香料旁及段不应支撑丁香性味归经。
- **理由：** 明显主语错配，需后续 source boundary 修复。
