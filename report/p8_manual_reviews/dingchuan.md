# dingchuan 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/acupoints/dingchuan.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 13 行
- **条目：** 定喘

## P26 问题段

P26 标记的 source_ref 指向伤寒论大青龙汤、麻杏甘石汤、热喘辨治的大段内容。该段虽然出现“气喘”，但不是“定喘穴”的直接来源，不能支撑穴位定位与归经。

## 来源与 FTS 摘要

- 当前正文保留了该伤寒论气喘大段，同时另有针灸篇来源候选。
- `data/acupoint_sources.jsonl` 有 12 个候选命中，优先命中为针灸篇第 195 页：`奇穴：大椎外五分定喘穴`，直接说明定喘穴位置和针灸治疗气喘语境。
- `data/acupoint_index.jsonl` 为 `verified_direct`，但 P26 指出旧 quote 为 `dirty_quote`。
- `data/source_fts.sqlite` exact MATCH `定喘` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。需注意正文 frontmatter 的长 quote 仍偏向方药气喘，不是最佳 source_ref；但正文内若已有针灸篇定喘段，可后续收窄。
- **registry 后续修复：** 建议后续把 source_ref 收窄到针灸篇第 195 页“大椎外五分定喘穴”直接段，并避免用方药气喘段支撑穴位字段。
- **理由：** 属 source boundary 问题；不在本轮批量改正文。
