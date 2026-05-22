# P7-B alias / synonym 复核报告

## 原则

- alias 用于扩大来源检索召回。
- alias hit 只能进入 candidate / needs_review，不自动 verified。
- 默认只生成 review 文件；`--apply-safe` 只应用白名单 safe_alias。

## 总览

- alias review rows: 130
- apply_safe: True
- aliases_changed: 0

### decision 分布

- needs_manual_review: 126
- safe_alias: 4

### kind 分布

- acupoint: 127
- herb: 3

## review 样例

| kind | item_id | name | alias | decision |
|------|---------|------|-------|----------|
| herb | haitongpi | 海桐皮 | 刺桐皮 | safe_alias |
| herb | zhangnao | 樟脑 | 韶脑 | safe_alias |
| herb | zihuadiding | 紫花地丁 | 地丁 | safe_alias |
| acupoint | bilao | 臂臑外 | 臂臑外穴 | needs_manual_review |
| acupoint | bilao | 臂臑外 | 臂臑外穴位 | needs_manual_review |
| acupoint | bitong | 臂臑二 | 臂臑二穴 | needs_manual_review |
| acupoint | bitong | 臂臑二 | 臂臑二穴位 | needs_manual_review |
| acupoint | chengfu2 | 承扶二 | 承扶二穴 | needs_manual_review |
| acupoint | chengfu2 | 承扶二 | 承扶二穴位 | needs_manual_review |
| acupoint | chengling_gb | 承灵二 | 承灵二穴 | needs_manual_review |
| acupoint | chengling_gb | 承灵二 | 承灵二穴位 | needs_manual_review |
| acupoint | ciliao2 | 次髎二 | 次髎二穴 | needs_manual_review |
| acupoint | ciliao2 | 次髎二 | 次髎二穴位 | needs_manual_review |
| acupoint | dabao2 | 大包二 | 大包二穴 | needs_manual_review |
| acupoint | dabao2 | 大包二 | 大包二穴位 | needs_manual_review |
| acupoint | daheng2 | 大横二 | 大横二穴 | needs_manual_review |
| acupoint | daheng2 | 大横二 | 大横二穴位 | needs_manual_review |
| acupoint | dazhong_k | 大钟二 | 大钟二穴 | needs_manual_review |
| acupoint | dazhong_k | 大钟二 | 大钟二穴位 | needs_manual_review |
| acupoint | ershenmen | 耳神门 | 耳神门穴 | needs_manual_review |
| acupoint | ershenmen | 耳神门 | 耳神门穴位 | needs_manual_review |
| acupoint | fengshi_gb | 风市二 | 风市二穴 | needs_manual_review |
| acupoint | fengshi_gb | 风市二 | 风市二穴位 | needs_manual_review |
| acupoint | fuai2 | 腹哀二 | 腹哀二穴 | needs_manual_review |
| acupoint | fuai2 | 腹哀二 | 腹哀二穴位 | needs_manual_review |
| acupoint | fujie2 | 腹结二 | 腹结二穴 | needs_manual_review |
| acupoint | fujie2 | 腹结二 | 腹结二穴位 | needs_manual_review |
| acupoint | fuyang2 | 跗阳二 | 跗阳二穴 | needs_manual_review |
| acupoint | fuyang2 | 跗阳二 | 跗阳二穴位 | needs_manual_review |
| acupoint | huagai_ren | 华盖二 | 华盖二穴 | needs_manual_review |
| acupoint | huagai_ren | 华盖二 | 华盖二穴位 | needs_manual_review |
| acupoint | jianjing_gb | 肩井二 | 肩井二穴 | needs_manual_review |
| acupoint | jianjing_gb | 肩井二 | 肩井二穴位 | needs_manual_review |
| acupoint | jianli_ren | 建里二 | 建里二穴 | needs_manual_review |
| acupoint | jianli_ren | 建里二 | 建里二穴位 | needs_manual_review |
| acupoint | jianyu2 | 肩髃二 | 肩髃二穴 | needs_manual_review |
| acupoint | jianyu2 | 肩髃二 | 肩髃二穴位 | needs_manual_review |
| acupoint | jiaoxin_k | 交信二 | 交信二穴 | needs_manual_review |
| acupoint | jiaoxin_k | 交信二 | 交信二穴位 | needs_manual_review |
| acupoint | jiexi2 | 解溪二 | 解溪二穴 | needs_manual_review |
| acupoint | jiexi2 | 解溪二 | 解溪二穴位 | needs_manual_review |
| acupoint | jingmen_gb | 京门二 | 京门二穴 | needs_manual_review |
| acupoint | jingmen_gb | 京门二 | 京门二穴位 | needs_manual_review |
| acupoint | jiuwei_ren | 鸠尾二 | 鸠尾二穴 | needs_manual_review |
| acupoint | jiuwei_ren | 鸠尾二 | 鸠尾二穴位 | needs_manual_review |
| acupoint | kunlun_bl | 昆仑二 | 昆仑二穴 | needs_manual_review |
| acupoint | kunlun_bl | 昆仑二 | 昆仑二穴位 | needs_manual_review |
| acupoint | liangmen | 梁门 | 梁门穴 | needs_manual_review |
| acupoint | liangmen | 梁门 | 梁门穴位 | needs_manual_review |
| acupoint | liangqiu2 | 梁丘二 | 梁丘二穴 | needs_manual_review |
| acupoint | liangqiu2 | 梁丘二 | 梁丘二穴位 | needs_manual_review |
| acupoint | lidui2 | 厉兑二 | 厉兑二穴 | needs_manual_review |
| acupoint | lidui2 | 厉兑二 | 厉兑二穴位 | needs_manual_review |
| acupoint | luoshen | 络却二 | 络却二穴 | needs_manual_review |
| acupoint | luoshen | 络却二 | 络却二穴位 | needs_manual_review |
| acupoint | naokong_gb | 脑空二 | 脑空二穴 | needs_manual_review |
| acupoint | naokong_gb | 脑空二 | 脑空二穴位 | needs_manual_review |
| acupoint | neiting2 | 内庭二 | 内庭二穴 | needs_manual_review |
| acupoint | neiting2 | 内庭二 | 内庭二穴位 | needs_manual_review |
| acupoint | qianding_du | 前顶二 | 前顶二穴 | needs_manual_review |
| acupoint | qianding_du | 前顶二 | 前顶二穴位 | needs_manual_review |
| acupoint | ququan_lv | 曲泉二 | 曲泉二穴 | needs_manual_review |
| acupoint | ququan_lv | 曲泉二 | 曲泉二穴位 | needs_manual_review |
| acupoint | ran gu | 然谷二 | 然谷二穴 | needs_manual_review |
| acupoint | ran gu | 然谷二 | 然谷二穴位 | needs_manual_review |
| acupoint | shangwan_ren | 上脘二 | 上脘二穴 | needs_manual_review |
| acupoint | shangwan_ren | 上脘二 | 上脘二穴位 | needs_manual_review |
| acupoint | shangxing_du | 上星二 | 上星二穴 | needs_manual_review |
| acupoint | shangxing_du | 上星二 | 上星二穴位 | needs_manual_review |
| acupoint | shenmai2 | 申脉三 | 申脉三穴 | needs_manual_review |
| acupoint | shenmai2 | 申脉三 | 申脉三穴位 | needs_manual_review |
| acupoint | shenmai_bl | 申脉二 | 申脉二穴 | needs_manual_review |
| acupoint | shenmai_bl | 申脉二 | 申脉二穴位 | needs_manual_review |
| acupoint | shenque_ren | 神阙二 | 神阙二穴 | needs_manual_review |
| acupoint | shenque_ren | 神阙二 | 神阙二穴位 | needs_manual_review |
| acupoint | shidou2 | 食窦二 | 食窦二穴 | needs_manual_review |
| acupoint | shidou2 | 食窦二 | 食窦二穴位 | needs_manual_review |
| acupoint | shuifen_ren | 水分二 | 水分二穴 | needs_manual_review |
| acupoint | shuifen_ren | 水分二 | 水分二穴位 | needs_manual_review |
| acupoint | sishencong | 四神聪 | 四神聪穴 | safe_alias |
