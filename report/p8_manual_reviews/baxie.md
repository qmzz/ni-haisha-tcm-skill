# baxie (八邪) — P8 R11 Review

## Review Queue Info
- **Line:** 147
- **item_id:** baxie
- **name:** 八邪
- **file:** knowledge/acupoints/baxie.md
- **review_status:** needs_review
- **reason:** 候选来源需人工复核
- **top_source:** 黄帝内经上册.json (quality_score: 62)

## 当前文件概况
- **trace_status:** verified
- **review_status:** verified (P6)
- **Has source_refs:** Yes — 黄帝内经上册.json（倪师讲八风八邪治末梢气血不通）
- **Has safety boundary:** Yes
- **No alias_of** — primary entry
- 正文无倪师讲解片段（仅有标准穴位信息部分）
- 正文有穴位定位、功效主治、针刺方法、配伍应用

## 来源/FTS 检索摘要
- `黄帝内经上册.json` 不在 FTS 中
- FTS 中 "八邪" 无独立命中
- review_queue 的 source quote 涉及倪师讲授八风八邪穴直接疏通末梢气血的内容，来源可靠
- acupoint_sources.jsonl 有完整候选来源记录

## 核查结论
- source_ref 引文准确指向倪师讲解八邪穴的临床应用（虫咬、狗咬、蛇咬、扭伤、破伤风、痛风等末梢气血不通）
- 条目结构完整，有安全声明，来源追溯状态 verified
- 正文缺少倪师讲解片段部分（与 bafeng 不同），但不影响来源追溯有效性

## 修改决定：不修改
- 来源准确、条目完整、安全声明到位
- 正文未包含倪师讲解引文片段，但 frontmatter source_refs 已正确引用，不影响追溯链路
- 可考虑后续将 source_ref 引文补充到正文，但当前复核不强制

## 不修改的医学内容
- 穴位定位、归经、功效主治、针刺方法、配伍 — 均不凭模型记忆修改

## 未决问题
- 无
