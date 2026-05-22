# P6-C no_source_found 专项治理报告

## 治理原则

- `no_source_found` 不自动提升为 verified。
- alias / FTS / 同义线索只进入候选与人工复核，不作为医学真实性判定。
- 找不到明确来源时保持待考，不凭模型记忆补写。

## 当前队列概览

- review_queue 总数：218
- 已有决策条目：117
- 未决队列：217
- 未决 no_source_found：184
- 未决 needs_review：33

### 未决 no_source_found 类型分布

- acupoint: 64
- herb: 120

## alias 候选线索

当前 no_source_found 中带 alias candidate 的条目数：4

| kind | item_id | name | alias_candidates |
|------|---------|------|------------------|
| herb | haitongpi | 海桐皮 | 刺桐皮 |
| herb | zhangnao | 樟脑 | 韶脑 |
| herb | zihuadiding | 紫花地丁 | 地丁 |
| acupoint | sishencong | 四神聪 | 四神聪穴 |

## 优先处理建议

1. 先处理 `needs_review`：多数已有候选来源，复核成本低于 no_source_found。
2. 对 herb no_source_found 做同名异写、简繁、古今名二次 alias 整理。
3. 对 acupoint no_source_found 优先补经穴编号 / 别名 / 经络归属，再重建来源索引。
4. 仍无来源者保留 `no_source_found`，不要降格自动写入正文。

## 未决样例（前 80 条）

