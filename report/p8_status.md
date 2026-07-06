# P8 手工来源精修状态

- **更新时间：** 2026-07-06 23:10+ R6
- **分支：** `p8-manual-source-refinement`
- **本轮范围：** `data/review_queue.jsonl` 第 38-60 行（从 `ganlan` / 橄榄到 `jianghuang` / 姜黄；其中第 46 `haima`、第 48 `hamayou`、第 55 `huangyaozi` 已由高风险轮次完成，本轮只复核记录，未重复修改知识正文）

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

### review_queue 第 18-37 行（R5）

- `bichengqie`, `bingpian`, `cangerzi`, `cansha`, `caodoukou`, `caoguo`, `chouwutong`, `chuanyubeimu`, `chuipencao`, `chunpi`, `cijili`, `daidaihua`, `daodou`, `dengxincao`, `diercao`, `dijincao`, `ezhu`, `fanxieye`（跳过重复改动）, `feizi`, `foshou`

## 本轮完成条目（review_queue 第 38-60 行）

38. `ganlan` / 橄榄
   - `needs_review`；review_queue top_source 为 football/橄榄球语境，判定为误命中，不作为药材来源。
   - source LIKE 另见“橄榄油”作为蒲灰散黏合用油语境，且原文明确“这些油本身没有功能”；只记录语境边界，不补药材正文。
39. `gijingcao` / 谷精草
   - `no_source_found`；FTS/LIKE 无命中；`p30/p36` 为 `external_source_required`；补充 P8 外部权威来源边界。
40. `gouteng` / 钩藤
   - `no_source_found`；FTS/LIKE 无命中；`p30/p36` 为 `external_source_required`；补充边界。
41. `guya` / 谷芽
   - `no_source_found`；FTS/LIKE 无命中；`p30/p36` 为 `external_source_required`；补充边界。
42. `haifengteng` / 海风藤
   - `no_source_found`；FTS/LIKE 无命中；补充边界。
43. `haifushi` / 海浮石
   - `no_source_found`；FTS/LIKE 无命中；补充边界。
44. `haigeqiao` / 海蛤壳
   - `no_source_found`；FTS/LIKE 无命中；补充边界。
45. `haijinsha` / 海金沙
   - `needs_review`；FTS/LIKE 检出多处四逆散加滑石、五倍子、海金沙治胆结石语境。
   - 仅证明倪师语料提及“海金沙”，不自动验证性味、归经、功效、主治等全部本草字段；本轮写 review note，不改正文。
46. `haima` / 海马
   - 已在高风险药材前序轮次完成；本轮复核既有边界，只更新 review note 记录“跳过重复改动”，未改知识正文。
47. `haitongpi` / 海桐皮
   - `no_source_found`；FTS/LIKE 无命中；补充边界。
48. `hamayou` / 哈蟆油
   - 已在高风险药材前序轮次完成；本轮复核既有边界，只更新 review note 记录“跳过重复改动”，未改知识正文。
49. `hechezi` / 黑芝麻
   - `no_source_found`；`p30/p36` 为 alias/duplicate mapped，canonical=`heizhima`；FTS/LIKE 无命中；补充别名/重复映射边界。
50. `heizhima` / 黑芝麻
   - `no_source_found`；canonical 候选仍无内部可追溯来源；补充规范条目候选边界。
51. `hesi` / 鹤虱
   - `no_source_found`；`p30` 为 `internal_research_exhausted`，canonical=`hesi`；FTS/LIKE 无命中；补充边界。
52. `hetaoren` / 核桃仁
   - `no_source_found`；FTS/LIKE 无命中；补充边界。
53. `hezi` / 鹤虱
   - `no_source_found`；别名/重复映射到 `hesi`；FTS/LIKE 无命中；补充边界。
54. `hongteng` / 红藤
   - `no_source_found`；FTS/LIKE 无命中；补充边界。
55. `huangyaozi` / 黄药子
   - 已在高风险药材前序轮次完成；本轮复核既有边界，只更新 review note 记录“跳过重复改动”，未改知识正文。
