# huajiao 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/huajiao.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 119 行
- **条目：** 花椒

## p26 问题段

P26 标记为 `dirty_quote`，来源指向原记录页码；该行 `quote_preview` 显示为目录/OCR/相邻条目残片。

## 来源 / FTS 摘要

P26 与 knowledge quote 来自干漆条目，讲采干漆时四川人用蜀椒/花椒粉防漆味入身。verified_sources 也是干漆段落。 本轮 FTS exact 检索未返回可用命中，判断主要依据 p26 行、knowledge frontmatter、`knowledge_completeness.jsonl` 与 `verified_sources.jsonl`。

## 核查结论

这是旁及提及，不支撑花椒药材条目；建议后续降级或另查花椒独立来源。

## 修改 / 不修改理由

本轮不修改 knowledge 正文、index 或 registry。P26 多数为 needs_review segment，先记录证据边界与后续修复方向。

## 未决问题

- 后续按上方结论同步 source_ref 边界或调整 source_quality；不得把旁及提及继续当作直接来源。
