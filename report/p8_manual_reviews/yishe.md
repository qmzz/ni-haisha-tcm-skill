# yishe 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/acupoints/yishe.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 58 行
- **条目：** 意舍

## P26 问题段

P26 quote 开头混有 `n俞外开一寸半` 和譩嘻、膈关、魂门等上文，随后进入意舍。段落边界过宽，但后半部分直接讲意舍、脾藏意、腹满虚胀等。

## 来源与 FTS 摘要

- 当前正文引用针灸篇第 104/105 页意舍段。
- `data/acupoint_sources.jsonl` 有 6 个候选命中，优先命中为针灸篇第 105 页“意舍是辅助脾俞的”，以及第 104 页“第十一椎下...意舍，因为脾藏意”。
- `data/acupoint_index.jsonl` 为 `verified_direct`，P26 标为 `dirty_quote`。
- `data/source_fts.sqlite` exact MATCH `意舍` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。
- **registry 后续修复：** 建议将 quote 收窄到针灸篇第 104-105 页意舍直接段，去掉譩嘻/膈关/魂门前置噪声。
- **理由：** 直接来源存在，主要问题是过宽段落边界。
