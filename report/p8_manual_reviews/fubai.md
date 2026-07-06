# fubai (浮白) — P8 R11 Review

## Review Queue Info
- **Line:** 160（实际为 fubai 在 review_queue 中对应行）
- **item_id:** fubai
- **name:** 浮白
- **review_status:** needs_review
- **reason:** quality_score_below_verified_threshold
- **top_source:** 黄帝内经.json (quality_score: 53)

## 当前文件概况
- **trace_status:** verified
- **review_status:** verified (P6)
- **无 alias_of**（独立条目）
- **Has source_refs:** Yes — 黄帝内经.json page 1
  - 引文来自《黄帝内经·气穴论篇第五十八》中的气穴列表，提及"目瞳子浮白二穴"
- 正文有穴位定位、功效主治、针刺方法、配伍应用

## 来源/FTS 检索摘要
- FTS 中 "浮白" 无命中（FTS 仅含14个文件，且检索机制可能未覆盖此条）
- acupoint_sources.jsonl: source_hit_count=1，仅黄帝内经.json（score=53）
- 针灸篇索引页有"浮白, 135"引用，但正文 page 135 可能在 FTS 中无该关键词

## 核查结论
- source_ref 引文准确 — 来自气穴论篇的穴位列表，确实提到"目瞳子浮白二穴"
- 这是经典原文中的穴位记载，属于权威文献引用
- 但该来源只是穴位名称列表，非倪师临床教学讲解
- 倪海厦人纪系列针灸篇可能在 page 135 有浮白穴教学，但 FTS 未检索到

## 修改决定：不修改
- 来源引用准确（黄帝内经原文穴位列表）
- 条目完整、安全声明到位
- 不补充来源（避免不确定来源绑定）

## 未决问题
- 针灸篇索引引用浮白在 page 135，建议后续核查该页是否有倪师教学正文
