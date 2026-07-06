# honghua 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/honghua.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 115 行
- **条目：** 红花

## p26 问题段

P26 标记为 `empty_quote`，来源指向原记录页码；该行 `quote_preview` 为空。

## 来源 / FTS 摘要

knowledge frontmatter 有 page 9 对藏红花、川红花药性差异的直接讲解；verified_sources 同页前半从药名变化总论切入，后续进入红花语境，边界偏宽。 本轮 FTS exact 检索未返回可用命中，判断主要依据 p26 行、knowledge frontmatter、`knowledge_completeness.jsonl` 与 `verified_sources.jsonl`。

## 核查结论

红花来源基本成立，但 source_ref 应收窄到红花讲解起点。

## 修改 / 不修改理由

本轮不修改 knowledge 正文、index 或 registry。P26 多数为 needs_review segment，先记录证据边界与后续修复方向。

## 未决问题

- 后续按上方结论同步 source_ref 边界或调整 source_quality；不得把旁及提及继续当作直接来源。
