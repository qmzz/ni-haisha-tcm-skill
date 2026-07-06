# P8 Manual Review: 西洋参 (xiyangshen)

- review_queue: `data/review_queue.jsonl:121`
- knowledge file: `knowledge/herbs/xiyangshen.md`
- registry/context checked: `data/herb_sources.jsonl:351`, `data/herb_index.jsonl:351`, `data/knowledge_completeness.jsonl:464`; `data/p30_no_source_classification.jsonl` and `data/p36_external_source_queue.jsonl` contain no entry for this verified item.
- source DB checked: `data/source_fts.sqlite` opened read-only; FTS query for `西洋参` returned 0 rows; LIKE query returned 2 rows: `05【视频同步文稿】人-金匮要略（可打印）.json` pages 475 and 476.

## Decision

Keep verified trace boundary. The LIKE hits directly mention 西洋参 in a 金匮要略 lung/津液 support context already reflected by existing `source_refs`/正文 quotation. No正文 change was made.

## Boundary Notes

This review confirms textual occurrence only; it does not validate missing structured 本草 fields (`properties`, `meridian`) listed by knowledge completeness, and does not promote any additional medical claims. The older P16 expanded excerpts include broad corpus snippets; this pass did not attempt bulk cleanup.

## Unresolved

If structured fields are to be completed later, they require explicit source-backed extraction rather than model memory. No registry updates were made.
