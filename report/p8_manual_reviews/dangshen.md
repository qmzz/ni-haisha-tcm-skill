# dangshen 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/dangshen.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 89 行
- **条目：** 党参

## P26 问题段

P26 标记为 `empty_quote`，队列 quote 为空；当前文件已补入长 quote。

## 来源与 FTS 摘要

- 当前正文由 `p17_content_quality` 补入神农本草经讲解，说明人参太贵时用党参取代人参，并接续人参本经原文、采收、独参汤等语境。
- `data/herb_sources.jsonl` 记录 56 个候选命中，但摘要 top hit 为空 quote，说明 sources registry 未同步正文长 quote。
- `data/herb_index.jsonl` 为 `verified_direct`，结构字段为甘平、脾肺、补虚药。
- `data/source_fts.sqlite` exact MATCH `党参` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。
- **registry 后续修复：** 建议同步第 60 页党参/人参替代语境到 herb_sources/index，并清理 empty_quote 标记。
- **理由：** 当前正文已有可追溯讲解，P26 问题主要是 registry 历史空 quote。
