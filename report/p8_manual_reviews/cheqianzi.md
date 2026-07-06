# cheqianzi 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/cheqianzi.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 78 行
- **条目：** 车前子

## P26 问题段

P26 标记为 `empty_quote`，队列 quote 为空；当前文件已经有非空讲解摘录。

## 来源与 FTS 摘要

- 当前正文由 `p17_content_quality` 补入神农本草经讲解，开头直接说“第三十四是车前子”，并解释车前子名称来源。
- `data/herb_sources.jsonl` 记录 34 个候选命中，摘要 top hit 的 quote 仍为空，说明 registry 候选需后续同步 P17 正文 quote。
- `data/herb_index.jsonl` 为 `verified_direct`，properties/meridian/category 已有结构字段。
- `data/source_fts.sqlite` exact MATCH `车前子` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。正文已有直接讲解。
- **registry 后续修复：** 建议把 P17 正文中的车前子直接段同步到 index/sources，清理 empty_quote 历史标记。
- **理由：** P26 的空 quote 已由正文补强，但 registry 仍未完全同步。
