# P5-C / Remaining needs_review Source Repair Final Report

> 边界：本阶段逐条重新检索原始 JSON，修复 source_refs 与 source_quality_level；不改写医学内容，不判断医学真实性、临床疗效或适用性。

## Input

P5-B 后剩余 `needs_review`：34 条。

- acupoint: 20
- herb: 14

## Method

- 使用原始 JSON 语料目录：`/home/percy/.openclaw/workspace/nihaixia/extracted`
- 对每条按条目名进行关键词检索
- 命中后根据 quote 是否包含条目名及直接标记，保守判为：
  - `verified_direct`
  - `verified_contextual`
  - `verified_alias`
  - `no_source`

## Result

| target | count |
|---|---:|
| `verified_direct` | 32 |
| `verified_contextual` | 2 |

`needs_review` 清零。

## Current Distribution

| file | verified_direct | verified_alias | verified_contextual | no_source |
|---|---:|---:|---:|---:|
| verified_sources | 660 | 49 | 15 | 77 |
| herb_index | 211 | 0 | 4 | 200 |
| acupoint_index | 336 | 49 | 11 | 15 |
| knowledge_completeness | 660 | 49 | 15 | 214 |

## Verification

```text
python3 tools/p21_audit_source_quality_conflicts.py
conflicts: 0
alias_risks: 0
```

```text
python3 -m unittest discover -s tests -v
Ran 29 tests
OK
```

## Remaining

- `verified_contextual`: 15 条，可后续人工精修
- `candidate_contextual`: 1 条，单独处理
- `no_source`: 保留待外部来源或后续专项治理
