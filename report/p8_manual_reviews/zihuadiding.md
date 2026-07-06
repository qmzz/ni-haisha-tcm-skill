# P8 Manual Review: 紫花地丁 (zihuadiding)

- review_queue: `data/review_queue.jsonl:143`
- knowledge file: `knowledge/herbs/zihuadiding.md`
- checked: `data/herb_sources.jsonl:409`, `data/herb_index.jsonl:409`, `data/knowledge_completeness.jsonl:522`, `data/p30_no_source_classification.jsonl:121`, `data/p36_external_source_queue.jsonl:121`, `data/source_fts.sqlite`.

## Decision

Keep `trace_status: no_source_found`. FTS/LIKE found no internal corpus hit for 「紫花地丁」.

## Change

Added a P8 source-boundary section. Existing classification, 性味、归经、功效 fields are explicitly treated as unverified until supported by external authoritative `source_refs`.
