# P8-A 知识库完整度审计

## 阶段定位

P8-A 用于盘点方剂、药材、穴位知识库的治理状态与内容完备度。此报告只做数据治理和补全优先级排序，不判断医学真实性，不生成新的医学结论。

## 总览

- 条目总数：939
- verified 来源链路：803
- frontmatter 标记 verified 但未进入 registry：0
- frontmatter 完整：939
- refined 条目：80
- complete 条目：723
- 数据明细：`data/knowledge_completeness.jsonl`

## 按类别统计

| kind | total | verified_registry | candidate | needs_review | no_source_found | unknown | stale_verified_fm | frontmatter_complete | source_refs | safety_boundary | refined | complete |
|------|-------|-------------------|-----------|--------------|-----------------|---------|-------------------|----------------------|-------------|-----------------|---------|----------|
| formula | 113 | 113 | 0 | 0 | 0 | 0 | 0 | 113 | 113 | 113 | 0 | 113 |
| herb | 415 | 294 | 3 | 0 | 118 | 0 | 0 | 415 | 297 | 415 | 80 | 214 |
| acupoint | 411 | 396 | 0 | 0 | 15 | 0 | 0 | 411 | 396 | 411 | 0 | 396 |

## quality_tier 分布

### formula
- complete: 113

### herb
- complete: 214
- refined: 80
- seed: 118
- traced: 3

### acupoint
- complete: 396
- seed: 15

## 内容缺口统计

### formula
- 暂无缺口

### herb
- meridian: 148
- properties: 95

### acupoint
- 暂无缺口

## P8-B/P8-C/P8-D 建议

1. 方剂优先：方剂总量较小，应优先把 verified 与 refined 覆盖继续拉高。
2. 药材分层：药材总量大，建议先做核心 100 味精修，不一次性铺开。
3. 穴位谨慎：穴位涉及操作风险，补全时必须保留“不作为针灸操作指导”的安全边界。
4. no_source_found 继续按 P7 分类结果小批量人工复核，alias hit 不自动 verified。

## 边界

- 本报告不凭模型记忆补医学内容。
- `quality_tier` 只代表资料治理完备度，不代表医学真实性或临床适用性。
- `verified` 只表示来源追溯链路通过复核。
- 找不到依据的条目继续保持 `no_source_found` / `needs_review` / `待考` / `待补充`。
