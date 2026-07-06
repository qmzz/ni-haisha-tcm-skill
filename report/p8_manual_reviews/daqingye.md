# daqingye 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/daqingye.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 91 行
- **条目：** 大青叶

## P26 问题段

P26 quote 主要讲青黛/蓝实粉末剂量、外用蛇毒、兰草和大青叶烘焙关系。它与“大青叶”有关，但核心讲解对象更偏青黛/蓝实，边界需要保守。

## 来源与 FTS 摘要

- 当前正文使用该青黛/蓝实段作为 source_ref。
- `data/herb_sources.jsonl` 显示 `source_hit_count=1`，本轮摘要未输出非空 top quote。
- `data/herb_index.jsonl` 为 `verified_direct`，P26 标为 `dirty_quote`。
- `data/source_fts.sqlite` exact MATCH `大青叶` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。
- **registry 后续修复：** 建议后续确认大青叶与青黛/蓝实的条目边界；若无法找到大青叶独立讲解，应降为 contextual 或标注“由青黛/蓝实制作来源旁及”。
- **理由：** 现有证据相关但主语不完全一致，需避免过度支撑结构字段。
