# zhongshu (中枢) — P8 R12 Review

## Review Queue Info
- **Line:** 211
- **item_id:** zhongshu
- **name:** 中枢
- **file:** knowledge/acupoints/zhongshu.md
- **review_status:** needs_review

## 当前文件概况
- **trace_status:** verified
- **review_status:** verified (P6)
- **Has source_refs:** Yes — 倪海厦人纪系列之伤寒论.json page 45
- **source_quality_level:** verified_direct
- **归经:** 督脉（DU7）

## 来源/FTS 检索摘要
- review_queue status: needs_review
- 文件 frontmatter 引用《伤寒论》p45，但引文内容为桂枝汤/麻黄汤方证讨论
- FTS 检索 "中枢" 在源语料中有命中（伤寒论 p45, 汉唐方剂 p61），但均非穴位讲解

## 核查结论

### ⚠️ Source_ref 质量问题

1. **引文不匹配：** 当前 source_ref 引用《伤寒论》p45，引文内容为太阳病篇桂枝汤/麻黄汤讨论，未提及 "中枢" 作为穴位的任何信息
2. **可能的匹配错误：** "中枢" 一词可能在《伤寒论》原文或倪注中以非穴位语境出现（如 "中枢神经" 等描述）
3. **实际来源状态：** 倪海厦人纪针灸篇语料中，"中枢穴"（督脉 DU7）未见明确的专节讲解

### 判定
- 当前 source_ref 为误匹配（false positive），引文与穴位无关
- 实际来源状态应为 no_source_found 或 weak_source
- 但本轮不改正文，记录此问题

## 修改决定：不修改正文
- ⚠️ 记录 source_ref 质量问题，建议后续数据质量专项处理
- 当前 trace_status: verified 和 source_quality_level: verified_direct 均基于错误引文，应降级

## 未决问题
- ⚠️ source_ref 引文与穴位无关，trace_status 应从 verified 降级为 no_source_found 或 weak_source
- ⚠️ source_quality_level: verified_direct 为误判，应修正
- 建议后续：重新审查 zhongshu 的来源状态，修正或移除错误 source_ref

## R19 action

- 已执行最小修复：清理 `knowledge/acupoints/zhongshu.md` 中错误 `source_refs` 与非穴位来源摘录。
- 已同步注册表：`acupoint_index.jsonl`、`knowledge_completeness.jsonl` 降级为 `trace_status=no_source_found`、`source_quality_level=no_source`，并从 `verified_sources.jsonl` 移除。
- 已加入 no-source / external-source 后续队列；未补写任何穴位医学字段。
