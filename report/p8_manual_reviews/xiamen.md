# xiamen 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/acupoints/xiamen.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 54 行
- **条目：** 侠白（xiamen）

## P26 问题段

P26 source_ref 与 `xiabai` 相同，来自黄帝内经上册经脉/滑脉讲解大段，属于宽泛旁证，不适合作为侠白穴主 source_ref。

## 来源与 FTS 摘要

- 当前文件 title 为“侠白”，并带 `alias_of: "xiabai"`；但 index 显示 `meridian: 足阳明胃经`，与侠白应属手太阴肺经不一致。
- `data/acupoint_sources.jsonl` 对该 item 返回的仍是侠白候选，优先为针灸篇第 42 页“侠白在天府下一寸”。
- `data/acupoint_index.jsonl` 为 `verified_direct`，但该重复/别名条目的归经字段存在明显疑点。
- `data/source_fts.sqlite` exact MATCH `侠白` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改，避免在 p26 队列中批量处理别名合并。
- **registry 后续修复：** 建议单列 `xiamen`/`xiabai` 别名与重复条目修复：确认是否应删除重复、改为 alias-only，或同步为手太阴肺经；同时替换 source_ref 为针灸篇第 42 页。
- **理由：** 这里不仅是 dirty quote，还存在 item_id/title/alias/meridian 数据一致性问题，需专项处理。
