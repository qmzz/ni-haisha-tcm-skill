# P30 / P6 no_source Classification

本报告将 no_source 条目分入后续治理队列。

> 边界：只做分类，不引入新来源，不补写医学内容，不判断医学真实性或疗效。

- Classified no_source rows: 215

## By classification

| classification | count |
|---|---:|
| `alias_or_duplicate_needs_mapping` | 9 |
| `external_source_required` | 115 |
| `internal_research_needed` | 91 |

## By kind

| kind | classification | count |
|---|---|---:|
| acupoint | `alias_or_duplicate_needs_mapping` | 3 |
| acupoint | `external_source_required` | 4 |
| acupoint | `internal_research_needed` | 8 |
| herb | `alias_or_duplicate_needs_mapping` | 6 |
| herb | `external_source_required` | 111 |
| herb | `internal_research_needed` | 83 |

## Policy

- `internal_research_needed`: 先重搜倪海厦原始 JSON/alias，不能直接外部补源。
- `alias_or_duplicate_needs_mapping`: 先确认 canonical mapping，再决定是否同步 source_refs。
- `external_source_required`: 当前倪师语料无来源；如要补内容必须建立外部来源白名单与引用字段。

Queue file: `data/p30_no_source_classification.jsonl`
