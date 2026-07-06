# gouteng 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/gouteng.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 51 行
- **条目：** 钩藤

## 当前文件概况

当前条目为 herb，frontmatter `trace_status: no_source_found`，有外部来源需求与 no_source 边界。正文已有性味、归经、功效、主治等占位医学内容，也已有 P8 手工来源复核边界说明。p11 队列本条 `missing_content_fields=[]`，但任务类型仍为 no_source boundary/external source。

## 来源 / FTS 摘要

- `herb_index.jsonl`：`source_quality_level=no_source`，`source_refs=[]`。
- `herb_sources.jsonl`：`status=no_source_found`，`source_hits=[]`。
- `knowledge_completeness.jsonl`：内容字段检查均为 true，但来源质量为 no_source。
- `source_fts.sqlite` 只读检索“钩藤”无命中。

## 是否直接支撑缺失字段

p11 未列缺失字段；现有性味、归经、功效、主治也未被内部来源直接支撑。

## 修改 / 不修改理由

不修改正文。本轮不删除占位医学内容，但报告明确这些内容不能视为倪海厦内部语料验证内容；后续如要质量提升，必须外部权威来源逐条核验。

## 未决问题

- 该类 no_source 但字段完整的条目，后续需要决定是保留占位内容并加强边界，还是在外部来源缺位时统一降噪。

