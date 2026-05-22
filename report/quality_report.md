# P3 质量看板

## 来源候选覆盖率

| kind | total | with_candidates | no_source | coverage |
|------|------:|----------------:|----------:|---------:|
| formula | 113 | 113 | 0 | 100.0% |
| herb | 415 | 294 | 121 | 70.8% |
| acupoint | 411 | 347 | 64 | 84.4% |

## Review Queue

| kind | status | count |
|------|--------|------:|
| acupoint | needs_review | 9 |
| acupoint | no_source_found | 64 |
| formula | needs_review | 4 |
| herb | needs_review | 25 |
| herb | no_source_found | 121 |

## Verified / Alias

- verified_sources：15
- alias kind 数：3
- acupoint alias 条目：23
- formula alias 条目：4
- herb alias 条目：43

## 治理原则

- candidate 不等于 verified。
- no_source_found 不自动补写医学内容。
- alias 命中只作为候选来源，仍需人工复核。
- 高风险症状不输出方剂治疗建议。
