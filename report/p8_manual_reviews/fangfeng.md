# fangfeng 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/fangfeng.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 99 行
- **条目：** 防风

## p26 问题段

P26 标记为 `empty_quote`，来源文件为 `02【视频同步文稿】人-神农本草经（可打印）.json` page 112，`quote_preview` 为空。

## 来源 / FTS 摘要

当前 knowledge 文件与 `verified_sources.jsonl` 均有 page 112 直接摘录，内容明确出现“第六十味药，防风”，并讲防风辛甘发散、去风、风湿关节、头痛、发表散寒等。`knowledge_completeness` 为 `verified_direct`。FTS exact 检索未返回可用命中。

## 核查结论

防风已有直接来源。P26 的 empty_quote 更像生成 p26 时未取到 quote，而不是当前正文或 registry 缺证。

## 修改 / 不修改理由

不修改正文或 registry。本轮只记录 P26 与当前状态差异。

## 未决问题

- 如后续重建 P26，应以当前 `source_refs` 重新计算，避免继续保留 empty_quote 误报。
