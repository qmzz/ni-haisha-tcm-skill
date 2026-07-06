# luoque 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/acupoints/luoque.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 31 行
- **条目：** 络却

## P26 问题段

P26 标记的 source_ref 来自针灸篇 page 1/JSON 边界，前段仍在讲眉冲、鼻科病，并夹入 page 91 JSON 开头。该段本身不直接支撑络却。

## 来源与 FTS 摘要

- 当前正文“倪师讲解”引用了天柱段前的上下文：`玉枕、通天、络却用的不多。但天柱用的较多`，并另有内耳不平衡语境提到 `络却、中脘、公孙、内关`。
- `data/acupoint_sources.jsonl` 有 8 个候选命中，优先命中为针灸篇第 91 页，出现络却与头晕/水饮停中焦、内耳不平衡语境。
- `data/acupoint_index.jsonl` 为 `verified_direct`，P26 标为 `dirty_quote`。
- `data/source_fts.sqlite` exact MATCH `络却` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。正文摘录为相关但偏旁及，仍可保留学习边界。
- **registry 后续修复：** 建议后续将 source_ref 收窄到针灸篇第 91 页络却直接出现的段落；若要支撑定位/功效，仍需更明确来源。
- **理由：** P26 脏段不可用，但候选证据显示条目非完全无源。
