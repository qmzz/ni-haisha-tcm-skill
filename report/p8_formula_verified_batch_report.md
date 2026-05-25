# P8-B 方剂 verified 扩展报告

## 阶段定位

P8-B 优先推进方剂知识库数据完备化。本批采用小批量人工白名单，只读取 `data/formula_index.jsonl` 中既有首选 `source_ref`，不凭模型记忆补医学内容。

## 本批结果

- whitelist: 69
- added: 0
- skipped_existing: 69
- errors: 0
- formula_verified_after: 113
- verified_total_after: 512

## 新增方剂

| item_id | name | source_file | page_num | quality_score | threshold |
|---------|------|-------------|----------|---------------|-----------|

## 边界

- verified 仅表示来源追溯链路通过复核，不代表医学真实性或临床适用性。
- 本批不修改医学正文，只通过既有标准化脚本补治理 frontmatter 与安全边界。
- candidate 不等于 verified；未进入本白名单的条目保持原状态。
- 少数低分尾部条目使用显式 QUALITY_OVERRIDES，仅表示人工纳入追溯链路复核，不代表医学判断。
