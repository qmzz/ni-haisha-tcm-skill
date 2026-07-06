# P8 Manual Review: 血竭 (xuhuang)

- review_queue: `data/review_queue.jsonl:124`
- knowledge file: `knowledge/herbs/xuhuang.md`
- registry/context checked: `data/herb_sources.jsonl:358`, `data/herb_index.jsonl:358`, `data/knowledge_completeness.jsonl:471`; `data/p30_no_source_classification.jsonl` and `data/p36_external_source_queue.jsonl` contain no entry for this verified item.
- source DB checked: `data/source_fts.sqlite` opened read-only; FTS query for `血竭` returned 0 rows; LIKE query returned 2 rows: `05【视频同步文稿】人-金匮要略（可打印）.json` page 257 and `倪海厦人纪系列之伤寒论.json` page 152. Additional FTS/LIKE queries for romanized `xuhuang` and `xuejie` returned 0 rows.

## Decision

Keep verified trace boundary. This appears to be a duplicate/alias entry for 血竭 with alias `xuejie`; the source hits are the same as `xuejie`. No正文 change was made.

## Boundary Notes

The source evidence supports textual mention of 血竭, not the existence of a distinct herb named `xuhuang`. Because registry synchronization/canonicalization could affect multiple files, this pass only documents the alias/duplicate boundary.

## Unresolved

Follow-up recommended: decide canonical item ID between `xuejie` and `xuhuang`, then clean duplicate mappings and field divergence in a dedicated registry-safe pass. No registry updates were made.
