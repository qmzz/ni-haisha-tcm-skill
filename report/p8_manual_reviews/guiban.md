# guiban 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/guiban.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 111 行
- **条目：** 龟板

## p26 问题段

P26 标记为 `empty_quote`，来源指向原记录页码；该行 `quote_preview` 为空。

## 来源 / FTS 摘要

当前 frontmatter 有龟板/龟甲滋阴益血、补肾、任督等长摘录，但 `verified_sources.jsonl` 的命中来自鹿茸段落中“任脉来说的话是龟板”，属于鹿角/鹿茸上下文旁及。 本轮 FTS exact 检索未返回可用命中，判断主要依据 p26 行、knowledge frontmatter、`knowledge_completeness.jsonl` 与 `verified_sources.jsonl`。

## 核查结论

当前正文可作为龟板相关来源参考，但 registry 的 `verified_direct` 证据边界偏乐观；应后续补龟板独立条目或降级 contextual。

## 修改 / 不修改理由

本轮不修改 knowledge 正文、index 或 registry。P26 多数为 needs_review segment，先记录证据边界与后续修复方向。

## 未决问题

- 后续按上方结论同步 source_ref 边界或调整 source_quality；不得把旁及提及继续当作直接来源。
