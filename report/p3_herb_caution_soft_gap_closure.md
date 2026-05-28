# P3 / Herb Contraindication Soft Gap Closure

> 边界：P3 不凭模型补写具体禁忌；只为缺少禁忌/慎用文字的药材条目添加 trace-safe 待考边界。

## Completed

- 对 116 个缺少显式禁忌/慎用文字的 herb markdown 条目追加 `## ⚠️ 禁忌与慎用（待考）`。
- 占位文案明确：当前未在已治理来源中提取到可追溯禁忌原文，不得推定“无禁忌”。
- 涉及实际用药、剂量、配伍、孕产妇、儿童、老人、基础病或正在服用其他药物等情况，必须由合格专业人士判断。

## Audit result

```text
hard_failures: []
missing_safety_boundary: 0
completeness_missing_safety: 0
soft_missing_contra_or_caution: 0
trace_safe_caution_placeholders: 116
```

## Coverage

| kind | total | with_safety_boundary | with_contra_or_caution_text |
|---|---:|---:|---:|
| formula | 113 | 113 | 113 |
| herb | 415 | 415 | 415 |
| acupoint | 411 | 411 | - |

## Files

- `tools/p23_add_herb_caution_placeholders.py` — 一次性补齐脚本
- `report/p23_herb_caution_placeholders.md` — 116 个变更文件列表
- `report/p22_medical_safety_audit.md` — P2/P3 后安全审计
- `tests/test_registry_consistency.py` — P3 回归测试

## Verification

```text
python3 -m unittest discover -s tests -v
Ran 26 tests in 3.359s
OK
```
