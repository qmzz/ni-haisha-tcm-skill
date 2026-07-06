# 马钱子 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/herbs/maqianzi.md`
- **队列位置：** `data/review_queue.jsonl` 第 82 行
- **条目：** 马钱子 (`maqianzi`)

## 当前文件概况

复核前队列状态为 `no_source_found`；该条目已在前序高风险药材轮次完成正文边界处理。本轮人工读取 knowledge 文件、review_queue 行，并核对 `data/herb_sources.jsonl`、`data/herb_index.jsonl`、`data/knowledge_completeness.jsonl`、`data/p30_no_source_classification.jsonl`、`data/p36_external_source_queue.jsonl`，只读查询 `data/source_fts.sqlite`。

## 查到的来源 / 引用摘要

- source FTS/LIKE 未检出“马钱子”可追溯命中。
- `herb_sources`：`source_hits=[]`，`source_hit_count=0`，`status=no_source_found`。
- p30/p36：`external_source_required`，risk=`high`，高风险安全字段要求保留，未满足前不得补写/提升医学内容。
- completeness：trace=`no_source_found`，quality=`no_source`。

## 修改点

- 本轮仅更新 review note；正文已含 P8 高风险外部来源复核边界，未重复修改。
- 未新增功效、主治、剂量、禁忌等医学正文。

## 保留边界

- 高风险 no_source 条目必须等待药典/权威现代中药学等外部来源，并逐项补齐毒性、禁忌、妊娠/哺乳/儿童、剂量、炮制/用法、相互作用/现代注意、法定限制、急症红旗等字段。

## 下一步

后续若纳入外部来源，应逐条补充明确 `source_refs`，并单独核验所有安全字段。
