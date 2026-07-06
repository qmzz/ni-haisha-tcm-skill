# P8 Manual Review: 棕榈炭 (zonglutan)

- review_queue: `data/review_queue.jsonl:145`
- knowledge file: `knowledge/herbs/zonglutan.md`
- checked: `data/herb_sources.jsonl:415`, `data/herb_index.jsonl:415`, `data/knowledge_completeness.jsonl:528`, `data/p30_no_source_classification.jsonl:123`, `data/p36_external_source_queue.jsonl:123`, `data/source_fts.sqlite`.

## Decision

Keep `trace_status: no_source_found`. FTS/LIKE found no internal corpus hit for 「棕榈炭」.

## Change

Added a P8 source-boundary section requiring external authoritative sources before any medical expansion.
