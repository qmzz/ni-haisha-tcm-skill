# congbai 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/congbai.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 84 行
- **条目：** 葱白

## P26 问题段

P26 标记为 `empty_quote`。当前 frontmatter quote 实际为防风条目，只有“徐之才曰得葱白行周身”旁及葱白，随后仍是防风主治、用量、禁忌。该段不支撑葱白药材条目。

## 来源与 FTS 摘要

- 当前正文来源存在防风条目污染。
- `data/herb_sources.jsonl` 记录 39 个候选命中，但摘要 top hit 为空 quote；本轮未见葱白独立讲解。
- `data/herb_index.jsonl` 为 `verified_direct`，但 P26 标为 `empty_quote`。
- `data/source_fts.sqlite` exact MATCH `葱白` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。
- **registry 后续修复：** 建议降级或重查葱白直接来源；防风“得葱白”只能作为配伍旁证，不能支撑葱白性味归经。
- **理由：** 明显旁及提及，不符合 verified_direct 主证据。
