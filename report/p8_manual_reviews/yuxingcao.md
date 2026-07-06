# P8 Manual Review: 鱼腥草 (yuxingcao)

- review_queue: `data/review_queue.jsonl:134`
- knowledge file: `knowledge/herbs/yuxingcao.md`
- checked: `data/herb_sources.jsonl:382`, `data/herb_index.jsonl:382`, `data/knowledge_completeness.jsonl:495`, `data/p30_no_source_classification.jsonl:115`, `data/p36_external_source_queue.jsonl:115`, `data/source_fts.sqlite`.

## Decision

Keep `trace_status: no_source_found`. FTS/LIKE found no internal corpus hit for 「鱼腥草」.

## Change

Added a P8 source-boundary section. Existing classification, 性味、归经、功效 fields are explicitly treated as unverified until supported by external authoritative `source_refs`.
