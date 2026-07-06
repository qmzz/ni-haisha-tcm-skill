# jiaji 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/acupoints/jiaji.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 20 行
- **条目：** 夹脊

## P26 问题段

P26 source_ref 指向伤寒论里柴胡、芒硝、大陷胸汤、止汗点等大段，虽末尾出现“华佗夹脊”，但前后边界过宽且混杂方药/病证内容，不适合作为穴位主 source_ref。

## 来源与 FTS 摘要

- 当前正文 frontmatter 仍保留该宽泛伤寒论段。
- `data/acupoint_sources.jsonl` 有 17 个候选命中，优先命中为针灸篇第 138 页，直接解释“督脉旁开五分”一条经称为“华陀夹脊”，并说明用于腰痛等。
- `data/acupoint_index.jsonl` 为 `verified_direct`，P26 标为 `dirty_quote`。
- `data/source_fts.sqlite` exact MATCH `夹脊` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。需后续收窄 frontmatter/source 摘录，避免以伤寒论宽段支撑夹脊穴。
- **registry 后续修复：** 建议替换为针灸篇第 138 页华陀夹脊直接段。
- **理由：** 直接来源存在，但当前 source_ref 边界过宽；按本轮规则只记录证据与后续修复项。
