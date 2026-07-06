# yinjiao_ren (阴交二) — P8 R12 Review

## Review Queue Info
- **Line:** 203
- **item_id:** yinjiao_ren
- **name:** 阴交二
- **file:** knowledge/acupoints/yinjiao_ren.md
- **review_status:** no_source_found
- **reason:** 未检索到来源候选

## 当前文件概况
- **trace_status:** no_source_found（frontmatter）
- **Has source_refs:** No
- **source_scope:** "not_in_nihaixia_source"
- **归经:** 任脉

## 来源/FTS 检索摘要
- FTS/LIKE 检索 "阴交二" 无命中
- FTS 检索 "阴交" 有命中：01针灸篇 p29 实质讲解 "三焦之募穴—阴交穴"
- acupoint_index.jsonl 有该条目记录：
  - source_quality_level: "verified_alias"
  - trace_status: "verified"（与文件 frontmatter 不一致！）
  - canonical_item_id: "yinjiao"
  - source_refs 引文为 p1 目录页（非实质内容引文）
  - p6b_resolution: "mapped_to_verified_canonical_as_alias"
- p30: next_action 不明

## 核查结论

### ⚠️ 发现重要数据不一致

1. **Frontmatter vs Index 不一致：**
   - 文件 frontmatter: trace_status = no_source_found
   - acupoint_index.jsonl: trace_status = verified
   - 应以文件 frontmatter 为准（no_source_found），index 记录可能有误

2. **Canonical mapping 错误：**
   - acupoint_index 将 yinjiao_ren（阴交二，任脉 CV7）映射到 canonical_item_id = "yinjiao"
   - 但 yinjiao（龈交，DU28）是完全不同的穴位（督脉）
   - 阴交 ≠ 龈交，这是 P6-B 阶段的映射错误

3. **实际来源可用：**
   - FTS 检索发现 01针灸篇 p29 有阴交穴实质讲解："4、三焦之募穴—阴交穴（1-03:25:05）"
   - 该来源可追溯，但当前未引用到文件中

## 修改决定：不修改正文（本轮来源审查范围内不改正文）
- ⚠️ 记录 canonical mapping 错误，建议后续数据质量专项处理
- ⚠️ 记录 frontmatter/index trace_status 不一致
- ⚠️ 记录 FTS 中实际存在可用来源（01针灸篇 p29 阴交穴讲解）

## 外部权威来源需求
- FTS 中有倪师来源可用，不严格需要外部来源
- 但需要后续将 FTS 来源补充到文件 source_refs 中

## 未决问题
- ⚠️ canonical_item_id 映射错误：yinjiao_ren（阴交）→ yinjiao（龈交），应为不同穴位
- ⚠️ frontmatter trace_status 与 index trace_status 不一致
- ⚠️ FTS 存在可用来源（p29 阴交穴讲解）但未引用
- 建议后续：修正 canonical mapping、补充 source_refs、统一 trace_status

## R19 action

- 已执行最小一致性修复：移除 `yinjiao_ren` 在 `acupoint_index.jsonl`、`knowledge_completeness.jsonl`、`verified_sources.jsonl` 中错误映射到 `yinjiao`（龈交）的 `canonical_item_id` / `verified_alias` 状态。
- 已统一为 `trace_status=no_source_found`、`source_quality_level=no_source`，并加入 no-source / external-source 后续队列。
- 未补写 p29 阴交穴来源；该来源需单独核查 quote 后再提升，避免本轮超出高确定性边界。
