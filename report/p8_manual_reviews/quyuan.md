# quyuan 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/acupoints/quyuan.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 39 行
- **条目：** 曲垣

## P26 问题段

P26 标记的 source_ref 为 JSON 边界残留，frontmatter 中甚至只有 `00703（第四次修改） 85`，明显不可用。

## 来源与 FTS 摘要

- 当前正文“倪师讲解”有针灸篇曲垣、秉风段，说明肩井往后直下三寸为曲垣，曲垣再旁开两寸为秉风，并提示肩部经络辨别。
- `data/acupoint_sources.jsonl` 有 7 个候选命中，优先命中为针灸篇第 86 页，直接出现“从肩井穴往后，直下三寸，就是...曲垣”。
- `data/acupoint_index.jsonl` 为 `verified_direct`，但 P26 标记旧 source_ref 为脏段。
- `data/source_fts.sqlite` exact MATCH `曲垣` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。正文摘录直接相关。
- **registry 后续修复：** 建议将 frontmatter/index 的脏 JSON 片段替换为针灸篇第 86 页曲垣直接段。
- **理由：** 来源可追溯，问题在 source_ref 抽取边界。
