# xiabai 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/acupoints/xiabai.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 53 行
- **条目：** 侠白

## P26 问题段

P26 source_ref 指向黄帝内经上册经脉/滑脉讲解大段，其中列出手太阴肺经穴位序列 `中府→云门→天府→侠白...`。该段可证明名称出现在经脉序列，但不适合作为侠白穴主讲解 source_ref。

## 来源与 FTS 摘要

- 当前正文 frontmatter 使用黄帝内经宽段；正文还应结合针灸篇侠白段。
- `data/acupoint_sources.jsonl` 有 14 个候选命中，优先命中为针灸篇第 42 页：`侠白在天府下一寸`，并讲天府、侠白用于流鼻血的随寸针语境。
- `data/acupoint_index.jsonl` 为 `verified_direct`。
- `data/source_fts.sqlite` exact MATCH `侠白` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。
- **registry 后续修复：** 建议以针灸篇第 42 页侠白直接讲解替换黄帝内经经脉宽段。
- **理由：** 黄帝内经段是经脉序列旁证，针灸篇候选才是穴位主 source。
