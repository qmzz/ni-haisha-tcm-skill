# P55 Long ASCII Dot Run Cleanup

Removed high-confidence layout residue made of long ASCII period runs from active content.
Only runs of ten or more periods were removed; shorter transcript ellipses were left unchanged.
Needs-review evidence queues outside the active JSONL registry set were left unchanged.

- Markdown files changed: 15
- JSONL files changed: 6
- Long ASCII dot runs removed: 50

## Markdown Changes
- `knowledge/herbs/buguzhi.md`: 1 long ASCII dot runs
- `knowledge/herbs/cangzhu.md`: 2 long ASCII dot runs
- `knowledge/herbs/dengxincao.md`: 2 long ASCII dot runs
- `knowledge/herbs/ezhu.md`: 2 long ASCII dot runs
- `knowledge/herbs/fuxiaomai.md`: 1 long ASCII dot runs
- `knowledge/herbs/ganlan.md`: 2 long ASCII dot runs
- `knowledge/herbs/huaihua.md`: 1 long ASCII dot runs
- `knowledge/herbs/kuandonghua.md`: 1 long ASCII dot runs
- `knowledge/herbs/lingxiaohua.md`: 1 long ASCII dot runs
- `knowledge/herbs/madouling.md`: 1 long ASCII dot runs
- `knowledge/herbs/mangxiao.md`: 2 long ASCII dot runs
- `knowledge/herbs/sanleng.md`: 1 long ASCII dot runs
- `knowledge/herbs/walengzi.md`: 1 long ASCII dot runs
- `knowledge/herbs/zhuru.md`: 2 long ASCII dot runs
- `knowledge/herbs/zisuan.md`: 2 long ASCII dot runs

## JSONL Changes
- `data/formula_index.jsonl`: 2 rows, 2 long ASCII dot runs
- `data/formula_sources.jsonl`: 8 rows, 11 long ASCII dot runs
- `data/herb_index.jsonl`: 4 rows, 4 long ASCII dot runs
- `data/review_decisions.jsonl`: 4 rows, 4 long ASCII dot runs
- `data/review_queue.jsonl`: 1 rows, 1 long ASCII dot runs
- `data/verified_sources.jsonl`: 6 rows, 6 long ASCII dot runs
