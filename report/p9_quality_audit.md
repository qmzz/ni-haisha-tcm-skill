# P9 数据质量审计报告

## 定位

本报告检查知识库内容质量，不修改医学正文，不自动提升 verified。

## 总览

- issues: 113
- by_level: {'info': 7, 'warning': 30, 'review': 76}
- by_kind: {'acupoint': 78, 'herb': 35}

## 问题类型 Top

| level | code | count |
|-------|------|-------|
| review | parent_expand_verified_needs_human_review | 51 |
| warning | duplicate_title | 30 |
| review | low_score_verified_needs_review | 25 |
| info | body_short | 7 |

## 样例（前 100 条）

| level | kind | code | file | detail |
|-------|------|------|------|--------|
| info | acupoint | body_short | knowledge/acupoints/huagai.md | lines=9 |
| info | acupoint | body_short | knowledge/acupoints/huantiao.md | lines=8 |
| info | acupoint | body_short | knowledge/acupoints/laogong.md | lines=8 |
| info | acupoint | body_short | knowledge/acupoints/xuanji.md | lines=9 |
| info | acupoint | body_short | knowledge/acupoints/yutang.md | lines=9 |
| info | acupoint | body_short | knowledge/acupoints/zhongzhu.md | lines=8 |
| info | acupoint | body_short | knowledge/acupoints/zigong.md | lines=9 |
| warning | herb | duplicate_title | knowledge/herbs/aishe.md | knowledge/herbs/aishe.md, knowledge/herbs/aoye.md |
| warning | herb | duplicate_title | knowledge/herbs/aoye.md | knowledge/herbs/aishe.md, knowledge/herbs/aoye.md |
| warning | herb | duplicate_title | knowledge/herbs/aoshugen.md | knowledge/herbs/aoshugen.md, knowledge/herbs/nuodaogenxu.md |
| warning | herb | duplicate_title | knowledge/herbs/nuodaogenxu.md | knowledge/herbs/aoshugen.md, knowledge/herbs/nuodaogenxu.md |
| warning | herb | duplicate_title | knowledge/herbs/diji.md | knowledge/herbs/diji.md, knowledge/herbs/diyu.md |
| warning | herb | duplicate_title | knowledge/herbs/diyu.md | knowledge/herbs/diji.md, knowledge/herbs/diyu.md |
| warning | herb | duplicate_title | knowledge/herbs/fupenzi.md | knowledge/herbs/fupenzi.md, knowledge/herbs/wuyaozi.md |
| warning | herb | duplicate_title | knowledge/herbs/wuyaozi.md | knowledge/herbs/fupenzi.md, knowledge/herbs/wuyaozi.md |
| warning | herb | duplicate_title | knowledge/herbs/guya.md | knowledge/herbs/guya.md, knowledge/herbs/shandou.md |
| warning | herb | duplicate_title | knowledge/herbs/shandou.md | knowledge/herbs/guya.md, knowledge/herbs/shandou.md |
| warning | herb | duplicate_title | knowledge/herbs/hechezi.md | knowledge/herbs/hechezi.md, knowledge/herbs/heizhima.md |
| warning | herb | duplicate_title | knowledge/herbs/heizhima.md | knowledge/herbs/hechezi.md, knowledge/herbs/heizhima.md |
| warning | herb | duplicate_title | knowledge/herbs/shijunzi.md | knowledge/herbs/shijunzi.md, knowledge/herbs/shizhangzi.md |
| warning | herb | duplicate_title | knowledge/herbs/shizhangzi.md | knowledge/herbs/shijunzi.md, knowledge/herbs/shizhangzi.md |
| warning | herb | duplicate_title | knowledge/herbs/zirantong.md | knowledge/herbs/zirantong.md, knowledge/herbs/zirun.md |
| warning | herb | duplicate_title | knowledge/herbs/zirun.md | knowledge/herbs/zirantong.md, knowledge/herbs/zirun.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/cuanzhu.md | knowledge/acupoints/cuanzhu.md, knowledge/acupoints/zanzhu.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/zanzhu.md | knowledge/acupoints/cuanzhu.md, knowledge/acupoints/zanzhu.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/jian Shi.md | knowledge/acupoints/jian Shi.md, knowledge/acupoints/jianshi.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/jianshi.md | knowledge/acupoints/jian Shi.md, knowledge/acupoints/jianshi.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/sanjiaoju.md | knowledge/acupoints/sanjiaoju.md, knowledge/acupoints/sanjiaoshu.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/sanjiaoshu.md | knowledge/acupoints/sanjiaoju.md, knowledge/acupoints/sanjiaoshu.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/taichong.md | knowledge/acupoints/taichong.md, knowledge/acupoints/taichong_lv.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/taichong_lv.md | knowledge/acupoints/taichong.md, knowledge/acupoints/taichong_lv.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/xiabai.md | knowledge/acupoints/xiabai.md, knowledge/acupoints/xiamen.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/xiamen.md | knowledge/acupoints/xiabai.md, knowledge/acupoints/xiamen.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/yangguan.md | knowledge/acupoints/yangguan.md, knowledge/acupoints/yaoyangguan.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/yaoyangguan.md | knowledge/acupoints/yangguan.md, knowledge/acupoints/yaoyangguan.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/zulinqi.md | knowledge/acupoints/zulinqi.md, knowledge/acupoints/zulinqi_gb.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/zulinqi_gb.md | knowledge/acupoints/zulinqi.md, knowledge/acupoints/zulinqi_gb.md |
| review | herb | low_score_verified_needs_review | knowledge/herbs/baiguo.md | P8-D verified via QUALITY_OVERRIDES (score=50, threshold=50) |
| review | herb | low_score_verified_needs_review | knowledge/herbs/baihuasheshecao.md | P8-D verified via QUALITY_OVERRIDES (score=59, threshold=50) |
| review | herb | low_score_verified_needs_review | knowledge/herbs/banlangen.md | P8-D verified via QUALITY_OVERRIDES (score=53, threshold=50) |
| review | herb | low_score_verified_needs_review | knowledge/herbs/bingpian.md | P8-D verified via QUALITY_OVERRIDES (score=62, threshold=50) |
| review | herb | low_score_verified_needs_review | knowledge/herbs/dengxincao.md | P8-D verified via QUALITY_OVERRIDES (score=56, threshold=50) |
| review | herb | low_score_verified_needs_review | knowledge/herbs/ezhu.md | P8-D verified via QUALITY_OVERRIDES (score=56, threshold=50) |
| review | herb | low_score_verified_needs_review | knowledge/herbs/ganlan.md | P8-D verified via QUALITY_OVERRIDES (score=50, threshold=50) |
| review | herb | low_score_verified_needs_review | knowledge/herbs/haijinsha.md | P8-D verified via QUALITY_OVERRIDES (score=56, threshold=50) |
| review | herb | low_score_verified_needs_review | knowledge/herbs/jianghuang.md | P8-D verified via QUALITY_OVERRIDES (score=56, threshold=50) |
| review | herb | low_score_verified_needs_review | knowledge/herbs/lugen.md | P8-D verified via QUALITY_OVERRIDES (score=59, threshold=50) |
| review | herb | low_score_verified_needs_review | knowledge/herbs/walengzi.md | P8-D verified via QUALITY_OVERRIDES (score=56, threshold=50) |
| review | herb | low_score_verified_needs_review | knowledge/herbs/xiyangshen.md | P8-D verified via QUALITY_OVERRIDES (score=53, threshold=50) |
| review | herb | low_score_verified_needs_review | knowledge/herbs/xuejie.md | P8-D verified via QUALITY_OVERRIDES (score=56, threshold=50) |
| review | herb | low_score_verified_needs_review | knowledge/herbs/xuhuang.md | P8-D verified via QUALITY_OVERRIDES (score=56, threshold=50) |
| review | herb | low_score_verified_needs_review | knowledge/herbs/yefujia.md | P8-D verified via QUALITY_OVERRIDES (score=56, threshold=50) |
| review | herb | low_score_verified_needs_review | knowledge/herbs/zaofan.md | P8-D verified via QUALITY_OVERRIDES (score=53, threshold=50) |
| review | herb | low_score_verified_needs_review | knowledge/herbs/zhuye.md | P8-D verified via QUALITY_OVERRIDES (score=56, threshold=50) |
| review | acupoint | low_score_verified_needs_review | knowledge/acupoints/bafeng.md | P8-F verified via QUALITY_OVERRIDES (score=62, threshold=55). 穴位内容仅作学习与来源追溯，不作为针灸操作指导。 |
| review | acupoint | low_score_verified_needs_review | knowledge/acupoints/baxie.md | P8-F verified via QUALITY_OVERRIDES (score=62, threshold=55). 穴位内容仅作学习与来源追溯，不作为针灸操作指导。 |
| review | acupoint | low_score_verified_needs_review | knowledge/acupoints/jimai.md | P8-F verified via QUALITY_OVERRIDES (score=62, threshold=55). 穴位内容仅作学习与来源追溯，不作为针灸操作指导。 |
| review | acupoint | low_score_verified_needs_review | knowledge/acupoints/naoshu.md | P8-F verified via QUALITY_OVERRIDES (score=56, threshold=55). 穴位内容仅作学习与来源追溯，不作为针灸操作指导。 |
| review | acupoint | low_score_verified_needs_review | knowledge/acupoints/tianfu2.md | P8-F verified via QUALITY_OVERRIDES (score=56, threshold=55). 穴位内容仅作学习与来源追溯，不作为针灸操作指导。 |
| review | acupoint | low_score_verified_needs_review | knowledge/acupoints/yixi.md | P8-F verified via QUALITY_OVERRIDES (score=65, threshold=55). 穴位内容仅作学习与来源追溯，不作为针灸操作指导。 |
| review | acupoint | low_score_verified_needs_review | knowledge/acupoints/yuanye.md | P8-F verified via QUALITY_OVERRIDES (score=59, threshold=55). 穴位内容仅作学习与来源追溯，不作为针灸操作指导。 |
| review | acupoint | low_score_verified_needs_review | knowledge/acupoints/zhongshu.md | P8-F verified via QUALITY_OVERRIDES (score=56, threshold=55). 穴位内容仅作学习与来源追溯，不作为针灸操作指导。 |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/bilao.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=臂臑) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/bitong.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=臂臑) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/chengfu2.md | P8-E parent name expand trace (acupoint_parent_expand, score=77, variant=承扶) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/chengling_gb.md | P8-E parent name expand trace (acupoint_parent_expand, score=74, variant=承灵) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/ciliao2.md | P8-E parent name expand trace (acupoint_parent_expand, score=74, variant=次髎) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/dabao2.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=大包) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/daheng2.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=大横) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/dazhong_k.md | P8-E parent name expand trace (acupoint_parent_expand, score=74, variant=大钟) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/fengshi_gb.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=风市) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/fuai2.md | P8-E parent name expand trace (acupoint_parent_expand, score=74, variant=腹哀) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/fujie2.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=腹结) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/huagai_ren.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=华盖) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/jianjing_gb.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=肩井) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/jianli_ren.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=建里) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/jianyu2.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=肩髃) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/jiaoxin_k.md | P8-E parent name expand trace (acupoint_parent_expand, score=77, variant=交信) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/jiexi2.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=解溪) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/jingmen_gb.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=京门) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/jiuwei_ren.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=鸠尾) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/kunlun_bl.md | P8-E parent name expand trace (acupoint_parent_expand, score=77, variant=昆仑) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/liangqiu2.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=梁丘) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/lidui2.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=厉兑) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/luoshen.md | P8-E parent name expand trace (acupoint_parent_expand, score=74, variant=络却) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/naokong_gb.md | P8-E parent name expand trace (acupoint_parent_expand, score=74, variant=脑空) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/neiting2.md | P8-E parent name expand trace (acupoint_parent_expand, score=77, variant=内庭) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/qianding_du.md | P8-E parent name expand trace (acupoint_parent_expand, score=77, variant=前顶) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/ququan_lv.md | P8-E parent name expand trace (acupoint_parent_expand, score=77, variant=曲泉) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/ran gu.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=然谷) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/shangwan_ren.md | P8-E parent name expand trace (acupoint_parent_expand, score=77, variant=上脘) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/shangxing_du.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=上星) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/shenmai2.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=申脉) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/shenmai_bl.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=申脉) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/shenque_ren.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=神阙) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/shidou2.md | P8-E parent name expand trace (acupoint_parent_expand, score=77, variant=食窦) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/shuifen_ren.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=水分) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/taiyi2.md | P8-E parent name expand trace (acupoint_parent_expand, score=77, variant=太乙) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/tianxi2.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=天溪) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/xiongxiang2.md | P8-E parent name expand trace (acupoint_parent_expand, score=77, variant=胸乡) |
