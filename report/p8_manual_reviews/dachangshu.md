# dachangshu 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/acupoints/dachangshu.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 9 行
- **条目：** 大肠俞

## P26 问题段

P26 标记的 source_ref 指向 `倪海厦人纪系列之伤寒论.json` 第 1 页，内容为猪苓、泽泻、赤石脂禹余粮等止利药物语境，并夹有 `{"page_num": 118` JSON 残留。该段不支撑大肠俞穴位字段。

## 来源与 FTS 摘要

- 当前正文“倪师讲解”引用针灸篇背俞穴/腰痛近取穴上下文。
- `data/acupoint_sources.jsonl` 有 8 个候选命中，优先命中来自针灸篇第 101 页，涉及肾俞、气海俞、大肠俞附近背俞穴序列和近取穴语境。
- `data/acupoint_index.jsonl` 为 `verified_direct`，但保留 P26 脏段历史原因。
- `data/source_fts.sqlite` exact MATCH `大肠俞` 未返回结果；本轮未用 FTS 提升等级。

## 复核结论

- **正文修复：** 本轮不改。正文未见明显相邻条目污染需要删除。
- **registry 后续修复：** 建议将旧伤寒论 source_ref 替换为针灸篇第 101 页直接命中；若需更严谨，可补查第 101 页完整背俞穴段。
- **理由：** P26 段为明显 false source_ref；但已有针灸篇候选可作为后续同步证据。
