# aoshu 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/herbs/aoshu.md`
- **队列位置：** `data/review_queue.jsonl` 第 8 行
- **条目：** 糯稻根

## 当前文件概况

当前条目为 `trace_status: no_source_found`，正文已有来源、分类、性味、归经、功效、主治等医学性内容，但未见倪海厦内部可追溯来源。“倪师讲解”原为空。

## 查到的来源 / 引用摘要

1. `data/review_queue.jsonl`
   - `review_status=no_source_found`
   - `top_source=null`
2. `data/herb_sources.jsonl`
   - 检索关键词：`糯稻根 / 稻根 / 稻根须 / 糯稻根须`
   - `source_hits=[]`，`source_hit_count=0`
3. `data/herb_index.jsonl` / `data/knowledge_completeness.jsonl`
   - `trace_status=no_source_found`
   - canonical 映射为 `nuodaogenxu`
   - `p7ba_outcome=canonical_is_no_source_stays_no_source`
4. `data/p30_no_source_classification.jsonl` / `data/p36_external_source_queue.jsonl`
   - `p7b_category=alias_first`，`risk_tier=medium`
   - 需先处理 canonical/alias，再做外部来源治理
5. `data/source_fts.sqlite`
   - 只读检索上述关键词，未见命中

## 修改点

- 在“倪师讲解”下补充无内部来源边界说明。
- 增加 P8 手工来源边界说明，明确 canonical 仍为 no_source。
- 调整学习边界中的来源表述，避免声称已有医学性内容来自倪海厦语料。

## 保留边界

- 保持 `trace_status: no_source_found`。
- 不新增功效、剂量、禁忌或临床用法。
- 现有医学性内容需外部权威来源核验，不升级质量。

## 下一步

优先确认 `糯稻根`、`糯稻根须` 与 canonical `nuodaogenxu` 的命名/别名关系；随后基于白名单外部来源补充或校正内容。
