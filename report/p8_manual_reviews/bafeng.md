# bafeng (八风) — P8 R11 Review

## Review Queue Info
- **Line:** 146
- **item_id:** bafeng
- **name:** 八风
- **file:** knowledge/acupoints/bafeng.md
- **review_status:** needs_review
- **reason:** 候选来源需人工复核
- **top_source:** 黄帝内经上册.json (quality_score: 62)

## 当前文件概况
- **trace_status:** verified
- **review_status:** verified (P6)
- **Has source_refs:** Yes — 黄帝内经上册.json（倪师讲课文稿，讲摇针治肿病时提到八风穴）
- **Has safety boundary:** Yes
- **No alias_of** — primary entry
- Frontmatter 已有完整 source_refs 和标准安全声明
- 正文包含倪师讲解片段 3 段（均来自黄帝内经相关文稿）
- 正文有穴位定位、功效主治、针刺方法、配伍应用

## 来源/FTS 检索摘要
- `黄帝内经上册.json` 不在 source_fts.sqlite 中（FTS 仅含 14 个来源文件，上册文稿未入库）
- FTS 中 "八风" 在 `黄帝内经.json`（经典原文）有 3 条命中，但均为中医理论中的"八风"概念（自然气候之风），非穴位
- 针灸篇中无 "八风" 命中
- review_queue 中的 top_source quote 明确涉及八风**穴位**的临床操作（摇针、治肿病），来源可靠

## 核查结论
- 当前 source_ref 指向的 `黄帝内经上册.json` 引文确实涉及八风穴位的针刺操作（摇针泄气治肿病），来源准确
- 但 FTS 中无法复核此来源（因上册文稿未入 FTS），该来源存在于 review_queue 的 acupoint_sources.jsonl 中，source_hit_count=41
- 正文中片段 1 的引文实际来自 `黄帝内经.json`（经典原文）中关于"八风四时"和"诊要经终论"的内容，这是中医理论中的"八风"概念而非穴位描述 — 存在**来源误绑**风险
- 片段 2 来自 `03黄帝内经-下册`，讨论九针对应人身，"八风就是气的出入" — 这是倪师解释经典中"八风"的含义，也非直接讲穴位
- 文件 frontmatter 的 source_ref 指向上册讲摇针的段落才是真正的穴位来源

## 修改决定：修改片段1来源标注
- 片段1当前标注来源为"黄帝内经"（经典原文），内容是"八风四时之胜"等理论文字 — 这并非穴位教学内容
- 需要将片段1的引文替换为 frontmatter source_ref 中真正的摇针教学段落，或标注为"理论引用（非穴位专论）"
- 保守处理：将片段1标注为理论背景引用，不做删除但加注释

## 不修改的医学内容
- 穴位定位、归经、功效主治、针刺方法、配伍 — 均不凭模型记忆修改

## 未决问题
- 黄帝内经上册.json 未入 FTS，无法在此次复核中直接验证引文完整性
- 建议后续将上册文稿纳入 FTS 索引
