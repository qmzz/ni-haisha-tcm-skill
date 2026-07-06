# 天竺黄 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/herbs/tianzhuhuang.md`
- **队列位置：** `data/review_queue.jsonl` 第 111 行
- **条目：** 天竺黄 (`tianzhuhuang`)

## 当前文件概况

本轮人工读取 knowledge 文件、review_queue 行，并核对 `data/herb_sources.jsonl`、`data/herb_index.jsonl`、`data/knowledge_completeness.jsonl`、`data/p30_no_source_classification.jsonl`、`data/p36_external_source_queue.jsonl`，只读查询 `data/source_fts.sqlite`。

## 查到的来源 / 引用摘要

- review_queue：`no_source_found`；reason=`未检索到来源候选`。
- herb_sources：status=`no_source_found`，source_hit_count=`0`，searched_keywords=['天竺黄'].
- herb_index：trace_status=`no_source_found`，source_quality_level=`no_source`，source_refs_count=0.
- completeness：trace_status=`no_source_found`，quality_tier=`seed`，source_quality_level=`no_source`。
- p30：classification=`external_source_required`，canonical_item_id=`None`，risk_tier=`low`。
- p36：category=`herb_standard`，risk_tier=`low`，recommended_source_scopes=['official_pharmacopoeia', 'modern_tcm_reference', 'classical_tcm_text'].
- source FTS/LIKE：按名称 `天竺黄` 检索得到 0 条 LIKE 命中；未检出可追溯命中。

## 修改点

- 本轮新增 P8 手工复核记录；no_source 条目仅补来源边界和外部权威来源需求，未补医学正文。

## 保留边界

- `no_source_found` / `external_source_required` 条目继续保持未验证边界；既有医学性字段仅作为待核验草稿或占位。
- 弱候选、上下文提及、别名/重复映射线索不等于医学内容全字段验证。

## 下一步

后续若纳入外部来源，应逐条补充明确 `source_refs`，并单独核验性味、归经、功效、主治、剂量、禁忌及特殊安全字段。
