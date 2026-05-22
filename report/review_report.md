# P3 Review Queue 审核报告

> 本报告由 `scripts/build_review_report.py` 生成，用于辅助 P3 阶段处理来源复核队列。

## 总览

- 复核队列总数：**221**

### 按类型统计

| kind | count |
|------|------:|
| acupoint | 73 |
| formula | 4 |
| herb | 144 |

### 按状态统计

| status | count |
|--------|------:|
| needs_review | 33 |
| no_source_found | 188 |

### 类型 × 状态

| kind | status | count |
|------|--------|------:|
| acupoint | needs_review | 9 |
| acupoint | no_source_found | 64 |
| formula | needs_review | 4 |
| herb | needs_review | 20 |
| herb | no_source_found | 124 |

## 优先处理建议

1. 先处理 `formula:needs_review`，数量少且影响辨证辅助主链路。
2. 再处理 `herb:needs_review` 与 `acupoint:needs_review`，优先高频药材/穴位。
3. `no_source_found` 不直接补写，先走 alias / 异名匹配后再判定。

## acupoint / needs_review

| kind | id | name | status | reason |
|------|----|------|--------|--------|
| acupoint | bafeng | 八风 | needs_review | 候选来源需人工复核 |
| acupoint | baxie | 八邪 | needs_review | 候选来源需人工复核 |
| acupoint | fubai | 浮白 | needs_review | 候选来源需人工复核 |
| acupoint | jimai | 急脉 | needs_review | 候选来源需人工复核 |
| acupoint | naoshu | 臑俞 | needs_review | 候选来源需人工复核 |
| acupoint | tianfu2 | 天府二 | needs_review | 候选来源需人工复核 |
| acupoint | yixi | 譩譆 | needs_review | 候选来源需人工复核 |
| acupoint | yuanye | 渊腋 | needs_review | 候选来源需人工复核 |
| acupoint | zhongshu | 中枢 | needs_review | 候选来源需人工复核 |

## acupoint / no_source_found

| kind | id | name | status | reason |
|------|----|------|--------|--------|
| acupoint | bilao | 臂臑外 | no_source_found | 未检索到来源候选 |
| acupoint | bitong | 臂臑二 | no_source_found | 未检索到来源候选 |
| acupoint | chengfu2 | 承扶二 | no_source_found | 未检索到来源候选 |
| acupoint | chengling_gb | 承灵二 | no_source_found | 未检索到来源候选 |
| acupoint | ciliao2 | 次髎二 | no_source_found | 未检索到来源候选 |
| acupoint | dabao2 | 大包二 | no_source_found | 未检索到来源候选 |
| acupoint | daheng2 | 大横二 | no_source_found | 未检索到来源候选 |
| acupoint | dazhong_k | 大钟二 | no_source_found | 未检索到来源候选 |
| acupoint | ershenmen | 耳神门 | no_source_found | 未检索到来源候选 |
| acupoint | fengshi_gb | 风市二 | no_source_found | 未检索到来源候选 |
| acupoint | fuai2 | 腹哀二 | no_source_found | 未检索到来源候选 |
| acupoint | fujie2 | 腹结二 | no_source_found | 未检索到来源候选 |
| acupoint | fuyang2 | 跗阳二 | no_source_found | 未检索到来源候选 |
| acupoint | huagai_ren | 华盖二 | no_source_found | 未检索到来源候选 |
| acupoint | jianjing_gb | 肩井二 | no_source_found | 未检索到来源候选 |
| acupoint | jianli_ren | 建里二 | no_source_found | 未检索到来源候选 |
| acupoint | jianyu2 | 肩髃二 | no_source_found | 未检索到来源候选 |
| acupoint | jiaoxin_k | 交信二 | no_source_found | 未检索到来源候选 |
| acupoint | jiexi2 | 解溪二 | no_source_found | 未检索到来源候选 |
| acupoint | jingmen_gb | 京门二 | no_source_found | 未检索到来源候选 |
| acupoint | jiuwei_ren | 鸠尾二 | no_source_found | 未检索到来源候选 |
| acupoint | kunlun_bl | 昆仑二 | no_source_found | 未检索到来源候选 |
| acupoint | liangmen | 梁门 | no_source_found | 未检索到来源候选 |
| acupoint | liangqiu2 | 梁丘二 | no_source_found | 未检索到来源候选 |
| acupoint | lidui2 | 厉兑二 | no_source_found | 未检索到来源候选 |
| acupoint | luoshen | 络却二 | no_source_found | 未检索到来源候选 |
| acupoint | naokong_gb | 脑空二 | no_source_found | 未检索到来源候选 |
| acupoint | neiting2 | 内庭二 | no_source_found | 未检索到来源候选 |
| acupoint | qianding_du | 前顶二 | no_source_found | 未检索到来源候选 |
| acupoint | ququan_lv | 曲泉二 | no_source_found | 未检索到来源候选 |

## formula / needs_review

