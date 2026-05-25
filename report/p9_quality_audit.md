# P9 数据质量审计报告

## 定位

本报告检查知识库内容质量，不修改医学正文，不自动提升 verified。

## 总览

- issues: 77
- by_level: {'info': 1, 'review': 76}
- by_kind: {'acupoint': 58, 'herb': 19}

## 问题类型 Top

| level | code | count |
|-------|------|-------|
| review | parent_expand_verified_needs_human_review | 51 |
| review | low_score_verified_needs_review | 25 |
| info | body_short | 1 |

## 样例（前 100 条）

| level | kind | code | file | detail |
|-------|------|------|------|--------|
| info | acupoint | body_short | knowledge/acupoints/laogong.md | lines=8 |
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
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/xuanji_ren.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=璇玑) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/yunmen2.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=云门) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/yutang_ren.md | P8-E parent name expand trace (acupoint_parent_expand, score=77, variant=玉堂) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/zhangmen_lv.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=章门) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/zhongdu_lv.md | P8-E parent name expand trace (acupoint_parent_expand, score=77, variant=中都) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/zhongfeng_lv.md | P8-E parent name expand trace (acupoint_parent_expand, score=77, variant=中封) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/zhongwan_ren.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=中脘) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/zhourong2.md | P8-E parent name expand trace (acupoint_parent_expand, score=77, variant=周荣) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/zhubin_k.md | P8-E parent name expand trace (acupoint_parent_expand, score=77, variant=筑宾) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/zigong_ren.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=紫宫) |
| review | acupoint | parent_expand_verified_needs_human_review | knowledge/acupoints/zusanli_st.md | P8-E parent name expand trace (acupoint_parent_expand, score=80, variant=足三里) |
| review | herb | parent_expand_verified_needs_human_review | knowledge/herbs/chuanyubeimu.md | P8-E parent name expand trace (herb_parent_expand, score=100, variant=贝母) |
| review | herb | parent_expand_verified_needs_human_review | knowledge/herbs/zhushagen.md | P8-E parent name expand trace (herb_parent_expand, score=100, variant=朱砂) |