56. `huazuirushi` / 花蕊石
   - `no_source_found`；FTS/LIKE 无命中；补充边界。
57. `hugulu` / 胡芦巴
   - `no_source_found`；FTS/LIKE 无命中；补充边界。
58. `huoxiang` / 广藿香
   - `no_source_found`；FTS/LIKE 无命中；既有“倪师讲解”未由内部语料复核证实，补充待核验边界。
59. `huzhang` / 虎杖
   - `no_source_found`；FTS/LIKE 无命中；补充边界。
60. `jianghuang` / 姜黄
   - `needs_review`；候选为“干姜黄芩黄连人参汤”跨词误切（干姜 + 黄芩），不是药材姜黄。
   - FTS/LIKE 命中均属方名语境；本轮写 review note 记录误命中，不改正文。

## 本轮新增 / 确认 review note

- `report/p8_manual_reviews/ganlan.md`
- `report/p8_manual_reviews/gijingcao.md`
- `report/p8_manual_reviews/gouteng.md`
- `report/p8_manual_reviews/guya.md`
- `report/p8_manual_reviews/haifengteng.md`
- `report/p8_manual_reviews/haifushi.md`
- `report/p8_manual_reviews/haigeqiao.md`
- `report/p8_manual_reviews/haijinsha.md`
- `report/p8_manual_reviews/haima.md`（高风险前序完成，本轮复核跳过）
- `report/p8_manual_reviews/haitongpi.md`
- `report/p8_manual_reviews/hamayou.md`（高风险前序完成，本轮复核跳过）
- `report/p8_manual_reviews/hechezi.md`
- `report/p8_manual_reviews/heizhima.md`
- `report/p8_manual_reviews/hesi.md`
- `report/p8_manual_reviews/hetaoren.md`
- `report/p8_manual_reviews/hezi.md`
- `report/p8_manual_reviews/hongteng.md`
- `report/p8_manual_reviews/huangyaozi.md`（高风险前序完成，本轮复核跳过）
- `report/p8_manual_reviews/huazuirushi.md`
- `report/p8_manual_reviews/hugulu.md`
- `report/p8_manual_reviews/huoxiang.md`
- `report/p8_manual_reviews/huzhang.md`
- `report/p8_manual_reviews/jianghuang.md`

## 测试状态

- 本轮初始基线：`38 passed`
- 第 39-44 行知识边界处理后：`38 passed`
- 第 47、49-53 行知识边界处理后：`38 passed`
- 第 54、56-59 行知识边界处理后：`38 passed`
- review note 与状态文件更新后最终复测：`38 passed`

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
- `0636b41 refine: manually review bichengqie bingpian cangerzi cansha caodoukou caoguo`
- `5ef663e refine: manually review chouwutong chuanyubeimu chuipencao chunpi cijili daidaihua`
- `db59c35 refine: manually review daodou dengxincao diercao dijincao ezhu feizi foshou`

本轮：

- `c269eac docs(p8): review no-source herb boundaries g-haigeqiao`
- `55d2687 docs(p8): review alias and no-source herb boundaries h`
- `4d34272 docs(p8): review hu-series no-source boundaries`
- `3b4de45 docs(p8): add R6 manual review notes and status`

## 工作边界

- 正文编辑逐条保守完成；脚本仅用于只读列清单、查询索引/来源/FTS、生成 review note 草稿与跑测试。
- 对 `no_source_found` / `external_source_required` 条目，未从模型记忆补正文；仅补充清晰来源边界与待外部权威来源核验说明。
- 对 football“橄榄球”、方名跨词“干姜黄芩”等误命中，明确降级为误命中/不可验证。
- 对弱候选 / contextual 候选条目，只保留可追溯提及边界，不扩大验证到功效、主治、性味归经、剂量、禁忌等字段。

## 下一条

- 若继续按 `data/review_queue.jsonl` 顺序推进，下一条为第 61 行。需先读取 `data/review_queue.jsonl` 第 61 行确认条目后再处理。