| kind | id | name | status | reason |
|------|----|------|--------|--------|
| formula | baizhu_fuzi | 白术附子汤 | needs_review | 候选来源需人工复核 |
| formula | guizhi_houpuxingzi | 桂枝加厚朴杏子汤 | needs_review | 候选来源需人工复核 |
| formula | mahuang_lianqiao | 麻黄连轺赤小豆汤 | needs_review | 候选来源需人工复核 |
| formula | zhishi_zhizi | 枳实栀子豉汤 | needs_review | 候选来源需人工复核 |

## herb / needs_review

| kind | id | name | status | reason |
|------|----|------|--------|--------|
| herb | baiguo | 白果 | needs_review | 候选来源需人工复核 |
| herb | baihe | 百合 | needs_review | 候选来源需人工复核 |
| herb | baihuasheshecao | 白花蛇舌草 | needs_review | 候选来源需人工复核 |
| herb | banlangen | 板蓝根 | needs_review | 候选来源需人工复核 |
| herb | chenxiang | 沉香 | needs_review | 候选来源需人工复核 |
| herb | dengxincao | 灯心草 | needs_review | 候选来源需人工复核 |
| herb | ezhu | 莪术 | needs_review | 候选来源需人工复核 |
| herb | ganlan | 橄榄 | needs_review | 候选来源需人工复核 |
| herb | haijinsha | 海金沙 | needs_review | 候选来源需人工复核 |
| herb | heshouwu | 何首乌 | needs_review | 候选来源需人工复核 |
| herb | jianghuang | 姜黄 | needs_review | 候选来源需人工复核 |
| herb | lugen | 芦根 | needs_review | 候选来源需人工复核 |
| herb | qumai | 瞿麦 | needs_review | 候选来源需人工复核 |
| herb | walengzi | 瓦楞子 | needs_review | 候选来源需人工复核 |
| herb | xiyangshen | 西洋参 | needs_review | 候选来源需人工复核 |
| herb | xuejie | 血竭 | needs_review | 候选来源需人工复核 |
| herb | xuhuang | 血竭 | needs_review | 候选来源需人工复核 |
| herb | yefujia | 夜交藤 | needs_review | 候选来源需人工复核 |
| herb | zaofan | 皂矾 | needs_review | 候选来源需人工复核 |
| herb | zhuye | 淡竹叶 | needs_review | 候选来源需人工复核 |

## herb / no_source_found

| kind | id | name | status | reason |
|------|----|------|--------|--------|
| herb | aidicha | 矮地茶 | no_source_found | 未检索到来源候选 |
| herb | anxixiang | 安息香 | no_source_found | 未检索到来源候选 |
| herb | aoshu | 糯稻根 | no_source_found | 未检索到来源候选 |
| herb | aoshugen | 糯稻根须 | no_source_found | 未检索到来源候选 |
| herb | baidoukou | 白豆蔻 | no_source_found | 未检索到来源候选 |
| herb | banzhilian | 半枝莲 | no_source_found | 未检索到来源候选 |
| herb | biandou | 白扁豆 | no_source_found | 未检索到来源候选 |
| herb | biba | 荜澄茄 | no_source_found | 未检索到来源候选 |
| herb | bibo | 荜茇 | no_source_found | 未检索到来源候选 |
| herb | bichengqie | 荜澄茄 | no_source_found | 未检索到来源候选 |
| herb | bingpian | 冰片 | no_source_found | 未检索到来源候选 |
| herb | cangerzi | 苍耳子 | no_source_found | 未检索到来源候选 |
| herb | cansha | 蚕砂 | no_source_found | 未检索到来源候选 |
| herb | caodoukou | 草豆蔻 | no_source_found | 未检索到来源候选 |
| herb | caoguo | 草果 | no_source_found | 未检索到来源候选 |
| herb | chouwutong | 臭梧桐 | no_source_found | 未检索到来源候选 |
| herb | chuanyubeimu | 川贝母 | no_source_found | 未检索到来源候选 |
| herb | chuipencao | 垂盆草 | no_source_found | 未检索到来源候选 |
| herb | chunpi | 椿皮 | no_source_found | 未检索到来源候选 |
| herb | cijili | 刺蒺藜 | no_source_found | 未检索到来源候选 |
| herb | daidaihua | 代代花 | no_source_found | 未检索到来源候选 |
| herb | daodou | 刀豆 | no_source_found | 未检索到来源候选 |
| herb | diercao | 地耳草 | no_source_found | 未检索到来源候选 |
| herb | dijincao | 地锦草 | no_source_found | 未检索到来源候选 |
| herb | fanxieye | 番泻叶 | no_source_found | 未检索到来源候选 |
| herb | feizi | 榧子 | no_source_found | 未检索到来源候选 |
| herb | foshou | 佛手 | no_source_found | 未检索到来源候选 |
| herb | gijingcao | 谷精草 | no_source_found | 未检索到来源候选 |
| herb | gouteng | 钩藤 | no_source_found | 未检索到来源候选 |
| herb | guya | 谷芽 | no_source_found | 未检索到来源候选 |
