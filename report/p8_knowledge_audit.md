# P8-A 知识库完整度审计

## 阶段定位

P8-A 用于盘点方剂、药材、穴位知识库的治理状态与内容完备度。此报告只做数据治理和补全优先级排序，不判断医学真实性，不生成新的医学结论。

## 总览

- 条目总数：939
- verified 来源链路：210
- frontmatter 标记 verified 但未进入 registry：0
- frontmatter 完整：369
- refined 条目：29
- complete 条目：181
- 数据明细：`data/knowledge_completeness.jsonl`

## 按类别统计

| kind | total | verified_registry | candidate | needs_review | no_source_found | unknown | stale_verified_fm | frontmatter_complete | source_refs | safety_boundary | refined | complete |
|------|-------|-------------------|-----------|--------------|-----------------|---------|-------------------|----------------------|-------------|-----------------|---------|----------|
| formula | 113 | 113 | 0 | 0 | 0 | 0 | 0 | 113 | 113 | 113 | 29 | 84 |
| herb | 415 | 47 | 248 | 0 | 120 | 0 | 0 | 206 | 295 | 206 | 0 | 47 |
| acupoint | 411 | 50 | 297 | 0 | 64 | 0 | 0 | 50 | 347 | 50 | 0 | 50 |

## quality_tier 分布

### formula
- complete: 84
- refined: 29

### herb
- complete: 47
- seed: 120
- traced: 248

### acupoint
- complete: 50
- seed: 64
- traced: 297

## 内容缺口统计

### formula
- usage: 29

### herb
- safety_boundary: 209

### acupoint
- safety_boundary: 361
- source_trace_notice: 361

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
