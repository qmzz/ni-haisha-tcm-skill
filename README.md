# 🏥 倪海厦中医 AI 助手 (ni-haisha TCM Skill)

> *"治病必求于本，本于阴阳"* — 倪海厦

基于倪海厦人纪系列（伤寒论、金匮要略、黄帝内经、神农本草经、针灸篇）构建的中医知识库、辨证辅助与经方检索系统。

> ⚠️ 本项目用于中医理论学习、资料检索和辨证思路参考，不能替代合格医师的面诊、诊断或治疗。项目内容必须尊重原始 PDF 提取数据，不能凭空扩写。

## ✨ 特性

- 🩺 **辨证辅助** — 基于六经辨证和八纲辨证，覆盖 50+ 方剂；输出仅作学习参考
- 📋 **医案库** — 51篇经典医案（伤寒/金匮/针灸/疑难杂症）
- 💊 **方剂查询** — 113 首经方，含倪海厦讲解，verified 全覆盖
- 🌿 **药材库** — 415 味药材（294 条 verified）
- 🪡 **穴位库** — 411 个穴位（396 条 verified）
- 📖 **概念库** — 45 个中医核心概念
- 🔗 **别名查询** — 80 条 alias 映射，支持别名自动跳转到标准条目
- 🛡️ **安全边界** — 939 条知识条目统一学习与安全声明
- 🧭 **P16 内容质量定版** — 条目正文占位词清零、来源摘录按句读重排、短正文从原始 JSON 扩展来源窗口；P9 issues 清零；详见 `report/p16_content_release.md`
- 📊 **数据文件** — 症状→方剂映射、概念关系图谱
- 🖥️ **CLI 工具** — 命令行诊断、查询、追溯、审核工具

## 🚀 快速开始

### 方式一：Python API 使用

```python
from internal.diagnosis_engine import DiagnosisEngine

engine = DiagnosisEngine()
result = engine.analyze(["发热", "恶寒", "无汗", "脉浮紧"])
print(result)
```

### 方式二：CLI 使用

