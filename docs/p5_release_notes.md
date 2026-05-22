# P5 Release Notes

P5 阶段定位：

```text
高价值知识条目精修与 verified 覆盖提升
```

## 完成内容

### P5-A 核心方剂 verified 扩展

- 新增 `scripts/p5_seed_core_formula_decisions.py`
- 核心方剂 verified 扩展 20 个
- 方剂 verified 达到 25 个

### P5-B 核心药材 verified 扩展

- 新增 `scripts/p5_seed_core_herb_decisions.py`
- 核心药材 verified 扩展 17 个
- 药材 verified 达到 22 个

### P5-C 核心穴位 verified 扩展

- 新增 `scripts/p5_seed_core_acupoint_decisions.py`
- 核心穴位 verified 扩展 20 个
- 穴位 verified 达到 25 个
- 穴位 review notes 明确：仅作学习与来源追溯，不作为针灸操作指导

### P5-D 样板条目标准化

- 新增 `scripts/p5_standardize_sample_frontmatter.py`
- 10 个样板条目完成 frontmatter / 安全边界标准化
- 新增 `docs/p5_refinement_samples.md`

### P5-E 收尾报告

- 新增 `scripts/build_p5_report.py`
- 新增 `report/p5_refinement_report.md`

## 当前指标

```text
verified_sources: 72
formula verified: 25
herb verified: 22
acupoint verified: 25
standardized sample entries: 10
```

## 安全原则

- 本项目不是医疗诊断系统。
- 不自动开方。
- 不提供针灸操作指导。
- 所有医学内容只作学习、资料检索、辨证辅助和来源追溯参考。
- 未经人工复核的 candidate 不等于 verified。
