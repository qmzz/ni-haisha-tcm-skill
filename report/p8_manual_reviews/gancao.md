# gancao 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/gancao.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 103 行
- **条目：** 甘草

## p26 问题段

P26 标记为 `empty_quote`，来源文件为 `02【视频同步文稿】人-神农本草经（可打印）.json` page 33，`quote_preview` 为空。

## 来源 / FTS 摘要

knowledge frontmatter page 33 摘录直接讲甘草生用、炙甘草入心、未炒入脾等炮制和药性语境。`verified_sources.jsonl` 仍保存 page 16 五色五味总论中“甘草是黄的”的片段，属于旁及提及，不足以支撑甘草条目。FTS exact 本轮未返回可用命中。

## 核查结论

正文有甘草相关直接语境；registry 的旧 quote 边界污染明显，应后续同步到当前 knowledge 使用的 page 33 片段。

## 修改 / 不修改理由

不修改正文。当前问题主要是 verified_sources/source_ref 不一致。

## 未决问题

- 后续清理 `verified_sources.jsonl` 中 page 16 的旁及片段，改为 page 33 甘草炮制直接摘录或更完整甘草独立条目。
