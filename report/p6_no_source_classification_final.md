# P6 Final Report: no_source Governance Completion

> 边界：P6 只治理来源追溯状态；不引入外部来源，不补写医学内容，不判断医学真实性、疗效、诊断、处方、剂量或针灸操作适用性。

## Input

P5-D 后 no_source inventory：215 条。

- herb: 200
- acupoint: 15

## P6-A: Classification

将 215 条 no_source 分为三类治理队列：

| classification | count |
|---|---:|
| `external_source_required` | 115 |
| `internal_research_needed` | 91 |
| `alias_or_duplicate_needs_mapping` | 9 |

输出：

- `tools/p30_classify_no_source_rows.py`
- `data/p30_no_source_classification.jsonl`
- `report/p30_no_source_classification.md`

## P6-B: Alias / duplicate mapping

处理 9 条 alias/duplicate 队列：

| target | count |
|---|---:|
| `verified_alias` | 2 |
| `no_source` | 7 |

说明：

- 2 条可映射到已验证 canonical 来源，标记为 `verified_alias`。
- 7 条只完成 canonical mapping，但 canonical 本身仍无来源，因此保留 `no_source`。

输出：

- `tools/p31_resolve_alias_duplicate_no_source.py`
- `report/p31_alias_duplicate_no_source_resolution.md`

## P6-C: Internal corpus re-search

对 91 条 `internal_research_needed` 执行倪海厦原始 JSON 语料重检索：

| target | count |
|---|---:|
| `verified_direct` | 56 |
| `verified_contextual` | 21 |
| `no_source` | 14 |

说明：

- 77 条通过内部语料重新找到可追溯 source_refs。
- 14 条内部语料检索耗尽，保留 no_source 并转入后续人工/外部来源策略。

输出：

- `tools/p32_research_internal_no_source.py`
- `report/p32_internal_no_source_research.md`

## P6-D: External source policy

对 P6 后仍为 no_source 的 136 条应用外部来源治理策略：

| remaining classification | count |
|---|---:|
| `external_source_required` | 115 |
| `internal_research_exhausted` | 14 |
| `alias_or_duplicate_mapped` | 7 |

策略文件：

- `data/external_source_policy.json`

要求：未来如需补外部来源，必须使用独立 source_scope、白名单来源、完整引用字段和人工复核，不得混入 Ni corpus verified levels。

输出：

- `tools/p33_apply_external_source_policy.py`
- `report/p33_external_source_policy.md`

## Final Audit

P6 完成后 `knowledge_completeness.jsonl` source_quality_level 分布：

| level | count |
|---|---:|
| `verified_direct` | 716 |
| `verified_contextual` | 36 |
| `verified_alias` | 51 |
| `no_source` | 136 |

剩余 no_source 全部具备：

- `no_source_classification`
- `no_source_reason`
- `next_action`
- `external_source_policy_version`
- `external_source_status`
- `source_scope`

审计输出：

- `tools/p34_audit_p6_completion.py`
- `report/p34_p6_completion_audit.md`

```text
python3 tools/p34_audit_p6_completion.py
problems: 0
queue_rows: 136
```

## Verification

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

## Conclusion

P6 已闭环：

- 215 条 no_source 已全部分类。
- 9 条 alias/duplicate 已处理。
- 91 条内部重检索完成，77 条恢复为 verified，14 条检索耗尽。
- 136 条剩余 no_source 已全部纳入外部来源治理策略，禁止未经人工复核直接补外部医学内容。
