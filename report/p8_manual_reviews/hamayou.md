# hamayou 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/hamayou.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 59 行
- **条目：** 哈蟆油

## 当前文件概况

当前条目为 herb，frontmatter `trace_status: no_source_found`，带 `review_status: pending_external_authoritative_source` 与 `risk_tier: high`。正文已有高风险外部来源复核边界，明确动物/限制性材料边界。

## 来源 / FTS 摘要

- `herb_index.jsonl`：`source_quality_level=no_source`，`source_refs=[]`。
- `herb_sources.jsonl`：`status=no_source_found`，`source_hits=[]`。
- `knowledge_completeness.jsonl`：缺失 `properties` 与 `meridian`，安全边界检查为 true。
- `source_fts.sqlite` 只读检索“哈蟆油”无命中。

## 是否直接支撑缺失字段

- properties：不支撑。
- meridian：不支撑。

## 修改 / 不修改理由

不修改正文，不补写来源、采制、性味、归经、剂量或禁忌。高风险条目需外部权威来源后再扩写。

## 未决问题

- 需确认别名“蛤蟆油/雪蛤”等外部检索策略，并核验法规或药典边界。
