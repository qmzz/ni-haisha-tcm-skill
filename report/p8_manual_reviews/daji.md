# daji 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/daji.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 87 行
- **条目：** 大戟

## P26 问题段

P26 标记为 `empty_quote`，但当前文件已补入长 quote。

## 来源与 FTS 摘要

- 当前正文由 `p17_content_quality` 补入神农本草经讲解，直接说明大戟味苦性寒、有小毒、泻脏腑水湿、消水肿、祛痰涎、利大小便及用量判断。
- `data/herb_sources.jsonl` 记录 80 个候选命中，但摘要 top hit 为空 quote，说明 sources registry 仍未同步正文长 quote。
- `data/herb_index.jsonl` 为 `verified_direct`，结构字段为苦寒有毒、肺脾肾、泻下药。
- `data/source_fts.sqlite` exact MATCH `大戟` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。正文已有直接讲解。
- **registry 后续修复：** 建议同步第 292 页大戟直接段到 herb_sources/index，清理 empty_quote 标记。
- **理由：** 当前 P26 问题为历史空 quote，已被正文补强覆盖。
