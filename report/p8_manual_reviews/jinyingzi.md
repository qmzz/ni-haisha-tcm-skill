# jinyingzi 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/jinyingzi.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 77 行
- **条目：** 金樱子

## 当前文件概况

当前条目为 herb，trace_status 为 `verified`。p11 缺失字段为 `properties, meridian`。

## 来源 / FTS 摘要

source_refs 指向 page 48，LIKE 命中 1 条；命中窗口只直接出现太乙金锁丹中使用金樱子，原 Markdown/registry quote 同时串入旋覆花、兰草、蛇床子等相邻条目。FTS MATCH 未返回，LIKE 可定位原页。

## 是否直接支撑缺失字段

不直接支撑。该页直接支撑金樱子作为太乙金锁丹组分及用量/禁忌语境，但未给出金樱子性味或归经。

## 修改 / 不修改理由

已手工收窄 knowledge/herbs/jinyingzi.md 的 frontmatter quote、倪师讲解和来源摘录，删除相邻旋覆花/兰草/蛇床子污染段落；不补 properties/meridian。

## 未决问题

data/herb_index.jsonl 与 verified_sources.jsonl 仍保存较宽污染 quote，后续可做 registry 同步清理；金樱子性味/归经仍需直接来源或外部权威来源。
