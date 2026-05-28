# P22 / P2 Medical Safety Audit

Read-only audit for medical safety coverage after P2 changes.

> 边界：本报告审计安全提示、红旗分流和输出约束，不判断医学真实性或临床疗效。

## Summary

- Hard failures: 0
- Markdown files missing safety boundary: 0
- completeness rows missing safety boundary: 0
- Formula/herb files without explicit 禁忌/注意/慎用 text: 0
- Trace-safe caution placeholders: 116

## Knowledge safety boundary coverage

| kind | total | with_safety_boundary | with_contra_or_caution_text |
|---|---:|---:|---:|
| formula | 113 | 113 | 113 |
| herb | 415 | 415 | 415 |
| acupoint | 411 | 411 | - |

## Tool safety checks

| check | result |
|---|---|
| `emergency_blocks` | PASS |
| `special_or_intent_blocks` | PASS |
| `diagnosis_blocks_treatment_intent` | PASS |
| `policy_exposes_p2_version` | PASS |

## Remaining soft gaps

Soft gap means the global safety boundary exists, but the individual formula/herb file lacks explicit contraindication/caution wording.

No soft gaps found.
