# yutang 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/acupoints/yutang.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 60 行
- **条目：** 玉堂

## P26 问题段

P26 source_ref 只有巨阙/心脏诊断尾句与“视频讲解为留豆许”注记，并夹有 page 32 JSON 边界；不能作为玉堂主 source_ref。

## 来源与 FTS 摘要

- 当前正文引用针灸篇肾经胸部穴位段，其中“灵墟在玉堂外开两寸。玉堂穴外开二寸就是灵墟”直接出现玉堂，但更像相邻定位参照。
- `data/acupoint_sources.jsonl` 有 15 个候选命中，优先为针灸篇第 120 页玉堂/灵墟定位；另有第 32 页校对注“本处有误，当为玉堂”。
- `data/acupoint_index.jsonl` 为 `verified_direct`，P26 标为 `dirty_quote`。
- `data/source_fts.sqlite` exact MATCH `玉堂` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。
- **registry 后续修复：** 建议用针灸篇第 120 页玉堂外开二寸的直接定位参照替换 page 1 脏段；若要支撑功效“宽胸降逆”，还需补查更直接讲解。
- **理由：** 当前 source_ref 污染明显，但已有相关候选可供后续收窄。
