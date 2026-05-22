# 🏥 倪海厦中医 AI 助手 (ni-haisha TCM Skill)

> *"治病必求于本，本于阴阳"* — 倪海厦

基于倪海厦人纪系列（伤寒论、金匮要略、黄帝内经、神农本草经、针灸篇）构建的中医知识库、辨证辅助与经方检索系统。

> ⚠️ 本项目用于中医理论学习、资料检索和辨证思路参考，不能替代合格医师的面诊、诊断或治疗。项目内容必须尊重原始 PDF 提取数据，不能凭空扩写。

## ✨ 特性

- 🩺 **辨证辅助** — 基于六经辨证和八纲辨证，覆盖 50+ 方剂；输出仅作学习参考
- 📋 **医案库** — 51篇经典医案（伤寒/金匮/针灸/疑难杂症）
- 💊 **方剂查询** — 113 首经方，含倪海厦讲解
- 🌿 **药材库** — 416 味药材（48 味核心完整）
- 🪡 **穴位库** — 412 个穴位（127 个核心穴位完整）
- 📖 **概念库** — 45 个中医核心概念
- 📊 **数据文件** — 症状→方剂映射、概念关系图谱
- 🖥️ **CLI 工具** — 命令行诊断、查询工具

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

**最后更新：** 2026-05-19
