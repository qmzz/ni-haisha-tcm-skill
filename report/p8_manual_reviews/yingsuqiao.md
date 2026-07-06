# P8 Manual Review: 罂粟壳 (yingsuqiao)

- review_queue: `data/review_queue.jsonl:129`
- knowledge file: `knowledge/herbs/yingsuqiao.md`
- checked: `data/herb_sources.jsonl:369`, `data/herb_index.jsonl:369`, `data/knowledge_completeness.jsonl:482`, `data/p30_no_source_classification.jsonl:110`, `data/p36_external_source_queue.jsonl:110`, `data/source_fts.sqlite`.

## Decision

Keep `trace_status: no_source_found`. FTS/LIKE found no internal corpus hit for 「罂粟壳」.

## Change

Added a P8 source-boundary section requiring external authoritative sources before any medical expansion.
