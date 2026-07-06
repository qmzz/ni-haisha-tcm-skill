# 瓦楞子 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/herbs/walengzi.md`
- **队列位置：** `data/review_queue.jsonl` 第 114 行
- **条目：** 瓦楞子 (`walengzi`)

## 当前文件概况

本轮人工读取 knowledge 文件、review_queue 行，并核对 `data/herb_sources.jsonl`、`data/herb_index.jsonl`、`data/knowledge_completeness.jsonl`、`data/p30_no_source_classification.jsonl`、`data/p36_external_source_queue.jsonl`，只读查询 `data/source_fts.sqlite`。

## 查到的来源 / 引用摘要

- review_queue：`needs_review`；reason=`quality_score_below_verified_threshold`。
- herb_sources：status=`candidate`，source_hit_count=`35`，searched_keywords=['瓦楞子'].
- herb_index：trace_status=`verified`，source_quality_level=`verified_direct`，source_refs_count=1.
- completeness：trace_status=`verified`，quality_tier=`refined`，source_quality_level=`verified_direct`。
- p30：classification=`None`，canonical_item_id=`None`，risk_tier=`None`。
- p36：category=`None`，risk_tier=`None`，recommended_source_scopes=None.
- source FTS/LIKE：按名称 `瓦楞子` 检索得到 3 条 LIKE 命中；前 3 条：[('04【视频同步文稿】人-伤寒论（可打印）.json', 92, '瓦楞子。瓦楞子也是攻坚\n用的，因为长得很像乳房，取它的象。'), ('05【视频同步文稿】人-金匮要略（可打印）.json', 132, '瓦楞子，这个\n瓦楞子呢长相啊，贝壳个这样子，长的就这个样子啊，你如果跑到南门市场去买，\n叫血蚶啊，这个贝壳呢打开，你看到里面是血，看看是血，很多血很多血在里面\n啊，这个血蚶的壳就叫做瓦楞子，因为它长相就像个乳房，像个乳房，然后呢，\n它里面是血，哦，这个瓦楞子呢也是味咸，咸味能够软坚，所以我在治疗那个乳\n房硬块、甲状腺的硬块、淋巴癌的时候，瓦楞子用得非常多，哦'), ('05【视频同步文稿】人-金匮要略（可打印）.json', 280, '瓦楞子，瓦楞子呢，\n比如说我用到五钱，为什么会选择瓦楞子呢？\n瓦楞子专门去这个痰饮，哦，痰饮，效果很好，那消积，有痰积到身体里面\n去，瓦楞子（可以消除）。现在再回头，如果一个女孩子乳房里面有硬块，是不\n是就是瓦楞子。一样啊，你把它想成痰水就好了。哦。如果结石很硬一块，排不\n出来的时候，经方呢欸这个还有啊，我们很多药啊可以选择，用牡蛎，牡蛎可以\n软坚，你说老师')]

## 修改点

- 本轮复核 verified/needs_review 候选：知识文件已有直接 source_refs 和摘录；仅记录候选来源状态与保留边界，未改写正文。

## 保留边界

- `no_source_found` / `external_source_required` 条目继续保持未验证边界；既有医学性字段仅作为待核验草稿或占位。
- 弱候选、上下文提及、别名/重复映射线索不等于医学内容全字段验证。

## 下一步

后续若纳入外部来源，应逐条补充明确 `source_refs`，并单独核验性味、归经、功效、主治、剂量、禁忌及特殊安全字段。
