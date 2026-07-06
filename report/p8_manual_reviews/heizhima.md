# heizhima 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/heizhima.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 61 行
- **条目：** 黑芝麻

## 当前文件概况

当前条目为 herb，frontmatter `trace_status: no_source_found`，有外部来源需求与 no_source 边界。正文基础信息存在字段串联与重复：性味、归经、功效、主治被合并在一行，归经重复。p11 队列本条 `missing_content_fields=[]`。

## 来源 / FTS 摘要

- `herb_index.jsonl`：`source_quality_level=no_source`，`source_refs=[]`。
- `herb_sources.jsonl`：`status=no_source_found`，`source_hits=[]`。
- `knowledge_completeness.jsonl`：字段检查为 true，但来源质量为 no_source。
- `source_fts.sqlite` 只读检索“黑芝麻”无命中。

## 是否直接支撑缺失字段

p11 未列缺失字段；现有性味、归经、功效、主治未被内部来源直接支撑。

## 修改 / 不修改理由

不修改医学内容。字段串联是格式问题，但本轮优先来源复核；若拆分，应保持 no_source 边界，不得因此提升质量。

## 未决问题

- 建议后续对 no_source 串联字段做格式降噪，并与 `hechezi` 别名条目一并规范。
