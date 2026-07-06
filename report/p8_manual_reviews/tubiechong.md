# tubiechong 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/herbs/tubiechong.md`
- **风险分类：** `herb_high_risk`

## 当前文件概况

当前条目为种子型 `no_source_found` 页面，frontmatter 标记 `aliases=["zhechong"]`。原文件包含“来源：神农本草经”种子信息、空的“倪师讲解”、禁忌待考与学习安全边界。P8 本轮未扩写医学内容，仅补充高风险边界和人工复核状态。

## 查到的来源 / 引用摘要

1. `data/herb_sources.jsonl`
   - `herb_id=tubiechong`
   - `searched_keywords=["土鳖虫"]`
   - `source_hits=[]`，`source_hit_count=0`，`status=no_source_found`
2. `data/review_queue.jsonl`
   - `review_status=no_source_found`
   - `reason=未检索到来源候选`
3. `data/source_fts.sqlite`
   - “土鳖虫”无直接命中
   - “地鳖虫”有 2 条命中；“蛰虫”有 2 条命中，其中包括神农本草经文稿第 256 页与金匮相关文稿第 131 页线索
   - 这些命中尚未由 `herb_sources` / `review_queue` 绑定到 `tubiechong`，本轮不提升为 `source_refs`
4. `data/no_source_classification.jsonl` / `data/p39_high_risk_external_review_queue.jsonl`
   - 一致标记为 `external_source_required` 与 `herb_high_risk`
   - 要求外部权威来源和完整安全字段复核

## 修改点

1. frontmatter 增加 `content_scope`、`safety_disclaimer_required`
2. frontmatter 增加 `reviewer: p8_manual_source_refinement`
3. frontmatter 增加 `review_status: pending_external_authoritative_source`
4. frontmatter 增加 `risk_tier: high`
5. 正文增加“高风险外部来源复核边界（P8 手工）”段落，并记录异名线索未绑定

## 保留边界

- 保持 `trace_status: no_source_found`
- 保留种子信息和 alias，但不据此扩写
- 不补写功效、剂量、毒性、禁忌、妊娠/儿童、相互作用或法定状态
- 不把“地鳖虫/蛰虫”FTS 线索自动提升为来源

## 未决问题

- 需后续人工判断“土鳖虫 / 蟅虫 / 蛰虫 / 地鳖虫”等异名关系，并为可用原文建立明确 `source_refs`
- 若后续扩写，需确定药典或现代中药学权威来源版本

## 是否需要外部权威资料

**需要。** 当前 registry 仍为 no_source_found；作为高风险药材，后续扩写必须依赖药典或同等级权威资料，或先完成内部异名 source_ref 绑定复核。


---

## R8 复核补记（2026-07-06）

- 队列位置：`data/review_queue.jsonl` 第 112 行；review_queue 状态=`no_source_found`。
- 本轮重新核对 knowledge 文件、review_queue、`herb_sources/herb_index/completeness/p30/p36`，并只读查询 `data/source_fts.sqlite`。
- herb_sources：status=`no_source_found`，source_hit_count=`0`，searched_keywords=['土鳖虫']。
- p30/p36：classification=`external_source_required`，category=`herb_high_risk`，risk_tier=`high`，canonical_item_id=`None`。
- source FTS/LIKE：按名称 `土鳖虫` 检索得到 0 条 LIKE 命中；未检出可追溯命中。
- 处理结论：既有 review note/高风险边界已存在，本轮只复核并记录跳过，不重复改写正文医学内容。
