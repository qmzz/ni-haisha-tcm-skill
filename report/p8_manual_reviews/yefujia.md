# P8 Manual Review: 夜交藤 (yefujia)

- review_queue: `data/review_queue.jsonl:128`
- knowledge file: `knowledge/herbs/yefujia.md`
- checked: `data/herb_sources.jsonl:365`, `data/herb_index.jsonl:365`, `data/knowledge_completeness.jsonl:478`, `data/source_fts.sqlite`.

## Decision

Keep verified trace boundary. The queue top source and LIKE hit directly mention 「夜交藤」 in a 何首乌藤 context. No正文 change was made.

## Boundary Notes

This confirms occurrence and local context only; it does not independently revalidate all structured medical fields. FTS returned 0 rows, LIKE returned the known page 229 hit.
