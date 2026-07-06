# gaoliangjiang 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/gaoliangjiang.md`
- **队列位置：** `data/p36_external_source_queue.jsonl` 第 41 行；`data/p30_no_source_classification.jsonl` 第 41 行
- **条目：** 高良姜

## 当前文件概况

当前 Markdown frontmatter 为 `trace_status: no_source_found`、`review_status: no_source_found`、`source_refs: []`。正文仅保留 P5 标准学习与安全边界、来源追溯状态和空内容边界，没有扩写性味、归经、功效、主治、剂量或禁忌。

## 队列与索引摘要

1. `data/p36_external_source_queue.jsonl`
   - `current_classification=external_source_required`
   - `p7b_category=herb_standard`
   - `risk_tier=low`
   - 推荐来源范围：`official_pharmacopoeia`、`modern_tcm_reference`、`classical_tcm_text`。
2. `data/p30_no_source_classification.jsonl`
   - `no_source_classification=external_source_required`
   - 原因：当前倪海厦语料库无可追溯来源；未来扩写需要白名单外部来源与人工复核。
3. `data/herb_index.jsonl`
   - `trace_status=no_source_found`
   - `source_refs=[]`
4. `data/knowledge_completeness.jsonl`
   - `quality_tier=needs_source`
   - `source_scope=nihaixia_corpus_not_found`
   - `required_review=manual_review_required_before_content_or_quality_promotion`

## FTS 摘要

只读检索 `data/source_fts.sqlite`：

- `高良姜`：无命中。
- `良姜`：无命中。

历史 `data/review_decisions.jsonl` 中曾有 `神农本草经.json` 片段提到“杜若，即今之高良姜”，但该片段是杜若条下的别名/考据语境，不足以支撑高良姜作为独立药材条目的系统性内容扩写。

## 核查结论

维持 `no_source_found` 与 `external_source_required`。当前文件边界清晰，不应凭模型记忆或非白名单外部资料补入性味、归经、功效、主治、剂量、禁忌等内容。

## 修改/不修改理由

本轮未修改知识正文：当前 Markdown 已为空壳边界状态，未发现来源不支撑的扩写正文或医学安全边界缺失。只补充本 review note 作为 P36/P30 人工核查记录。

## 未决问题

若未来要补全高良姜，应优先使用官方药典、权威现代中药学参考或经典本草来源，逐条记录 `source_refs`，再进行人工复核和内容提升。