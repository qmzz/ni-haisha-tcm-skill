# P5-D / candidate_contextual Resolution Final Report

> 边界：本阶段只同步来源治理状态，不改写医学内容，不判断医学真实性、疗效或临床适用性。

## Input

P5-C 后仅剩 1 条 `candidate_contextual`：

- `herb:fanxieye` 番泻叶

## Finding

`fanxieye` 在各文件状态不一致：

- `knowledge/herbs/fanxieye.md`: `trace_status: no_source_found`, `source_refs: []`
- `data/herb_index.jsonl`: `trace_status: no_source_found`, `source_quality_level: no_source`
- `data/knowledge_completeness.jsonl`: stale `candidate_contextual`

## Decision

以 frontmatter + herb_index 的无来源状态为准，将 completeness 中的 stale `candidate_contextual` 同步为：

```text
trace_status: no_source_found
source_quality_level: no_source
review_status: needs_source
has_source_refs: false
```

## Result

- candidate_contextual: 0
- needs_review: 0
- conflicts: 0
- alias_risks: 0
- tests: 31 OK

## Current Distribution

| file | verified_direct | verified_alias | verified_contextual | no_source |
|---|---:|---:|---:|---:|
| verified_sources | 660 | 49 | 15 | 77 |
| herb_index | 211 | 0 | 4 | 200 |
| acupoint_index | 336 | 49 | 11 | 15 |
| knowledge_completeness | 660 | 49 | 15 | 215 |
