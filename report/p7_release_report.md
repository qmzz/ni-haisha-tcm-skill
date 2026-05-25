# P7 发布收口报告

## 阶段定位

P7 聚焦知识治理深水区与可用性产品化：在不凭模型记忆扩写医学内容的前提下，继续推进来源治理、alias 复核、第三批 verified 精修，并把 Agent 查询编排能力产品化到 CLI / 文档。

## P7 完成项

- [x] P7-A：no_source_found 分类治理，生成 `data/no_source_classification.jsonl` 与 `report/p7_no_source_classification.md`。
- [x] P7-B：alias / synonym 治理增强，生成 `data/alias_review.jsonl` 与 `report/p7_alias_review.md`，safe_alias 可控应用。
- [x] P7-C：第三批 verified 精修，新增 30 个 verified。
- [x] P7-D：Agent 查询编排增强，新增 lookup、trace 解释、review dashboard、batch trace。
- [x] P7-E：CLI / 文档产品化，CLI 对齐 P7-D 查询编排能力。
- [x] P7-F：版本发布准备，补充 changelog、release notes 与阶段收口报告。

## 当前累计指标

### verified sources

- 总数：147
- 方剂：50
- 药材：47
- 穴位：50

> verified 仅表示来源追溯链路已复核通过，不代表医学真实性或临床适用性。

### review queue

- 总数：218
- needs_review: 34
- no_source_found: 184

### no_source_found 分类

- acupoint_name_variant: 63
- alias_candidate: 4
- herb_name_review: 57
- no_obvious_lead: 60

### alias review

- needs_manual_review: 126
- safe_alias: 4

### frontmatter audit 摘要

```text
# Frontmatter Audit

- files: 939
- missing_required: 0
- warnings: 0

| file | kind | missing | warnings |
|------|------|---------|----------|
```

## P7 新增 CLI / Agent 入口

### CLI

```bash
python3 cli.py lookup 白头翁汤
python3 cli.py explain-trace 白头翁汤
python3 cli.py review-dashboard
python3 cli.py batch-trace 桂枝汤,白头翁汤,大敦
```

以上命令均支持 `--json`，便于 Agent 或外部系统消费。

### Agent JSON tools

```bash
python3 tools/tcm_tools.py tcm_lookup '{"query":"白头翁汤"}'
python3 tools/tcm_tools.py tcm_explain_trace '{"query":"白头翁汤"}'
python3 tools/tcm_tools.py tcm_review_dashboard '{}'
python3 tools/tcm_tools.py tcm_batch_trace '{"queries":["桂枝汤","白头翁汤"]}'
```

## 安全与治理边界

- 不凭模型记忆补医学内容。
- 所有医学知识补全必须来自原始 JSON、既有知识文件或明确可追溯来源。
- 找不到依据只能标记 `待考`、`待补充`、`no_source_found` 或 `needs_review`。
- `candidate` 不等于 `verified`。
- `alias hit` 只能进入 candidate / needs_review，不自动 verified。
- `quality_score` 只用于治理排序和复核优先级，不等于医学真实性判定。
- 穴位内容仅作学习与来源追溯，不作为针灸操作指导。

## 建议后续

- P8 可继续围绕人工复核效率、CLI 打包、语义检索和 release tag 展开。
- 对 `no_source_found` 的 herb/acupoint 条目继续坚持小批量、可追溯、人工白名单推进。
