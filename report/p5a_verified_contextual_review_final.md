# P5-A / verified_contextual Review Final Report

> 边界：只评估来源片段与条目名的关系质量，不判断医学真实性、临床适用性或疗效。

## Summary

- 原始 verified_contextual: 244 rows (97 herb + 147 acupoint)
- P5-A 机械复核后：
  - 升级 verified_direct: 71
  - 降级 needs_review: 160
  - 保留 verified_contextual: 13
- source quality 冲突审计: 0 conflicts
- 测试: 29 tests OK

## Bucket After Review

| kind | verified_direct | verified_contextual | needs_review |
|---|---:|---:|---:|
| herb | 199 | 2 | 91 |
| acupoint | 316 | 11 | 69 |
| verified_sources | 628 | 13 | 160 |

## Decision Rules

- `verified_direct`: 条目名在 source_refs.quote 中，且 name 附近 100 字符内有该类条目的直接标记
- `verified_contextual`: quote 提到条目名但无直接标记
- `needs_review`: quote 为空、含 OCR/JSON 脏字符、或不含条目名

## Files Changed

- `tools/p25_review_verified_contextual.py` — P5-A 复核脚本
- `data/verified_sources.jsonl` — source_quality_level + p5a_review_reason
- `data/herb_index.jsonl` — synced from registry
- `data/acupoint_index.jsonl` — synced from registry
- `data/knowledge_completeness.jsonl` — synced from registry
- `report/p25_verified_contextual_review.md` — 逐条决策清单

## Verification

```text
python3 -m unittest discover -s tests -v
Ran 29 tests in 3.621s
OK
```

## Remaining

- 160 条 needs_review 条目待人工复核
- 13 条 verified_contextual 保留待进一步确认
- 1 条 candidate_contextual 仍需人工复核
