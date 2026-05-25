# 更新日志

所有对本项目的重大更改都将记录在此文件中。

## [Unreleased]

### P9 数据质量治理（进行中）

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
- **当前 P9 issues: 113 (error: 0, warning: 30, review: 76, info: 7)**

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
