# 荜澄茄 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/herbs/bichengqie.md`
- **队列位置：** `data/review_queue.jsonl` 第 18 行
- **条目：** 荜澄茄

## 当前文件概况

当前条目类型为药材，复核前队列状态为 `no_source_found`。本轮按要求读取当前 knowledge 文件、review_queue 行、`data/herb_sources.jsonl`、`data/herb_index.jsonl`、`data/knowledge_completeness.jsonl`、`data/p30_no_source_classification.jsonl`、`data/p36_external_source_queue.jsonl`（如有），并对 `data/source_fts.sqlite` 作只读检索。

## 查到的来源 / 引用摘要

- `review_queue`：第 18 行记录为 `no_source_found`。
- `herb_sources` / `herb_index` / `knowledge_completeness`：与队列结论一致，未能形成可支撑本条医学正文的直接来源链。
- `p30/p36`：若入列，均要求人工复核后再考虑外部权威来源；不得凭内部弱命中或模型记忆扩写正文。
- `source_fts.sqlite`：FTS 检索「荜澄茄/毕澄茄」无命中；p30/p36 为 alias_first，canonical 仍 no_source。

## 修改点

- 在知识文件中新增/修正 P8 手工来源边界说明。
- 未新增功效、主治、剂量、禁忌等医学正文。
- 对弱命中或通名/别名命中，仅记录可追溯提及边界，不把它扩展为专名条目验证。

## 保留边界

- no_source/external_source_required 条目继续保持未验证边界；既有医学性字段仅作为待核验草稿或占位。
- 需要官方药典、现代中药学参考或经典本草等白名单来源后，方可补充或提升质量。

## 下一步

后续若纳入外部来源，应逐条补充明确 `source_refs`，并单独核验性味、归经、功效、主治、剂量、禁忌等字段。
