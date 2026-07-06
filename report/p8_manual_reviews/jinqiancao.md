# 金钱草 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/herbs/jinqiancao.md`
- **队列位置：** `data/review_queue.jsonl` 第 64 行
- **条目：** 金钱草 (`jinqiancao`)

## 当前文件概况

复核前队列状态为 `no_source_found`；本轮人工读取 knowledge 文件、review_queue 行，并核对 `data/herb_sources.jsonl`、`data/herb_index.jsonl`、`data/knowledge_completeness.jsonl`、`data/p30_no_source_classification.jsonl`、`data/p36_external_source_queue.jsonl`，只读查询 `data/source_fts.sqlite`。

## 查到的来源 / 引用摘要

- source FTS/LIKE 未检出该名称可追溯命中。
- `herb_sources`：`source_hits=[]`，`source_hit_count=0`，`status=no_source_found`。
- p30：`external_source_required`；canonical=`None`；risk=`low`。
- p36：`external_source_required`；分类=`herb_standard`；建议来源范围=`official_pharmacopoeia`、`modern_tcm_reference`、`classical_tcm_text`。
- completeness：trace=`no_source_found`，quality=`no_source`。

## 修改点

- 在知识文件中补充 P8 手工来源复核/外部权威来源边界说明。
- 未新增功效、主治、剂量、禁忌等医学正文。

## 保留边界

- no_source/external_source_required 条目继续保持未验证边界；既有医学性字段仅作为待核验草稿或占位。
- 弱候选或上下文提及不等于医学内容全字段验证。

## 下一步

后续若纳入外部来源，应逐条补充明确 `source_refs`，并单独核验性味、归经、功效、主治、剂量、禁忌及特殊安全字段。