---

# R7 更新（2026-07-06 23:40+）

- **分支：** `p8-manual-source-refinement`
- **本轮范围：** `data/review_queue.jsonl` 第 61-85 行（从 `jiangxiang` / 降香 到 `muhudie` / 木蝴蝶；其中第 69 `leigongteng`、第 74 `luhui`、第 82 `maqianzi` 已由高风险轮次完成，本轮只复核记录，未重复修改知识正文）

## R7 启动检查

- 当前分支：`p8-manual-source-refinement`
- 初始 `git status --short`：工作区干净
- 初始基线：`.venv/bin/python -m pytest -q` → `38 passed`

## R7 完成条目（review_queue 第 61-85 行）

61. `jiangxiang` / 降香
   - `no_source_found`；FTS/LIKE 无命中；p30/p36 为 `external_source_required`；补充 P8 外部权威来源边界。
62. `jiguanhua` / 鸡冠花
   - `no_source_found`；FTS/LIKE 无命中；补充外部权威来源边界。
63. `jinguolan` / 金果榄
   - `no_source_found`；FTS/LIKE 无命中；p7b 为 modern/regional；补充外部来源边界。
64. `jinqiancao` / 金钱草
   - `no_source_found`；FTS/LIKE 无命中；补充边界。
65. `jiucaizi` / 韭菜子
   - `no_source_found`；FTS/LIKE 无命中；补充边界。
66. `jixueteng` / 鸡血藤
   - `no_source_found`；FTS/LIKE 无命中；p7b 为 modern/regional；补充边界。
67. `laifuzi` / 莱菔子
   - `no_source_found`；FTS/LIKE 对“莱菔子/萝卜子”均无命中；补充边界。
68. `laoguancao` / 老鹳草
   - `no_source_found`；FTS/LIKE 无命中；补充边界。
69. `leigongteng` / 雷公藤
   - 已在高风险药材前序轮次完成；本轮复核 FTS/LIKE 无命中及高风险边界，只更新 review note，未改正文。
70. `lianxu` / 莲须
   - `no_source_found`；FTS/LIKE 无命中；补充边界。
71. `liujinu` / 刘寄奴
   - `no_source_found`；FTS/LIKE 无命中；补充边界。
72. `lizhihe` / 荔枝核
   - `no_source_found`；p30 为 `internal_research_exhausted`；FTS/LIKE 无命中；补充内部复查耗尽/外部来源边界。
73. `lugen` / 芦根
   - `needs_review`；《金匮要略》食禁/食物中毒语境 2 处提及“芦根煮汁/煮芦根汁饮之”。
   - 仅证明特定语境提及，不扩展为性味、归经、通用功效、主治、剂量或禁忌全字段验证；本轮只写 review note，不改正文。
74. `luhui` / 芦荟
   - 已在高风险药材前序轮次完成；本轮复核 P6-C `internal_research_exhausted`、FTS/LIKE 无命中及高风险边界，只更新 review note，未改正文。
75. `lulutong` / 路路通
   - `no_source_found`；FTS/LIKE 对“路路通/枫香果”均无命中；补充边界。
76. `luobuma` / 罗布麻叶
   - `no_source_found`；别名/重复映射到 canonical=`luobumaye`，规范条目仍无内部来源；补充别名映射边界。
77. `luobumaye` / 罗布麻叶
   - `no_source_found`；FTS/LIKE 无命中；补充规范条目边界。
78. `luohanguo` / 罗汉果
   - `no_source_found`；FTS/LIKE 无命中；p7b 为 modern/regional；补充边界。
79. `lvtuomei` / 绿萼梅
   - `no_source_found`；FTS/LIKE 无命中；补充边界。
80. `mabo` / 马勃
   - `no_source_found`；FTS/LIKE 无命中；p7b 为 modern/regional；补充边界。
81. `machixian` / 马齿苋
   - `no_source_found`；FTS/LIKE 对“马齿苋/马齿草”均无命中；补充边界。
