# P8 Manual Review: 月季花 (yuejihua)

- review_queue: `data/review_queue.jsonl:132`
- knowledge file: `knowledge/herbs/yuejihua.md`
- checked: `data/herb_sources.jsonl:378`, `data/herb_index.jsonl:378`, `data/knowledge_completeness.jsonl:491`, `data/p30_no_source_classification.jsonl:113`, `data/p36_external_source_queue.jsonl:113`, `data/source_fts.sqlite`.

## Decision

Keep `trace_status: no_source_found`. FTS/LIKE found no internal corpus hit for 「月季花」.

## Change

Added a P8 source-boundary section requiring external authoritative sources before any medical expansion. Existing medical fields remain unverified.
