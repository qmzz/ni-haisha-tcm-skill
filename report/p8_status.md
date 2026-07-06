# P8 手工来源精修状态

- **更新时间：** 2026-07-06 21:26+ 后续轮次
- **分支：** `p8-manual-source-refinement`
- **本轮范围：** 高风险药材队列第 7-14 条 + 方剂 review_queue 前 3 条

## 本轮启动检查

- `git branch --show-current` → `p8-manual-source-refinement`
- 初始 `git status --short` → 干净
- 初始基线：`.venv/bin/python -m pytest -q` → `38 passed`

## 已完成高风险药材

上一轮已完成并提交：

1. `fanxieye` / 番泻叶
2. `haima` / 海马
3. `hamayou` / 蛤蟆油
4. `huangyaozi` / 黄药子
5. `leigongteng` / 雷公藤
6. `luhui` / 芦荟

本轮继续完成：

7. `maqianzi` / 马钱子
8. `qianjinzi` / 千金子
9. `qishe` / 蕲蛇
10. `shandougen` / 山豆根
11. `tubiechong` / 土鳖虫
12. `yadanzi` / 鸦胆子
13. `yangjinhua` / 洋金花
14. `zhechong` / 土鳖虫

每条均已人工读取当前知识文件、`data/herb_sources.jsonl`、`data/review_queue.jsonl`、`data/herb_index.jsonl` / no-source 分类、`data/p39_high_risk_external_review_queue.jsonl`，并用 `data/source_fts.sqlite` 只读检索相关中文名/异名。

## 本轮完成方剂队列前 3 条

1. `baizhu_fuzi` / 白术附子汤
   - 对照 `review_queue` top_source、`formula_sources`、`formula_index`、当前知识文件 source_refs。
   - 结论：top_source 可直接支撑方名、条文与方后组成；仅新增 review note，不改写正文。
2. `guizhi_houpuxingzi` / 桂枝加厚朴杏子汤
   - 对照 exact-name source 与别名“桂枝加厚朴杏仁汤”命中。
   - 结论：exact-name top_source 可支撑 verified；别名仅列为后续 alias 复核线索。
3. `mahuang_lianqiao` / 麻黄连轺赤小豆汤
   - 对照 exact-name source 与“连翘/连轺”别名命中。
   - 结论：exact-name top_source 可支撑 verified；文本差异保留为后续版本/alias 复核线索。

## 测试状态

- 本轮初始基线：`38 passed`
- `maqianzi qianjinzi qishe` 后：`38 passed`
- `shandougen tubiechong yadanzi yangjinhua zhechong` 后：`38 passed`
- 方剂前 3 条 review note 后：`38 passed`

## Commits

上一轮：

- `39ebfa6 refine: manually review fanxieye haima hamayou`
- `b379c90 refine: manually review huangyaozi leigongteng luhui`

本轮：

- `f00b29e refine: manually review maqianzi qianjinzi qishe`
- `8be3577 refine: manually review shandougen tubiechong yadanzi yangjinhua zhechong`
- `c4cc788 refine: manually review baizhu_fuzi guizhi_houpuxingzi mahuang_lianqiao`

## 工作边界

- 未使用脚本批量生成或批量修改知识正文；脚本仅用于只读查询与测试。
- 高风险药材保持保守边界：无可追溯来源时保持 `no_source_found` / `external_source_required`，不补剂量、禁忌、毒性、妊娠/儿童、现代相互作用或法定状态。
- `tubiechong` / `zhechong` 检索到“地鳖虫/蛰虫/蟅虫”FTS 线索，但当前 registry 仍未绑定 source_refs，本轮不自动提升来源，仅记录待后续人工 alias/source_ref 复核。
- 方剂前 3 条本轮仅写 review note；正文中现代应用、药理研究、临证加减等未逐项追溯，建议后续内容质量任务继续处理。

## 下一条

- 若继续 `data/review_queue.jsonl` 方剂队列：下一条为第 4 条（请从 `review_queue` 第 4 行开始，避免重复 `baizhu_fuzi`、`guizhi_houpuxingzi`、`mahuang_lianqiao`）。
