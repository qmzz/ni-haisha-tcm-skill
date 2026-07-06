# qucha 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/acupoints/qucha.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 37 行
- **条目：** 曲差

## P26 问题段

P26 标记的 quote 从眼科放血、角膜炎讲到“眉冲穴至玉枕穴”，再进入眉冲定位。段内只出现“曲差和神庭的正中间”用于定位眉冲，属于相邻穴位语境，不是曲差直接讲解。

## 来源与 FTS 摘要

- 当前 frontmatter 使用该宽段；正文也主要保留眉冲/神庭/曲差相邻定位语境。
- `data/acupoint_sources.jsonl` 仅 1 个候选命中，来自针灸篇第 90 页，仍为“曲差和神庭的正中间是眉冲”的上下文。
- `data/acupoint_index.jsonl` 为 `verified_direct`，但 P26 已标 `dirty_quote`。
- `data/source_fts.sqlite` exact MATCH `曲差` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。正文无明显串联污染删除需求，但直接来源较弱。
- **registry 后续修复：** 建议后续降为 contextual/needs_review 或补查更直接曲差来源；现有 quote 只能说明曲差作为眉冲定位参照。
- **理由：** 现有证据边界不足以强支撑功效字段，需后续 source quality 细分。
