# baiguo 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/herbs/baiguo.md`
- **队列位置：** `data/review_queue.jsonl` 第 11 行
- **条目：** 白果

## 当前文件概况

当前条目为 `trace_status: verified`，frontmatter 有 `source_refs` 指向 `04【视频同步文稿】人-伤寒论（可打印）.json` 第 144 页。正文基础信息、功效、主治较完整，但现有引用只是在四神汤/肾脏积水语境中提及白果。

## 查到的来源 / 引用摘要

1. `data/review_queue.jsonl`
   - `review_status=needs_review`
   - `quality_score=50`，低于自动 verified 阈值
   - 候选为 exact-name「白果」命中
2. `data/herb_sources.jsonl`
   - 同一页有 2 条白果命中，语境均为四神汤组成及“有时候白果改成淮山”
3. `data/herb_index.jsonl` / `data/knowledge_completeness.jsonl`
   - `trace_status=verified`
   - `source_quality_level=verified_direct`
4. `data/source_fts.sqlite`
   - 只读 FTS 检索「白果」命中 1 条：`04【视频同步文稿】人-伤寒论（可打印）.json` 第 144 页

## 修改点

- 在 P5 来源追溯状态中增加 P8 手工复核说明。
- 在正文增加“来源边界说明（P8 手工复核）”，限定现有引用只支撑“倪师提及白果”。

## 保留边界

- 保留 `trace_status: verified`，因为内部语料确有 exact-name 可追溯提及。
- 不把现有引用扩大解释为能验证性味、归经、功效、主治、禁忌。
- 不新增医学内容。

## 下一步

若需核验本文本草学字段，应引入外部权威来源或找到更直接的内部专门讲解。
