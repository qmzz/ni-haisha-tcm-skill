# fuling 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/fuling.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 102 行
- **条目：** 茯苓

## p26 问题段

P26 标记为 `empty_quote`，指向 `02【视频同步文稿】人-神农本草经（可打印）.json` page 23，`quote_preview` 为空。

## 来源 / FTS 摘要

knowledge frontmatter 的 page 23 摘录主要是药物相需相恶、五脏补泻等总论，只有“白术跟茯苓常常放在一起”之类旁及。`verified_sources.jsonl` 记录 page 68 白术段落，讲白术与茯苓并用、茯苓甘淡渗湿、利尿。该证据提到茯苓药性，但仍偏白术条目语境，非独立茯苓条目。FTS exact 本轮未返回可用命中。

## 核查结论

当前来源可支撑“白术茯苓并用/茯苓利水渗湿”局部语义，但 `verified_direct` 边界偏乐观；建议后续查找独立茯苓条目或降级为 contextual。

## 修改 / 不修改理由

不修改正文。P26 是 needs_review segment，本轮仅标记 source boundary 风险。

## 未决问题

- 后续复查是否存在茯苓独立条目；若无，应同步 registry 降级为 `verified_contextual` 或候选来源。
