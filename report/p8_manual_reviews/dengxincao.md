# 灯心草 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/herbs/dengxincao.md`
- **队列位置：** `data/review_queue.jsonl` 第 31 行
- **条目：** 灯心草

## 当前文件概况

当前条目类型为药材，复核前队列状态为 `needs_review / contextual candidate`。本轮读取当前 knowledge 文件、review_queue 行、`data/herb_sources.jsonl`、`data/herb_index.jsonl`、`data/knowledge_completeness.jsonl`、`data/p30_no_source_classification.jsonl`、`data/p36_external_source_queue.jsonl`（如适用），并对 `data/source_fts.sqlite` 作只读检索。

## 查到的来源 / 引用摘要

- `review_queue`：第 31 行记录为 `needs_review / contextual candidate`。
- `herb_sources` / `herb_index` / `knowledge_completeness`：未形成可逐项支撑本草正文的直接来源链；若为 verified/contextual 条目，仅表示内部语料中有可追溯提及。
- `p30/p36`：no_source 条目均要求人工复核后再考虑外部权威来源；不得凭模型记忆扩写正文。
- `source_fts.sqlite`：队列候选为分消汤语境，review_decisions 已保留 verified；FTS 未额外检出条目页。

## 修改点

- 在知识文件中新增/修正 P8 手工来源边界说明。
- 未新增功效、主治、剂量、禁忌等医学正文。
- 对 contextual 或 exact-name 弱验证条目，仅限定为可追溯提及，不扩展到全部医学字段验证。

## 保留边界

- no_source/external_source_required 条目继续保持未验证边界；既有医学性字段仅作为待核验草稿或占位。
- verified_contextual/弱验证条目不等于医学内容全字段验证。

## 下一步

后续若纳入外部来源，应逐条补充明确 `source_refs`，并单独核验性味、归经、功效、主治、剂量、禁忌等字段。
