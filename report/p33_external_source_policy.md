# P33 / P6-D External Source Policy

本报告记录对剩余 no_source 行应用外部来源治理策略。

> 边界：P6-D 不引入外部来源，不补写医学内容，不做医学真实性/疗效判断；只规定未来补源所需白名单、字段与人工复核要求。

- Remaining no_source rows governed: 136
- Policy file: `data/external_source_policy.json`

## By classification

| classification | count |
|---|---:|
| `alias_or_duplicate_mapped` | 7 |
| `external_source_required` | 115 |
| `internal_research_exhausted` | 14 |

## By external_source_status

| status | count |
|---|---:|
| `canonical_mapping_recorded_but_canonical_no_source` | 7 |
| `eligible_for_manual_review_or_external_source_policy` | 14 |
| `policy_required_before_any_content_expansion` | 115 |

## Required future external source fields

- `source_scope`
- `source_title`
- `source_file_or_url`
- `page_num_or_section`
- `quote`
- `license_or_access_note`
- `reviewer`
- `review_status`

## Forbidden without manual review

- promote external rows to verified_direct or verified_contextual
- mix external source_refs with nihaixia source_refs without source_scope
- add dosage, contraindication, pregnancy, pediatric, emergency, or treatment claims from unsourced text
- remove safety disclaimers or source_quality_policy
