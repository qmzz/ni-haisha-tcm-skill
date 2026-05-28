# P26 / P5-B needs_review Segmentation

本报告将 P5-A 降级出的 `needs_review` 条目按问题类型分成后续可执行队列。

> 边界：只做来源关系分型，不改写医学内容，不判断医学真实性或疗效。

## Summary

- needs_review rows segmented: 160

## By segment

| segment | count |
|---|---:|
| `dirty_quote` | 32 |
| `empty_quote` | 77 |
| `name_mismatch` | 51 |

## By kind and segment

| kind | segment | count |
|---|---|---:|
| acupoint | `dirty_quote` | 20 |
| acupoint | `name_mismatch` | 49 |
| herb | `dirty_quote` | 12 |
| herb | `empty_quote` | 77 |
| herb | `name_mismatch` | 2 |

## Next actions

- `empty_quote`: 重新检索来源或降级为 no_source/needs_review 队列，不保留 verified 语义。
- `dirty_quote`: 先做 OCR/TOC/JSON 片段清理，再重新检索。
- `name_mismatch`: 检查 alias/重复二级条目/错配 source_refs，优先修 item_id 与来源关系。
- `weak_context`: 人工判断是否可保留 contextual 或降级。

Queue file: `data/p26_needs_review_segments.jsonl`
