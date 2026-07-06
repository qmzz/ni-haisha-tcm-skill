# P8 手工来源精修状态

- **更新时间：** 2026-07-06 22:45+ R5
- **分支：** `p8-manual-source-refinement`
- **本轮范围：** `data/review_queue.jsonl` 第 18-37 行（从 `bichengqie` / 荜澄茄到 `foshou` / 佛手；其中第 35 行 `fanxieye` 已由高风险药材前序轮次完成，本轮复核既有记录后未重复修改）

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

### review_queue 第 6-17 行（R4）

- `aidicha`, `anxixiang`, `aoshu`, `aoshugen`, `baidoukou`, `baiguo`, `baihuasheshecao`, `banlangen`, `banzhilian`, `biandou`, `biba`, `bibo`

## 本轮完成条目（review_queue 第 18-37 行）

18. `bichengqie` / 荜澄茄
   - `no_source_found`；FTS 检索「荜澄茄 / 毕澄茄」无命中。
   - `p30/p36` 标记 `alias_first`，canonical 仍 no_source；补充来源边界。
19. `bingpian` / 冰片
   - `needs_review`；候选为「龙脑」别名级命中，且位于复方/他药语境。
   - FTS 未见「冰片」专名；移除正文中误落在 frontmatter 后的 no_source 元数据文本，并补充 alias/contextual 边界。
20. `cangerzi` / 苍耳子
   - `no_source_found`；FTS 检索无命中。
   - 对既有“倪师讲解”加未验证提示，补充 no_source 边界。
21. `cansha` / 蚕砂
   - `no_source_found`；FTS 检索无命中；补充外部权威来源核验边界。
22. `caodoukou` / 草豆蔻
   - `no_source_found`；FTS 检索「草豆蔻 / 草蔻」无命中；补充外部权威来源核验边界。
23. `caoguo` / 草果
   - `no_source_found`；FTS 检索无命中；补充外部权威来源核验边界。
24. `chouwutong` / 臭梧桐
   - `no_source_found`；FTS 检索无命中；`p36` 为 `herb_modern_or_regional`；补充边界。
25. `chuanyubeimu` / 川贝母
   - `no_source_found`；扩展命中为「贝母」通名，不等同「川贝母」专名。
   - 保持 no_source，不以通名命中验证川贝母功效主治等字段。
26. `chuipencao` / 垂盆草
   - `no_source_found`；FTS 检索无命中；`p36` 为 `herb_modern_or_regional`；补充边界。
27. `chunpi` / 椿皮
   - `no_source_found`；FTS 检索无命中；`p30/p36` 为 `internal_research_exhausted`；补充边界。
28. `cijili` / 刺蒺藜
   - `no_source_found`；FTS 无「刺蒺藜」专名，仅有「蒺藜/蒺藜子/白蒺藜」通名或近缘语境。
   - 不以通名命中验证专名条目，补充边界。
29. `daidaihua` / 代代花
   - `no_source_found`；FTS 检索无命中；补充外部权威来源核验边界。
30. `daodou` / 刀豆
   - `no_source_found`；FTS 检索无命中；`p30/p36` 为 `internal_research_exhausted`；补充边界。
31. `dengxincao` / 灯心草
   - `needs_review`；候选为分消汤/医案加味语境中的可追溯提及。
   - 保留既有 verified/contextual，但明确不验证性味、归经、功效、主治、剂量、禁忌等本草字段。
32. `diercao` / 地耳草
   - `no_source_found`；FTS 检索无命中；`p36` 为 `herb_modern_or_regional`；补充边界。
33. `dijincao` / 地锦草
   - `no_source_found`；FTS 检索无命中；`p36` 为 `herb_modern_or_regional`；补充边界。
34. `ezhu` / 莪术
   - `needs_review`；exact-name 提及存在，语境为三棱莪术破血力量较强及妇科/攻坚用药讨论。
   - 保留可追溯提及，不扩展验证到“神农本草经”来源、性味、归经、功效、主治等全部字段。
35. `fanxieye` / 番泻叶
   - 已在高风险药材前序轮次完成；本轮复核既有 `report/p8_manual_reviews/fanxieye.md` 与边界，无重复修改。
36. `feizi` / 榧子
   - `no_source_found`；FTS 检索无命中；补充外部权威来源核验边界。
37. `foshou` / 佛手
   - `no_source_found`；FTS 检索无命中；补充外部权威来源核验边界。

## 本轮新增 review note

- `report/p8_manual_reviews/bichengqie.md`
- `report/p8_manual_reviews/bingpian.md`
- `report/p8_manual_reviews/cangerzi.md`
- `report/p8_manual_reviews/cansha.md`
- `report/p8_manual_reviews/caodoukou.md`
- `report/p8_manual_reviews/caoguo.md`
- `report/p8_manual_reviews/chouwutong.md`
- `report/p8_manual_reviews/chuanyubeimu.md`
- `report/p8_manual_reviews/chuipencao.md`
- `report/p8_manual_reviews/chunpi.md`
- `report/p8_manual_reviews/cijili.md`
- `report/p8_manual_reviews/daidaihua.md`
- `report/p8_manual_reviews/daodou.md`
- `report/p8_manual_reviews/dengxincao.md`
- `report/p8_manual_reviews/diercao.md`
- `report/p8_manual_reviews/dijincao.md`
- `report/p8_manual_reviews/ezhu.md`
- `report/p8_manual_reviews/feizi.md`
- `report/p8_manual_reviews/foshou.md`

## 测试状态

- 本轮初始基线：`38 passed`
- 第 18-29 行处理后：`38 passed`
- 第 30-37 行处理后：`38 passed`
- 每批提交后复测：`38 passed`
- 状态文件更新后最终复测：待运行

## Commits

前序轮次：

- `39ebfa6 refine: manually review fanxieye haima hamayou`
- `b379c90 refine: manually review huangyaozi leigongteng luhui`
- `f00b29e refine: manually review maqianzi qianjinzi qishe`
- `8be3577 refine: manually review shandougen tubiechong yadanzi yangjinhua zhechong`
- `c4cc788 refine: manually review baizhu_fuzi guizhi_houpuxingzi mahuang_lianqiao`
- `567d25e refine: manually review formulas muli_zexie zhishi_zhizi`
- `85d0d43 refine: manually review aidicha anxixiang aoshu aoshugen baidoukou`
- `1fbda90 refine: manually review baiguo baihuasheshecao banlangen banzhilian biandou biba bibo`

本轮：

- `0636b41 refine: manually review bichengqie bingpian cangerzi cansha caodoukou caoguo`
- `5ef663e refine: manually review chouwutong chuanyubeimu chuipencao chunpi cijili daidaihua`
- `db59c35 refine: manually review daodou dengxincao diercao dijincao ezhu feizi foshou`

## 工作边界

- 未使用脚本批量生成或批量修改知识正文；脚本仅用于只读列清单、查询索引/来源/FTS、生成同构 review note 草稿与跑测试，正文改动逐条保守完成。
- 对 `no_source_found` / `external_source_required` 条目，未从模型记忆补正文；仅补充清晰来源边界与待外部权威来源核验说明。
- 对弱候选 / contextual 候选条目，只保留可追溯提及边界，不扩大验证到功效、主治、性味归经、剂量、禁忌等字段。

## 下一条

- 若继续按 `data/review_queue.jsonl` 顺序推进，下一条为第 38 行：`ganlan` / 橄榄（药材，当前原因：`quality_score_below_verified_threshold`，候选疑似 football“橄榄球”误命中）。
