# P5-B / needs_review Segmentation and Safe Resolution Final Report

> 边界：本阶段只处理来源关系治理，不改写医学内容，不判断医学真实性、疗效或临床适用性。

## Input

P5-A 后 `needs_review` 共 160 条：

- herb: 91
- acupoint: 69

## P26 Segmentation

将 160 条分为：

| segment | count | meaning |
|---|---:|---|
| `empty_quote` | 77 | 缺 source quote 或 quote 太短 |
| `dirty_quote` | 32 | quote 疑似 OCR / TOC / JSON / 页码片段 |
| `name_mismatch` | 51 | quote 不含完整条目名 |

## P27 Safe Resolution

可机械安全处理 126 条：

| target | count | rule |
|---|---:|---|
| `no_source` | 77 | empty_quote 无可追溯片段，降级为 no_source_found/no_source |
| `verified_alias` | 49 | 二级/后缀重复穴位条目，quote 含基础穴名，标记 verified_alias |

保留人工复核：

| target | count |
|---|---:|
| `needs_review` | 34 |

## Current Distribution

| file | verified_direct | verified_alias | verified_contextual | needs_review | no_source |
|---|---:|---:|---:|---:|---:|
| verified_sources | 628 | 49 | 13 | 34 | 77 |
| herb_index | 199 | 0 | 2 | 14 | 200 |
| acupoint_index | 316 | 49 | 11 | 20 | 15 |
| knowledge_completeness | 628 | 49 | 13 | 34 | 214 |

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

## Remaining Manual Queue

- 34 条 `needs_review` 需要重新检索或人工抽取 source_refs
- 13 条 `verified_contextual` 保留为上下文型 verified
- 1 条 `candidate_contextual` 仍需单独处理
