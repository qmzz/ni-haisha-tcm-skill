# P8 Manual Review: 寻骨风 (xungufeng)

- review_queue: `data/review_queue.jsonl:125`
- knowledge file: `knowledge/herbs/xungufeng.md`
- registry/context checked: `data/herb_sources.jsonl:359`, `data/herb_index.jsonl:359`, `data/knowledge_completeness.jsonl:472`, `data/p30_no_source_classification.jsonl:107`, `data/p36_external_source_queue.jsonl:107`.
- source DB checked: `data/source_fts.sqlite` opened read-only; FTS query for `寻骨风` returned 0 rows; LIKE query for `寻骨风` returned 0 rows.

## Decision

Keep `trace_status: no_source_found`. No正文 expansion or medical-content correction was made, because the current Ni corpus still has no traceable occurrence for `寻骨风`.

## Boundary Notes

Existing registry context classifies this as `external_source_required` / `herb_standard`, with manual review required before any content or quality promotion. The current file already carries no-source frontmatter boundary fields and a safety boundary.

## Unresolved

Knowledge completeness lists missing `properties` and `meridian`; these should not be filled without whitelisted external source_refs and manual review. No registry updates were made.
