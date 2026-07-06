# P8 Manual Review: 雪莲花 (xuelianhua)

- review_queue: `data/review_queue.jsonl:123`
- knowledge file: `knowledge/herbs/xuelianhua.md`
- registry/context checked: `data/herb_sources.jsonl:356`, `data/herb_index.jsonl:356`, `data/knowledge_completeness.jsonl:469`, `data/p30_no_source_classification.jsonl:106`, `data/p36_external_source_queue.jsonl:106`.
- source DB checked: `data/source_fts.sqlite` opened read-only; FTS query for `雪莲花` returned 0 rows; LIKE query for `雪莲花` returned 0 rows.

## Decision

Keep `trace_status: no_source_found`. No正文 expansion or medical-content correction was made, because the current Ni corpus still has no traceable occurrence for `雪莲花`.

## Boundary Notes

Existing registry context classifies this as `external_source_required` / `herb_standard`, with manual review required before any content or quality promotion. The current file already carries no-source frontmatter boundary fields and a safety boundary.

## Unresolved

Knowledge completeness lists missing `properties` and `meridian`; these should not be filled without whitelisted external source_refs and manual review. No registry updates were made.
