# 海金沙 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/herbs/haijinsha.md`
- **队列位置：** `data/review_queue.jsonl` 第 45 行
- **条目：** 海金沙 (`haijinsha`)

## 当前文件概况

复核前队列状态为 `needs_review`；本轮人工读取 knowledge 文件、review_queue 行，并核对 `data/herb_sources.jsonl`、`data/herb_index.jsonl`、`data/knowledge_completeness.jsonl`、`data/p30_no_source_classification.jsonl`、`data/p36_external_source_queue.jsonl`，只读查询 `data/source_fts.sqlite`。

## 查到的来源 / 引用摘要

- source FTS/LIKE 检出多处“海金沙”命中，主要为四逆散加滑石、五倍子、海金沙处理胆结石语境。
- 该命中可证明倪师语料提及海金沙，但不自动验证 frontmatter 中全部性味、归经、功效、主治字段。
- completeness：trace=`verified`，quality=`verified_direct`。

## 修改点

- 本轮仅写 review note 记录来源边界；未改知识正文，避免对既有 verified 元数据作批量性结构调整。
- 未新增功效、主治、剂量、禁忌等医学正文。

## 保留边界

- no_source/external_source_required 条目继续保持未验证边界；既有医学性字段仅作为待核验草稿或占位。
- 弱候选或上下文提及不等于医学内容全字段验证。

## 下一步

后续若纳入外部来源，应逐条补充明确 `source_refs`，并单独核验性味、归经、功效、主治、剂量、禁忌及特殊安全字段。
