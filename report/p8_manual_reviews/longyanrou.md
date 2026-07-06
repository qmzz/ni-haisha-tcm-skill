# longyanrou 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/longyanrou.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 137 行
- **条目：** 龙眼肉

## p26 问题段

P26 标记为 `dirty_quote`；`quote_preview` 含相邻条目或本条尾部跨段残片。

## 来源 / FTS 摘要

P26/knowledge/verified_sources page 242 直接讲龙眼养心安神、血虚怔忡劳神健忘、气血虚可食等，尾部带下一条“松萝”开头导致 dirty_quote。 FTS exact 本轮无可用返回；证据来自 p26 行、knowledge 文件、`knowledge_completeness.jsonl` 与 `verified_sources.jsonl` 对照。

## 核查结论

龙眼肉直接来源成立，问题是 quote 尾部跨入下一条。

## 修改 / 不修改理由

本轮不修改正文或 registry。直接来源先记录边界问题；错配/旁及来源先记录降级或补源建议。

## 未决问题

- 后续按本条结论清理 source_ref、同步 registry 或调整 source_quality。
