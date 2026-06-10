# P54 ASCII Dot Tail Cleanup

Removed high-confidence truncated table-of-contents tails made of long ASCII period runs from active content.
Only runs of ten or more periods at a string or line boundary were removed; shorter transcript ellipses were left unchanged.
Needs-review evidence queues outside the active JSONL registry set were left unchanged.

- Markdown files changed: 8
- JSONL files changed: 4
- ASCII dot tails removed: 25

## Markdown Changes
- `knowledge/acupoints/luozhen.md`: 1 ASCII dot tails
- `knowledge/acupoints/tongtian.md`: 1 ASCII dot tails
- `knowledge/formulas/danggui_shengjiang.md`: 2 ASCII dot tails
- `knowledge/formulas/fuling_rongyan.md`: 2 ASCII dot tails
- `knowledge/formulas/wenjing_tang.md`: 2 ASCII dot tails
- `knowledge/formulas/yuebi_tang.md`: 2 ASCII dot tails
- `knowledge/herbs/heshouwu.md`: 2 ASCII dot tails
- `knowledge/herbs/mangxiao.md`: 2 ASCII dot tails

## JSONL Changes
- `data/formula_sources.jsonl`: 1 rows, 1 ASCII dot tails
- `data/herb_index.jsonl`: 4 rows, 4 ASCII dot tails
- `data/review_decisions.jsonl`: 2 rows, 2 ASCII dot tails
- `data/verified_sources.jsonl`: 4 rows, 4 ASCII dot tails
