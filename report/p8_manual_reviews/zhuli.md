# P8 Manual Review: 竹沥 (zhuli)

- review_queue: `data/review_queue.jsonl:139`
- knowledge file: `knowledge/herbs/zhuli.md`
- checked: `data/herb_sources.jsonl:400`, `data/herb_index.jsonl:400`, `data/knowledge_completeness.jsonl:513`, `data/p30_no_source_classification.jsonl:119`, `data/p36_external_source_queue.jsonl:119`, `data/source_fts.sqlite`.

## Decision

Keep `trace_status: no_source_found`. FTS/LIKE found no internal corpus hit for 「竹沥」.

## Change

Added a P8 source-boundary section requiring external authoritative sources before any medical expansion. Existing medical fields remain unverified.
