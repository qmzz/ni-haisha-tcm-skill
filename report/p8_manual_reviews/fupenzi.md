# fupenzi 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/fupenzi.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 47 行
- **条目：** 覆盆子

## 当前文件概况

当前条目为 herb，frontmatter `trace_status: verified`，有 `source_refs`，正文含安全边界、基础信息、倪师讲解、P16 扩展摘录和来源摘录。`knowledge_completeness` 显示 `properties=false`、`meridian=false`，功效、禁忌、倪师讲解与安全边界检查为 true。

## 来源 / FTS 摘要

- `herb_index.jsonl` / `verified_sources.jsonl`：`source_quality_level=verified_direct`，主引用为 `02【视频同步文稿】人-神农本草经（可打印）.json` page 170。
- 主引用直接出现“覆盆子”，并含“本经的原文，味酸平，安五脏，益精气长阴，令坚强志，倍力有子”以及“补涩的要药”“小便太频”“阳不举”等讲解。
- `herb_sources.jsonl` 有 5 个候选命中，含 page 170 与 `倪海厦人纪系列之神农本草经.json` page 71。
- `source_fts.sqlite` 只读检索“覆盆子”有多条命中，包括 `神农本草经.json` 与人纪神农本草经索引/正文页。

## 是否直接支撑缺失字段

- properties：直接支撑。来源明确写“味酸平”。
- meridian：未直接支撑。已查引用未见明确“归经/入某经”表述。

## 修改 / 不修改理由

本轮不修改 Markdown 或 index 结构字段。按 p11 要求，仅在来源明确直接支撑时记录“后续可同步字段”；覆盆子的性味可后续同步为“酸、平”，归经仍不应补写。

## 未决问题

- P16 扩展摘录看起来从 `神农本草经.json` 相邻页大段引入，包含寄生、杜仲、女贞实、木兰等相邻条目内容，存在 source boundary 过宽问题；本轮未清理，建议后续单独做 P16 扩展摘录边界治理。

