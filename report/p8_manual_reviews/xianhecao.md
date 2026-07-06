# P8 Manual Review: 仙鹤草 (xianhecao)

- review_queue: `data/review_queue.jsonl:116`
- knowledge file: `knowledge/herbs/xianhecao.md`
- registry/context checked: `data/herb_sources.jsonl:339`, `data/herb_index.jsonl:339`, `data/knowledge_completeness.jsonl:452`, `data/p30_no_source_classification.jsonl:101`, `data/p36_external_source_queue.jsonl:101`
- source DB checked: `data/source_fts.sqlite` opened read-only; FTS query for `仙鹤草` returned 0 rows; LIKE query for `仙鹤草` returned 0 rows.

## Decision

Keep `trace_status: no_source_found`. No正文 expansion or medical-content correction was made, because the current Ni corpus still has no traceable occurrence for `仙鹤草`.

## Boundary Notes

Existing registry context classifies this as `external_source_required` / `herb_standard`, with manual review required before any content or quality promotion. The current file already carries no-source frontmatter boundary fields and a safety boundary. Any future enrichment should use whitelisted external source_refs and a separate manual review pass.

## Unresolved

The knowledge file may contain seed structured content, but this pass did not validate or promote it medically. No p30/p36/herb_index/verified_sources registry updates were made.
