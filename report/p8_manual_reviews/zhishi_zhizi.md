# P8 人工来源复核：枳实栀子豉汤（zhishi_zhizi）

- 复核时间：2026-07-06
- 队列位置：`data/review_queue.jsonl` 第 5 行
- 当前知识文件：`knowledge/formulas/zhishi_zhizi.md`
- 条目类型：方剂

## 当前文件概况

当前条目 frontmatter 为：

- `review_status: verified`
- `trace_status: verified`
- `source: 伤寒论`
- `category: 清热剂`
- `source_refs` 已指向 `桂林古本伤寒杂病论 .json`

正文包含组成、主治、倪师讲解、临证加减、现代应用、来源摘录与功效。正文中“临证加减”“现代应用/药理研究”不由本轮古本 exact-name quote 自动验证。

## 来源引用摘要

### review_queue / top_source

`data/review_queue.jsonl` 第 5 行候选来源为 `桂林古本伤寒杂病论 .json`，quote 明确包含：

> 大病差后，劳复者，枳实栀子豉汤主之；若有宿食者，加大黄如博棋子大五六枚。枳实栀子豉汤方 枳实三枚（炙） 栀子十四枚（劈）香豉一升（棉襄）……温分再服，覆令微似汗。

### formula_sources / formula_index

`data/formula_sources.jsonl` 与 `data/formula_index.jsonl` 均有 `zhishi_zhizi` 记录：

- exact name 命中“枳实栀子豉汤”
- `searched_keywords` 包含“枳实栀子豉汤”“枳实栀子汤”“枳实栀豉汤”
- `matched_keyword: 枳实栀子豉汤`
- `quality_score: 77`
- `match_reason` 包含 `matched_exact_name`、`primary_keyword`、`preferred_source_file`、`contains_tcm_context_keyword`
- `risk_flags: []`

`formula_sources` 还收录了倪海厦《金匮要略》相关讲解，包含劳复、豆豉需包煮、清浆水煮法、宿食加大黄等内容。

### source_fts.sqlite 只读检索

对 `source_fts.sqlite` 进行只读检索时，完整方名 FTS match 未返回额外命中；基础表 `source_pages` 中可检得枳实、栀子等药名零散出现。因 `review_queue` 与 `formula_sources` 已有完整方名和条文 quote，本轮未用零散药名命中替代原文依据。

## 核查结论

- 方名、主治“大病差后，劳复”、组成、煎服法、宿食加大黄的方后说明，可由 `桂林古本伤寒杂病论 .json` 的 exact-name quote 直接支撑。
- 当前 frontmatter 的 `verified` / `trace_status: verified` 与 `source_refs` 可保留。
- 倪师讲解来源摘录与 `formula_sources` 中人纪讲稿可互相印证为讲解线索。

## 修改/不修改理由

本轮不修改知识正文，仅新增本人工复核记录。理由：

1. 当前 `source_refs` 足以支撑方名、条文、组成与煎服法的来源追溯。
2. 正文“组成”以现代克数列剂量，而古本为“枳实三枚、栀子十四枚、香豉一升”；是否替换或并列显示需统一剂量治理，不在本轮单条贸然改写。
3. 正文“临证加减”“现代应用”“药理研究”未逐项追溯原始来源，本轮不把这些内容提升为 verified。

## 未决问题

- 建议后续统一处理古籍剂量与现代克数之间的展示规则。
- “心中懊憹、胸脘痞闷、失眠、焦虑症、慢性胃炎”等扩展主治/现代应用需另行来源核查。
- `香豉/淡豆豉`、`棉襄/绵裹` 等术语差异建议纳入后续术语标准化。
