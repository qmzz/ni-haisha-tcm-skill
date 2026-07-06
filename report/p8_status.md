# P8 手工来源精修状态

- **更新时间：** 2026-07-06 22:00+ 后续轮次
- **分支：** `p8-manual-source-refinement`
- **本轮范围：** `data/review_queue.jsonl` 方剂第 4-5 条（从第 4 条继续，未重复前三条）

## 本轮启动检查

- `git checkout p8-manual-source-refinement` → 已在目标分支
- 初始 `git status --short --branch` → `## p8-manual-source-refinement`，工作区干净
- 初始基线：`.venv/bin/python -m pytest -q` → `38 passed`

## 已完成高风险药材

前序轮次已完成并提交：

1. `fanxieye` / 番泻叶
2. `haima` / 海马
3. `hamayou` / 蛤蟆油
4. `huangyaozi` / 黄药子
5. `leigongteng` / 雷公藤
6. `luhui` / 芦荟
7. `maqianzi` / 马钱子
8. `qianjinzi` / 千金子
9. `qishe` / 蕲蛇
10. `shandougen` / 山豆根
11. `tubiechong` / 土鳖虫
12. `yadanzi` / 鸦胆子
13. `yangjinhua` / 洋金花
14. `zhechong` / 土鳖虫

## 已完成方剂队列

前序轮次完成 `data/review_queue.jsonl` 方剂前 3 条：

1. `baizhu_fuzi` / 白术附子汤
2. `guizhi_houpuxingzi` / 桂枝加厚朴杏子汤
3. `mahuang_lianqiao` / 麻黄连轺赤小豆汤

本轮从第 4 条继续，完成：

4. `muli_zexie` / 牡蛎泽泻散
   - 人工读取当前知识文件、`review_queue` top_source、`formula_sources`、`formula_index`，并只读检查 `source_fts.sqlite`。
   - 结论：`桂林古本伤寒杂病论 .json` exact-name quote 可支撑方名、主治“大病差后，从腰以下有水气”、组成与服法；保留当前 `verified` / `trace_status: verified`。
   - 不修改正文；现代克数、临证加减、现代应用/药理研究列为后续内容质量与剂量治理问题。
5. `zhishi_zhizi` / 枳实栀子豉汤
   - 人工读取当前知识文件、`review_queue` top_source、`formula_sources`、`formula_index`，并只读检查 `source_fts.sqlite`。
   - 结论：`桂林古本伤寒杂病论 .json` exact-name quote 可支撑方名、主治“大病差后，劳复”、组成、煎服法及宿食加大黄说明；保留当前 `verified` / `trace_status: verified`。
   - 不修改正文；现代克数、扩展主治、临证加减、现代应用/药理研究列为后续内容质量与剂量治理问题。

本轮新增 review note：

- `report/p8_manual_reviews/muli_zexie.md`
- `report/p8_manual_reviews/zhishi_zhizi.md`

## 测试状态

- 本轮初始基线：`38 passed`
- `muli_zexie zhishi_zhizi` review note 后：`38 passed`

## Commits

前序轮次：

- `39ebfa6 refine: manually review fanxieye haima hamayou`
- `b379c90 refine: manually review huangyaozi leigongteng luhui`
- `f00b29e refine: manually review maqianzi qianjinzi qishe`
- `8be3577 refine: manually review shandougen tubiechong yadanzi yangjinhua zhechong`
- `c4cc788 refine: manually review baizhu_fuzi guizhi_houpuxingzi mahuang_lianqiao`

本轮：

- `567d25e refine: manually review formulas muli_zexie zhishi_zhizi`

## 工作边界

- 未使用脚本批量生成或批量修改知识正文；脚本仅用于只读列队列、查索引/来源、检查 FTS 表、跑测试。
- 本轮只新增逐条人工 review note，没有改动方剂正文。
- 对方剂正文中的现代应用、药理研究、临证加减，未在本轮追溯到原始来源者，均未改写为 verified，仅记录为后续内容质量任务。

## 下一条

- `data/review_queue.jsonl` 中方剂条目已完成到第 5 行；只读扫描显示第 4 行以后仅有 `muli_zexie` 与 `zhishi_zhizi` 两条方剂。
- 若继续按 `review_queue` 顺序推进，下一条为第 6 行：`aidicha` / 矮地茶（药材，非方剂，当前原因：未检索到来源候选）。
