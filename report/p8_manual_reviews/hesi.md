# hesi 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/hesi.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 62 行
- **条目：** 鹤虱

## 当前文件概况

当前条目为 herb，frontmatter `trace_status: no_source_found`，`aliases: ["hezi"]`，有外部来源需求与 no_source 边界。正文已有 P8 手工来源复核说明，提到 P30 将本条标为 `internal_research_exhausted`。`knowledge_completeness` 显示缺失 `properties` 与 `meridian`。

## 来源 / FTS 摘要

- `herb_index.jsonl`：名称为鹤虱，`source_quality_level=no_source`，`source_refs=[]`。
- `herb_sources.jsonl`：`status=no_source_found`，`source_hits=[]`。
- `no_source_classification.jsonl`：`review_status=no_source_found`。
- `source_fts.sqlite` 只读检索“鹤虱”无命中。

## 是否直接支撑缺失字段

- properties：不支撑。
- meridian：不支撑。

## 修改 / 不修改理由

不修改正文，不补写字段。内部语料复搜已尽且未得可靠来源，应等待外部权威来源。

## 未决问题

- 需与 `hezi` 重复/别名条目合并治理，避免同一药材两份 no_source 内容状态不一致。
