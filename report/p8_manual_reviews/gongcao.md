# gongcao 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/gongcao.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 105 行
- **条目：** 茺蔚子

## p26 问题段

P26 标记为 `empty_quote`，来源文件为 `02【视频同步文稿】人-神农本草经（可打印）.json` page 30，`quote_preview` 为空。

## 来源 / FTS 摘要

knowledge frontmatter page 30 有“二十八、充蔚子”条目，正文含本经原文、产地、性味、主治、禁忌、益母草附录等；虽标题写作“充蔚子”，内容说明“即茺蔚子”。`verified_sources.jsonl` 也有直接长摘录，但前部带牛膝段尾。FTS exact 检索“茺蔚子”未返回可用命中。

## 核查结论

来源直接支撑茺蔚子，主要问题是 OCR/异体写法“充蔚子”和 quote 前部带上一条牛膝尾巴。

## 修改 / 不修改理由

不修改正文。当前正文可保留；后续只需收窄 source_ref 边界并记录异名。

## 未决问题

- 后续将 source_ref 起点收窄到“二十八、充蔚子”，避免带牛膝段尾。