82. `maqianzi` / 马钱子
   - 已在高风险药材前序轮次完成；本轮复核 FTS/LIKE 无命中及高风险边界，只更新 review note，未改正文。
83. `menghua` / 密蒙花
   - `no_source_found`；FTS/LIKE 无命中；补充边界。
84. `mohantian` / 墨旱莲
   - `no_source_found`；FTS/LIKE 无命中；p7b 为 modern/regional；补充边界。
85. `muhudie` / 木蝴蝶
   - `no_source_found`；FTS/LIKE 无命中；补充边界。

## R7 新增 / 更新 review note

- `report/p8_manual_reviews/jiangxiang.md`
- `report/p8_manual_reviews/jiguanhua.md`
- `report/p8_manual_reviews/jinguolan.md`
- `report/p8_manual_reviews/jinqiancao.md`
- `report/p8_manual_reviews/jiucaizi.md`
- `report/p8_manual_reviews/jixueteng.md`
- `report/p8_manual_reviews/laifuzi.md`
- `report/p8_manual_reviews/laoguancao.md`
- `report/p8_manual_reviews/leigongteng.md`（高风险前序完成，本轮复核跳过正文）
- `report/p8_manual_reviews/lianxu.md`
- `report/p8_manual_reviews/liujinu.md`
- `report/p8_manual_reviews/lizhihe.md`
- `report/p8_manual_reviews/lugen.md`
- `report/p8_manual_reviews/luhui.md`（高风险前序完成，本轮复核跳过正文）
- `report/p8_manual_reviews/lulutong.md`
- `report/p8_manual_reviews/luobuma.md`
- `report/p8_manual_reviews/luobumaye.md`
- `report/p8_manual_reviews/luohanguo.md`
- `report/p8_manual_reviews/lvtuomei.md`
- `report/p8_manual_reviews/mabo.md`
- `report/p8_manual_reviews/machixian.md`
- `report/p8_manual_reviews/maqianzi.md`（高风险前序完成，本轮复核跳过正文）
- `report/p8_manual_reviews/menghua.md`
- `report/p8_manual_reviews/mohantian.md`
- `report/p8_manual_reviews/muhudie.md`

## R7 测试状态

- 本轮初始基线：`38 passed`
- 第 61-68 行知识边界处理后：`38 passed`
- 第 69-85 行知识边界 / review note 处理后：`38 passed`
- 状态文件更新后最终复测：待本段提交前执行

## R7 Commits

- `f533cf3 docs(p8): review j-l no-source herb boundaries`
- `c4e3d2d docs(p8): review l-m herb source boundaries`
- 状态文件最终提交：待提交

## R7 工作边界

- 正文编辑逐条保守完成；脚本仅用于只读列清单、查询索引/来源/FTS、生成 review note 草稿与跑测试。
- 对 `no_source_found` / `external_source_required` / `internal_research_exhausted` 条目，未从模型记忆补正文；仅补充清晰来源边界与待外部权威来源核验说明。
- 对 `lugen` 这类弱候选 / contextual 候选，只保留可追溯提及边界，不扩大验证到功效、主治、性味归经、剂量、禁忌等字段。
- 对前序高风险已处理条目，只复核并更新 review note，不重复改正文。

## 下一条

- 若继续按 `data/review_queue.jsonl` 顺序推进，下一条为第 86 行 `mujinpi` / 木槿皮。

---

# R8 更新（2026-07-06 22:44+）

- **分支：** `p8-manual-source-refinement`
- **本轮范围：** `data/review_queue.jsonl` 第 86-115 行（从 `mujinpi` / 木槿皮 到 `xiangyuan` / 香橼；其中第 92 `qianjinzi`、第 95 `qishe`、第 100 `shandougen`、第 112 `tubiechong` 已由高风险轮次完成，本轮只复核记录，未重复修改知识正文）

## R8 启动检查

- 当前分支：`p8-manual-source-refinement`
- 初始 `git status --short`：工作区干净
- 初始基线：`.venv/bin/python -m pytest -q` → `38 passed`

