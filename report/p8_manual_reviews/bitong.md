# bitong (臂臑二) — P8 R11 Review

## Review Queue Info
- **Line:** 149
- **item_id:** bitong
- **name:** 臂臑二
- **file:** knowledge/acupoints/bitong.md
- **review_status:** no_source_found
- **reason:** 未检索到来源候选
- **top_source:** null

## 当前文件概况
- **trace_status:** verified
- **review_status:** verified (P6)
- **alias_of:** "bitong" （⚠️ 自引用异常）
- **title:** "臂臑二"
- **Has source_refs:** Yes — 01针灸篇 page 50（臂臑穴定位教学）
- 正文有倪师讲解片段（来自臂臑教学段落）
- 正文有穴位定位、功效主治、针刺方法、配伍应用

## 来源/FTS 检索摘要
- FTS 中 "臂臑" 有 2 条命中（索引页）
- acupoint_index.jsonl 显示 source_quality_level: "verified_alias"
- p5b_review_segment: "name_mismatch"，p5b_resolution: "duplicate_suffix_base_name_match"
- 这表明系统识别到 bitong（臂臑二）是 binao（臂臑）的重复/别名条目

## 核查结论
### 发现问题：
1. **alias_of 自引用异常**：`alias_of: "bitong"` 指向自身，应该指向 "binao"（臂臑的主条目）
2. **主治内容混杂**：正文主治写"鼻塞，鼻渊，鼻衄"和配伍"配迎香、印堂，治鼻塞" — 这些是**鼻通穴**（经外奇穴，在鼻唇沟中）的主治，不是臂臑穴的主治
3. **刺法内容矛盾**：正文写"向上斜刺0.3-0.5寸，一般不灸"，但臂臑穴应直刺或斜刺0.5-1寸
4. **item_id "bitong" 可能原指"鼻通"穴**，在 P6 标准化时被错误映射为"臂臑二"

### 来源追溯有效：
- source_ref 指向针灸篇 page 50 的臂臑教学，来源准确
- 但 item_id 命名（bitong = 鼻通拼音）与 title（臂臑二）之间存在根本性矛盾

## 修改决定：记录问题，保守不改正文医学内容
- alias_of 自引用应修正为 alias_of: "binao"（与 bilao 条目一致）
- 主治/配伍内容混杂问题不在此轮修改（涉及医学内容判断，需专业审核）
- 将主治中明显错误的鼻部内容标注为存疑

## 未修改项（超出本轮保守复核范围）
- ⚠️ 主治内容（鼻塞/鼻渊/鼻衄）与臂臑穴不匹配，疑似数据混杂
- ⚠️ alias_of 自引用问题
- 建议后续专项审核：核对 bitong 条目原始意图（鼻通穴 vs 臂臑二别名）

## 修改记录
- alias_of 修正待定（不在此轮单独修改，因涉及索引一致性）
