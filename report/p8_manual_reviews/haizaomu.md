# haizaomu 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/haizaomu.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 112 行
- **条目：** 海藻

## p26 问题段

P26 标记为 `empty_quote`，来源指向原记录页码；该行 `quote_preview` 为空。

## 来源 / FTS 摘要

knowledge 与 verified_sources 均有 page 224 直接摘录，明确“第一百九十二，海藻”，讲海藻作为长寿零食、咸能软坚、甲状腺/淋巴结语境。 本轮 FTS exact 检索未返回可用命中，判断主要依据 p26 行、knowledge frontmatter、`knowledge_completeness.jsonl` 与 `verified_sources.jsonl`。

## 核查结论

直接来源成立；P26 empty_quote 是历史抽取缺口。

## 修改 / 不修改理由

本轮不修改 knowledge 正文、index 或 registry。P26 多数为 needs_review segment，先记录证据边界与后续修复方向。

## 未决问题

- 后续按上方结论同步 source_ref 边界或调整 source_quality；不得把旁及提及继续当作直接来源。
