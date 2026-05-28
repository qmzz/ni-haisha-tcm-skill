# Final Governance Release Report

本报告汇总本轮 P1-P4 治理收尾结果。

> 边界：本轮工作只做来源治理、医学安全约束、内容卫生清理与测试护栏，不判断医学真实性、临床疗效或适用性。

## Completed Phases

### P1 Source Quality Rollout

- `source_quality_level` / `source_quality_policy` 已落入全部治理数据文件。
- Trace / lookup / explain / diagnose 输出已暴露 `source_quality_level`。
- Registry / index / frontmatter 冲突审计为 0。
- Alias 风险审计为 0。
- 白豆蔻、白扁豆弱 alias 候选已按 frontmatter 降为 `no_source_found`。

### P2 Medical Safety Enhancement

- 安全策略版本：`p2-2026-05-28`。
- 三类风险：急症红旗、特殊人群、实际治疗/操作意图。
- `tcm_diagnose_assist` 命中安全风险时停止方剂输出。
- 新增 `tcm_safety_policy` 工具。

### P3 Herb Caution Soft Gap Closure

- 116 个 herb 条目补充 `禁忌与慎用（待考）` trace-safe 占位边界。
- 不凭模型补写具体禁忌；明确不得推定“无禁忌”。

### P4 Content Hygiene Final Pass

- 机械清理明显 OCR 重复字尾巴。
- 新增内容卫生测试，阻止明显重复 OCR 章节尾巴回归。

## Verification

```text
python3 -m unittest discover -s tests
Ran 27 tests in 3.363s
OK
```

### Source Quality Conflict Audit

```text
conflicts: 0
alias_risks: 0
p1_no_source_resolutions: 2
```

### Medical Safety Audit

```text
hard_failures: []
missing_safety_boundary: 0
completeness_missing_safety: 0
soft_missing_contra_or_caution: 0
trace_safe_caution_placeholders: 116
```

Coverage:

| kind | total | with_safety_boundary | with_contra_or_caution_text |
|---|---:|---:|---:|
| formula | 113 | 113 | 113 |
| herb | 415 | 415 | 415 |
| acupoint | 411 | 411 | - |

## Key Reports

- `report/p20_source_quality_rollout.md`
- `report/p21_source_quality_conflict_audit.md`
- `report/p22_medical_safety_audit.md`
- `report/p23_herb_caution_placeholders.md`
- `report/p24_ocr_tail_trim.md`
- `report/p_final_governance_release.md`
