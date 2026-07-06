# ganlan 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/ganlan.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 48 行
- **条目：** 橄榄

## 当前文件概况

当前条目为 herb，frontmatter `trace_status: verified`，有 `source_refs`，正文含安全边界、倪师讲解、来源摘录。`knowledge_completeness` 显示缺失 `properties` 与 `meridian`。

## 来源 / FTS 摘要

- `herb_index.jsonl` / `verified_sources.jsonl`：标记 `source_quality_level=verified_direct`，引用 `05【视频同步文稿】人-金匮要略（可打印）.json` page 80。
- 该引用实际语境为 football 面罩下“两条黑”、胆/盲肠化脓、赤豆当归散等内容，其中“橄榄”只出现在“美国那个 football（美国把橄榄球叫football）”。
- `herb_sources.jsonl` 对 ganlan 为 `source_hits=[]`，状态仍为 candidate，和 verified registry 不一致。
- `source_fts.sqlite` 只读检索“橄榄”无命中。

## 是否直接支撑缺失字段

- properties：不支撑。未见药材橄榄性味原文。
- meridian：不支撑。未见药材橄榄归经原文。

## 修改 / 不修改理由

本轮不补写缺失字段。当前 verified 引用属于 false positive / 语义污染，不应作为橄榄药材来源。正文中的“橄榄油也可以”片段也只是蒲灰散外用调和介质，不是药材橄榄条目的直接讲解。

## 未决问题

- 建议后续将该条从 verified 降级或重新进入 no_source/external source 流程，并清理 frontmatter `source_refs` 与正文中无关来源摘录；需要与 `herb_index`、`verified_sources`、`knowledge_completeness` 协同更新，避免单改 Markdown 造成状态分裂。

## R19 action

- 已执行最小修复：清理 `knowledge/herbs/ganlan.md` 中 football/橄榄球语境的错误 `source_refs` 与无关来源摘录。
- 已同步注册表：`herb_index.jsonl`、`knowledge_completeness.jsonl` 降级为 `trace_status=no_source_found`、`source_quality_level=no_source`，并从 `verified_sources.jsonl` 移除。
- 已加入 no-source / external-source 后续队列；未补写 `properties` 或 `meridian`。
