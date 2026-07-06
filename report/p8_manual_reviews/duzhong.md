# duzhong 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/duzhong.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 97 行
- **条目：** 杜仲

## P26 问题段

P26 标记为 `empty_quote`，队列 quote 为空；当前文件已有长 quote。

## 来源与 FTS 摘要

- 当前正文由 `p17_content_quality` 补入神农本草经讲解，直接说明第 107 杜仲、产地、真伪鉴别、妇科常用、补筋骨壮腰肾、腰背痛/坐骨神经痛等。
- `data/herb_sources.jsonl` 记录 42 个候选命中，但摘要 top hit 为空 quote，需同步正文长 quote。
- `data/herb_index.jsonl` 为 `verified_direct`，结构字段为甘温、肝肾、补虚药。
- `data/source_fts.sqlite` exact MATCH `杜仲` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。
- **registry 后续修复：** 建议同步第 147 页杜仲直接讲解，清理 empty_quote 标记。
- **理由：** 直接来源明确，问题为历史空 quote 与 registry 未同步。
