# chenxiang 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/chenxiang.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 77 行
- **条目：** 沉香

## P26 问题段

P26 标记为 `empty_quote`。当前 frontmatter quote 虽非空，但内容是柏子仁散/柏子仁丸中方药列表旁及“沉香”，随后进入茯苓条目。该段不支撑沉香药材性味归经。

## 来源与 FTS 摘要

- 当前正文来源边界较弱，主要是方剂组成中旁及沉香。
- `data/herb_sources.jsonl` 记录 26 个候选命中，但本轮摘要只显示第 56 页空 quote，需要后续逐条打开核验是否有沉香独立讲解。
- `data/herb_index.jsonl` 为 `verified_direct`，但 P26 标为 `empty_quote`。
- `data/source_fts.sqlite` exact MATCH `沉香` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。
- **registry 后续修复：** 建议降级或重查沉香直接来源；若只有方剂组成旁及，不应维持 verified_direct 支撑结构字段。
- **理由：** 当前可见证据为旁及提及和相邻茯苓条目污染。
