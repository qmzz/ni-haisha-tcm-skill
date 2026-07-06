# dilong 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/dilong.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 93 行
- **条目：** 地龙

## P26 问题段

P26 标记为 `empty_quote`，队列 quote 为空；当前文件已有长 quote。

## 来源与 FTS 摘要

- 当前正文由 `p17_content_quality` 补入神农本草经讲解，直接说明白颈蚯蚓俗名地龙、味咸寒、解毒、攻坚、干血痨、脑积水/脑瘤语境以及用量注意。
- `data/herb_sources.jsonl` 记录 35 个候选命中，但摘要 top hit 为空 quote，需同步正文 quote。
- `data/herb_index.jsonl` 为 `verified_direct`，结构字段为咸寒、肝脾膀胱。
- `data/source_fts.sqlite` exact MATCH `地龙` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。
- **registry 后续修复：** 建议同步第 315 页地龙直接讲解，清理 empty_quote 标记。
- **理由：** 当前正文已有直接来源，registry 仍有历史空 quote。
