# leigongteng 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/herbs/leigongteng.md`
- **风险分类：** `herb_high_risk`

## 当前文件概况

当前条目为种子型 `no_source_found` 页面。原文件包含“来源：神农本草经”“性味：苦辛寒”“功效：祛风湿，活血通络，消肿止痛”“倪师讲解：顽痹肿痛”等种子内容，但 registry 与 FTS 均未给出可追溯来源。P8 本轮将既有功效/讲解明确标为待外部来源核验，不新增医学内容。

## 查到的来源 / 引用摘要

1. `data/herb_sources.jsonl`
   - `herb_id=leigongteng`
   - `searched_keywords=["雷公藤"]`
   - `source_hits=[]`，`source_hit_count=0`，`status=no_source_found`
2. `data/review_queue.jsonl`
   - `review_status=no_source_found`
   - `reason=未检索到来源候选`
3. `data/source_fts.sqlite`
   - 以“雷公藤”检索 `source_pages_fts`，无命中
4. `data/p30_no_source_classification.jsonl` / `data/p36_external_source_queue.jsonl` / `data/p39_high_risk_external_review_queue.jsonl`
   - 一致标记为 `external_source_required` 与 `herb_high_risk`
   - 要求外部权威来源和完整安全字段复核

## 修改点

1. frontmatter 增加 `reviewer: p8_manual_source_refinement`
2. frontmatter 增加 `review_status: pending_external_authoritative_source`
3. frontmatter 增加 `risk_tier: high`
4. 将“功效”标题改为“功效（待外部来源核验）”，并说明原种子内容不可作为用药依据
5. 将“倪师讲解”标题改为“倪师讲解（未检出可追溯原文）”
6. 正文增加“高风险外部来源复核边界（P8 手工）”段落

## 保留边界

- 保持 `trace_status: no_source_found`
- 不删除历史种子内容，但明确降级为待核验占位
- 不补写剂量、毒性、禁忌、妊娠/儿童或相互作用

## 未决问题

- 既有“性味/功效/顽痹肿痛”种子内容来源不明，后续需决定是否删除、迁移为候选字段，或用外部权威来源核验
- 若后续扩写，需确定药典或现代中药学权威来源版本

## 是否需要外部权威资料

**需要。** 当前内部语料无命中；作为高风险药材，后续扩写必须依赖药典或同等级权威资料。