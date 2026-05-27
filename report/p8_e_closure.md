# P8-E 收口报告

## 任务
处理 no_source_found 条目，采用四步法：
1. 盘点清单
2. 扩展搜索
3. 小批量白名单
4. 收口测试与文档

## 结果

### P8-E-1: 盘点
- herb no_source_found: 120（全部 uncategorized，无明显命名变体）
- acupoint no_source_found: 64
  - naming_variant: 51（二/三/外号变体）
  - uncategorized: 13
- 输出：`report/p8_no_source_inventory.md`、`report/p8_acupoint_no_source_variant.md`

### P8-E-2: 扩展搜索
- 扩展命中总数：156 条
- 主要来源：
  - acupoint 命名变体去掉「二/三/外」后缀后命中 parent_name
  - herb 常见别名回退（川贝母→贝母、朱砂根→朱砂）
- 输出：`data/p8_e_no_source_expand_hits.jsonl`

### P8-E-3: 小批量白名单
- 自动候选：51 条
  - acupoint: 49 条（parent_name quality_score ≥ 74）
  - herb: 2 条（alias quality_score = 100）
- 人工复核：1 条（跗阳二，quality=71，暂不处理）
- 输出：`data/p8_e_3_auto_candidates.jsonl`、`report/p8_e_3_auto_candidates.md`

### P8-E-4: 收口测试与文档
- 全量测试：76 个通过 ✅
- frontmatter audit: missing_required = 0 ✅

## 当前状态

```
verified_total: 512
  - formula: 113
  - herb: 292
  - acupoint: 107

review_queue: 218 (unresolved=137)
  - needs_review: 34
  - no_source_found: 184
    - herb: 120 (已减少 2 via parent expand)
    - acupoint: 64 (已减少 49 via parent expand)
    - formula: 0
```

## 关键决策

- acupoint 命名变体（二/三/外号）通过 parent_name 扩展搜索验证，notes 标记为「P8-E parent name expand trace」
- herb 别名回退仅接受 quality_score ≥ 95 的高置信命中
- 低分/模糊命中保持 needs_review 或 no_source_found，不自动 verified

## 新增脚本

- 盘点 no_source_found 清单。
- 完成 acupoint 命名变体分类。
- 完成扩展搜索。
- 完成自动候选生成。
- 完成 verified 落库。
