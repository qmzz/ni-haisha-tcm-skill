# P8 Manual Review: 余甘子 (yuganzi)

- review_queue: `data/review_queue.jsonl:133`
- knowledge file: `knowledge/herbs/yuganzi.md`
- checked: `data/herb_sources.jsonl:379`, `data/herb_index.jsonl:379`, `data/knowledge_completeness.jsonl:492`, `data/p30_no_source_classification.jsonl:114`, `data/p36_external_source_queue.jsonl:114`, `data/source_fts.sqlite`.

## Decision

Keep `trace_status: no_source_found`. FTS/LIKE found no internal corpus hit for 「余甘子」.

## Change

Added a P8 source-boundary section requiring external authoritative sources before any medical expansion.
