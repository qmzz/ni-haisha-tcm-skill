# fengmi 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/fengmi.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 45 行
- **条目：** 蜂蜜

## 当前文件概况

文件为 verified 药材条目，P11 标记缺失 `properties` 与 `meridian`。正文有蜂蜜作为丸剂黏着剂、补中益气、滋润脏腑等讲解，并有 P16 扩展摘录。

## 来源 / FTS 摘要

source_ref 和 FTS 命中第 161 页，明确提到“味甘”“滋养脾胃”“调和营卫”等。P16 扩展摘录有《神农本草经》石蜜“味甘平”内容。未见归经字段。

## 核查结论

现有来源可支撑性味/性状字段“味甘平”或至少“味甘”，但归经无直接来源。本轮不做单点字段同步。

## 修改/不修改理由

未改正文。建议后续结构化同步时补 `properties`，不补 `meridian`。

## 未决问题

后续可清理 P16 扩展摘录过长问题，并统一 Markdown/frontmatter/index 字段。