# P6 规模化精修与可用性增强发布报告

## 阶段结论

P6 已完成：标准化、第二批 verified 扩展、no_source_found 专项治理报告、Agent 查询体验增强与文档发布收口。

## P6-A：全部 verified 标准化

- verified 条目标准化脚本：`scripts/standardize_verified_frontmatter.py`
- 当前 frontmatter audit：

```text
files: 939
missing_required: 821
warnings: 0
```

## P6-B：第二批 verified 扩展

- verified 总数：117
- 方剂：40
- 药材：37
- 穴位：40

第二批新增 45 个 verified 条目。verified 仅表示来源已纳入复核链路，不代表医学真实性或临床适用性结论。

## P6-C：no_source_found 专项治理

- review_queue 总数：218
- 未决队列：217
- 未决 no_source_found：184
- 未决 needs_review：33
- 专项报告：`report/p6_no_source_report.md`

治理原则：no_source_found 不自动提升为 verified；alias / FTS / 同义线索只作为人工复核入口。

## P6-D：Agent 查询体验增强

新增 Agent JSON 工具：

- `tcm_trace_summary`：返回压缩后的来源追溯摘要。
- `tcm_verified_stats`：返回 verified 总量与分类统计。
- `tcm_no_source_report`：返回 P6-C 专项治理报告。

## P6-E：文档发布收口

- README 增加 P6 命令与报告入口。
- roadmap 标记 P6-B/C/D/E 完成。
- 发布报告：`report/p6_release_report.md`

## 安全边界

- 本项目用于中医学习、资料检索、辨证辅助与来源追溯。
- 不替代合格医师面诊、诊断或治疗。
- 方剂、剂量、针灸操作不得直接作为用药或操作依据。
