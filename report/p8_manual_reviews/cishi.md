# cishi 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/cishi.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 82 行
- **条目：** 磁石

## P26 问题段

P26 标记为 `empty_quote`。当前 frontmatter quote 实际是丹砂条目，只有“畏磁石恶盐水”一句旁及磁石，随后继续丹砂主治、别录、禁忌等；不支撑磁石药材条目。

## 来源与 FTS 摘要

- 当前正文开头来源为丹砂段，存在相邻/旁及污染风险。
- `data/herb_sources.jsonl` 记录 34 个候选命中，但摘要 top hit 为空 quote，本轮未见磁石独立讲解证据。
- `data/herb_index.jsonl` 为 `verified_direct`，但 P26 标为 `empty_quote`。
- `data/source_fts.sqlite` exact MATCH `磁石` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。
- **registry 后续修复：** 建议降级或重查磁石独立来源；现有丹砂“畏磁石”旁及段不应支撑磁石 properties/meridian。
- **理由：** 明显 source boundary 错配，需专项修复。
