# biba 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/herbs/biba.md`
- **队列位置：** `data/review_queue.jsonl` 第 16 行
- **条目：** 荜澄茄

## 当前文件概况

当前条目为 `trace_status: no_source_found`，frontmatter 有 `aliases: ["bichengqie"]`。正文已有来源、性味、归经、功效、主治，但“倪师讲解”为空，未见内部语料支撑。

## 查到的来源 / 引用摘要

1. `data/review_queue.jsonl`
   - `review_status=no_source_found`
   - `top_source=null`
2. `data/herb_sources.jsonl`
   - 检索关键词：`荜澄茄`
   - `source_hits=[]`，`source_hit_count=0`
3. `data/herb_index.jsonl` / `data/knowledge_completeness.jsonl`
   - `no_source_classification=alias_or_duplicate_mapped`
   - canonical 映射为 `bichengqie`
   - canonical 仍为 no_source
4. `data/p30_no_source_classification.jsonl` / `data/p36_external_source_queue.jsonl`
   - `p7b_category=alias_first`，`risk_tier=medium`
   - 需先处理 canonical/alias
5. `data/source_fts.sqlite`
   - 只读检索「荜澄茄 / 毕澄茄」未见命中

## 修改点

- 在“倪师讲解”下补充无内部来源边界说明。
- 增加 P8 手工来源边界说明，明确 canonical `bichengqie` 仍为 no_source。
- 调整学习边界中的来源表述。

## 保留边界

- 保持 `trace_status: no_source_found` 与 alias/canonical 边界。
- 不新增医学正文。
- 现有基础信息、功效、主治需外部权威来源核验。

## 下一步

与 `bichengqie` 条目合并复核或确认 canonical 后，再引入官方药典或现代中药学来源。
