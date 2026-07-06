# biandou 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/herbs/biandou.md`
- **队列位置：** `data/review_queue.jsonl` 第 15 行
- **条目：** 白扁豆

## 当前文件概况

当前条目 frontmatter 标记 `trace_status: no_source_found`，但原 frontmatter 边界异常，`source_scope` 等字段落在正文。本轮修正边界。正文已有基础信息、功效、主治和一段《金匮要略》“扁豆，寒热者不可食之”候选引文。

## 查到的来源 / 引用摘要

1. `data/review_queue.jsonl`
   - `review_status=needs_review`
   - 原因：`alias_match_only；alias_requires_review`
   - top_source 来自 `金匮要略.json`，命中词为「扁豆」
2. `data/herb_sources.jsonl`
   - 检索关键词：`白扁豆 / 扁豆 / 白藊豆`
   - 仅有别名候选，`quality_score=16`
3. `data/herb_index.jsonl` / `data/knowledge_completeness.jsonl`
   - `p1_resolution=frontmatter no_source_found prevails over weak alias candidate`
4. `data/p30_no_source_classification.jsonl` / `data/p36_external_source_queue.jsonl`
   - `no_source_classification=external_source_required`
   - `p7b_category=herb_standard`，`risk_tier=low`
5. `data/source_fts.sqlite`
   - 只读检索仅见「扁豆」命中 1 条；未见「白扁豆 / 白藊豆」命中

## 修改点

- 修正 frontmatter 边界。
- 增加 P8 手工来源边界说明，明确该候选仅为扁豆食忌线索，不能作为白扁豆专门来源。
- 调整学习边界中的来源表述。

## 保留边界

- 保持 `trace_status: no_source_found`。
- 不删除原候选摘录，但不提升质量。
- 现有功效主治等需外部权威来源核验。

## 下一步

需先确认白扁豆与扁豆在本库命名中的对应关系，再使用外部权威来源补证。
