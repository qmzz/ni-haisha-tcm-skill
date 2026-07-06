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