## R8 完成条目（review_queue 第 86-115 行）

86. `mujinpi` / 木槿皮：`no_source_found`；FTS/LIKE 无命中；补充 P8 外部权威来源边界。
87. `niubangzi` / 牛蒡子：`no_source_found`；FTS/LIKE 无命中；补充边界。
88. `nuodaogenxu` / 糯稻根须：`no_source_found`；canonical=`nuodaogenxu`，p36 为 alias-first；补充 canonical/alias 边界。
89. `oujie` / 藕节：`no_source_found`；FTS/LIKE 无命中；补充边界。
90. `poshi` / 娑罗子：`no_source_found`；FTS/LIKE 无命中；补充边界。
91. `pugongying` / 蒲公英：`no_source_found`；p30 为 `internal_research_exhausted`；补充内部复查耗尽/外部来源边界。
92. `qianjinzi` / 千金子：高风险前序已完成；本轮复核 `herb_sources`、p30/p36 与 FTS/LIKE 无命中，只追加 review note 补记，未重复改正文。
93. `qiannianjian` / 千年健：`no_source_found`；FTS/LIKE 无命中；补充边界。
94. `qianniuzi` / 牵牛子：`no_source_found`；FTS/LIKE 无命中；补充边界。
95. `qishe` / 蕲蛇：高风险前序已完成；本轮复核无命中及高风险边界，只追加 review note 补记，未重复改正文。
96. `roudoukou` / 肉豆蔻：`no_source_found`；FTS/LIKE 无命中；补充边界。
97. `sangshen` / 桑葚：`no_source_found`；FTS/LIKE 无命中；补充边界。
98. `sangye` / 桑叶：`no_source_found`；FTS/LIKE 无命中；补充边界。
99. `shandou` / 谷芽：`no_source_found`；p30 canonical=`guya`；补充别名/重复映射边界，不升级验证。
100. `shandougen` / 山豆根：高风险前序已完成；本轮复核无命中及高风险边界，只追加 review note 补记，未重复改正文。
101. `shanzha` / 山楂：`no_source_found`；既有“倪师讲解”等医学字段未由本轮内部语料复核证实；补充待核验边界。
102. `shayuanzi` / 沙苑子：`no_source_found`；FTS/LIKE 无命中；补充边界。
103. `shidi` / 柿蒂：`no_source_found`；FTS/LIKE 无命中；补充边界。
104. `shiliupi` / 石榴皮：`no_source_found`；FTS/LIKE 无命中；补充边界。
105. `shouwuteng` / 首乌藤：`no_source_found`；FTS/LIKE 无命中；补充边界。
106. `suhexiang` / 苏合香：`no_source_found`；FTS/LIKE 无命中；补充边界。
107. `sumu` / 苏木：`no_source_found`；与 `suomu` 重复/别名线索；补充边界，不合并、不升级验证。
108. `suomu` / 苏木：`no_source_found`；与 `sumu` 重复/别名线索；补充边界，不合并、不升级验证。
109. `taizishen` / 太子参：`no_source_found`；FTS/LIKE 无命中；补充边界。
110. `tanxiang` / 檀香：`no_source_found`；既有“神农本草经 + 倪海厦人纪系列”等来源/医学字段未由本轮内部语料复核证实；补充待核验边界。
111. `tianzhuhuang` / 天竺黄：`no_source_found`；FTS/LIKE 无命中；补充边界。
112. `tubiechong` / 土鳖虫：高风险前序已完成；本轮复核无命中及异名线索边界，只追加 review note 补记，未重复改正文。
113. `tujingpi` / 土荆皮：`no_source_found`；FTS/LIKE 无命中；补充边界。
114. `walengzi` / 瓦楞子：`needs_review`；FTS/LIKE 可检出倪师语料多处上下文提及，知识文件已有 source_refs 与摘录；本轮只写 review note，保留“提及不等于全字段验证”边界，未改正文。
115. `xiangyuan` / 香橼：`no_source_found`；FTS/LIKE 无命中；补充边界。

