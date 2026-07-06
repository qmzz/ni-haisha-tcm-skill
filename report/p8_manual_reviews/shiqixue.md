# shiqixue 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/acupoints/shiqixue.md`
- **队列位置：** `data/p36_external_source_queue.jsonl` 第 3 行；`data/p30_no_source_classification.jsonl` 第 3 行
- **条目：** 十七 / 十七穴

## 当前文件概况

复核前 Markdown frontmatter 仍标为 `trace_status: verified`，并保留来自 `金匮要略.json` 的“第十七”章节标题片段；正文还有泛化的定位、主治、刺灸法、配伍等内容。索引侧 `data/acupoint_index.jsonl` 与 `data/knowledge_completeness.jsonl` 已将本条目治理为 `no_source_found` / `contextual_false_positive_demoted`，两边存在 source boundary 不一致。

## 队列与索引摘要

1. `data/p36_external_source_queue.jsonl`
   - `current_classification=contextual_false_positive_demoted`
   - `p7b_category=acupoint_extra_or_uncertain`
   - `risk_tier=medium`
   - 要求引入 `acupoint_standard_reference` 或 `modern_tcm_reference` 后再人工复核。
2. `data/p30_no_source_classification.jsonl`
   - `p7a_action=demoted_false_positive_to_no_source`
   - 原因：既有 quote 是数字章节/页码噪声，不是条目来源。
3. `data/acupoint_index.jsonl`
   - `trace_status=no_source_found`
   - `source_refs=[]`
4. `data/knowledge_completeness.jsonl`
   - `trace_status=no_source_found`，但记录到复核前 Markdown frontmatter 仍为 `verified`。

## FTS 摘要

只读检索 `data/source_fts.sqlite`：

- `十七`：命中《神农本草经》药物编号、伤寒论条文编号、金匮章节编号、针灸篇“第十七椎”等上下文。
- `十七穴`：无命中。

这些命中不能证明存在名为“十七穴”的可追溯穴位条目，也不能支撑正文中的定位、主治、刺法、灸法或配伍。

## 核查结论

维持 `no_source_found`。本条不应使用 `金匮要略` “第十七”章节标题或针灸篇“第十七椎”作为 source_ref；这类命中属于数字/上下文误命中。

## 修改点与理由

- 将 Markdown frontmatter 收紧为 `review_status: no_source_found`、`trace_status: no_source_found`、`source_refs: []`。
- 移除具体定位、主治、刺灸法和配伍应用，改为待权威穴位标准来源核验。
- 增加 P8 来源边界说明，明确 FTS 命中不支撑本条目。

## 未决问题

若需要恢复或扩写“十七穴”，需先引入白名单外部来源（穴位国家标准、权威针灸教材或现代中医参考书），记录可核验 `source_refs` 后再复核。