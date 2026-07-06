# bilao (臂臑外) — P8 R11 Review

## Review Queue Info
- **Line:** 148
- **item_id:** bilao
- **name:** 臂臑外
- **file:** knowledge/acupoints/bilao.md
- **review_status:** no_source_found
- **reason:** 未检索到来源候选
- **top_source:** null

## 当前文件概况
- **trace_status:** verified
- **review_status:** verified (P6)
- **alias_of:** "binao"
- **Has source_refs:** Yes — 01【视频同步文稿】人-针灸篇（可打印）.json, page 50
  - 引文讲的是臂臑穴的定位和临床应用
- **Has safety boundary:** Yes
- 正文有完整的倪师讲解片段，内容丰富

## 来源/FTS 检索摘要
- FTS 中 "臂臑" 有 2 条命中（针灸篇索引页），未直接命中正文教学段落
- "臂臑外" 和 "臂臑二" 无 FTS 命中
- 但当前文件已有 source_ref 指向针灸篇 page 50，内容明确是倪师讲解臂臑穴

## 核查结论
- review_queue 标记为 no_source_found，但实际文件已有 source_refs（指向针灸篇 page 50）
- 这是因为 review_queue 的检索关键词可能未匹配到（"臂臑外"作为别名不在检索词中）
- **alias_of: "binao"** 表明这是 binao（臂臑）的别名条目
- 实际来源通过 alias 链路可追溯到 binao 条目
- 文件内容完整、来源准确、安全声明到位

## 修改决定：不修改
- 别名条目已有正确的 source_refs（通过主条目 binao 的来源）
- review_queue 的 no_source_found 是检索层面的假阴性，不影响内容质量
- 来源追溯链路完整：bilao → alias_of binao → 针灸篇 page 50

## 不修改的医学内容
- 穴位定位、归经、功效主治、针刺方法、配伍 — 均不凭模型记忆修改

## 未决问题
- review_queue 检索机制对 alias 条目可能存在系统性遗漏，建议后续优化
