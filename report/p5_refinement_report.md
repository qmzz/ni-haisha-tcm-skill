# P5 数据精修阶段汇总报告

## 总览

- verified_sources：72
- review_decisions：72
- review_queue：218
- 样板标准化条目：10/10

## Verified 分布

| kind | count |
|------|------:|
| acupoint | 25 |
| formula | 25 |
| herb | 22 |

## P5 Reviewer 分布

| reviewer | count |
|----------|------:|
| p5_core_acupoint_seed | 20 |
| p5_core_formula_seed | 20 |
| p5_core_herb_seed | 17 |

## Review Queue 分布

| kind | status | count |
|------|--------|------:|
| acupoint | needs_review | 9 |
| acupoint | no_source_found | 64 |
| formula | needs_review | 5 |
| herb | needs_review | 20 |
| herb | no_source_found | 120 |

## P5 样板标准化条目

| file | standardized |
|------|--------------|
| knowledge/formulas/guizhi_tang.md | True |
| knowledge/formulas/mahuang_tang.md | True |
| knowledge/formulas/xiaochaihu_tang.md | True |
| knowledge/formulas/wuling_san.md | True |
| knowledge/formulas/banxia_xiexin.md | True |
| knowledge/herbs/mahuang.md | True |
| knowledge/herbs/guizhi.md | True |
| knowledge/herbs/gancao.md | True |
| knowledge/herbs/fuzi.md | True |
| knowledge/herbs/banxia.md | True |

## P5 已完成内容

- P5-A：核心方剂 verified 扩展首批 20 个。
- P5-B：核心药材 verified 扩展首批 17 个。
- P5-C：核心穴位 verified 扩展首批 20 个。
- P5-D：10 个样板条目完成 frontmatter / 安全边界标准化。
- P5-E：生成本汇总报告与发布说明。

## 后续精修建议

1. 每批继续只处理 10-20 个 verified 条目。
2. 优先扩展已 verified 但未标准化的方剂、药材、穴位。
3. 不自动改写医学正文，不新增未溯源医学结论。
4. 候选来源仍需人工复核，candidate 不等于 verified。