```bash
# 辨证辅助（学习参考）
python3 cli.py diagnose "发热,恶寒,无汗,脉浮紧"

# 查询方剂
python3 cli.py formula 桂枝汤

# 查询药材
python3 cli.py herb 麻黄

# 查看统计
python3 cli.py stats

# 查看原始 JSON 来源清单
python3 cli.py sources

# 检索原始 PDF 提取文本，作为补全依据
python3 cli.py source 桂枝汤

# 查询方剂来源候选
python3 cli.py formula-source 桂枝汤

# 生成原始来源索引
python3 scripts/build_source_index.py

# 生成方剂来源候选索引
python3 scripts/build_formula_sources.py

# 生成方剂结构化索引
python3 scripts/build_formula_index.py

# 生成药材/穴位来源候选与结构化索引
python3 scripts/build_herb_sources.py && python3 scripts/build_herb_index.py
python3 scripts/build_acupoint_sources.py && python3 scripts/build_acupoint_index.py

# 生成 P1 复核队列
python3 scripts/build_review_queue.py

# 初始化 P2 verified 试点并生成 verified 来源索引
python3 scripts/init_review_decisions.py
python3 scripts/build_verified_sources.py

# verified frontmatter 试点回写（默认 dry-run，加 --apply 才写入）
python3 scripts/apply_verified_frontmatter.py --dry-run
python3 scripts/apply_verified_frontmatter.py --apply

# OpenClaw / Agent JSON 工具入口
python3 tools/tcm_tools.py tcm_trace '{"query":"桂枝汤"}'
python3 tools/tcm_tools.py tcm_diagnose_assist '{"symptoms":["发热","恶寒","无汗","脉浮紧"]}'

# P3 review queue 筛选与报告
python3 cli.py review-queue --kind herb --status no_source_found --limit 20
python3 scripts/build_review_report.py

# P3 alias/异名匹配后重建来源索引
python3 scripts/build_formula_sources.py && python3 scripts/build_formula_index.py
python3 scripts/build_herb_sources.py && python3 scripts/build_herb_index.py
python3 scripts/build_acupoint_sources.py && python3 scripts/build_acupoint_index.py
python3 scripts/build_review_queue.py

# P3 SQLite FTS、复核模板与质量报告
python3 scripts/build_sqlite_fts.py
python3 cli.py fts-search 桂枝汤 --limit 5
python3 cli.py review-next --kind herb --status needs_review --limit 10
python3 cli.py review-export --kind herb --status no_source_found --limit 50
# P4 Review 决策闭环、质量评分与二次 alias 治理
python3 cli.py review-import data/review_decisions.template.jsonl
python3 cli.py review-apply
python3 cli.py review-stats
python3 scripts/build_alias_candidates.py
python3 scripts/apply_alias_candidates.py
python3 scripts/build_quality_report.py

# P4 Agent tools / frontmatter / docs
python3 tools/tcm_tools.py tcm_review_stats '{}'
python3 tools/tcm_tools.py tcm_search_sources_fts '{"query":"桂枝汤","limit":5}'
python3 tools/tcm_tools.py tcm_compare_formulas '{"names":["桂枝汤","麻黄汤"]}'
python3 scripts/check_frontmatter_schema.py

# P5 核心方剂 verified 扩展
python3 scripts/p5_seed_core_formula_decisions.py
python3 scripts/build_verified_sources.py
python3 scripts/apply_verified_frontmatter.py --apply

# P5 核心药材 verified 扩展
# P5 核心穴位 verified 扩展
python3 scripts/p5_seed_core_acupoint_decisions.py
python3 scripts/build_verified_sources.py
python3 scripts/apply_verified_frontmatter.py --apply

# P5 样板条目 frontmatter / 安全边界标准化
python3 scripts/p5_standardize_sample_frontmatter.py
python3 scripts/check_frontmatter_schema.py

# P5 收尾报告
python3 scripts/build_p5_report.py

# P6 verified 条目标准化
python3 scripts/standardize_verified_frontmatter.py --apply
python3 scripts/check_frontmatter_schema.py
# 报告：report/p6_standardization_report.md

# P6 第二批 verified 扩展 + 治理报告
python3 scripts/p6_seed_second_batch_decisions.py
python3 scripts/build_verified_sources.py
python3 scripts/apply_verified_frontmatter.py --apply
python3 scripts/standardize_verified_frontmatter.py --apply
python3 scripts/build_p6_no_source_report.py
python3 scripts/build_p6_release_report.py
# 报告：report/p6_no_source_report.md, report/p6_release_report.md

# P7 no_source 与 alias 治理
python3 scripts/p7_classify_no_source.py
python3 scripts/p7_build_alias_review.py --apply-safe
# 报告：report/p7_no_source_classification.md, report/p7_alias_review.md

# P7 第三批 verified 精修
python3 scripts/p7_seed_verified_batch3.py
python3 scripts/build_verified_sources.py
python3 scripts/apply_verified_frontmatter.py --apply
python3 scripts/standardize_verified_frontmatter.py --apply
python3 scripts/check_frontmatter_schema.py
# 报告：report/p7_verified_batch3_report.md

# P7 CLI / 文档产品化与发布收口
python3 cli.py lookup 白头翁汤 --json
python3 cli.py explain-trace 白头翁汤 --json
python3 cli.py review-dashboard --json
python3 cli.py batch-trace 桂枝汤,白头翁汤,大敦 --json
python3 scripts/build_p7_release_report.py
# 报告：report/p7_release_report.md

# P8 verified 扩展与审计刷新
python3 scripts/p8_seed_formula_verified_batch.py
python3 scripts/p8_seed_herb_verified_batch.py
python3 scripts/build_verified_sources.py
python3 scripts/build_p8_knowledge_audit.py
python3 cli.py review-dashboard --json
# 审计明细：data/knowledge_completeness.jsonl
# 审计报告：report/p8_knowledge_audit.md
# 方剂报告：report/p8_formula_verified_batch_report.md
# 药材报告：report/p8_herb_verified_batch_report.md

# P8-D herb needs_review 处理 (score >= 50)
python3 scripts/p8_seed_herb_candidate_review.py
python3 scripts/build_verified_sources.py

# P8-F acupoint needs_review 处理 (score >= 55)
python3 scripts/p8_seed_acupoint_verified_batch.py
python3 scripts/build_verified_sources.py

# P8-E no_source_found 扩展治理
python3 scripts/p8_e_1_no_source_inventory.py
python3 scripts/p8_e_1_acupoint_variant.py
python3 scripts/p8_e_2_expand_search.py
python3 scripts/p8_e_3_build_auto_candidates.py
python3 scripts/p8_e_3_seed_verified.py
python3 scripts/build_verified_sources.py
python3 scripts/apply_verified_frontmatter.py --apply
python3 scripts/standardize_verified_frontmatter.py --apply
python3 scripts/check_frontmatter_schema.py
python3 scripts/build_p8_knowledge_audit.py
# 报告：report/p8_e_closure.md
# 当前 verified: 642 (formula 113, herb 292, acupoint 237)
# frontmatter missing_required: 0

# P9 数据质量治理
python3 scripts/p9_quality_audit.py
python3 scripts/p9_fix_verified_source_refs.py
python3 scripts/p9_fix_empty_titles.py
python3 scripts/p9_build_review_queue.py
# 报告：report/p9_quality_audit.md
# 当前 P9 issues: 0
# error/warning/review/info: 0
```

