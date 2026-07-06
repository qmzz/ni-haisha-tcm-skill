# heshouwu 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/heshouwu.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 114 行
- **条目：** 何首乌

## p26 问题段

P26 标记为 `dirty_quote`，来源指向原记录页码；该行 `quote_preview` 显示为目录/OCR/相邻条目残片。

## 来源 / FTS 摘要

P26/knowledge frontmatter 的 quote 是《汉唐中医方剂讲解》目录页，列出 HT-97 何首乌丸等，属于目录/OCR 残片。verified_sources 另有 page 10 丸散膏丹总论中“何首乌/首乌可以熬成膏”，也是旁及。 本轮 FTS exact 检索未返回可用命中，判断主要依据 p26 行、knowledge frontmatter、`knowledge_completeness.jsonl` 与 `verified_sources.jsonl`。

## 核查结论

当前证据不支撑何首乌药材 `verified_direct`，建议后续查找独立来源或降级。

## 修改 / 不修改理由

本轮不修改 knowledge 正文、index 或 registry。P26 多数为 needs_review segment，先记录证据边界与后续修复方向。

## 未决问题

- 后续按上方结论同步 source_ref 边界或调整 source_quality；不得把旁及提及继续当作直接来源。