## R8 新增 / 更新 review note

- `report/p8_manual_reviews/mujinpi.md`
- `report/p8_manual_reviews/niubangzi.md`
- `report/p8_manual_reviews/nuodaogenxu.md`
- `report/p8_manual_reviews/oujie.md`
- `report/p8_manual_reviews/poshi.md`
- `report/p8_manual_reviews/pugongying.md`
- `report/p8_manual_reviews/qianjinzi.md`（高风险前序完成，本轮复核跳过正文）
- `report/p8_manual_reviews/qiannianjian.md`
- `report/p8_manual_reviews/qianniuzi.md`
- `report/p8_manual_reviews/qishe.md`（高风险前序完成，本轮复核跳过正文）
- `report/p8_manual_reviews/roudoukou.md`
- `report/p8_manual_reviews/sangshen.md`
- `report/p8_manual_reviews/sangye.md`
- `report/p8_manual_reviews/shandou.md`
- `report/p8_manual_reviews/shandougen.md`（高风险前序完成，本轮复核跳过正文）
- `report/p8_manual_reviews/shanzha.md`
- `report/p8_manual_reviews/shayuanzi.md`
- `report/p8_manual_reviews/shidi.md`
- `report/p8_manual_reviews/shiliupi.md`
- `report/p8_manual_reviews/shouwuteng.md`
- `report/p8_manual_reviews/suhexiang.md`
- `report/p8_manual_reviews/sumu.md`
- `report/p8_manual_reviews/suomu.md`
- `report/p8_manual_reviews/taizishen.md`
- `report/p8_manual_reviews/tanxiang.md`
- `report/p8_manual_reviews/tianzhuhuang.md`
- `report/p8_manual_reviews/tubiechong.md`（高风险前序完成，本轮复核跳过正文）
- `report/p8_manual_reviews/tujingpi.md`
- `report/p8_manual_reviews/walengzi.md`
- `report/p8_manual_reviews/xiangyuan.md`

## R8 测试状态

- 本轮初始基线：`38 passed`
- 第 86-91 行处理后：`38 passed`
- 第 92-98 行处理后：`38 passed`
- 第 99-105 行处理后：`38 passed`
- 第 106-112 行处理后：`38 passed`
- 第 113-115 行处理后：`38 passed`
- 状态文件更新后最终复测：待本段提交前执行

## R8 Commits

- `fa7defc P8 manual review herbs 86-91`
- `7507771 P8 manual review herbs 92-98`（已因覆盖既有高风险 note 而回滚）
- `b7ea8d9 Revert "P8 manual review herbs 92-98"`
- `e080bfd P8 manual review herbs 92-98`
- `6065c24 P8 manual review herbs 99-105`
- `569a4a1 P8 manual review herbs 106-112`
- `1a69a08 P8 manual review herbs 113-115`
- 状态文件最终提交：待提交

## R8 工作边界

- 正文编辑逐条保守完成；脚本仅用于只读列清单、查询索引/来源/FTS、生成 review note 草稿与跑测试。
- 对 `no_source_found` / `external_source_required` / `internal_research_exhausted` 条目，未从模型记忆补正文；仅补充来源边界与待外部权威来源核验说明。
- 对 `walengzi` 这类 `needs_review` / contextual 候选，只保留可追溯提及边界，不扩大验证到性味、归经、功效、主治、剂量、禁忌等字段。
- 对前序高风险已处理条目，只复核并更新 review note，不重复改正文。
- 对 `shandou`/`guya`、`sumu`/`suomu` 等别名或重复映射线索，只标注 canonical/alias 边界，不合并条目、不升级验证。

## 下一条

- 若继续按 `data/review_queue.jsonl` 顺序推进，下一条为第 116 行。需先读取 `data/review_queue.jsonl` 第 116 行确认条目后再处理。

---

# R9-redo 更新（2026-07-06 23:21+）

