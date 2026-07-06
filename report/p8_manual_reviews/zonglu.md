# P8 Manual Review: 棕榈 (zonglu)

- review_queue: `data/review_queue.jsonl:144`
- knowledge file: `knowledge/herbs/zonglu.md`
- checked: `data/herb_sources.jsonl:414`, `data/herb_index.jsonl:414`, `data/knowledge_completeness.jsonl:527`, `data/p30_no_source_classification.jsonl:122`, `data/p36_external_source_queue.jsonl:122`, `data/source_fts.sqlite`.

## Decision

Keep `trace_status: no_source_found`. FTS/LIKE found no internal corpus hit for 「棕榈」.

## Change

Added a P8 source-boundary section. Existing medical fields and visible field-concatenation contamination are unverified; cleanup should be handled in a separate targeted data-quality pass.
