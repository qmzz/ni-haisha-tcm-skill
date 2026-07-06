# aoshugen 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/herbs/aoshugen.md`
- **队列位置：** `data/review_queue.jsonl` 第 9 行
- **条目：** 糯稻根须

## 当前文件概况

当前条目 frontmatter 为 `trace_status: no_source_found`，并有 `alias_of: nuodaogenxu`。正文已有基础信息、功效与主治，但没有倪海厦内部可追溯来源支撑；“倪师讲解”原为空。

## 查到的来源 / 引用摘要

1. `data/review_queue.jsonl`
   - `review_status=no_source_found`
   - `top_source=null`
2. `data/herb_sources.jsonl`
   - 检索关键词：`糯稻根须 / 糯稻根 / 稻根须 / 稻根`
   - `source_hits=[]`，`source_hit_count=0`
3. `data/herb_index.jsonl` / `data/knowledge_completeness.jsonl`
   - canonical 映射为 `nuodaogenxu`
   - canonical 仍为 no_source，不能因别名映射提升质量
4. `data/p30_no_source_classification.jsonl` / `data/p36_external_source_queue.jsonl`
   - `p7b_category=alias_first`，`risk_tier=medium`
   - `required_review=manual_review_required_before_content_or_quality_promotion`
5. `data/source_fts.sqlite`
   - 只读检索上述关键词，未见命中

## 修改点

- 在“倪师讲解”下补充无内部来源边界说明。
- 增加 P8 手工来源边界说明，明确 canonical 仍为 no_source。
- 调整学习边界中的来源表述。

## 保留边界

- 保持 `trace_status: no_source_found` 与别名映射。
- 不新增医学正文，不将现有内容升级为 verified。
- 现有基础信息、功效与主治均需外部权威来源核验。

## 下一步

与 `aoshu` 一并确认 canonical/alias 后，再引入官方药典或现代中药学权威来源进行内容校正。
