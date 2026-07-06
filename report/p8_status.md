# P8 手工来源精修状态

- **更新时间：** 2026-07-06 21:49+ R4
- **分支：** `p8-manual-source-refinement`
- **本轮范围：** `data/review_queue.jsonl` 第 6-17 行（从 `aidicha` / 矮地茶开始，连续 12 条）

## 本轮启动检查

- 当前分支：`p8-manual-source-refinement`
- 初始 `git status --short`：工作区干净
- 初始基线：`.venv/bin/python -m pytest -q` → `38 passed`

## 前序已完成

### 高风险药材（前序轮次）

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

### review_queue 方剂前 5 条（前序轮次）

1. `baizhu_fuzi` / 白术附子汤
2. `guizhi_houpuxingzi` / 桂枝加厚朴杏子汤
3. `mahuang_lianqiao` / 麻黄连轺赤小豆汤
4. `muli_zexie` / 牡蛎泽泻散
5. `zhishi_zhizi` / 枳实栀子豉汤

## 本轮完成条目（review_queue 第 6-17 行）

6. `aidicha` / 矮地茶
   - `no_source_found`；人工读取知识文件、review_queue、herb_sources、herb_index、knowledge_completeness、p30、p36，并只读检索 FTS。
   - FTS 检索 `矮地茶 / 紫金牛 / 平地木 / 叶下红` 无命中。
   - 正文补充 no_source 边界，现有医学性内容标明待外部权威来源核验，不升级质量。
7. `anxixiang` / 安息香
   - `no_source_found`；FTS 检索 `安息香 / 拙贝罗香` 无命中。
   - 补充无内部来源边界；现有功效主治等只保留为待核验内容。
8. `aoshu` / 糯稻根
   - `no_source_found`；canonical 映射 `nuodaogenxu`，但 canonical 仍 no_source。
   - FTS 检索 `糯稻根 / 稻根 / 稻根须 / 糯稻根须` 无命中。
   - 补充 alias/canonical 与外部来源边界。
9. `aoshugen` / 糯稻根须
   - `no_source_found`；canonical 映射 `nuodaogenxu`，但 canonical 仍 no_source。
   - FTS 检索同组关键词无命中。
   - 补充 alias/canonical 与外部来源边界。
10. `baidoukou` / 白豆蔻
   - `needs_review`；候选仅为「豆蔻」别名级弱命中，`alias_match_only`。
   - 修正 frontmatter 边界；补充说明候选不能作为白豆蔻专门来源，维持 no_source。
11. `baiguo` / 白果
   - `needs_review`；内部语料 exact-name 提及白果于四神汤/肾脏积水语境。
   - 保留 `trace_status: verified` 作为可追溯提及，但新增边界说明：不支撑性味归经、功效主治等本草字段。
12. `baihuasheshecao` / 白花蛇舌草
   - `needs_review`；exact-name 提及于批评胆结石/肝炎清热药语境。
   - 保留可追溯提及，新增边界说明：不支撑本文功效、主治及“神农本草经”来源字段。
13. `banlangen` / 板蓝根
   - `needs_review`；contextual trace，水病/表证失治语境中提及并作负面评价。
   - 保留 `verified_contextual`，新增边界说明：不支撑功效主治等字段。
14. `banzhilian` / 半枝莲
   - `no_source_found`；FTS 检索「半枝莲」无命中。
   - 补充 no_source 边界；现有医学性内容待外部权威来源核验。
15. `biandou` / 白扁豆
   - `needs_review`；候选仅为「扁豆」别名级食忌线索，`alias_match_only`。
   - 修正 frontmatter 边界；补充说明不能作为白扁豆专门来源，维持 no_source。
16. `biba` / 荜澄茄
   - `no_source_found`；映射 canonical `bichengqie`，但 canonical 仍 no_source。
   - FTS 检索「荜澄茄 / 毕澄茄」无命中。
   - 补充 alias/canonical 与外部来源边界。
17. `bibo` / 荜茇
   - `no_source_found`；FTS 检索「荜茇 / 毕拨 / 荜拨」无命中。
   - 在既有边界页上补充 P8 手工复核说明。

## 本轮新增 review note

- `report/p8_manual_reviews/aidicha.md`
- `report/p8_manual_reviews/anxixiang.md`
- `report/p8_manual_reviews/aoshu.md`
- `report/p8_manual_reviews/aoshugen.md`
- `report/p8_manual_reviews/baidoukou.md`
- `report/p8_manual_reviews/baiguo.md`
- `report/p8_manual_reviews/baihuasheshecao.md`
- `report/p8_manual_reviews/banlangen.md`
- `report/p8_manual_reviews/banzhilian.md`
- `report/p8_manual_reviews/biandou.md`
- `report/p8_manual_reviews/biba.md`
- `report/p8_manual_reviews/bibo.md`

## 测试状态

- 本轮初始基线：`38 passed`
- 第 6-10 行完成后：`38 passed`
- 第 11-17 行完成后：`38 passed`
- 状态文件更新后最终复测：待运行

## Commits

前序轮次：

- `39ebfa6 refine: manually review fanxieye haima hamayou`
- `b379c90 refine: manually review huangyaozi leigongteng luhui`
- `f00b29e refine: manually review maqianzi qianjinzi qishe`
- `8be3577 refine: manually review shandougen tubiechong yadanzi yangjinhua zhechong`
- `c4cc788 refine: manually review baizhu_fuzi guizhi_houpuxingzi mahuang_lianqiao`
- `567d25e refine: manually review formulas muli_zexie zhishi_zhizi`

本轮：

- `85d0d43 refine: manually review aidicha anxixiang aoshu aoshugen baidoukou`
- `1fbda90 refine: manually review baiguo baihuasheshecao banlangen banzhilian biandou biba bibo`

## 工作边界

- 未使用脚本批量生成或批量修改知识正文；脚本仅用于只读列清单、查询索引/来源/FTS、跑测试。
- 对 `no_source_found` / `external_source_required` 条目，未从模型记忆补正文；仅补充清晰来源边界与待外部权威来源核验说明。
- 对弱候选 / contextual 候选条目，只保留可追溯提及边界，不扩大验证到功效、主治、性味归经、剂量、禁忌等字段。

## 下一条

- 若继续按 `data/review_queue.jsonl` 顺序推进，下一条为第 18 行：`bichengqie` / 荜澄茄（药材，当前原因：未检索到来源候选）。
