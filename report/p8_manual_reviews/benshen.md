# benshen 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/acupoints/benshen.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 1 行
- **条目：** 本神

## P26 问题段

P26 标记的 `source_refs` 指向 `黄帝内经.json` 第 1 页目录片段：`本输第二 / 小针解第三 / ... / 本神第八`。该段只是目录命中，属于 `empty_or_dirty_quote` / `dirty_quote`，不能支撑本神穴定位、归经或功效字段。

## 来源与 FTS 摘要

- 当前正文已包含较可用的针灸篇摘录：头维与本神同线、头临泣再跨过来一寸为本神、阳白之前为本神等上下文。
- `data/acupoint_sources.jsonl` 有 22 个候选命中，优先命中来自 `01【视频同步文稿】人-针灸篇（可打印）.json` 第 52、51、135 页，其中第 52 页明确说“本神是胆经的穴道，本神旁一寸五分”。
- `data/acupoint_index.jsonl` 已为 `verified_direct`，但仍保留 P5/P26 的脏段来源标记。
- `data/source_fts.sqlite` exact MATCH `本神` 未返回结果；本轮以 jsonl 候选与正文摘录为主要证据。

## 复核结论

- **正文修复：** 本轮不改。正文已有针灸篇直接语境，未见明显串联污染需要立即删除。
- **registry 后续修复：** 建议后续将 frontmatter/index 中的 `黄帝内经.json` 目录段替换为针灸篇第 52 或 135 页直接命中；保留 traceability-only 边界。
- **理由：** P26 问题只针对旧 source_ref 脏段；正文证据边界较清楚，适合后续小范围同步 source_ref，而非批量改正文。
