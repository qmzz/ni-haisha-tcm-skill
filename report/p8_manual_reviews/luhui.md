# luhui 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/herbs/luhui.md`
- **风险分类：** `herb_high_risk`

## 当前文件概况

当前条目为 P5 标准边界型 `no_source_found` 页面，原文件已包含学习用途声明、来源追溯状态和无专门讲解说明。P8 本轮补充高风险外部来源复核边界，并将 frontmatter reviewer/review_status 调整为人工精修状态。

## 查到的来源 / 引用摘要

1. `data/herb_sources.jsonl`
   - `herb_id=luhui`
   - `searched_keywords=["芦荟"]`
   - `source_hits=[]`，`source_hit_count=0`，`status=no_source_found`
2. `data/review_queue.jsonl`
   - `review_status=no_source_found`
   - `reason=未检索到来源候选`
3. `data/source_fts.sqlite`
   - 以“芦荟 / 卢会 / 卢荟”检索 `source_pages_fts`，无命中
4. `data/p30_no_source_classification.jsonl` / `data/knowledge_completeness.jsonl`
   - `no_source_classification=internal_research_exhausted`
   - `p6c_resolution=internal_no_hit`
5. `data/p36_external_source_queue.jsonl` / `data/p39_high_risk_external_review_queue.jsonl`
   - 标记为 `herb_high_risk`
   - 要求外部权威来源和完整安全字段复核

## 修改点

1. frontmatter reviewer 改为 `p8_manual_source_refinement`
2. frontmatter review_status 改为 `pending_external_authoritative_source`
3. 增加 `risk_tier: high`、`external_reference_required: true`、`no_source_policy`
4. 来源追溯说明中补充 P6-C 已 `internal_research_exhausted`
5. 正文增加“高风险外部来源复核边界（P8 手工）”段落

## 保留边界

- 保持 `trace_status: no_source_found`
- 保持 P6-C `internal_research_exhausted` 判断
- 不补写功效、剂量、毒性、禁忌、妊娠/儿童或相互作用

## 未决问题

- 若后续扩写，需确定药典或现代中药学权威来源版本
- 是否需要对常见异名进一步建立人工别名清单，需权威来源支撑

## 是否需要外部权威资料

**需要。** 当前内部语料检索已耗尽无可靠命中；作为高风险药材，后续扩写必须依赖药典或同等级权威资料。