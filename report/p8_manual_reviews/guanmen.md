# guanmen 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/acupoints/guanmen.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 18 行
- **条目：** 关门

## P26 问题段

P26 标记的旧 source_ref 来自金匮要略 OCR 重复字与 JSON 边界污染，内容与关门穴无关。

## 来源与 FTS 摘要

- 当前文件已经由 `p17_content_quality` 调整 source_ref，但 frontmatter 仍可见针灸篇第 209 页索引类长段，直接性有限。
- `data/acupoint_sources.jsonl` 有 9 个候选命中，优先命中来自针灸篇第 57 页，直接列出“关门、太乙、滑肉门”，属于足阳明胃经腹部穴位序列。
- `data/acupoint_index.jsonl` 为 `verified_direct`，P26 仍保留旧 `dirty_quote` 标记。
- `data/source_fts.sqlite` exact MATCH `关门` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。正文未见明显需要删除的医学串联污染。
- **registry 后续修复：** 建议优先使用针灸篇第 57 页“关门、太乙、滑肉门”直接段替换索引/金匮脏段；第 209 页索引段不宜作为主 source_ref。
- **理由：** 需要后续 source_ref 收窄，不宜在 p26 note 阶段批量改正文。
