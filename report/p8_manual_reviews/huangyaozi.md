# huangyaozi 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/huangyaozi.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 66 行
- **条目：** 黄药子

## 当前文件概况

当前条目为 herb，frontmatter `trace_status: no_source_found`，带 `review_status: pending_external_authoritative_source` 与 `risk_tier: high`。正文已有高风险外部来源复核边界，明确不得补写毒性、功效、剂量等。

## 来源 / FTS 摘要

- `herb_index.jsonl`：`source_quality_level=no_source`，`source_refs=[]`。
- `herb_sources.jsonl`：`status=no_source_found`，`source_hits=[]`。
- `knowledge_completeness.jsonl`：缺失 `properties` 与 `meridian`，安全边界检查为 true。
- `source_fts.sqlite` 只读检索“黄药子”无命中。

## 是否直接支撑缺失字段

- properties：不支撑。
- meridian：不支撑。

## 修改 / 不修改理由

不修改正文，不补写性味、归经、毒性或禁忌。该条为高风险外部来源候选，缺少内部可追溯来源。

## 未决问题

- 后续需药典或权威中药学来源核验毒性、禁忌、剂量、炮制和现代用药风险。
