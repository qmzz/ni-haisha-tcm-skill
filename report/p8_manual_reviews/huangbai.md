# huangbai 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/huangbai.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 120 行
- **条目：** 黄柏

## p26 问题段

P26 标记为 `empty_quote`，来源指向原记录页码；该行 `quote_preview` 为空。

## 来源 / FTS 摘要

knowledge/verified_sources page 21 是药材取枝、皮、心的总论，举例“黄柏取皮达皮肤”，不是黄柏独立讲解。 本轮 FTS exact 检索未返回可用命中，判断主要依据 p26 行、knowledge frontmatter、`knowledge_completeness.jsonl` 与 `verified_sources.jsonl`。

## 核查结论

当前证据为理论举例旁及，不足以 `verified_direct` 支撑黄柏条目；建议后续查直接来源或降级。

## 修改 / 不修改理由

本轮不修改 knowledge 正文、index 或 registry。P26 多数为 needs_review segment，先记录证据边界与后续修复方向。

## 未决问题

- 后续按上方结论同步 source_ref 边界或调整 source_quality；不得把旁及提及继续当作直接来源。
