# hamayou 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/herbs/hamayou.md`
- **风险分类：** `herb_animal_or_restricted`

## 当前文件概况

当前条目为种子型 `no_source_found` 页面。原文件包含“来源：神农本草经”种子信息、空的“倪师讲解”、禁忌待考与学习安全边界。P8 本轮未扩写医学内容，仅补充高风险动物/限制性材料边界和人工复核状态。

## 查到的来源 / 引用摘要

1. `data/herb_sources.jsonl`
   - `herb_id=hamayou`
   - `searched_keywords=["哈蟆油"]`
   - `source_hits=[]`，`source_hit_count=0`，`status=no_source_found`
2. `data/review_queue.jsonl`
   - `review_status=no_source_found`
   - `reason=未检索到来源候选`
3. `data/source_fts.sqlite`
   - 以“哈蟆油 / 蛤蟆油 / 雪蛤”检索 `source_pages_fts`，无命中
4. `data/p30_no_source_classification.jsonl` / `data/p36_external_source_queue.jsonl` / `data/p39_high_risk_external_review_queue.jsonl`
   - 一致标记为 `external_source_required`
   - P7B 分类为 `herb_animal_or_restricted`，要求 legal/ethical status 与安全字段手工复核

## 修改点

1. frontmatter 增加 `reviewer: p8_manual_source_refinement`
2. frontmatter 增加 `review_status: pending_external_authoritative_source`
3. frontmatter 增加 `risk_tier: high`
4. 正文增加“高风险外部来源复核边界（P8 手工）”段落，明确动物/限制性材料、毒性、妊娠/儿童、剂量、炮制、相互作用、法定状态均缺少可追溯来源

## 保留边界

- 保持 `trace_status: no_source_found`
- 保留现有种子信息但不据此扩写
- 不补写剂量、功效、毒性、禁忌或法定状态
- 不用模型常识替代外部权威来源

## 未决问题

- “来源：神农本草经”种子信息是否准确，需外部/内部来源进一步核验
- 别名/规范名是否应统一为“哈蟆油、蛤蟆油、雪蛤油”等，需权威药典或术语表确认
- 作为动物来源材料，是否涉及保护、贸易或地方合规限制，需权威法规或药典资料确认

## 是否需要外部权威资料

**需要。** 当前内部语料无命中；后续扩写必须依赖药典、法规或现代中药学权威资料。
## R6 顺序复核补记（2026-07-06）

- 对应 `data/review_queue.jsonl` 第 48 行；本轮按顺序复核 knowledge 文件、review_queue、p30/p36、completeness 与 source FTS。
- 该条已在高风险轮次完成；本轮确认继续保持 `no_source_found` 与动物/限制性材料外部权威来源边界，不重复改动知识正文。