- **分支：** `p8-manual-source-refinement`
- **本轮范围：** `data/review_queue.jsonl` 第 116-125 行（`xianhecao` / 仙鹤草 到 `xungufeng` / 寻骨风）
- **R9-redo 原则：** 上轮 R9 dirty diff 已隔离回滚；本轮未复用 dirty diff，逐条读取知识正文、review_queue、herb_sources/herb_index/knowledge_completeness/p30/p36（verified 条目 p30/p36 无对应 no-source 记录时已在 note 说明），并只读查询 `source_fts.sqlite`。

## R9-redo 启动检查

- 当前分支：`p8-manual-source-refinement`
- 初始基线：`.venv/bin/python -m pytest -q` → `38 passed`

## R9-redo 完成条目（review_queue 第 116-125 行）

116. `xianhecao` / 仙鹤草
   - `no_source_found`；FTS/LIKE 无命中；p30/p36 为 `external_source_required`；只写 review note，未改正文。
117. `xianmao` / 仙茅
   - `no_source_found`；FTS/LIKE 无命中；p30/p36 为 `external_source_required`；只写 review note，未改正文。
118. `xiecao` / 缬草
   - `no_source_found`；FTS/LIKE 无命中；p30/p36 为 `external_source_required`；只写 review note，未改正文。
119. `xihonghua` / 西红花
   - `no_source_found`；FTS/LIKE 无命中；p30/p36 为 `external_source_required`；只写 review note，未改正文。
120. `xiqiancao` / 豨莶草
   - `no_source_found`；FTS/LIKE 无命中；p30/p36 为 `external_source_required`；只写 review note，未改正文。
121. `xiyangshen` / 西洋参
   - `needs_review` in queue but already verified in registry；FTS 0、LIKE 2（05 金匮 pages 475/476）；保留现有 verified trace boundary，未补结构字段、未改正文。
122. `xuejie` / 血竭
   - `needs_review` in queue but already verified in registry；FTS 0、LIKE 2（05 金匮 page 257、伤寒论 page 152）；记录伤科/破瘀语境边界，未改正文。
123. `xuelianhua` / 雪莲花
   - `no_source_found`；FTS/LIKE 无命中；p30/p36 为 `external_source_required`；只写 review note，未改正文。
124. `xuhuang` / 血竭
   - `needs_review` in queue but already verified in registry；与 `xuejie` 为 duplicate/alias 血竭条目；FTS/LIKE for `血竭` 同上，romanized `xuhuang`/`xuejie` 无命中；只记录 canonicalization follow-up，未改正文/registry。
125. `xungufeng` / 寻骨风
   - `no_source_found`；FTS/LIKE 无命中；p30/p36 为 `external_source_required`；只写 review note，未改正文。

## R9-redo 新增 review note

- `report/p8_manual_reviews/xianhecao.md`
- `report/p8_manual_reviews/xianmao.md`
- `report/p8_manual_reviews/xiecao.md`
- `report/p8_manual_reviews/xihonghua.md`
- `report/p8_manual_reviews/xiqiancao.md`
- `report/p8_manual_reviews/xiyangshen.md`
- `report/p8_manual_reviews/xuejie.md`
- `report/p8_manual_reviews/xuelianhua.md`
- `report/p8_manual_reviews/xuhuang.md`
- `report/p8_manual_reviews/xungufeng.md`

## R9-redo 测试状态

- 启动基线：`38 passed`
- 第 116-120 行完成后：`38 passed`
- 第 121-125 行与状态文件完成后最终复测：`38 passed`

## R9-redo follow-up

- `xuejie` 与 `xuhuang` 均为 血竭，且互设 aliases；建议后续单独做 canonical item ID/registry 字段一致性清理，不在本轮批量改 registry。
- `xuejie` frontmatter/index 中存在结构字段串联污染（性味/归经/功效/主治拼接），建议后续数据质量专项处理。

## 下一条

- 下一条为 `data/review_queue.jsonl` 第 126 行；继续前需先读取该行确认条目。