### 方式三：作为 OpenClaw Skill 使用

```bash
# 复制到 OpenClaw skills 目录
cp -r . ~/.openclaw/workspace/skills/ni-haisha
```

## 📊 知识库统计

| 类别 | 数量 | 核心完整度 |
|------|------|------------|
| 药材 | 416 味 | 48 味完整 |
| 穴位 | 412 个 | 127 个完整 |
| 方剂 | 114 首 | 113 首有讲解 |
| 医案 | 51 篇 | 100% |
| 概念 | 45 个 | 100% |
| 诊断 | 45 篇 | 100% |


## 🧭 P7 来源治理与 Agent 查询编排

P7 已完成 no_source 分类、alias review、第三批 verified 精修与查询编排产品化，后续阶段已进一步扩展 verified 覆盖。当前累计 verified 来源链路：

| 类型 | 数量 |
|------|------|
| 方剂 | 113 |
| 药材 | 292 |
| 穴位 | 107 |
| **合计** | **512** |

> verified 仅表示来源追溯链路通过复核，不代表医学真实性或临床适用性。

### CLI 查询编排

```bash
python3 cli.py lookup 白头翁汤
python3 cli.py explain-trace 白头翁汤
python3 cli.py review-dashboard
python3 cli.py batch-trace 桂枝汤,白头翁汤,大敦
```

以上命令均支持 `--json`，适合 Agent 或外部系统集成。

### Agent JSON 工具

```bash
python3 tools/tcm_tools.py tcm_lookup '{"query":"白头翁汤"}'
python3 tools/tcm_tools.py tcm_lookup '{"query":"zanzhu"}'  # alias 自动跳转到攒竹
python3 tools/tcm_tools.py tcm_explain_trace '{"query":"白头翁汤"}'
python3 tools/tcm_tools.py tcm_review_dashboard '{}'
python3 tools/tcm_tools.py tcm_batch_trace '{"queries":["桂枝汤","白头翁汤"]}'
```

详见：

- [Agent 集成文档](docs/agent_integration.md)
- [P7 verified batch3 报告](report/p7_verified_batch3_report.md)
- [P7 发布收口报告](report/p7_release_report.md)

## 📌 P8 发布后增强

P8 已从“审计”进入“知识库数据完备化”阶段：先完成方剂全覆盖，再推进药材扩展。

### P8-A 知识库完整度审计

P8-A 用于盘点方剂、药材、穴位条目的治理状态与内容完备度。当前审计输出：

```text
data/knowledge_completeness.jsonl
report/p8_knowledge_audit.md
```

当前结论摘要：

```text
条目总数：939
verified 来源链路：374
frontmatter 标记 verified 但未进入 registry：0
frontmatter 完整：374
complete 条目：345
```

该审计只做数据治理和补全优先级排序，不判断医学真实性，不生成新的医学结论。

### P8-B 方剂 verified 全覆盖

P8-B 已完成，方剂知识库已实现 verified 全覆盖：

