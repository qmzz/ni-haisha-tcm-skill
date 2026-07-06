# gaohuangshu 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/acupoints/gaohuangshu.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 17 行
- **条目：** 膏肓俞

## P26 问题段

P26 标记 page 1 脏段，但 quote 内容本身是膏肓痛、肩胛骨、放血处理的直接讲解，尾部有“视频作‘膏肓俞’”注记。问题主要是页码/JSON 抽取边界不佳，不是完全错配。

## 来源与 FTS 摘要

- 当前正文 frontmatter 与“倪师讲解”均使用该膏肓痛直接段。
- `data/acupoint_sources.jsonl` 仅 1 个候选命中，来自针灸篇第 103 页，内容同样指向膏肓痛与放血语境，并带“视频作‘膏肓俞’”注记。
- `data/acupoint_index.jsonl` 为 `verified_direct`，P26 仍标 `empty_or_dirty_quote`。
- `data/source_fts.sqlite` exact MATCH `膏肓俞` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。现有摘录虽页码/边界需修，但内容直接相关。
- **registry 后续修复：** 建议将 page_num 从脏 page 1 来源同步为针灸篇第 103 页候选，并保留“膏肓/膏肓俞”异文说明。
- **理由：** P26 风险为 metadata 边界，不是正文污染。
