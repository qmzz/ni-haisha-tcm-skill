# chuanxiong 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/chuanxiong.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 81 行
- **条目：** 川芎

## P26 问题段

P26 标记为 `empty_quote`，队列 quote 为空；当前文件已补入长 quote。

## 来源与 FTS 摘要

- 当前正文由 `p17_content_quality` 补入神农本草经讲解：川芎旧名芎穷，味辛性温，用于肝病、头痛、妇科等倪师讲解上下文。
- `data/herb_sources.jsonl` 记录 80 个候选命中，但摘要 top hit 为空 quote，需后续同步正文 quote。
- `data/herb_index.jsonl` 为 `verified_direct`，结构字段为辛温、肝胆心包、活血化瘀药。
- `data/source_fts.sqlite` exact MATCH `川芎` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。
- **registry 后续修复：** 建议将当前正文第 103 页川芎直接讲解同步回 herb_sources/index，清理 empty_quote 标记。
- **理由：** 直接讲解存在，问题是历史队列与 registry quote 未同步。
