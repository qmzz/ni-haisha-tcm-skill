# xinhui 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/acupoints/xinhui.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 55 行
- **条目：** 囟会

## P26 问题段

P26 quote 从素髎、酒糟鼻、水沟、人中讲到尾注“一作囟会，视频作聪会”。该段主要是相邻督脉穴位与异文注记，边界偏宽；直接支撑囟会的力度有限。

## 来源与 FTS 摘要

- 当前正文缺少完整“倪师讲解”段，主要保留来源追溯边界；frontmatter quote 是水沟段尾注。
- `data/acupoint_sources.jsonl` 有 3 个候选命中，优先命中为针灸篇第 38 页尾注“一作囟会，视频作聪会”；另两个为索引页。
- `data/acupoint_index.jsonl` 为 `verified_direct`，但 P26 标为 `dirty_quote`。
- `data/source_fts.sqlite` exact MATCH `囟会` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。
- **registry 后续修复：** 建议降级或补查更直接囟会来源；现有针灸篇命中更像异文/索引命中，不足以支撑功效字段。
- **理由：** source_ref 不是完全错配，但直接性弱，应保持边界。
