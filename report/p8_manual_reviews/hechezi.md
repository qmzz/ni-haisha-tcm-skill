# hechezi 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/hechezi.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 60 行
- **条目：** 黑芝麻（alias_of: heizhima）

## 当前文件概况

当前条目为 herb，frontmatter `trace_status: no_source_found`，并标记 `alias_of: "heizhima"`。正文含性味、归经、功效、主治等占位内容，以及别名/重复映射边界说明。p11 队列本条 `missing_content_fields=[]`。

## 来源 / FTS 摘要

- `herb_index.jsonl`：名称为黑芝麻，`source_quality_level=no_source`，`source_refs=[]`。
- `herb_sources.jsonl`：`status=no_source_found`，`source_hits=[]`。
- `knowledge_completeness.jsonl`：字段检查为 true，但来源质量为 no_source。
- `source_fts.sqlite` 只读检索“黑芝麻”无命中。

## 是否直接支撑缺失字段

p11 未列缺失字段；现有性味、归经、功效、主治未被内部来源直接支撑。

## 修改 / 不修改理由

不修改正文。该条是 `heizhima` 的别名/重复条目，规范化前不应独立扩写或提升质量等级。

## 未决问题

- 需后续统一 `hechezi` 命名是否误拼/误映射；当前文件标题为黑芝麻，与 item_id 不直观。
