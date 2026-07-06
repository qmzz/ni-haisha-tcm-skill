# danggui 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/danggui.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 88 行
- **条目：** 当归

## P26 问题段

P26 标记为 `empty_quote`。当前 quote 开头讨论“吃当归也会下利”，随后转入药味厚薄、辛甘发散、酸苦涌泄、藏红花等药性总论；有当归提及，但边界过宽。

## 来源与 FTS 摘要

- 当前正文 source_ref 能证明倪师曾讨论当归药味厚、会攻下/下利等，但不足以完整支撑补虚药、性味归经等结构字段。
- `data/herb_sources.jsonl` 记录 80 个候选命中，但摘要 top hit 为空 quote，需后续查找当归独立条目或更直接段落。
- `data/herb_index.jsonl` 为 `verified_direct`，P26 标为 `empty_quote`。
- `data/source_fts.sqlite` exact MATCH `当归` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。
- **registry 后续修复：** 建议后续收窄到当归独立讲解段；当前药性总论可作为补充，不宜作为唯一主 source_ref。
- **理由：** source_ref 相关但边界偏宽，需保守记录。
