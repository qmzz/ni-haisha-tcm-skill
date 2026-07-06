# P8 Manual Review: 珍珠母 (zhenzhumu)

- review_queue: `data/review_queue.jsonl:138`
- knowledge file: `knowledge/herbs/zhenzhumu.md`
- checked: `data/herb_sources.jsonl:394`, `data/herb_index.jsonl:394`, `data/knowledge_completeness.jsonl:507`, `data/p30_no_source_classification.jsonl:118`, `data/p36_external_source_queue.jsonl:118`, `data/source_fts.sqlite`.

## Decision

Keep `trace_status: no_source_found`. FTS/LIKE found no internal corpus hit for 「珍珠母」.

## Change

Added a P8 source-boundary section requiring external authoritative sources before any medical expansion.
