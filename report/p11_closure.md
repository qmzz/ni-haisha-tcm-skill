# P11 内容质量提升阶段收口报告

## 阶段定位

P11 的目标不是追求 verified 百分比，而是在不凭模型记忆扩写医学内容的前提下，提高知识库结构完整度、治理稳定性、来源边界清晰度与后续可维护性。

核心原则：

- 不凭模型记忆补医学内容。
- candidate 不等于 verified。
- verified 仅表示来源追溯链路通过，不代表医学真实性、临床适用性或针灸操作指导。
- no_source_found 不强行补内容，必须保持边界或等待外部可追溯来源。
- seed 脚本必须固定白名单、幂等，避免测试/管线动态推进数据。

## P11 已完成事项

### P11-A/B：内容质量队列与方剂 usage 结构补全

- 建立内容质量队列：`data/p11_content_quality_queue.jsonl`。
- 29 个 verified 方剂补齐 `## 用法` 结构。
- 16 个从既有 `source_refs.quote` 摘录明确用法。
- 13 个明确标记：现有 verified 来源未提供明确用法，待补充。
- 方剂 complete：`113 / 113`。

### P11-C/D：穴位 candidate verified 小批量扩展

- P11-C：固定白名单 100 条穴位 verified。
- P11-D：direct-quote 固定白名单 30 条穴位 verified。
- 入选约束：来源链路明确；P11-D 额外要求 quote 直接包含穴位中文名。
- 不改医学正文，不凭模型记忆扩写。
- P11-C/D seed 已纳入测试链路，避免数据回归。

### P11-E：no_source_found 来源范围边界

- 133 条 no_source_found 补充 scope 元数据。
- 标记为当前倪海厦原始资料未命中，需要外部可追溯来源。
- 不改变 trace_status，不补医学正文。

### 治理稳定性修复

- P9-F 追溯复核纳入测试与管线闭环，防止 review_status 重建后丢失。
- 清理 `knowledge/acupoints/laogong.md` 历史 JSON patch 残留，P9 quality audit 清零。

## 当前核心指标

- total: 939
- verified: 803 / 939
- candidate: 3 / 939
- no_source_found: 133 / 939
- verified_sources: 803
- alias_index: 80

### 按类型追溯状态

| kind | total | verified | candidate | no_source_found |
|------|-------|----------|-----------|-----------------|
| formula | 113 | 113 | 0 | 0 |
| herb | 415 | 294 | 3 | 118 |
| acupoint | 411 | 396 | 0 | 15 |

## 质量治理状态

- P9 quality issues: 41
- P9 by_level: {'info': 41}
- frontmatter schema: missing_required 0, warnings 0（见 `report/frontmatter_audit.md`）
- stale_verified_frontmatter: 0（见 `report/p8_stale_verified_fix_report.md`）

## P11 当前队列

- queue total: 216
- by_priority: {'P2': 133, 'P1': 3, 'P0': 80}
- by_task: {'no_source_boundary_or_external_source': 133, 'review_candidate_source_refs': 3, 'fill_verified_missing_content_field': 80}
- by_kind: {'herb': 201, 'acupoint': 15}

解释：P11 队列剩余项不是本阶段必须清空的缺陷，而是下一阶段复核/外部来源策略入口。

## no_source_found 边界覆盖

- no_source_found total: 133
- source_scope marked: 133 / 133
- external_reference_required: 133 / 133
- no_source_policy marked: 133 / 133

## P11 收口结论

P11 可以收口。当前知识库具备：

1. 方剂结构完整闭环。
2. verified 来源链路扩展且 seed 幂等稳定。
3. no_source_found 有明确边界与后续来源策略。
4. P9 质量审计清零。
5. 文档、测试、管线状态同步。

## P12 建议入口

P12 不建议继续粗放扩 verified。建议方向：

1. candidate 分层人工复核与抽检报告。
2. 外部可追溯来源接入策略，用于 no_source_found 的二阶段提升。
3. 查询体验提升：语义检索、多轮辨证辅助状态机、CLI 安装体验。
4. Agent 工具说明增强：明确安全边界、来源解释与 alias redirect 展示。

---

本报告由 `scripts/p11_finalize_closure.py` 生成。
