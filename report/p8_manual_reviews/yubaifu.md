# P8 Manual Review: 禹白附 (yubaifu)

- review_queue: `data/review_queue.jsonl:130`
- knowledge file: `knowledge/herbs/yubaifu.md`
- checked: `data/herb_sources.jsonl:376`, `data/herb_index.jsonl:376`, `data/knowledge_completeness.jsonl:489`, `data/p30_no_source_classification.jsonl:111`, `data/p36_external_source_queue.jsonl:111`, `data/source_fts.sqlite`.

## Decision

Keep `trace_status: no_source_found`. FTS/LIKE found no internal corpus hit for 「禹白附」.

## Change

Added a P8 source-boundary section requiring external authoritative sources before any medical expansion.
