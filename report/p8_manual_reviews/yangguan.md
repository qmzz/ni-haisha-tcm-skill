# yangguan (腰阳关-alias) — P8 R12 Review

## Review Queue Info
- **Line:** 200
- **item_id:** yangguan
- **name:** 腰阳关
- **file:** knowledge/acupoints/yangguan.md
- **review_status:** no_source_found
- **reason:** 未检索到来源候选

## 当前文件概况
- **trace_status:** no_source_found
- **alias_of:** "yaoyangguan"
- **Has source_refs:** No
- **source_scope:** "not_in_nihaixia_source"
- **external_reference_required:** true
- **no_source_policy:** "keep_boundary_until_traceable_source"
- **归经:** 标注为足少阳胆经（但实际腰阳关应为督脉 DU3）

## 来源/FTS 检索摘要
- FTS 检索 "腰阳关" 无命中
- LIKE 检索 "腰阳关" 无命中
- yangguan 不在 acupoint_index.jsonl 中
- yaoyangguan（canonical）在 index 中：source_quality_level: "no_source"，trace_status: "no_source_found"
- p30: p6b_resolution: "mapped_to_canonical_but_canonical_is_no_source"

## 核查结论
- yangguan 是 yaoyangguan 的别名/重复条目
- 两者均为 no_source_found，倪师人纪语料中未检索到 "腰阳关" 的讲解
- **发现问题：** frontmatter 标注归经为 "足少阳胆经"，但腰阳关实际为督脉穴（DU3）。主条目 yaoyangguan 正确标注为督脉。此为数据错误，但不属本轮来源审查范围，记录待后续修正。

## 修改决定：不修改正文
- 条目保持 no_source_found 边界
- 发现归经标注错误（标为胆经，应为督脉），但不在本轮来源审查中修改

## 外部权威来源需求
- **推荐来源类型：** acupoint_standard_reference
- **推荐来源：** 《针灸大成》、GB/T 12346-2021

## 未决问题
- ⚠️ 归经标注不一致：yangguan.md 标为 "足少阳胆经"，yaoyangguan.md 标为 "督脉"；主条目正确，别名条目有误。建议后续数据质量专项修正。
