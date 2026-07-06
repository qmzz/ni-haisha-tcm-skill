# P8 人工来源复核：牡蛎泽泻散（muli_zexie）

- 复核时间：2026-07-06
- 队列位置：`data/review_queue.jsonl` 第 4 行
- 当前知识文件：`knowledge/formulas/muli_zexie.md`
- 条目类型：方剂

## 当前文件概况

当前条目 frontmatter 为：

- `review_status: verified`
- `trace_status: verified`
- `source: 伤寒论`
- `category: 利水剂`
- `source_refs` 已指向 `桂林古本伤寒杂病论 .json`

正文包含组成、主治、倪师讲解、临证加减、现代应用、来源摘录与功效。正文中“临证加减”“现代应用/药理研究”属于后续内容质量核查范围，本轮未将这些内容视为已由古本条文直接验证。

## 来源引用摘要

### review_queue / top_source

`data/review_queue.jsonl` 第 4 行候选来源为 `桂林古本伤寒杂病论 .json`，quote 明确包含：

> 大病差后，从腰以下有水气者，牡蛎泽泻散主之。牡蛎泽泻散方 牡蛎 泽泻 括蒌根 蜀漆（洗去腥）葶历（熬）商陆根（熬）海藻（洗去腥）……右七味等分……白饮和服方寸匙，日三服，小便利止后服。

### formula_sources / formula_index

`data/formula_sources.jsonl` 与 `data/formula_index.jsonl` 均有 `muli_zexie` 记录：

- exact name 命中“牡蛎泽泻散”
- `matched_keyword: 牡蛎泽泻散`
- `quality_score: 80`
- `match_reason` 包含 `matched_exact_name`、`primary_keyword`、`preferred_source_file`、`contains_tcm_context_keyword`
- `risk_flags: []`

同时 `formula_sources` 中还收录了倪海厦《金匮要略》讲解片段，支持“腰以下水肿”“散剂”“小便利止后服”及蜀漆/商陆等讲解线索。

### source_fts.sqlite 只读检索

对 `source_fts.sqlite` 进行只读检索时，FTS 表名为 `source_pages_fts`；直接用完整方名进行 FTS match 未返回额外命中，改用基础表 `source_pages` 的 `LIKE` 可见相关药名散见于本草讲稿。因 `review_queue` 与 `formula_sources` 已有明确 quote，本轮未依赖零散药名命中提升结论。

## 核查结论

- 方名、主治条文、组成、煎服/服法可由 `桂林古本伤寒杂病论 .json` 的 exact-name quote 直接支撑。
- 当前 frontmatter 的 `verified` / `trace_status: verified` 与 `source_refs` 可保留。
- 倪师讲解片段中也有同名方与方后说明，可作为讲解来源线索保留。

## 修改/不修改理由

本轮不修改知识正文，仅新增本人工复核记录。理由：

1. 当前 `source_refs` 已能支撑方名、条文、方后组成和服法的来源追溯。
2. 正文中“组成”使用现代克数，与古本“等分、方寸匙”并非逐字一致；本轮不贸然改写剂量体系，保留为后续剂量标准化/内容质量任务。
3. “临证加减”“现代应用”“药理研究”未在本轮逐项追溯到原始来源，不升级其医学内容可信度，仅记录待后续复核。

## 未决问题

- 现代克数剂量是否应改为古籍原文剂量或增加“现代换算仅供学习”提示，建议在后续统一剂量治理任务中处理。
- “临证加减”与“现代应用/药理研究”需要独立来源或标注为未核验内容。
- `葶历/葶苈子`、`括蒌根/栝楼根` 等字词差异可在后续术语/异名标准化中统一处理。
