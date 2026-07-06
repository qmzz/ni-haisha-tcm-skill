# chenpi 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/chenpi.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 76 行
- **条目：** 陈皮

## P26 问题段

P26 标记为 `empty_quote`，队列中的 `quote_preview` 为空，说明旧 source_ref 曾缺 quote 或 quote 过短。

## 来源与 FTS 摘要

- 当前正文已由 `p17_content_quality` 补入完整神农本草经讲解：橘柚/陈皮、广陈皮、辛温、利水谷、下气通神、青皮与陈皮区别等。
- `data/herb_sources.jsonl` 有 63 个候选命中，优先命中含 `倪海厦人纪系列之神农本草经.json` 第 61-62 页橘柚/陈皮本经原文、性味、主治、用量禁忌等。
- `data/herb_index.jsonl` 为 `verified_direct`，P26 的问题是历史 empty_quote 标记。
- `data/source_fts.sqlite` exact MATCH `陈皮` 未返回结果。

## 复核结论

- **正文修复：** 本轮不改。当前正文已有完整直接讲解。
- **registry 后续修复：** 如需同步，建议确认 frontmatter/index quote 与 P17 正文一致，并清理旧 `empty_quote` 标记。
- **理由：** P26 问题已被现有正文质量修复覆盖，当前只补人工 note。
