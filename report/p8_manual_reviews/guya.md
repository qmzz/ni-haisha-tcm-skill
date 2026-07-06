# guya 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/guya.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 53 行
- **条目：** 谷芽

## 当前文件概况

当前条目为 herb，frontmatter `trace_status: no_source_found`，有外部来源需求与 no_source 边界。正文基础信息存在字段串联格式问题：性味、归经、功效、主治被合并在一行且归经重复。p11 队列本条 `missing_content_fields=[]`。

## 来源 / FTS 摘要

- `herb_index.jsonl`：`source_quality_level=no_source`，`source_refs=[]`。
- `herb_sources.jsonl`：`status=no_source_found`，`source_hits=[]`。
- `knowledge_completeness.jsonl`：内容字段检查均为 true，但来源质量为 no_source。
- `source_fts.sqlite` 只读检索“谷芽”无命中。

## 是否直接支撑缺失字段

p11 未列缺失字段；现有字段未被内部来源直接支撑。

## 修改 / 不修改理由

本轮不改医学内容。该条有明显 Markdown 字段串联/重复问题，但属于格式清理而非来源支撑；为避免误提升 no_source 条目质量，本轮仅记录问题，不新增或改写医学字段。

## 未决问题

- 建议后续做 no_source 条目的格式降噪：把串联字段拆回可读格式，同时保留未核验边界；若要确认内容，需外部权威来源。

