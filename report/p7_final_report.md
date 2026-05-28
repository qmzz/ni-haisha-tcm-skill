# P7 Final Report: Source Governance Completion

> 边界：P7 只治理来源追溯与外部来源策略，不引入外部正文，不补写医学内容，不判断医学真实性、疗效、诊断、处方或针灸操作适用性。

## P7-A: verified_contextual Tightening

处理 P6 后 `verified_contextual: 36`。

| action | count |
|---|---:|
| `promoted_to_verified_direct` | 33 |
| `kept_verified_contextual_with_rationale` | 2 |
| `demoted_false_positive_to_no_source` | 1 |

最终 verified_contextual：2 条（均有 `p7a_rationale`）。

## P7-B: External Source Policy & Review Queue

建立 137 条 no_source 的外部来源治理框架：

- 外部来源白名单（6 类 bundle）
- risk tier 分层
- 人工复核强制要求

## P7-B-A: alias_first Resolution

处理 11 条 alias_first no_source：

- 全部映射到 canonical no_source 条目
- 无 verified canonical 可用，全部保留 no_source
- 已去重，避免重复治理

## P7-B-D: High-risk Safety Review Template

14 条 high-risk no_source 标记为 `pending_human_review`，禁止在人工复核前：

- 提升 source_quality_level
- 引入外部医学内容
- 删除安全边界声明

必填安全字段（10 项）：

1. `toxicity_profile`
2. `contraindications`
3. `pregnancy_lactation_warning`
4. `pediatric_warning`
5. `dose_range_source_required`
6. `processing_method_if_applicable`
7. `drug_interaction_or_modern_caution`
8. `legal_or_restricted_status`
9. `emergency_red_flags`
10. `reviewer` + `review_status`

## Final Audit (P40)

```text
python3 tools/p40_audit_p7_completion.py
problems: 0
```

## Final Distribution

### knowledge_completeness.jsonl

| level | count |
|---|---:|
| `verified_direct` | 749 |
| `verified_alias` | 51 |
| `verified_contextual` | 2 |
| `no_source` | 137 |

### verified_sources.jsonl

| level | count |
|---|---:|
| `verified_direct` | 749 |
| `verified_alias` | 49 |
| `verified_contextual` | 2 |

### no_source by p7b_category

| category | count |
|---|---:|
| `herb_standard` | 79 |
| `herb_modern_or_regional` | 16 |
| `alias_first` | 11 |
| `herb_high_risk` | 12 |
| `herb_animal_or_restricted` | 2 |
| `herb_internal_exhausted` | 4 |
| `acupoint_standard` | 8 |
| `acupoint_extra_or_uncertain` | 5 |

### Risk tiers

| tier | count |
|---|---:|
| `low` | 107 |
| `medium` | 16 |
| `high` | 14 |

## Verification

```text
python3 tools/p37_audit_external_source_queue.py
problems: 0
```

```text
python3 tools/p34_audit_p6_completion.py
problems: 0
queue_rows: 137
```

```text
python3 tools/p21_audit_source_quality_conflicts.py
conflicts: 0
alias_risks: 0
```

```text
python3 -m unittest discover -s tests -v
Ran 33 tests
OK
```

## Output Files

### Scripts
- `tools/p35_tighten_verified_contextual.py`
- `tools/p36_build_external_source_queue.py`
- `tools/p37_audit_external_source_queue.py`
- `tools/p38_resolve_alias_first_items.py`
- `tools/p39_high_risk_safety_review_template.py`
- `tools/p40_audit_p7_completion.py`

### Data
- `data/p36_external_source_queue.jsonl`
- `data/p39_high_risk_external_review_queue.jsonl`

### Reports
- `report/p35_verified_contextual_tightening.md`
- `report/p36_external_source_queue.md`
- `report/p37_external_source_queue_audit.md`
- `report/p38_alias_first_resolution.md`
- `report/p39_high_risk_safety_review_template.md`
- `report/p40_p7_completion_audit.md`
- `report/p7a_verified_contextual_tightening_final.md`
- `report/p7b_external_source_policy_final.md`
- `report/p7_final_report.md`
