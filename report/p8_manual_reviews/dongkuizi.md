# dongkuizi 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/dongkuizi.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 95 行
- **条目：** 冬葵子

## P26 问题段

P26 标记为 `empty_quote`，但当前文件已有长 quote。quote 直接讲“这个药叫冬葵子”，并讨论与姑活可能为南北差异、下乳、痈疽出头等语境。

## 来源与 FTS 摘要

- 当前正文已由 P17 补入冬葵子直接讲解。
- `data/herb_sources.jsonl` 记录 24 个候选命中，但摘要 top hit 为空 quote，需同步正文。
- `data/herb_index.jsonl` 为 `verified_direct`，但本轮发现结构字段异常：`properties` 与 `meridian` 混入了 Markdown 片段（功效/主治文本），需后续字段清理。
- `data/source_fts.sqlite` exact MATCH `冬葵子` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。
- **registry 后续修复：** 建议同步第 173 页冬葵子直接 quote，并专项修复 herb_index 的 properties/meridian 字段串联污染。
- **理由：** 直接来源存在，但 registry 字段存在明显结构污染。
