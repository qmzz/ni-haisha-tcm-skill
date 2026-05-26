# 更新日志

所有对本项目的重大更改都将记录在此文件中。

## [Unreleased]

### P12 candidate 批量收口

- 新增 `scripts/p12_candidate_batch.py` 与 `report/p12_candidate_batch_report.md`。
- 对剩余 164 条 candidate 做一次性来源检索与分流：
  - 161 条在原始 JSON 中找到中文名命中，提取 source_refs 并纳入 verified。
  - 3 条 herb（白豆蔻、白扁豆、番泻叶）仅有低质量 alias 命中，保留 candidate/needs_review，不强行 verified。
- 测试 seed 链纳入 P12 脚本，并调整 pipeline 顺序为 build -> apply -> standardize -> stale fix，避免测试降级新 verified frontmatter。
- 当前指标：
  - `verified: 803 / 939`
  - `candidate: 3 / 939`
  - `no_source_found: 133 / 939`
  - `P9 quality issues: 0`
  - 测试：`84 passed`

### P11 内容质量与治理闭环

- P11-A/B: 内容质量队列与方剂 usage 结构补全
  - 新增 `scripts/p11_build_content_quality_queue.py`、`scripts/p11_b_fill_formula_usage.py`。
  - 29 个 verified 方剂补齐 `## 用法` 结构：16 个摘录现有 source_refs，13 个明确标记“现有 verified 来源未提供明确用法，待补充”。
  - 方剂 complete: `113 / 113`。
- P11-C/D: 穴位 candidate verified 小批量扩展
  - P11-C 固定白名单 100 条，P11-D direct-quote 固定白名单 30 条。
  - 新增 `scripts/p11_c_seed_acupoint_verified.py`、`scripts/p11_d_seed_acupoint_verified.py`。
  - 所有 seed 均幂等，已纳入测试链路，避免动态推进导致数据回归。
  - verified 总数：`512 -> 642`；穴位 verified：`107 -> 237`。
- P11-E: no_source_found 来源范围边界标记
  - 新增 `scripts/p11_e_mark_no_source_scope.py`。
  - 为 133 条 no_source_found 补充 `source_scope: not_in_nihaixia_source`、`external_reference_required: true`、`no_source_policy: keep_boundary_until_traceable_source`。
  - 不改变 trace_status，不补医学正文；后续提升必须引入可追溯外部来源。
- 治理稳定性：
  - P9-F 追溯复核纳入测试与管线闭环，避免 `review_status` 在重建后丢失。
  - 清理 `knowledge/acupoints/laogong.md` 历史 JSON patch 残留，P9 quality audit issues 清零。
- P11 收口：
  - 新增 `scripts/p11_finalize_closure.py` 与 `report/p11_closure.md`，固定 P11 阶段产物、指标、边界与 P12 入口。
- 当前指标：
  - `verified: 642 / 939`
  - `candidate: 164 / 939`
  - `no_source_found: 133 / 939`
  - `safety_boundary: 939 / 939`
  - `P9 quality issues: 0`
  - 测试：`84 passed`

### P10 查询质量与可用性增强

- P10-B: alias 查询闭环
  - 新增 `scripts/build_alias_index.py` 与 `data/alias_index.jsonl`（80 条 alias_of 映射）。
  - `TraceService.trace()` 支持 alias redirect：`alias_id -> target_id -> trace_core`。
  - `tcm_lookup` / `tcm_trace` 输出透传 `alias_redirect`，Agent 可直接展示标准条目跳转说明。
  - 新增 `tests/test_p10b_alias_query.py`，覆盖 herb / acupoint alias 查询。
- P10-C: safety_boundary 全覆盖
  - 新增 `scripts/p10c_add_safety_boundary.py`，为所有知识条目补学习与安全边界。
  - 新增 `scripts/p10c_add_acupoint_notice.py`，为全部穴位补来源追溯声明与“仅作学习与来源追溯，不作为针灸操作指导”。
  - `safety_boundary: 939 / 939`，`acupoint source_trace_notice: 411 / 411`。
- P10-D: no_source_found 残余治理
  - 新增 `scripts/p10d_nsf_source_search.py`：对 133 条 no_source_found 做中文正名原始资料检索，命中 0。
  - 新增 `scripts/p10d_nsf_alias_search.py`：结合 `data/aliases.json` 做别名原始资料检索，命中 0。
  - 结论：剩余 133 条 no_source_found 在当前倪海厦原始 JSON 中无明确命中，保持 no_source_found，不凭模型记忆补内容。
- P10-E: body_short 收口
  - P11 后已清理 `knowledge/acupoints/laogong.md` 历史格式残留，P9 quality audit issues 已清零。
- 当前指标：
  - `verified: 512 / 939`
  - `candidate: 294 / 939`
  - `no_source_found: 133 / 939`
  - `safety_boundary: 939 / 939`
  - 测试：`84 passed`

### P9 数据质量治理（已完成）

- P9-A: 创建数据质量审计脚本 `scripts/p9_quality_audit.py`，从内容一致性、完整性、准确性等维度检查。
- P9-A 修复: 解决 `registry_verified_but_frontmatter_not_verified` 313 个严重一致性错误，错误级问题清零。
  - 修复 `standardize_verified_frontmatter.py`：补写 `trace_status: verified`。
  - 修复 P8-E seed 脚本：从 index 文件获取 `item_id -> file` 映射，消除 51 条空 file。
  - 新增 `p9_fix_verified_source_refs.py`：为 51 条 parent_expand 条目补 `source_refs` frontmatter。
  - 新增 `p9_fix_empty_titles.py`：修复 427 个 frontmatter 空 title。
