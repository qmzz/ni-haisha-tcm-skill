# dicang 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/acupoints/dicang.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 12 行
- **条目：** 地仓

## P26 问题段

P26 source_ref 指向 `倪海厦人纪系列之伤寒论.json` 第 1 页葛根升津、发汗、肠胃津液等语境，且混入 JSON 页边界残留。该段不是地仓穴讲解。

## 来源与 FTS 摘要

- 当前正文已引用针灸篇面部中风、地仓透颊车、流涎等直接语境。
- `data/acupoint_sources.jsonl` 有 32 个候选命中，优先命中为针灸篇第 174 页，直接出现“面部中风，光针地仓没有用，一定要地仓透颊车”。
- `data/acupoint_index.jsonl` 为 `verified_direct`，P26 标记为 `dirty_quote`。
- `data/source_fts.sqlite` exact MATCH `地仓` 未返回结果；候选 jsonl 足以说明 source_ref 后续可替换方向。

## 复核结论

- **正文修复：** 本轮不改。正文与候选来源一致，边界可接受。
- **registry 后续修复：** 建议将伤寒论葛根误段替换为针灸篇第 174 页地仓透颊车直接段。
- **理由：** 问题为 source_ref 串错来源；正文暂无明显污染。
