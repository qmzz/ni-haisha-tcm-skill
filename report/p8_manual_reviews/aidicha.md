# aidicha 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/herbs/aidicha.md`
- **队列位置：** `data/review_queue.jsonl` 第 6 行
- **条目：** 矮地茶

## 当前文件概况

当前条目 frontmatter 为 `trace_status: no_source_found`，并带有 `external_reference_required: true` 与 `no_source_policy: keep_boundary_until_traceable_source`。正文已有来源、分类、性味、归经、功效、主治等医学性内容，但“倪师讲解”为空；这些医学性内容未见倪海厦内部来源支撑。

## 查到的来源 / 引用摘要

1. `data/review_queue.jsonl`
   - `review_status=no_source_found`
   - `top_source=null`
   - `source_quality_level=no_source`
2. `data/herb_sources.jsonl`
   - 检索关键词：`矮地茶 / 紫金牛 / 平地木 / 叶下红`
   - `source_hits=[]`，`source_hit_count=0`
3. `data/herb_index.jsonl` / `data/knowledge_completeness.jsonl`
   - `trace_status=no_source_found`
   - `no_source_classification=external_source_required`
   - `p7b_category=herb_modern_or_regional`，`risk_tier=low`
4. `data/p30_no_source_classification.jsonl` / `data/p36_external_source_queue.jsonl`
   - 均要求外部权威来源与人工复核后才可扩写或质量提升
5. `data/source_fts.sqlite`
   - 只读检索 `矮地茶 / 紫金牛 / 平地木 / 叶下红`，未见命中

## 修改点

- 在“倪师讲解”下补充无内部来源边界说明。
- 增加“来源边界说明（P8 手工复核）”，明确 review_queue、herb_sources、FTS 均无可追溯来源。
- 调整学习边界中的来源表述，避免声称当前内容来源于倪海厦教学资料。

## 保留边界

- 保持 `trace_status: no_source_found`。
- 不补写新的功效、主治、剂量、禁忌或临床用法。
- 已有医学性内容仅标为待外部权威来源核验，不提升质量等级。

## 下一步

若需扩写或验证现有医学内容，应引入白名单外部来源（如官方药典、现代中药学权威参考或经典本草），并逐条记录 `source_refs` 后再人工复核。
