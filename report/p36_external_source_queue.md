# P36 / P7-B External Source Queue

> 边界：本阶段只建立外部来源白名单与人工复核队列，不引入外部正文，不提升 source_quality_level，不补写医学内容。

- Queue rows: 137

## By category

| category | count |
|---|---:|
| `acupoint_extra_or_uncertain` | 5 |
| `acupoint_standard` | 8 |
| `alias_first` | 11 |
| `herb_animal_or_restricted` | 2 |
| `herb_high_risk` | 12 |
| `herb_internal_exhausted` | 4 |
| `herb_modern_or_regional` | 16 |
| `herb_standard` | 79 |

## By phase

| phase | count |
|---|---:|
| `P7B-A` | 11 |
| `P7B-B` | 8 |
| `P7B-C` | 5 |
| `P7B-D` | 14 |
| `P7B-E` | 16 |
| `P7B-F` | 83 |

## By risk

| risk | count |
|---|---:|
| `high` | 14 |
| `low` | 107 |
| `medium` | 16 |

## Source bundles

- `herb_standard`: official_pharmacopoeia, modern_tcm_reference, classical_tcm_text
- `herb_high_risk`: official_pharmacopoeia, modern_tcm_reference
- `herb_animal_or_restricted`: official_pharmacopoeia, modern_tcm_reference
- `herb_alias`: official_pharmacopoeia, modern_tcm_reference
- `acupoint_standard`: acupoint_standard_reference
- `acupoint_extra`: acupoint_standard_reference, modern_tcm_reference
