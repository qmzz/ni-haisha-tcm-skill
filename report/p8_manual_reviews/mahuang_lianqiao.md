# mahuang_lianqiao 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/formulas/mahuang_lianqiao.md`
- **队列位置：** `data/review_queue.jsonl` 方剂队列第 3 条

## 当前文件概况

当前条目 frontmatter 已为 `trace_status: verified`，并含 `source_refs` 指向 `桂林古本伤寒杂病论 .json`。正文包含 P5 学习与安全边界、组成、主治、倪师讲解、来源摘录与功效段落。

## 对照来源 / 引用摘要

1. `data/review_queue.jsonl`
   - `item_id=mahuang_lianqiao`
   - `review_status=needs_review`
   - `top_source.source_file=桂林古本伤寒杂病论 .json`
   - `matched_keyword=麻黄连轺赤小豆汤`
   - `quality_score=74`
   - `risk_flags=[]`
   - 引文包含“伤寒瘀热在里，其身必黄，麻黄连轺赤小豆汤主之”及方后组成、煎服法
2. `data/formula_sources.jsonl`
   - `source_hit_count=21`，状态为 `candidate`
   - exact name 命中桂林古本；另有“麻黄连翘赤小豆汤 / 麻黄连翘赤小豆”别名命中，带 `alias_match_only` 风险标记
3. `data/formula_index.jsonl`
   - 当前已登记 `trace_status=verified`
   - `source_refs` 与知识文件 frontmatter 一致
4. `data/source_fts.sqlite`
   - 来源摘录与当前 frontmatter quote 可互相对照，直接命中方名和方后组成

## 复核结论

- `review_queue` 的 top_source 可直接支撑“麻黄连轺赤小豆汤”方名、主治条文和方后组成。
- “连轺/连翘”“赤小豆/赤子豆”等文本差异需保留为版本/别名复核线索；本轮不自动合并或改写。
- 当前知识文件中的 `source_refs` 与队列 top_source 一致，保留 verified 状态合理。
- 本轮不改写正文剂量、功效、现代应用或临证加减；这些内容如需进一步校准，应另开内容质量复核任务，逐项绑定来源。

## 修改点

- 本轮仅新增本手工复核记录；未修改知识正文。

## 未决问题

- 是否在 alias registry 中明确“麻黄连翘赤小豆汤”与“麻黄连轺赤小豆汤”的关系，需要另行人工确认。
- 正文中现代应用、药理研究、临证加减等内容未在本轮逐项追溯。
