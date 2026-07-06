# P8 Manual Review: 苎麻根 (zhumagen)

- review_queue: `data/review_queue.jsonl:140`
- knowledge file: `knowledge/herbs/zhumagen.md`
- checked: `data/herb_sources.jsonl:402`, `data/herb_index.jsonl:402`, `data/knowledge_completeness.jsonl:515`, `data/p30_no_source_classification.jsonl:120`, `data/p36_external_source_queue.jsonl:120`, `data/source_fts.sqlite`.

## Decision

Keep `trace_status: no_source_found`. FTS/LIKE found no internal corpus hit for 「苎麻根」.

## Change

Added a P8 source-boundary section requiring external authoritative sources before any medical expansion.
