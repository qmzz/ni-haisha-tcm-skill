# P8 Manual Review: 血竭 (xuejie)

- review_queue: `data/review_queue.jsonl:122`
- knowledge file: `knowledge/herbs/xuejie.md`
- registry/context checked: `data/herb_sources.jsonl:355`, `data/herb_index.jsonl:355`, `data/knowledge_completeness.jsonl:468`; `data/p30_no_source_classification.jsonl` and `data/p36_external_source_queue.jsonl` contain no entry for this verified item.
- source DB checked: `data/source_fts.sqlite` opened read-only; FTS query for `血竭` returned 0 rows; LIKE query returned 2 rows: `05【视频同步文稿】人-金匮要略（可打印）.json` page 257 and `倪海厦人纪系列之伤寒论.json` page 152.

## Decision

Keep verified trace boundary. The source hits directly mention 血竭, but the page 152 context is a cautionary/negative case about adding 南派破瘀/伤科 drugs after 十枣汤, and page 257 is an external-use wound context. No正文 change was made.

## Boundary Notes

This review confirms mention and context only; it does not independently validate the embedded structured 性味/归经/功效/主治 fields. The frontmatter currently has formatting contamination where multiple fields are concatenated; this is a data-quality follow-up, not changed in this small pass.

## Unresolved

`xuejie` and `xuhuang` are duplicate/alias-mapped 血竭 entries. Registry canonicalization/field cleanup should be handled in a separate targeted pass. No registry updates were made.
