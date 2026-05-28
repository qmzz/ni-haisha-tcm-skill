# P20 / P1 Source Quality Rollout

本报告记录 P1 将 source quality 分级从文档说明落地到数据行的结果。

> 边界：source_quality_level 只描述资料链路可信度，不代表医学真实性、临床适用性、疗效或治疗建议。

## Changed files

- `data/verified_sources.jsonl`: 801 rows
- `data/formula_index.jsonl`: 113 rows
- `data/herb_index.jsonl`: 415 rows
- `data/acupoint_index.jsonl`: 411 rows
- `data/knowledge_completeness.jsonl`: 939 rows
- `data/review_queue.jsonl`: 218 rows

## Distribution

### verified_sources

| source_quality_level | count |
|---|---:|
| `verified_contextual` | 244 |
| `verified_direct` | 557 |

### formula_index.jsonl

| source_quality_level | count |
|---|---:|
| `verified_direct` | 113 |

### herb_index.jsonl

| source_quality_level | count |
|---|---:|
| `no_source` | 123 |
| `verified_contextual` | 97 |
| `verified_direct` | 195 |

### acupoint_index.jsonl

| source_quality_level | count |
|---|---:|
| `no_source` | 15 |
| `verified_contextual` | 147 |
| `verified_direct` | 249 |

### knowledge_completeness

| source_quality_level | count |
|---|---:|
| `candidate_contextual` | 1 |
| `no_source` | 137 |
| `verified_contextual` | 244 |
| `verified_direct` | 557 |

### review_queue

| source_quality_level | count |
|---|---:|
| `needs_review` | 34 |
| `no_source` | 184 |

## Rules applied

- `verified_direct`: verified row with source quote that appears to discuss the item directly.
- `verified_contextual`: verified row with source refs but quote appears contextual or insufficiently direct.
- `verified_alias`: verified row involving alias/异名/别名 risk or notes.
- `candidate_direct/contextual/alias`: candidate rows with analogous relation quality; still require review.
- `no_source`: no source refs or explicit no_source_found.
- `needs_review`: review queue entries or unresolved source relationship.

## P1 completion status

- [x] source_quality_level applied to all trace registry files (2897 rows total, 0 missing)
- [x] source_quality_level exposed in trace/lookup/explain/diagnose tool outputs
- [x] registry consistency tests for mandatory source_quality_level (19 tests pass)
- [x] registry/index/frontmatter conflict audit clean (0 conflicts)
- [x] alias risk audit: 2 weak alias candidates (白豆蔻/白扁豆) resolved to no_source_found per frontmatter policy
- [x] no candidate_alias rows remain in index files

## Files changed in P1

- `internal/source_quality.py` — added classify_source_quality()
- `internal/trace_service.py` — rollup source_quality_level in trace results
- `tools/p20_apply_source_quality_levels.py` — batch rollout script
- `tools/p21_audit_source_quality_conflicts.py` — read-only conflict audit
- `data/*.jsonl` — source_quality_level + source_quality_policy on all trace files
- `report/p20_source_quality_rollout.md` — this report
- `report/p21_source_quality_conflict_audit.md` — conflict audit report
- `tests/test_registry_consistency.py` — 5 new tests
- `tests/test_tcm_tools.py` — 4 new tests