- P9-B: 生成质量复核队列 `data/p9_review_queue.jsonl`（173 条）。
- P9-C: 修复 P8 seed 脚本幂等性问题（`p8_seed_herb_candidate_review.py`、`p8_seed_acupoint_verified_batch.py`、`p8_e_3_seed_verified.py`），避免重复追加 verified 决策。
- P9-D: duplicate_title 治理，90 条降至 30 条
  - 为 45 组重复名添加 alias/alias_of frontmatter
  - p9_d_resolve_duplicate_titles.py: herb aliases + acupoint variant 标注
  - p9_quality_audit.py: 排除已有 alias 标注的重复名
- P9-D: duplicate_title 治理，90 条降至 30 条
  - 为 45 组重复名添加 alias/alias_of frontmatter
  - p9_d_resolve_duplicate_titles.py: herb aliases + acupoint variant 标注
  - p9_quality_audit.py: 排除已有 alias 标注的重复名
- P9-E: 清理剩余 15 组 duplicate_title，warning 清零
  - 为 7 组 herb 别名对 + 8 组 acupoint 异写/别名添加 alias_of 标注
  - p9_e_resolve_remaining_duplicates.py: 基于 index 真实数据治理
- P9-F: 追溯复核通过 76 条 review 项
  - p9_f_review_decisions.py: 对来源链路完整的 review 项标记 trace_review_passed
  - parent_expand_verified_needs_human_review: 51 -> 0
  - low_score_verified_needs_review: 25 -> 0
- **当前 P9 issues: 7 (仅剩 info: body_short)**
- **error: 0, warning: 0, review: 0 ✅**

### P8-E no_source_found 扩展治理

- P8-E-1: 盘点 herb 120 + acupoint 64 个 no_source_found 清单
- P8-E-2: 扩展搜索命中 156 条（acupoint parent_name / herb alias 回退）
- P8-E-3: 51 条高置信命中落库为 verified（acupoint 49 + herb 2）
- 修复数据回归：`review_decisions.jsonl` 从 261 恢复到正确状态
- **当前 verified: 512（formula 113, herb 292, acupoint 107）**
- **frontmatter missing_required: 0**

### P8-D/F + Frontmatter 标准化

- P8-D herb needs_review 处理：17 个 score ≥ 50 的条目通过 QUALITY_OVERRIDES 验证。
- P8-F acupoint needs_review 处理：8 个 score ≥ 55 的条目通过 QUALITY_OVERRIDES 验证。
- Frontmatter 标准化：为 478 个知识文件添加基础 frontmatter (kind + trace_status)。

### P8-B/C 收口
- 补齐 P8-B/C 文档：在 `README.md` 与 `docs/roadmap.md` 中记录方剂 verified 全覆盖与药材 verified 扩展进展。
- 将 `README.md` 中累计 verified 数值从 147 更新为当前实际值 374。
- 在 `README.md` 中补充 P8 常用命令与数据刷新提示，避免 `p8_seed_*` 后读到旧 dashboard 数值。

> 本次为文档与收口同步，不涉及额外医学内容扩展。

## [1.1.0] - 2026-05-22

### P7 知识治理与查询产品化

- 完成 P7-A no_source_found 分类治理：输出 `data/no_source_classification.jsonl` 与 `report/p7_no_source_classification.md`。
- 完成 P7-B alias / synonym 治理增强：输出 `data/alias_review.jsonl` 与 `report/p7_alias_review.md`，safe_alias 采用白名单可控应用。
- 完成 P7-C 第三批 verified 精修：累计 verified_sources 提升至 147（方剂 50、药材 47、穴位 50）。
- 完成 P7-D Agent 查询编排增强：新增 `tcm_lookup`、`tcm_explain_trace`、`tcm_review_dashboard`、`tcm_batch_trace`。
- 完成 P7-E CLI / 文档产品化：新增 `lookup`、`explain-trace`、`review-dashboard`、`batch-trace` CLI 命令，均支持 `--json`。
- 完成 P7-F 发布准备：新增 `scripts/build_p7_release_report.py` 与 `report/p7_release_report.md`。

### 安全边界

- verified 仅表示来源追溯链路通过复核，不代表医学真实性或临床适用性。
- alias hit 仍只进入 candidate / needs_review，不自动 verified。
- 穴位内容仅作学习与来源追溯，不作为针灸操作指导。

## [1.0.0] - 2026-05-19

### 首次发布

#### 知识库
- ✅ **医案库**：51 篇经典医案（伤寒 20 + 金匮 16 + 针灸 10 + 疑难 5）
- ✅ **核心药材**：48味伤寒论核心药材完整字段
- ✅ **方剂讲解**：113 首经方倪师讲解
- ✅ **核心穴位**：127 个穴位完整信息
- ✅ **概念库**：45 个中医核心概念（全部≥80行）

#### 数据文件
- ✅ `symptom_formula.json`：55 个常见症状→方剂映射
- ✅ `concept_graph.json`：100+ 节点/200+ 概念关系边
- ✅ `learning_paths.json`：4 个学习阶段路径

#### 技术模块
- ✅ **诊断引擎**：覆盖 50+ 方剂，支持六经辨证和八纲辨证
- ✅ **CLI 工具**：7 个命令（diagnose/formula/herb/acupoint/concept/case/stats）
- ✅ **提示词模板**：5 种场景系统提示词

#### 项目文件
- ✅ README.md
- ✅ LICENSE（MIT）
- ✅ CONTRIBUTING.md
- ✅ CHANGELOG.md
- ✅ .gitignore

---

## 待发布

### 1.2.0（计划中）
- 继续小批量人工复核 no_source_found 条目
- CLI 打包与安装体验优化
- 改进诊断引擎算法与多轮问诊状态机
- 优化数据结构与语义检索体验

### 2.0.0（计划中）
- Web API 接口
- 多语言支持
- 移动端适配
