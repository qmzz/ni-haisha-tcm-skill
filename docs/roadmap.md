# 改造路线图

## 核心原则

- 尊重 `project/nihaixia/` 原始 JSON。
- 不凭模型记忆补医学内容。
- 先做安全、溯源、索引、测试，再做知识补全。

## P0：安全与溯源底座

- [x] 输出定位从“智能诊断”收敛为“辨证辅助 / 学习参考”。
- [x] 增加统一免责声明。
- [x] 增加红旗症状检测，高风险输入停止方剂参考。
- [x] 增加补充问诊问题。
- [x] 修正典型太阳伤寒组合被粗判为热证的问题。
- [x] 增加 `--json` 输出，方便 OpenClaw 消费结构化结果。
- [x] 增加原始 JSON 来源清单和关键词检索。
- [x] 增加 `data/source_manifest.json` 与 `data/source_pages.jsonl` 构建脚本。
- [x] 增加基础回归测试。

## P1：可追溯知识补全

- [x] 编写方剂来源候选提取器：给现有方剂条目匹配原始 JSON 片段。
- [x] 建立 `data/formula_sources.jsonl`，为 113 个方剂生成来源候选。
- [x] 建立 `data/formula_index.jsonl`，关联现有 Markdown 方剂条目与前三条来源候选。
- [x] 编写药材/穴位来源引用提取器：给现有知识条目匹配原始 JSON 片段。
- [x] 建立 `data/herb_sources.jsonl`、`data/herb_index.jsonl`。
- [x] 建立 `data/acupoint_sources.jsonl`、`data/acupoint_index.jsonl`。
- [x] 制定 frontmatter 回写策略：`docs/frontmatter_strategy.md`。
- [x] 建立 `data/review_queue.jsonl`，收纳 `no_source_found` 与 `needs_review` 条目。
- [x] 增加 CLI 来源查询：`formula-source`、`herb-source`、`acupoint-source`。
- [ ] 为少量 verified 试点条目增加 frontmatter：`status/source_file/page_num/quote`。
- [ ] 所有补全脚本必须输出来源引用，不允许无来源扩写。
- [ ] 修正历史 ID 命名问题，例如 `dahuoluo_tang` 实际内容为大青龙汤。

## P2：OpenClaw 工具化

- [ ] 拆分 OpenClaw 工具：`tcm_safety_check`、`tcm_diagnose_assist`、`tcm_source_search`、`tcm_formula_query` 等。
- [ ] 多轮问诊状态机：先补采关键信息，再输出辨证思路。
- [ ] 输出包含证据引用：来源文件、页码、原文片段。

## P2：可复核知识治理与工具化

- [x] 建立 `data/review_decisions.jsonl` 试点复核决策。
- [x] 建立 `data/verified_sources.jsonl`，首批 15 个 verified 条目。
- [x] 增加统一 trace 服务：`internal/trace_service.py`。
- [x] 增加 CLI：`trace`、`verified-source`、`review-queue`。
- [x] OpenClaw 工具化：`tcm_safety_check`、`tcm_source_search`、`tcm_trace`、`tcm_formula_query`、`tcm_herb_query`、`tcm_acupoint_query`、`tcm_diagnose_assist`。
- [x] verified frontmatter 试点回写：15 个 verified 条目。

## P5：高价值知识条目精修与 verified 覆盖提升

- [x] P5-A：核心方剂 verified 扩展首批 20 个。
- [x] P5-B：核心药材 verified 扩展首批 17 个。
- [ ] P5-C：核心穴位 verified 扩展。
- [ ] P5-D：精修条目 frontmatter / 正文结构标准化。
- [ ] P5-E：质量、review、frontmatter 报告更新与发布说明。

## P4：知识治理成熟化

- [x] P4-A：Review 决策闭环增强（review-import / review-apply / review-stats / review_progress）。
- [x] P4-C：检索质量评分升级（quality_score / match_reason / risk_flags / needs_review_reason）。
- [x] P4-B：no_source_found 二次治理（alias_candidates / alias_candidates.md / apply_alias_candidates）。
- [x] P4-D：Agent 工具体验升级。
- [x] P4-E：frontmatter 标准化。
- [x] P4-F：发布与集成文档。

## P3：检索增强、复核效率提升与知识治理闭环

- [x] P3-A：review_queue 支持 kind/status/limit 过滤。
- [x] P3-A：生成 `report/review_report.md` 审核报告。
- [x] P3-B：alias / 异名 / 繁简匹配，降低 no_source_found。
- [x] P3-C：SQLite FTS5 轻量全文检索。
- [x] P3-D：review decision 增量标记工作流。
- [x] P3-E：quality_report 质量看板。

- [ ] 基于 `source_pages.jsonl` 建 SQLite FTS5 检索。
- [ ] 支持按方剂/药材/穴位/症状/证型检索原文。
- [ ] 医案检索增加证型、方剂、症状标签。
