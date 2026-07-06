# chuanshanjia 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/chuanshanjia.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 27 行
- **条目：** 穿山甲

## 当前文件概况

文件为 verified 药材条目，P11 标记缺失 `properties` 与 `meridian`。正文与 frontmatter source_ref 含穿山甲民间方片段，但随后大段串入升麻、青蘘/胡麻等相邻条目内容。

## 来源 / FTS 摘要

`herb_index` 为 `verified_direct`，但 source_ref 来自整理版 52 页，主要是“王不留行，穿山甲...”民间方提及，后续接入升麻条。FTS 检索可确认穿山甲被提及，但未见穿山甲自身性味、归经的直接来源。

## 核查结论

当前正文存在结构字段串联污染和 source boundary 不清。不能用现有片段补 `properties` 或 `meridian`。

## 修改/不修改理由

本轮只写 review note，未改正文。该条需要单独清理：至少应删除升麻、胡麻等非穿山甲内容，并保留为配伍/民间方提及边界，或重新检索直接来源后再重建。

## 未决问题

优先进入后续内容质量清理；同时涉及动物药和现实保护/合规风险，扩写需更严格来源和安全边界。