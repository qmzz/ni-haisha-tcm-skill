# gouqizi 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/gouqizi.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 106 行
- **条目：** 枸杞子

## p26 问题段

P26 标记为 `empty_quote`，指向 `02【视频同步文稿】人-神农本草经（可打印）.json` page 56，`quote_preview` 为空。

## 来源 / FTS 摘要

knowledge frontmatter 与 `verified_sources.jsonl` 均有直接摘录，内容包括枸杞子性味、滋肾养肝、生精润肺、明目、用量与禁忌。摘录后部带下一条柏子仁开头，存在轻微尾部边界污染。FTS exact 本轮未返回可用命中。

## 核查结论

枸杞子直接来源成立。P26 empty_quote 与当前文件状态不一致，应视为历史抽取误报。

## 修改 / 不修改理由

不修改正文。仅建议后续微调 source_ref 尾部边界。

## 未决问题

- 后续把 quote 截止在枸杞子禁忌段，去掉下一条“九十七、柏实”。
