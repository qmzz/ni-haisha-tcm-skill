# dahuang 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/dahuang.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 86 行
- **条目：** 大黄

## P26 问题段

P26 标记为 `empty_quote`。当前 quote 为药物炮制通论，其中以大黄酒制举例，讨论酒制、姜制、盐炒、醋制等；它可说明“大黄酒制”加工语境，但不是大黄药材独立讲解。

## 来源与 FTS 摘要

- 当前正文保留炮制段作为来源，直接性不足以支撑大黄性味归经与泻下功效。
- `data/herb_sources.jsonl` 记录 80 个候选命中，但摘要 top hit 为空 quote，需后续查找大黄独立条目或伤寒/金匮核心用法段。
- `data/herb_index.jsonl` 为 `verified_direct`，P26 标为 `empty_quote`。
- `data/source_fts.sqlite` exact MATCH `大黄` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。
- **registry 后续修复：** 建议重查并替换为大黄独立讲解或经典条文用法段；当前炮制举例只能作为补充证据。
- **理由：** source boundary 不足，需后续人工收窄。
