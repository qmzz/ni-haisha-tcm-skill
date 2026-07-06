# niuhuang 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/niuhuang.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 153 行
- **条目：** 牛黄

## p26 问题段

P26 标记为 `empty_quote`，`quote_preview` 为空。

## 来源 / FTS 摘要

knowledge 与 verified_sources page 153 直接讲牛黄用于癫痫、小儿出疹/红疹、剂量五分到一钱等；尾部跨入熊脂条目且中间有 OCR 空洞。 FTS exact 本轮未返回可用命中；已对照 knowledge 文件、`knowledge_completeness.jsonl` 与 `verified_sources.jsonl`。

## 核查结论

牛黄来源直接但 quote 边界较脏，后续需截断到牛黄段并清理 OCR 残片。

## 修改 / 不修改理由

本轮不修改正文、index、sources 或 registry。仅记录证据边界、错配与后续修复建议。

## 未决问题

- 后续按本条结论同步 source_ref、收窄 quote 或调整 source_quality。
