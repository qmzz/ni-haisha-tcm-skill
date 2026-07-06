# yangjinhua 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/herbs/yangjinhua.md`
- **风险分类：** `herb_high_risk`

## 当前文件概况

当前条目为种子型 `no_source_found` 页面。原文件包含“来源：神农本草经”种子信息、空的“倪师讲解”、禁忌待考与学习安全边界。P8 本轮未扩写医学内容，仅补充高风险边界和人工复核状态。

## 查到的来源 / 引用摘要

1. `data/herb_sources.jsonl`
   - `herb_id=yangjinhua`
   - `searched_keywords=["洋金花"]`
   - `source_hits=[]`，`source_hit_count=0`，`status=no_source_found`
2. `data/review_queue.jsonl`
   - `review_status=no_source_found`
   - `reason=未检索到来源候选`
3. `data/source_fts.sqlite`
   - 以“洋金花 / 曼陀罗”检索 `source_pages_fts`，无命中
4. `data/no_source_classification.jsonl` / `data/p39_high_risk_external_review_queue.jsonl`
   - 一致标记为 `external_source_required` 与 `herb_high_risk`
   - 要求外部权威来源和完整安全字段复核

## 修改点

1. frontmatter 增加 `content_scope`、`safety_disclaimer_required`
2. frontmatter 增加 `reviewer: p8_manual_source_refinement`
3. frontmatter 增加 `review_status: pending_external_authoritative_source`
4. frontmatter 增加 `risk_tier: high`
5. 正文增加“高风险外部来源复核边界（P8 手工）”段落

## 保留边界

- 保持 `trace_status: no_source_found`
- 保留种子信息但不据此扩写
- 不补写功效、剂量、毒性、禁忌、妊娠/儿童、相互作用或法定状态

## 未决问题

- “来源：神农本草经”种子信息是否准确，需外部/内部来源进一步核验
- 若后续扩写，需确定药典或现代中药学权威来源版本

## 是否需要外部权威资料

**需要。** 当前内部语料无命中；作为高风险药材，后续扩写必须依赖药典或同等级权威资料。