```text
formula verified: 113 / 113
```

相关输出：

```text
scripts/p8_seed_formula_verified_batch.py
report/p8_formula_verified_batch_report.md
```

说明：少量低分尾部条目采用显式 `QUALITY_OVERRIDES`，仅表示人工纳入追溯链路复核，不代表医学判断。

### P8-C 药材 verified 扩展（进行中）

P8-C 已完成高分与中分批次扩展，当前药材 verified 状态：

```text
herb verified: 211
herb candidate: 84
herb no_source_found: 120
```

相关输出：

```text
scripts/p8_seed_herb_verified_batch.py
report/p8_herb_verified_batch_report.md
```

### 常用 P8 命令

```bash
python3 scripts/p8_seed_formula_verified_batch.py
python3 scripts/p8_seed_herb_verified_batch.py
python3 scripts/build_verified_sources.py
python3 scripts/apply_verified_frontmatter.py --apply
python3 scripts/standardize_verified_frontmatter.py --apply
python3 scripts/check_frontmatter_schema.py
python3 scripts/build_p8_knowledge_audit.py
python3 cli.py review-dashboard --json
```

> 注意：若先执行 `p8_seed_*` 再运行其他统计/看板命令，建议按上述完整链路刷新数据，避免 dashboard 出现旧值。

## 🔧 诊断引擎

基于六经辨证和八纲辨证的辨证辅助系统：

- **六经辨证**：太阳、阳明、少阳、太阴、少阴、厥阴
- **八纲辨证**：阴阳、表里、寒热、虚实
- **覆盖方剂**：50+ 首（伤寒论 + 金匮要略）
- **症状映射**：55 个常见症状 → 对应方剂

## 📁 项目结构

```
ni-haisha/
├── SKILL.md                    # Skill 定义
├── cli.py                      # CLI 入口
├── internal/                   # 核心模块
│   ├── diagnosis_engine.py     # 诊断引擎（50+ 方剂）
│   └── formula_recommender.py  # 方剂推荐器
├── data/                       # 数据文件
│   ├── symptom_formula.json    # 症状→方剂映射
│   ├── concept_graph.json      # 概念关系图谱
│   └── learning_paths.json     # 学习路径
├── knowledge/                  # 知识库
│   ├── herbs/                  # 药材（416 味）
│   ├── acupoints/              # 穴位（412 个）
│   ├── formulas/               # 方剂（114 首）
│   ├── concepts/               # 概念（45 个）
│   ├── diagnosis/              # 诊断知识（45 篇）
│   └── cases/                  # 医案（51 篇）
├── prompts/                    # 提示词模板
├── scripts/                    # 批量处理脚本
└── docs/                       # 文档
```

## 📖 知识来源

本 Skill 知识蒸馏自倪海厦人纪系列与相关中医经典资料。当前工作区中的 `project/nihaixia/` 存放从 PDF 提取的结构化 JSON，是后续补全与校验的第一依据。详见 [原始数据使用原则](docs/source_data_policy.md)。

| 资料 | 内容 | 页数 |
|------|------|------|
| 伤寒论 | 六经辨证、113 经方 | 198 页 |
| 金匮要略 | 杂病治疗方剂 | 492 页 |
| 黄帝内经 | 中医基础理论 | 308 页 |
| 神农本草经 | 中药学基础 | 339 页 |
| 针灸篇 | 针灸理论与实务 | 216 页 |
| 汉唐中医方剂 | 方剂讲解 | 235 页 |

## ⚠️ 免责声明

本 Skill 提供的信息仅供参考，不能替代专业中医师的诊断和治疗。如有健康问题，请咨询合格的中医师。

- 本 Skill 基于倪海厦教学资料构建
- 方剂剂量仅供参考，实际应用需因人而异
- 孕妇、儿童、老人等特殊人群用药需谨慎
- 中药可能与西药产生相互作用，请告知医师您正在服用的所有药物

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 许可证

[MIT License](LICENSE)

## 🙏 致谢

- 倪海厦 — 人纪系列教学资料
- 张仲景 — 《伤寒论》《金匮要略》

---

**最后更新：** 2026-05-22
