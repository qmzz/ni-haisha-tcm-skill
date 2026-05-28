# P7-A Final Report: verified_contextual Tightening

> 边界：P7-A 只调整来源追溯等级与 rationale，不补写医学内容，不判断医学真实性、疗效、处方或针灸操作适用性。

## Input

P6 后 `verified_contextual: 36`。

## Method

- 使用倪海厦原始 JSON 语料重搜 36 条 contextual rows。
- 仅当 quote 在条目名附近出现保守 direct marker 时，升级为 `verified_direct`。
- 如果 quote 只是提及但缺少 direct marker，则保留 `verified_contextual` 并写入 `p7a_rationale`。
- 如果 quote 明显是噪声/误命中，则降为 `no_source` 并纳入外部来源治理队列。

## Result

| action | count |
|---|---:|
| `promoted_to_verified_direct` | 33 |
| `kept_verified_contextual_with_rationale` | 2 |
| `demoted_false_positive_to_no_source` | 1 |

剩余 `verified_contextual`：

| kind | item_id | name | rationale |
|---|---|---|---|
| herb | `banlangen` | 板蓝根 | quote mentions item but lacks conservative direct marker |
| herb | `dengxincao` | 灯心草 | quote mentions item but lacks conservative direct marker |

降级噪声：

| kind | item_id | name | reason |
|---|---|---|---|
| acupoint | `shiqixue` | 十七 | existing quote is numeric chapter/page noise, not a traceable item source |

## Final distribution

`verified_sources.jsonl`:

| level | count |
|---|---:|
| `verified_direct` | 749 |
| `verified_alias` | 49 |
| `verified_contextual` | 2 |

`knowledge_completeness.jsonl`:

| level | count |
|---|---:|
| `verified_direct` | 749 |
| `verified_alias` | 51 |
| `verified_contextual` | 2 |
| `no_source` | 137 |

## Verification

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
