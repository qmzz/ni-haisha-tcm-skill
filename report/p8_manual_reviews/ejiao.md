# ejiao 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/ejiao.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 98 行
- **条目：** 阿胶

## p26 问题段

P26 标记为 `empty_quote`，原因是 `source_refs` 缺失或 quote 过短；指向 `02【视频同步文稿】人-神农本草经（可打印）.json` page 155，但 `quote_preview` 为空。

## 来源 / FTS 摘要

当前 knowledge 文件 frontmatter 已有 page 155 的阿胶长摘录，直接讲阿井水制阿胶、阿胶不能煮、补血补心血、安胎止血及月经期禁忌等。`knowledge_completeness` 显示 `verified_direct`。但 `verified_sources.jsonl` 中同条 source_refs 仍指向 page 105 黄连阿胶汤/黄连语境，属于 registry/source_refs 未同步或边界污染。FTS exact 检索本轮未返回可用命中。

## 核查结论

正文有阿胶直接来源，不需要改正文；registry 层仍需把旧的黄连阿胶汤片段替换为 page 155 的阿胶直接摘录。

## 修改 / 不修改理由

本轮不修改正文。问题集中在 p26 记录与 verified_sources 的 quote 边界，不是正文内容错误。

## 未决问题

- 后续同步 `verified_sources.jsonl` / 相关 index 的 source_ref 到 `knowledge/herbs/ejiao.md` 当前 page 155 直接摘录。
