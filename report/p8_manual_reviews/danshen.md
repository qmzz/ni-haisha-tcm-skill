# danshen 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/danshen.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 90 行
- **条目：** 丹参

## P26 问题段

P26 标记为 `empty_quote`，队列 quote 为空；当前文件已有完整 quote。

## 来源与 FTS 摘要

- 当前正文由 `p17_content_quality` 补入神农本草经讲解，直接说明丹参味苦微寒、活血化瘀、利水补气、妇科常用、“一味抵四物汤”等。
- `data/herb_sources.jsonl` 记录 44 个候选命中，但摘要 top hit 为空 quote，需要同步正文长 quote。
- `data/herb_index.jsonl` 为 `verified_direct`，结构字段为苦微寒、心肝、活血化瘀药。
- `data/source_fts.sqlite` exact MATCH `丹参` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。
- **registry 后续修复：** 建议同步第 118 页丹参直接段，清理 empty_quote 标记。
- **理由：** 直接来源明确，问题为历史空 quote 未同步。
