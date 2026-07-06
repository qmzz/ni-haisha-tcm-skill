# fanxieye 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/herbs/fanxieye.md`
- **风险分类：** `herb_high_risk`

## 当前文件概况

当前条目为 `no_source_found` 边界型页面，原文件已包含学习用途声明、来源追溯状态与“当前未在倪海厦知识库中找到专门讲解”的说明。P8 本轮补充了高风险外部来源复核边界段落，并将 frontmatter reviewer/review_status 调整为人工精修状态。

## 查到的来源 / 引用摘要

1. `data/herb_sources.jsonl`
   - `herb_id=fanxieye`
   - `source_hit_count=1`，但 `source_hits=[]`，`trace_status=no_source_found`
2. `data/review_queue.jsonl`
   - 唯一候选来自 `倪海夏-汉唐中医方剂讲解.json` 第 132 页
   - 引文仅提到“减肥药/排泄药里配的大黄、泻叶”，命中词是别名级 `泻叶`
   - `quality_score=13`，`risk_flags=["alias_match_only","alias_requires_review"]`
   - 不能证明该处就是条目“番泻叶”的专门来源
3. `data/source_fts.sqlite`
   - 以“番泻叶 / 旃那叶 / 泻叶”检索；未发现可直接支撑条目的可靠 FTS 页面命中（别名“泻叶”仅在 review_queue 中保留低质量线索）
4. `data/p30_no_source_classification.jsonl` / `data/p36_external_source_queue.jsonl` / `data/p39_high_risk_external_review_queue.jsonl`
   - 一致标记为 `external_source_required` + `high risk`
   - 明确要求外部权威来源与手工安全字段复核

## 修改点

1. frontmatter reviewer 改为 `p8_manual_source_refinement`
2. frontmatter review_status 改为 `pending_external_authoritative_source`
3. 补充 `risk_tier: high`、`external_reference_required: true`、`no_source_policy`
4. 在正文增加“高风险外部来源复核边界（P8 手工）”段落
5. 在来源追溯说明中明确：review_queue 的“泻叶”只是低分别名命中，不能当作番泻叶来源

## 保留边界

- 保持 `trace_status: no_source_found`
- 不补写功效、剂量、毒性、妊娠/儿童、相互作用等具体医学内容
- 不把 alias 命中提升为可追溯来源

## 未决问题

- 是否后续允许引入白名单外部药典 / 现代中药学来源进行扩写
- 若允许扩写，需先确定番泻叶的权威来源版本与引用格式

## 是否需要外部权威资料

**需要。** 该条目属于高风险药材，且倪海厦内部语料无可追溯专门来源；若要补任何医学性内容，必须先引入药典或同等级权威现代中药学资料。