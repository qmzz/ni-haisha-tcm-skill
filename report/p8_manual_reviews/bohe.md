# bohe 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/bohe.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 72 行
- **条目：** 薄荷

## P26 问题段

P26 quote 来自金匮要略腹满/承气汤辨证段，只有“美国人刷舌苔、吃薄荷东西导致舌苔蓝色”这一旁及提及。该段不支撑薄荷药材的性味、归经、功效或主治。

## 来源与 FTS 摘要

- 当前 frontmatter 与正文仍使用该金匮要略旁及段，正文后续还混入腹水、分消汤、补气建中汤等内容，source boundary 明显不属于薄荷药材讲解。
- `data/herb_index.jsonl` 为 `verified_direct`，但 P26 标为 `dirty_quote`。
- `data/herb_sources.jsonl` 记录 `source_hit_count=12`，本轮只读摘要未见可用 top hit 输出；需后续逐条重查。
- `data/source_fts.sqlite` exact MATCH `薄荷` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改，但该条存在明显旁及提及污染风险。
- **registry 后续修复：** 建议后续降级为 contextual/needs_review 或重查内部直接来源；当前金匮段不应作为薄荷 verified_direct 主证据。
- **理由：** 现有来源只说明“薄荷味/薄荷物影响舌苔观察”，不支撑药材条目。
