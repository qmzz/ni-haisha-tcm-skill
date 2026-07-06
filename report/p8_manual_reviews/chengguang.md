# chengguang 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/acupoints/chengguang.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 5 行
- **条目：** 承光

## P26 问题段

P26 标记的片段来自针灸篇 page 1 的 JSON 拼接边界，内容实际在讲神庭、曲差、眉冲一带，并夹有 `V2-20100703... {"page_num": 91` 之类结构残留。该段不能作为承光的直接 source_ref。

## 来源与 FTS 摘要

- 当前正文的“倪师讲解”已引用针灸篇承光段：`神庭后五分就是上星，上星过来一寸半，就是五处...承光从五处往后面一寸半...承光就是眼看不到光...`。
- `data/acupoint_sources.jsonl` 有 6 个候选命中，优先命中为 `01【视频同步文稿】人-针灸篇（可打印）.json` 第 91 页，直接出现承光并解释命名及眼科语境。
- `data/acupoint_index.jsonl` 为 `verified_direct`，但仍带 `empty_or_dirty_quote` / `dirty_quote` 历史标记。
- `data/source_fts.sqlite` exact MATCH `承光` 未返回结果；以候选 jsonl 与正文摘录为准。

## 复核结论

- **正文修复：** 本轮不改。正文主体摘录能直接支撑条目边界。
- **registry 后续修复：** 建议把 frontmatter/index 的脏 JSON 边界段替换为针灸篇第 91 页承光直接段。
- **理由：** 问题集中在旧 source_ref 抽取边界，不是正文串联污染。
