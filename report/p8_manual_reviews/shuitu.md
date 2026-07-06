# shuitu 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/acupoints/shuitu.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 48 行
- **条目：** 水突

## P26 问题段

P26 quote 从天仓、地仓、青春痘、大迎一路串到人迎/水突/气舍，边界偏宽。后半段有“中间就是水突，再下来就是气舍”“水突比较常用”，可用但不够收窄。

## 来源与 FTS 摘要

- 当前正文摘录包含水突、人迎、气舍的相邻定位及瘰疬、甲状腺肿大语境。
- `data/acupoint_sources.jsonl` 有 5 个候选命中，优先命中为针灸篇第 53 页，直接出现“人迎、中间就是水突，再下来就是气舍”。
- `data/acupoint_index.jsonl` 为 `verified_direct`，P26 仍标 `dirty_quote`。
- `data/source_fts.sqlite` exact MATCH `水突` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。现有正文相关，但 source_ref 可收窄。
- **registry 后续修复：** 建议将 quote 收窄到针灸篇第 53 页从大迎、人迎到水突、气舍的直接段，去掉天仓/地仓/青春痘前置噪声。
- **理由：** 不是错配，而是段落边界过宽。
