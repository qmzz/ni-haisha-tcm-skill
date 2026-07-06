# tongtian 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/acupoints/tongtian.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 51 行
- **条目：** 通天

## P26 问题段

P26 source_ref 是 `黄帝内经.json` 第 1 页整本 JSON 元数据/目录开头，含 `filename / total_pages / full_text / 目录`，属于明显 JSON 碎片，不支撑通天穴。

## 来源与 FTS 摘要

- 当前正文有针灸篇摘录，提到“玉枕、通天、络却用的不多”，但更直接候选在鼻科段。
- `data/acupoint_sources.jsonl` 有 36 个候选命中，优先命中为针灸篇第 172 页：百会外开一寸半再往前一寸为膀胱经通天穴，并说明“通天穴是很有名的鼻科大穴”。
- `data/acupoint_index.jsonl` 为 `verified_direct`，P26 标为 `dirty_quote`。
- `data/source_fts.sqlite` exact MATCH `通天` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。正文可接受，但 source_ref 应替换。
- **registry 后续修复：** 建议以针灸篇第 172 页通天鼻科大穴段替换黄帝内经 JSON 目录碎片。
- **理由：** 直接来源充足，问题为旧 registry source_ref 严重污染。
