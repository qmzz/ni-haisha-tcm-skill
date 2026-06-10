# P52 ASCII TOC Dot Leader Cleanup

Removed high-confidence ASCII table-of-contents dot leaders with trailing page numbers from active content.
Only runs of six or more periods followed by page number groups were removed; entry text and ordinary page references were left unchanged.
Needs-review evidence queues outside the active JSONL registry set were left unchanged.

- Markdown files changed: 24
- JSONL files changed: 4
- ASCII dot leader page markers removed: 862

## Markdown Changes
- `knowledge/acupoints/benshen.md`: 10 ASCII dot leader page markers
- `knowledge/acupoints/luozhen.md`: 3 ASCII dot leader page markers
- `knowledge/acupoints/tongtian.md`: 7 ASCII dot leader page markers
- `knowledge/formulas/dahuang_gansui.md`: 30 ASCII dot leader page markers
- `knowledge/formulas/danggui_shengjiang.md`: 30 ASCII dot leader page markers
- `knowledge/formulas/didang_tang.md`: 30 ASCII dot leader page markers
- `knowledge/formulas/fuling_rongyan.md`: 30 ASCII dot leader page markers
- `knowledge/formulas/honglanhua_jiu.md`: 30 ASCII dot leader page markers
- `knowledge/formulas/huashi_baiyu.md`: 30 ASCII dot leader page markers
- `knowledge/formulas/linggui_zhugan.md`: 20 ASCII dot leader page markers
- `knowledge/formulas/puhui_san.md`: 30 ASCII dot leader page markers
- `knowledge/formulas/shechuangzi_san.md`: 26 ASCII dot leader page markers
- `knowledge/formulas/shegan_mahuang.md`: 30 ASCII dot leader page markers
- `knowledge/formulas/tingli_dazao.md`: 26 ASCII dot leader page markers
- `knowledge/formulas/wenjing_tang.md`: 28 ASCII dot leader page markers
- `knowledge/formulas/yiyi_fuzi.md`: 16 ASCII dot leader page markers
- `knowledge/formulas/yuebi_tang.md`: 30 ASCII dot leader page markers
- `knowledge/formulas/zaojia_wan.md`: 30 ASCII dot leader page markers
- `knowledge/formulas/zeqi_tang.md`: 30 ASCII dot leader page markers
- `knowledge/formulas/zhishi_shaoyao.md`: 30 ASCII dot leader page markers
- `knowledge/herbs/heshouwu.md`: 50 ASCII dot leader page markers
- `knowledge/herbs/huanglian.md`: 2 ASCII dot leader page markers
- `knowledge/herbs/lurong.md`: 2 ASCII dot leader page markers
- `knowledge/herbs/mangxiao.md`: 68 ASCII dot leader page markers

## JSONL Changes
- `data/formula_sources.jsonl`: 11 rows, 42 ASCII dot leader page markers
- `data/herb_index.jsonl`: 4 rows, 91 ASCII dot leader page markers
- `data/review_decisions.jsonl`: 3 rows, 20 ASCII dot leader page markers
- `data/verified_sources.jsonl`: 4 rows, 91 ASCII dot leader page markers
