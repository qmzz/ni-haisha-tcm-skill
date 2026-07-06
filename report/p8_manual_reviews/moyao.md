# moyao 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/moyao.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 148 行
- **条目：** 没药

## p26 问题段

P26 标记为 `empty_quote`，`quote_preview` 为空。

## 来源 / FTS 摘要

knowledge frontmatter page 330 有没药直接讲解，说明没药/乳香为树脂、味苦辛、散血消肿定痛生肌、伤科跌打损伤等；verified_sources 却指牡蛎段落，明显错配。 FTS exact 本轮未返回可用命中；已对照 knowledge 文件、`knowledge_completeness.jsonl` 与 `verified_sources.jsonl`。

## 核查结论

正文有直接来源，但 registry 未同步；需后续把 verified_sources 改为没药 page 330 直接摘录。

## 修改 / 不修改理由

本轮不修改正文、index、sources 或 registry。仅记录证据边界、错配与后续修复建议。

## 未决问题

- 后续按本条结论同步 source_ref、收窄 quote 或调整 source_quality。
