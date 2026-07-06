# 芦根 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/herbs/lugen.md`
- **队列位置：** `data/review_queue.jsonl` 第 73 行
- **条目：** 芦根 (`lugen`)

## 当前文件概况

复核前队列状态为 `needs_review`；本轮人工读取 knowledge 文件、review_queue 行，并核对 `data/herb_sources.jsonl`、`data/herb_index.jsonl`、`data/knowledge_completeness.jsonl`，只读查询 `data/source_fts.sqlite`。

## 查到的来源 / 引用摘要

- `review_queue` top_source 与 `herb_sources` 均指向《金匮要略》食禁/食物中毒语境，包含“芦根煮汁，服之即解”“煮芦根汁饮之，良”等片段。
- source FTS/LIKE 检出 2 处“芦根”命中，均为《金匮要略》同类食物中毒解救语境。
- `herb_index` / completeness 当前为 trace=`verified`，quality=`verified_direct`，但 queue 标记 `needs_review` 原因是 quality_score 低于 verified 阈值。

## 修改点

- 本轮仅写 review note 记录：该来源可证明倪师语料/经方语料中提及“芦根”及相关煮汁用法语境。
- 未改知识正文，避免把食禁章节片段扩展为性味、归经、通用功效、主治、剂量或禁忌的全字段验证。

## 保留边界

- 该命中是特定语境提及，不等于本草全字段验证。
- 后续若提升医学正文质量，应另行核验性味、归经、功效、主治、剂量和禁忌，并补足明确 source_refs。

## 下一步

继续从 `luhui` / 芦荟之后的 no_source/external_source 条目推进；对已在高风险轮次处理的条目只复核记录，不重复改正文。
