# P53 Middle Dot Tail Cleanup

Removed high-confidence truncated table-of-contents tails made of long middle-dot runs from active content.
Only runs of six or more middle dots were removed; ordinary single middle dots in titles and names were left unchanged.
Needs-review evidence queues outside the active JSONL registry set were left unchanged.

- Markdown files changed: 38
- JSONL files changed: 5
- Middle-dot tails removed: 174

## Markdown Changes
- `knowledge/acupoints/baihuanshu.md`: 1 middle-dot tails
- `knowledge/acupoints/bingfeng.md`: 1 middle-dot tails
- `knowledge/acupoints/daheng2.md`: 1 middle-dot tails
- `knowledge/acupoints/daimai.md`: 2 middle-dot tails
- `knowledge/acupoints/dazhong.md`: 2 middle-dot tails
- `knowledge/acupoints/fengshi.md`: 2 middle-dot tails
- `knowledge/acupoints/fuyang_bl.md`: 2 middle-dot tails
- `knowledge/acupoints/guanchong.md`: 2 middle-dot tails
- `knowledge/acupoints/guanmen.md`: 2 middle-dot tails
- `knowledge/acupoints/jianyu.md`: 2 middle-dot tails
- `knowledge/acupoints/jiquan.md`: 2 middle-dot tails
- `knowledge/acupoints/jugu.md`: 2 middle-dot tails
- `knowledge/acupoints/jutiao.md`: 1 middle-dot tails
- `knowledge/acupoints/lingtai.md`: 1 middle-dot tails
- `knowledge/acupoints/mubian.md`: 1 middle-dot tails
- `knowledge/acupoints/pucan.md`: 1 middle-dot tails
- `knowledge/acupoints/qingling.md`: 2 middle-dot tails
- `knowledge/acupoints/quanliao.md`: 1 middle-dot tails
- `knowledge/acupoints/rangu.md`: 2 middle-dot tails
- `knowledge/acupoints/shendao.md`: 1 middle-dot tails
- `knowledge/acupoints/shenzhu.md`: 1 middle-dot tails
- `knowledge/acupoints/shuiquan.md`: 2 middle-dot tails
- `knowledge/acupoints/tianjing.md`: 2 middle-dot tails
- `knowledge/acupoints/tianzhu.md`: 2 middle-dot tails
- `knowledge/acupoints/tiaokou.md`: 1 middle-dot tails
- `knowledge/acupoints/toulinqi.md`: 1 middle-dot tails
- `knowledge/acupoints/waiqiu.md`: 1 middle-dot tails
- `knowledge/acupoints/yinyu.md`: 1 middle-dot tails
- `knowledge/acupoints/yongquan.md`: 2 middle-dot tails
- `knowledge/acupoints/yuzhen.md`: 1 middle-dot tails
- `knowledge/acupoints/zhizheng.md`: 2 middle-dot tails
- `knowledge/acupoints/zhongchong.md`: 2 middle-dot tails
- `knowledge/herbs/difuzi.md`: 2 middle-dot tails
- `knowledge/herbs/huaijiao.md`: 1 middle-dot tails
- `knowledge/herbs/jiangcan.md`: 2 middle-dot tails
- `knowledge/herbs/jingjie.md`: 2 middle-dot tails
- `knowledge/herbs/manjingzi.md`: 2 middle-dot tails
- `knowledge/herbs/nvzhenzi.md`: 2 middle-dot tails

## JSONL Changes
- `data/acupoint_index.jsonl`: 21 rows, 21 middle-dot tails
- `data/acupoint_sources.jsonl`: 42 rows, 43 middle-dot tails
- `data/herb_index.jsonl`: 5 rows, 5 middle-dot tails
- `data/review_decisions.jsonl`: 19 rows, 19 middle-dot tails
- `data/verified_sources.jsonl`: 26 rows, 26 middle-dot tails
