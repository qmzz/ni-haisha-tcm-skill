# chantui 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/chantui.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 24 行
- **条目：** 蝉蜕

## 当前文件概况

文件为 P17 content quality verified 条目，正文已有别名、性味、功效、主治、剂量和两段完整讲解。P11 队列标记缺失 `meridian`。

## 来源 / FTS 摘要

FTS 检索“蝉蜕”命中《神农本草经》20、251 页和《金匮要略》484 页等。正文 source_refs 已整理到第 251、318 页，内容直接支撑蝉蜕/雀瓮、质轻、皮肤病、眼翳、剂量等语境。未见明确归经字段。

## 核查结论

现有来源支撑正文主要内容，但不支撑补归经。`herb_index` 的 source_ref 仍停留在第 11 页剂量单位泛论片段，与 Markdown frontmatter 已不同步，属于后续索引同步问题。

## 修改/不修改理由

本轮未改知识正文，不补 `meridian`。正文医学安全边界存在，未发现来源不支撑的明显扩写需要立即删除。

## 未决问题

建议后续同步 `herb_index` source_refs 到 Markdown 中较干净的第 251/318 页引用。