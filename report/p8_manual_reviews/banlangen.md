# banlangen 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/herbs/banlangen.md`
- **队列位置：** `data/review_queue.jsonl` 第 13 行
- **条目：** 板蓝根

## 当前文件概况

当前条目为 `trace_status: verified`，frontmatter 引用 `05【视频同步文稿】人-金匮要略（可打印）.json` 第 260 页。正文主要为来源摘录，未列出完整基础信息段。现有引用是在水病/表证失治语境中提及板蓝根并作负面评价。

## 查到的来源 / 引用摘要

1. `data/review_queue.jsonl`
   - `review_status=needs_review`
   - `quality_score=53`
   - 候选为 exact-name「板蓝根」命中
2. `data/herb_sources.jsonl`
   - 对板蓝根 `source_hits=[]`，但后续索引已有 raw_search_contextual_hit
3. `data/herb_index.jsonl` / `data/knowledge_completeness.jsonl`
   - `source_quality_level=verified_contextual`
   - `p7a_rationale=quote mentions item but lacks conservative direct marker; retained as contextual trace only`
4. `data/source_fts.sqlite`
   - FTS MATCH 对长词无额外命中；只读 LIKE 可复现第 260 页 exact-name 片段

## 修改点

- 在 P5 来源追溯状态中加入 P8 手工复核说明。
- 在正文增加“来源边界说明（P8 手工复核）”，明确该引用为 contextual trace，不支撑功效主治等字段。

## 保留边界

- 保留 `trace_status: verified` 与 `verified_contextual` 边界。
- 不新增基础信息、功效、主治或禁忌。
- 不把倪师负面评价片段扩大解释为系统本草条文。

## 下一步

若需完善板蓝根条目的本草字段，应另行引入外部权威资料；若只维护倪师语料，应保留为 contextual trace。
