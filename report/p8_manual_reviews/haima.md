# haima 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/haima.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 57 行
- **条目：** 海马

## 当前文件概况

当前条目为 herb，frontmatter `trace_status: no_source_found`，带 `external_reference_required: true`、`review_status: pending_external_authoritative_source`、`risk_tier: high`。正文已有高风险外部来源复核边界，标明动物/限制性材料边界与不得扩写。

## 来源 / FTS 摘要

- `herb_index.jsonl`：`source_quality_level=no_source`，`source_refs=[]`。
- `herb_sources.jsonl`：`status=no_source_found`，`source_hits=[]`。
- `knowledge_completeness.jsonl`：缺失 `properties` 与 `meridian`，但功效、禁忌、倪师讲解、安全边界检查为 true。
- `source_fts.sqlite` 只读检索“海马”无命中。

## 是否直接支撑缺失字段

- properties：不支撑。
- meridian：不支撑。

## 修改 / 不修改理由

不修改正文，不补写性味、归经或动物来源细节。该条属于高风险外部来源候选，当前内部语料无命中，必须等待权威外部来源后再补全。

## 未决问题

- 需要药典、法规或权威数据库确认来源、限制状态、性味归经、剂量与禁忌。
