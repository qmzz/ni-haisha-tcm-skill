# P8 Manual Review: 朱砂根 (zhushagen)

- review_queue: `data/review_queue.jsonl:141`
- knowledge file: `knowledge/herbs/zhushagen.md`
- checked: `data/herb_sources.jsonl:405`, `data/herb_index.jsonl:405`, `data/knowledge_completeness.jsonl:518`, `data/source_fts.sqlite`.

## Decision

Changed the knowledge file from verified-style presentation to `needs_review`, because the existing `source_refs` and body excerpts are about 「朱砂」, not 「朱砂根」. FTS/LIKE for 「朱砂根」 returned no internal corpus hit.

## Change

Updated frontmatter `review_status` / `trace_status` and added a P8 boundary section explaining the source mis-binding. Kept the old quote visible for source_ref cleanup traceability, but marked it as invalid for validating 「朱砂根」.

## Unresolved

Requires separate source_ref repair / registry sync. No medical content was added.
