# baizhu_fuzi 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/formulas/baizhu_fuzi.md`
- **队列位置：** `data/review_queue.jsonl` 方剂队列第 1 条

## 当前文件概况

当前条目 frontmatter 已为 `trace_status: verified`，并含 `source_refs` 指向 `桂林古本伤寒杂病论 .json`。正文包含 P5 学习与安全边界、组成、主治、用法、倪师讲解与来源摘录。

## 对照来源 / 引用摘要

1. `data/review_queue.jsonl`
   - `item_id=baizhu_fuzi`
   - `review_status=needs_review`
   - `top_source.source_file=桂林古本伤寒杂病论 .json`
   - `matched_keyword=白术附子汤`
   - `quality_score=74`
   - `risk_flags=[]`
   - 引文包含“若大便坚，小便自利者，白术附子汤主之”及“白术附子汤方 白术一两 附子一枚（炮） 甘草二两（炙） 生姜一两半 大枣六枚……”
2. `data/formula_sources.jsonl`
   - `source_hit_count=46`，状态为 `candidate`
   - 前几条命中包括桂林古本原文、金匮要略同步文稿及倪海厦金匮讲解
3. `data/formula_index.jsonl`
   - 当前已登记 `trace_status=verified`
   - `source_refs` 与知识文件 frontmatter 一致，reviewer 为 `p8_formula_verified_batch`
4. `data/source_fts.sqlite`
   - 来源摘录与当前 frontmatter quote 可互相对照，直接命中方名和方后组成

## 复核结论

- `review_queue` 的 top_source 可直接支撑“白术附子汤”方名、条文和方后组成。
- 当前知识文件中的 `source_refs` 与队列 top_source 一致，保留 verified 状态合理。
- 本轮不改写正文剂量、功效、现代应用或临证加减；这些内容如需进一步校准，应另开内容质量复核任务，逐项绑定来源。

## 修改点

- 本轮仅新增本手工复核记录；未修改知识正文。

## 未决问题

- 正文中现代应用、药理研究、临证加减等内容未在本轮逐项追溯。
- 若未来提升内容可信度，建议将“来源摘录”与正文每个医学断言逐项映射。
