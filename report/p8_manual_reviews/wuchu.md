# wuchu 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/acupoints/wuchu.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 52 行
- **条目：** 五处

## P26 问题段

P26 quote 仍在眉冲段，且夹有版本页边界；它没有直接讲五处，只能作为相邻头部穴位上下文。

## 来源与 FTS 摘要

- 当前正文已引用针灸篇第 91 页：`神庭后五分就是上星，上星过来一寸半，就是五处`，并说明五处、承光、通天的眼科/鼻科语境。
- `data/acupoint_sources.jsonl` 有 3 个候选命中，优先命中为针灸篇第 91 页五处直接段。
- `data/acupoint_index.jsonl` 为 `verified_direct`，P26 标为 `dirty_quote`。
- `data/source_fts.sqlite` exact MATCH `五处` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。
- **registry 后续修复：** 建议用针灸篇第 91 页“五处”直接段替换眉冲脏段。
- **理由：** 直接来源明确，当前问题为 source_ref 错段。
