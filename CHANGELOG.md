# 更新日志

所有对本项目的重大更改都将记录在此文件中。

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
