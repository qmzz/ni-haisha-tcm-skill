# hezi 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/hezi.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 64 行
- **条目：** 鹤虱（aliases: hesi）

## 当前文件概况

当前条目为 herb，frontmatter `trace_status: no_source_found`，`aliases: ["hesi"]`。正文含性味、归经、功效、主治等占位内容，并说明本条为 `hesi` 的别名/重复映射条目。p11 队列本条 `missing_content_fields=[]`。

## 来源 / FTS 摘要

- `herb_index.jsonl`：名称为鹤虱，`source_quality_level=no_source`，`source_refs=[]`。
- `herb_sources.jsonl`：`status=no_source_found`，`source_hits=[]`。
- `knowledge_completeness.jsonl`：字段检查为 true，但来源质量为 no_source。
- `source_fts.sqlite` 只读检索“鹤虱”无命中。

## 是否直接支撑缺失字段

p11 未列缺失字段；现有性味、归经、功效、主治未被内部来源直接支撑。

## 修改 / 不修改理由

不修改正文。该条为 `hesi` 的重复/别名条目，不应独立扩写或提升质量。

## 未决问题

- item_id `hezi` 通常可能指“诃子”，但当前文件和索引均为鹤虱；需后续核查是否存在命名污染或别名映射误配。
