# P8 Manual Review: 禹白附 (yubaizi)

- review_queue: `data/review_queue.jsonl:131`
- knowledge file: `knowledge/herbs/yubaizi.md`
- checked: `data/herb_sources.jsonl:377`, `data/herb_index.jsonl:377`, `data/knowledge_completeness.jsonl:490`, `data/p30_no_source_classification.jsonl:112`, `data/p36_external_source_queue.jsonl:112`, `data/source_fts.sqlite`.

## Decision

Keep `trace_status: no_source_found`. FTS/LIKE found no internal corpus hit for 「禹白附」.

## Change

Added a P8 source-boundary section and noted the duplicate/same-name relationship with `yubaifu`. Existing medical fields remain unverified pending external sources and alias cleanup.
