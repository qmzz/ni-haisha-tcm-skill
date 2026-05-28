# P31 / P6-B alias_or_duplicate no_source Resolution

本报告记录 P6-B 对 alias/duplicate no_source 队列的 canonical mapping 处理。

> 边界：只建立 canonical mapping 与来源治理状态，不改写医学内容，不判断医学真实性或疗效。

- Decisions: 9

## By target source_quality_level

| target | count |
|---|---:|
| `no_source` | 7 |
| `verified_alias` | 2 |

## Decision list

- `herb:biba` 荜澄茄 → `bichengqie`; canonical_status=no_source_found; target=`no_source` (mapped_to_canonical_but_canonical_is_no_source)
- `herb:bichengqie` 荜澄茄 → `bichengqie`; canonical_status=no_source_found; target=`no_source` (mapped_to_canonical_but_canonical_is_no_source)
- `herb:hechezi` 黑芝麻 → `heizhima`; canonical_status=no_source_found; target=`no_source` (mapped_to_canonical_but_canonical_is_no_source)
- `herb:heizhima` 黑芝麻 → `heizhima`; canonical_status=no_source_found; target=`no_source` (mapped_to_canonical_but_canonical_is_no_source)
- `herb:hezi` 鹤虱 → `hesi`; canonical_status=no_source_found; target=`no_source` (mapped_to_canonical_but_canonical_is_no_source)
- `herb:luobuma` 罗布麻叶 → `luobumaye`; canonical_status=no_source_found; target=`no_source` (mapped_to_canonical_but_canonical_is_no_source)
- `acupoint:fuyang2` 跗阳二 → `fuyang_bl`; canonical_status=verified; target=`verified_alias` (mapped_to_verified_canonical_as_alias)
- `acupoint:yaoyangguan` 腰阳关 → `yangguan`; canonical_status=no_source_found; target=`no_source` (mapped_to_canonical_but_canonical_is_no_source)
- `acupoint:yinjiao_ren` 阴交二 → `yinjiao`; canonical_status=verified; target=`verified_alias` (mapped_to_verified_canonical_as_alias)
