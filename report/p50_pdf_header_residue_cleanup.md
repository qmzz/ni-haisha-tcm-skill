# P50 PDF Header Residue Cleanup

Removed high-confidence PDF date/book headers and dot-wrapped page markers from active content.
Needs-review evidence queues outside the active JSONL registry set were left unchanged.
Compact page references like `page 263` were left unchanged because many are source citations or transcript content.

- Markdown files changed: 30
- JSONL files changed: 5
- Date/book header pairs removed: 33
- Standalone date headers removed: 89
- Standalone book headers removed: 93
- Dot page markers removed: 157

## Markdown Changes
- `knowledge/acupoints/chengshan.md`: 0 date/book pairs, 1 dates, 1 book headers, 0 dot page markers
- `knowledge/acupoints/feiyang.md`: 0 date/book pairs, 1 dates, 1 book headers, 0 dot page markers
- `knowledge/acupoints/fenglong.md`: 0 date/book pairs, 1 dates, 1 book headers, 0 dot page markers
- `knowledge/acupoints/heyang.md`: 0 date/book pairs, 1 dates, 1 book headers, 0 dot page markers
- `knowledge/acupoints/huiyin.md`: 0 date/book pairs, 1 dates, 1 book headers, 0 dot page markers
- `knowledge/acupoints/jiaosun.md`: 1 date/book pairs, 1 dates, 1 book headers, 0 dot page markers
- `knowledge/acupoints/jimai.md`: 2 date/book pairs, 0 dates, 0 book headers, 0 dot page markers
- `knowledge/acupoints/jinggu.md`: 0 date/book pairs, 1 dates, 1 book headers, 0 dot page markers
- `knowledge/acupoints/kunlun.md`: 0 date/book pairs, 0 dates, 1 book headers, 0 dot page markers
- `knowledge/acupoints/pianli.md`: 0 date/book pairs, 1 dates, 1 book headers, 0 dot page markers
- `knowledge/acupoints/ququan.md`: 0 date/book pairs, 1 dates, 1 book headers, 0 dot page markers
- `knowledge/acupoints/renying.md`: 0 date/book pairs, 1 dates, 1 book headers, 0 dot page markers
- `knowledge/acupoints/shangwan.md`: 0 date/book pairs, 1 dates, 1 book headers, 0 dot page markers
- `knowledge/acupoints/shaoze.md`: 1 date/book pairs, 0 dates, 0 book headers, 0 dot page markers
- `knowledge/acupoints/shugu_bl.md`: 0 date/book pairs, 1 dates, 1 book headers, 0 dot page markers
- `knowledge/acupoints/taichong_lv.md`: 0 date/book pairs, 1 dates, 1 book headers, 0 dot page markers
- `knowledge/acupoints/taixi_k.md`: 0 date/book pairs, 1 dates, 1 book headers, 0 dot page markers
- `knowledge/acupoints/tianrong.md`: 0 date/book pairs, 1 dates, 1 book headers, 0 dot page markers
- `knowledge/acupoints/tongli.md`: 0 date/book pairs, 1 dates, 1 book headers, 0 dot page markers
- `knowledge/acupoints/toulinqi_bl.md`: 0 date/book pairs, 1 dates, 1 book headers, 0 dot page markers
- `knowledge/acupoints/wangu_gb.md`: 1 date/book pairs, 0 dates, 0 book headers, 0 dot page markers
- `knowledge/acupoints/xuanlu.md`: 1 date/book pairs, 1 dates, 1 book headers, 0 dot page markers
- `knowledge/acupoints/yaoshugu.md`: 0 date/book pairs, 1 dates, 1 book headers, 0 dot page markers
- `knowledge/acupoints/yinbai.md`: 0 date/book pairs, 1 dates, 1 book headers, 0 dot page markers
- `knowledge/acupoints/yingu.md`: 0 date/book pairs, 1 dates, 1 book headers, 0 dot page markers
- `knowledge/acupoints/yingu_k.md`: 0 date/book pairs, 1 dates, 1 book headers, 0 dot page markers
- `knowledge/acupoints/yixi.md`: 1 date/book pairs, 0 dates, 0 book headers, 0 dot page markers
- `knowledge/acupoints/yuanye.md`: 4 date/book pairs, 0 dates, 0 book headers, 0 dot page markers
- `knowledge/acupoints/zhongfeng.md`: 0 date/book pairs, 1 dates, 1 book headers, 0 dot page markers
- `knowledge/concepts/zongqi.md`: 1 date/book pairs, 0 dates, 0 book headers, 0 dot page markers

## JSONL Changes
- `data/acupoint_index.jsonl`: 44 rows, 88 pattern groups, 3 date/book pairs, 21 dates, 22 book headers, 47 dot page markers
- `data/acupoint_sources.jsonl`: 6 rows, 11 pattern groups, 9 date/book pairs, 0 dates, 0 book headers, 7 dot page markers
- `data/review_decisions.jsonl`: 50 rows, 100 pattern groups, 3 date/book pairs, 24 dates, 25 book headers, 54 dot page markers
- `data/review_queue.jsonl`: 3 rows, 5 pattern groups, 3 date/book pairs, 0 dates, 0 book headers, 2 dot page markers
- `data/verified_sources.jsonl`: 44 rows, 88 pattern groups, 3 date/book pairs, 21 dates, 22 book headers, 47 dot page markers
