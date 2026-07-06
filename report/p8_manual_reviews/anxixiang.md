# anxixiang 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/herbs/anxixiang.md`
- **队列位置：** `data/review_queue.jsonl` 第 7 行
- **条目：** 安息香

## 当前文件概况

当前条目 frontmatter 为 `trace_status: no_source_found`，并要求外部来源。正文已有来源、分类、性味、归经、功效、主治等医学性内容，但“倪师讲解”为空；这些内容未见倪海厦内部语料支撑。

## 查到的来源 / 引用摘要

1. `data/review_queue.jsonl`
   - `review_status=no_source_found`
   - `top_source=null`
2. `data/herb_sources.jsonl`
   - 检索关键词：`安息香 / 拙贝罗香`
   - `source_hits=[]`，`source_hit_count=0`
3. `data/herb_index.jsonl` / `data/knowledge_completeness.jsonl`
   - `trace_status=no_source_found`
   - `no_source_classification=external_source_required`
4. `data/p30_no_source_classification.jsonl` / `data/p36_external_source_queue.jsonl`
   - `p7b_category=herb_standard`，`risk_tier=low`
   - 要求外部权威来源与人工复核后才可扩写或提升质量
5. `data/source_fts.sqlite`
   - 只读检索 `安息香 / 拙贝罗香`，未见命中

## 修改点

- 在“倪师讲解”下补充无内部来源边界说明。
- 增加 P8 手工来源边界说明，列明 review_queue、herb_sources、FTS 均未发现来源。
- 调整学习边界中的来源表述，避免将无来源内容归为倪海厦教学资料。

## 保留边界

- 保持 `trace_status: no_source_found`。
- 不新增任何医学正文。
- 已有基础信息、功效与主治仅作为待核验内容保留，不升级质量。

## 下一步

如需继续治理，应先引入官方药典、现代中药学参考或经典本草等白名单外部来源，并人工确认对应 `source_refs`。
