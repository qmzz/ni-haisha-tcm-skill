# P7-B Final Report: External Source Policy & Review Queue

> 边界：P7-B 只建立外部来源白名单、risk tier 与人工复核队列，不引入外部正文，不提升 source_quality_level，不补写医学内容，不判断医学真实性、疗效、诊断或处方。

## Input

P6 后 no_source inventory：137 条。

| kind | count |
|---|---:|
| herb | 123 |
| acupoint | 14 |

## Phase 1: Whitelist & Queue (P36)

### External source bundles

| bundle | scopes |
|---|---|
| herb_standard | `official_pharmacopoeia`, `modern_tcm_reference`, `classical_tcm_text` |
| herb_high_risk | `official_pharmacopoeia`, `modern_tcm_reference` |
| herb_animal_or_restricted | `official_pharmacopoeia`, `modern_tcm_reference` |
| herb_alias | `official_pharmacopoeia`, `modern_tcm_reference` |
| acupoint_standard | `acupoint_standard_reference` |
| acupoint_extra | `acupoint_standard_reference`, `modern_tcm_reference` |

### Category breakdown

| category | count | meaning |
|---|---:|---|
| `herb_standard` | 79 | standard herb external-source candidate |
| `herb_modern_or_regional` | 16 | modern/regional materia medica, external source likely required |
| `alias_first` | 11 | resolve canonical/alias mapping before external sourcing |
| `herb_high_risk` | 12 | toxic/strong-action herbs; external review must include safety fields |
| `herb_animal_or_restricted` | 2 | animal/restricted materials; must include legal/ethical status |
| `herb_internal_exhausted` | 4 | not found after Ni corpus re-search |
| `acupoint_standard` | 8 | standard acupoint candidate |
| `acupoint_extra_or_uncertain` | 5 | extra/uncertain acupoint; manual review required |

### Risk tiers

| tier | count |
|---|---:|
| `low` | 107 |
| `medium` | 16 |
| `high` | 14 |

### Required review rule

Every no_source row is flagged:

```text
manual_review_required_before_content_or_quality_promotion
```

This applies to all rows, regardless of risk tier.

## Phase 2: Audit (P37)

```text
python3 tools/p37_audit_external_source_queue.py
problems: 0
queue_rows: 137
```

## Output

- `data/external_source_policy.json`
- `data/p36_external_source_queue.jsonl`
- `report/p36_external_source_queue.md`
- `report/p37_external_source_queue_audit.md`
- `tools/p36_build_external_source_queue.py`
- `tools/p37_audit_external_source_queue.py`

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

## Conclusion

P7-B establishes the external-source review framework without importing external content. The 137 remaining no_source rows are now categorized by risk tier, source bundle, and phase. The next step would be to begin Phase P7-B-A (alias resolution) and P7-B-D (high-risk herb review) with human oversight.
