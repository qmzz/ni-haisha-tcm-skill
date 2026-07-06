# baidoukou 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/herbs/baidoukou.md`
- **队列位置：** `data/review_queue.jsonl` 第 10 行
- **条目：** 白豆蔻

## 当前文件概况

当前条目 frontmatter 标记 `trace_status: no_source_found`，但原文件 frontmatter 结束位置异常，`source_scope` 等字段落在正文之外。本轮修正 frontmatter 边界。正文已有基础信息、功效、主治和一段「豆蔻」候选引文；该引文为别名级弱命中，不能作为白豆蔻专门来源。

## 查到的来源 / 引用摘要

1. `data/review_queue.jsonl`
   - `review_status=needs_review`
   - 原因：`alias_match_only；alias_requires_review`
   - top_source 来自 `02【视频同步文稿】人-神农本草经（可打印）.json` 第 131 页，命中词为「豆蔻」
2. `data/herb_sources.jsonl`
   - 检索关键词：`白豆蔻 / 豆蔻 / 白蔻仁 / 白蔻`
   - 仅有 1 条候选，`matched_keyword=豆蔻`，`quality_score=31`
3. `data/herb_index.jsonl` / `data/knowledge_completeness.jsonl`
   - `trace_status=no_source_found`
   - `p1_resolution=frontmatter no_source_found prevails over weak alias candidate`
4. `data/p30_no_source_classification.jsonl` / `data/p36_external_source_queue.jsonl`
   - `no_source_classification=external_source_required`
   - `p7b_category=herb_standard`，`risk_tier=low`
5. `data/source_fts.sqlite`
   - 只读检索 `白豆蔻 / 豆蔻 / 白蔻仁 / 白蔻` 未见可支撑本条的直接命中

## 修改点

- 修正 frontmatter 边界，将 `source_scope` / `external_reference_required` / `no_source_policy` 纳入 frontmatter。
- 增加 P8 手工来源边界说明，明确「豆蔻」候选为弱别名命中。
- 调整学习边界中的来源表述。

## 保留边界

- 保持 `trace_status: no_source_found`。
- 不删除原候选摘录，但明确不能作为白豆蔻专门来源。
- 不新增医学正文；已有功效主治需外部权威来源核验。

## 下一步

后续需以官方药典、现代中药学参考或经典本草确认白豆蔻来源、性味归经、功效主治与禁忌后，再补充可追溯 `source_refs`。
