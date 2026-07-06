# bibo 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/herbs/bibo.md`
- **队列位置：** `data/review_queue.jsonl` 第 17 行
- **条目：** 荜茇

## 当前文件概况

当前条目为 `trace_status: no_source_found`，正文已有学习边界、来源追溯状态和基础信息。基础信息中的分类、性味、归经均已标注“待外部来源验证”，整体较符合 no_source 边界。

## 查到的来源 / 引用摘要

1. `data/review_queue.jsonl`
   - `review_status=no_source_found`
   - `top_source=null`
2. `data/herb_sources.jsonl`
   - 检索关键词：`荜茇`
   - `source_hits=[]`，`source_hit_count=0`
3. `data/herb_index.jsonl` / `data/knowledge_completeness.jsonl`
   - `trace_status=no_source_found`
   - `no_source_classification=external_source_required`
4. `data/p30_no_source_classification.jsonl` / `data/p36_external_source_queue.jsonl`
   - `p7b_category=herb_standard`，`risk_tier=low`
   - 推荐外部来源范围为官方药典、现代中药学参考、经典本草
5. `data/source_fts.sqlite`
   - 只读检索「荜茇 / 毕拨 / 荜拨」未见命中

## 修改点

- 在既有来源边界说明后增加 P8 手工复核说明，记录 review_queue、herb_sources 与 FTS 结果。

## 保留边界

- 保持 `trace_status: no_source_found`。
- 不新增功效、主治、剂量或禁忌。
- 已标“待外部来源验证”的基础字段继续保守保留，不升级质量。

## 下一步

引入白名单外部来源后再补充 source_refs；否则只保留边界页。
