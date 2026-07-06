# P8 Manual Review: 樟脑 (zhangnao)

- review_queue: `data/review_queue.jsonl:136`
- knowledge file: `knowledge/herbs/zhangnao.md`
- checked: `data/herb_sources.jsonl:391`, `data/herb_index.jsonl:391`, `data/knowledge_completeness.jsonl:504`, `data/p30_no_source_classification.jsonl:116`, `data/p36_external_source_queue.jsonl:116`, `data/source_fts.sqlite`.

## Decision

Keep `trace_status: no_source_found`. FTS/LIKE found no internal corpus hit for 「樟脑」.

## Change

Added a P8 source-boundary section requiring external authoritative sources before any medical expansion.
