# kunbu 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/kunbu.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 131 行
- **条目：** 昆布

## p26 问题段

P26 标记为 `empty_quote`；`quote_preview` 为空。

## 来源 / FTS 摘要

knowledge frontmatter page 224 是海藻讲解中提到“海藻/昆布差不多，藻类利小便”；verified_sources 则是海藻条目“海藻昆布皆生于水中”。 本轮 FTS exact 检索未返回可用命中；已对照 knowledge 文件、`knowledge_completeness.jsonl` 与 `verified_sources.jsonl`。

## 核查结论

当前为海藻条目中的昆布旁及/类比，不足以作为昆布独立直接来源；建议查昆布独立来源或降级 contextual。

## 修改 / 不修改理由

本轮不修改正文、index、sources 或 registry。对直接来源仅记录边界清理；对旁及提及仅记录降级/补源建议。

## 未决问题

- 后续按本条结论处理 source_ref 同步、边界收窄、重复条目或 source_quality 调整。