| kind | status | item_id | name | reason |
|------|--------|---------|------|--------|
| formula | needs_review | baizhu_fuzi | 白术附子汤 | 候选来源需人工复核 |
| formula | needs_review | mahuang_lianqiao | 麻黄连轺赤小豆汤 | 候选来源需人工复核 |
| formula | needs_review | muli_zexie | 牡蛎泽泻散 | 候选来源需人工复核 |
| formula | needs_review | zhishi_zhizi | 枳实栀子豉汤 | 候选来源需人工复核 |
| herb | no_source_found | aidicha | 矮地茶 | 未检索到来源候选 |
| herb | no_source_found | anxixiang | 安息香 | 未检索到来源候选 |
| herb | no_source_found | aoshu | 糯稻根 | 未检索到来源候选 |
| herb | no_source_found | aoshugen | 糯稻根须 | 未检索到来源候选 |
| herb | needs_review | baidoukou | 白豆蔻 | alias_match_only；alias_requires_review |
| herb | needs_review | baiguo | 白果 | quality_score_below_verified_threshold |
| herb | needs_review | baihuasheshecao | 白花蛇舌草 | quality_score_below_verified_threshold |
| herb | needs_review | banlangen | 板蓝根 | quality_score_below_verified_threshold |
| herb | no_source_found | banzhilian | 半枝莲 | 未检索到来源候选 |
| herb | needs_review | biandou | 白扁豆 | alias_match_only；alias_requires_review |
| herb | no_source_found | biba | 荜澄茄 | 未检索到来源候选 |
| herb | no_source_found | bibo | 荜茇 | 未检索到来源候选 |
| herb | no_source_found | bichengqie | 荜澄茄 | 未检索到来源候选 |
| herb | needs_review | bingpian | 冰片 | alias_match_only；alias_requires_review |
| herb | no_source_found | cangerzi | 苍耳子 | 未检索到来源候选 |
| herb | no_source_found | cansha | 蚕砂 | 未检索到来源候选 |
| herb | no_source_found | caodoukou | 草豆蔻 | 未检索到来源候选 |
| herb | no_source_found | caoguo | 草果 | 未检索到来源候选 |
| herb | no_source_found | chouwutong | 臭梧桐 | 未检索到来源候选 |
| herb | no_source_found | chuanyubeimu | 川贝母 | 未检索到来源候选 |
| herb | no_source_found | chuipencao | 垂盆草 | 未检索到来源候选 |
| herb | no_source_found | chunpi | 椿皮 | 未检索到来源候选 |
| herb | no_source_found | cijili | 刺蒺藜 | 未检索到来源候选 |
| herb | no_source_found | daidaihua | 代代花 | 未检索到来源候选 |
| herb | no_source_found | daodou | 刀豆 | 未检索到来源候选 |
| herb | needs_review | dengxincao | 灯心草 | quality_score_below_verified_threshold |
| herb | no_source_found | diercao | 地耳草 | 未检索到来源候选 |
| herb | no_source_found | dijincao | 地锦草 | 未检索到来源候选 |
| herb | needs_review | ezhu | 莪术 | quality_score_below_verified_threshold |
| herb | needs_review | fanxieye | 番泻叶 | alias_match_only；alias_requires_review |
| herb | no_source_found | feizi | 榧子 | 未检索到来源候选 |
| herb | no_source_found | foshou | 佛手 | 未检索到来源候选 |
| herb | needs_review | ganlan | 橄榄 | quality_score_below_verified_threshold |
| herb | no_source_found | gijingcao | 谷精草 | 未检索到来源候选 |
| herb | no_source_found | gouteng | 钩藤 | 未检索到来源候选 |
| herb | no_source_found | guya | 谷芽 | 未检索到来源候选 |
| herb | no_source_found | haifengteng | 海风藤 | 未检索到来源候选 |
| herb | no_source_found | haifushi | 海浮石 | 未检索到来源候选 |
| herb | no_source_found | haigeqiao | 海蛤壳 | 未检索到来源候选 |
| herb | needs_review | haijinsha | 海金沙 | quality_score_below_verified_threshold |
| herb | no_source_found | haima | 海马 | 未检索到来源候选 |
| herb | no_source_found | haitongpi | 海桐皮 | 未检索到来源候选 |
| herb | no_source_found | hamayou | 哈蟆油 | 未检索到来源候选 |
| herb | no_source_found | hechezi | 黑芝麻 | 未检索到来源候选 |
| herb | no_source_found | heizhima | 黑芝麻 | 未检索到来源候选 |
| herb | no_source_found | hesi | 鹤虱 | 未检索到来源候选 |
| herb | no_source_found | hetaoren | 核桃仁 | 未检索到来源候选 |
| herb | no_source_found | hezi | 鹤虱 | 未检索到来源候选 |
| herb | no_source_found | hongteng | 红藤 | 未检索到来源候选 |
| herb | no_source_found | huangyaozi | 黄药子 | 未检索到来源候选 |
| herb | no_source_found | huazuirushi | 花蕊石 | 未检索到来源候选 |
| herb | no_source_found | hugulu | 胡芦巴 | 未检索到来源候选 |
| herb | no_source_found | huoxiang | 广藿香 | 未检索到来源候选 |
| herb | no_source_found | huzhang | 虎杖 | 未检索到来源候选 |
| herb | needs_review | jianghuang | 姜黄 | quality_score_below_verified_threshold |
| herb | no_source_found | jiangxiang | 降香 | 未检索到来源候选 |
| herb | no_source_found | jiguanhua | 鸡冠花 | 未检索到来源候选 |
| herb | no_source_found | jinguolan | 金果榄 | 未检索到来源候选 |
| herb | no_source_found | jinqiancao | 金钱草 | 未检索到来源候选 |
| herb | no_source_found | jiucaizi | 韭菜子 | 未检索到来源候选 |
| herb | no_source_found | jixueteng | 鸡血藤 | 未检索到来源候选 |
| herb | no_source_found | laifuzi | 莱菔子 | 未检索到来源候选 |
| herb | no_source_found | laoguancao | 老鹳草 | 未检索到来源候选 |
| herb | no_source_found | leigongteng | 雷公藤 | 未检索到来源候选 |
| herb | no_source_found | lianxu | 莲须 | 未检索到来源候选 |
| herb | no_source_found | liujinu | 刘寄奴 | 未检索到来源候选 |
| herb | no_source_found | lizhihe | 荔枝核 | 未检索到来源候选 |
| herb | needs_review | lugen | 芦根 | quality_score_below_verified_threshold |
| herb | no_source_found | luhui | 芦荟 | 未检索到来源候选 |
| herb | no_source_found | lulutong | 路路通 | 未检索到来源候选 |
| herb | no_source_found | luobuma | 罗布麻叶 | 未检索到来源候选 |
| herb | no_source_found | luobumaye | 罗布麻叶 | 未检索到来源候选 |
| herb | no_source_found | luohanguo | 罗汉果 | 未检索到来源候选 |
| herb | no_source_found | lvtuomei | 绿萼梅 | 未检索到来源候选 |
| herb | no_source_found | mabo | 马勃 | 未检索到来源候选 |
| herb | no_source_found | machixian | 马齿苋 | 未检索到来源候选 |
