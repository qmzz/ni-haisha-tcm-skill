# gansui 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/gansui.md`
- **队列位置：** `data/p26_needs_review_segments.jsonl` 第 104 行
- **条目：** 甘遂

## p26 问题段

P26 标记为 `empty_quote`，指向 `02【视频同步文稿】人-神农本草经（可打印）.json` page 282，`quote_preview` 为空。

## 来源 / FTS 摘要

knowledge frontmatter page 282 主要在葶苈大枣/甘遂半夏/十枣汤语境中提及甘遂，不是甘遂独立条目。`verified_sources.jsonl` 记录 page 85 淮山段落“恶甘遂”，也只是禁忌旁及。`knowledge_completeness` 当前为 `verified_direct`，但证据边界不足。FTS exact 未返回可用命中。

## 核查结论

甘遂当前来源更接近方剂/禁忌旁及，不足以作为药材独立 `verified_direct`。需要后续查找甘遂独立来源或降级。

## 修改 / 不修改理由

不修改正文。未发现正文串联污染需要立即删除，但来源等级应后续复核。

## 未决问题

- 建议后续将 source_quality 从 `verified_direct` 复核为 contextual/needs_review，除非补到甘遂独立讲解。
