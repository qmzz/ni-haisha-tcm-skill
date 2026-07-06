# duhuo 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/duhuo.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 96 行
- **条目：** 独活

## P26 问题段

P26 标记为 `empty_quote`。当前 quote 主要讲麝香开窍与诸窍闭塞，旁及“风塞的用独活羌活”，随后继续麝香/当归/急救语境。该段不构成独活独立讲解。

## 来源与 FTS 摘要

- 当前 source_ref 为麝香/开窍段中的独活羌活旁及。
- `data/herb_sources.jsonl` 记录 39 个候选命中，但摘要 top hit 为空 quote；本轮未见独活独立讲解。
- `data/herb_index.jsonl` 为 `verified_direct`，P26 标为 `empty_quote`。
- `data/source_fts.sqlite` exact MATCH `独活` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。
- **registry 后续修复：** 建议重查独活直接来源；若无独立讲解，应降级为旁及/contextual，不支撑性味归经。
- **理由：** 当前证据只是“风塞用独活羌活”的旁及提及。
