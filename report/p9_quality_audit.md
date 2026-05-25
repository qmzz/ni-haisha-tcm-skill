# P9 数据质量审计报告

## 定位

本报告检查知识库内容质量，不修改医学正文，不自动提升 verified。

## 总览

- issues: 173
- by_level: {'info': 7, 'warning': 90, 'review': 76}
- by_kind: {'acupoint': 114, 'herb': 59}

## 问题类型 Top

| level | code | count |
|-------|------|-------|
| warning | duplicate_title | 90 |
| review | parent_expand_verified_needs_human_review | 51 |
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
| warning | herb | duplicate_title | knowledge/herbs/biba.md | knowledge/herbs/biba.md, knowledge/herbs/bichengqie.md |
| warning | herb | duplicate_title | knowledge/herbs/bichengqie.md | knowledge/herbs/biba.md, knowledge/herbs/bichengqie.md |
| warning | herb | duplicate_title | knowledge/herbs/diji.md | knowledge/herbs/diji.md, knowledge/herbs/diyu.md |
| warning | herb | duplicate_title | knowledge/herbs/diyu.md | knowledge/herbs/diji.md, knowledge/herbs/diyu.md |
| warning | herb | duplicate_title | knowledge/herbs/fupenzi.md | knowledge/herbs/fupenzi.md, knowledge/herbs/wuyaozi.md |
| warning | herb | duplicate_title | knowledge/herbs/wuyaozi.md | knowledge/herbs/fupenzi.md, knowledge/herbs/wuyaozi.md |
| warning | herb | duplicate_title | knowledge/herbs/geda.md | knowledge/herbs/geda.md, knowledge/herbs/gegen.md |
| warning | herb | duplicate_title | knowledge/herbs/gegen.md | knowledge/herbs/geda.md, knowledge/herbs/gegen.md |
| warning | herb | duplicate_title | knowledge/herbs/gualou.md | knowledge/herbs/gualou.md, knowledge/herbs/gualue.md |
| warning | herb | duplicate_title | knowledge/herbs/gualue.md | knowledge/herbs/gualou.md, knowledge/herbs/gualue.md |
| warning | herb | duplicate_title | knowledge/herbs/guya.md | knowledge/herbs/guya.md, knowledge/herbs/shandou.md |
| warning | herb | duplicate_title | knowledge/herbs/shandou.md | knowledge/herbs/guya.md, knowledge/herbs/shandou.md |
| warning | herb | duplicate_title | knowledge/herbs/hechezi.md | knowledge/herbs/hechezi.md, knowledge/herbs/heizhima.md |
| warning | herb | duplicate_title | knowledge/herbs/heizhima.md | knowledge/herbs/hechezi.md, knowledge/herbs/heizhima.md |
| warning | herb | duplicate_title | knowledge/herbs/hesi.md | knowledge/herbs/hesi.md, knowledge/herbs/hezi.md |
| warning | herb | duplicate_title | knowledge/herbs/hezi.md | knowledge/herbs/hesi.md, knowledge/herbs/hezi.md |
| warning | herb | duplicate_title | knowledge/herbs/huangbai.md | knowledge/herbs/huangbai.md, knowledge/herbs/huangbo.md |
| warning | herb | duplicate_title | knowledge/herbs/huangbo.md | knowledge/herbs/huangbai.md, knowledge/herbs/huangbo.md |
| warning | herb | duplicate_title | knowledge/herbs/kualianpi.md | knowledge/herbs/kualianpi.md, knowledge/herbs/kulianpi.md |
| warning | herb | duplicate_title | knowledge/herbs/kulianpi.md | knowledge/herbs/kualianpi.md, knowledge/herbs/kulianpi.md |
| warning | herb | duplicate_title | knowledge/herbs/luobuma.md | knowledge/herbs/luobuma.md, knowledge/herbs/luobumaye.md |
| warning | herb | duplicate_title | knowledge/herbs/luobumaye.md | knowledge/herbs/luobuma.md, knowledge/herbs/luobumaye.md |
| warning | herb | duplicate_title | knowledge/herbs/shijunzi.md | knowledge/herbs/shijunzi.md, knowledge/herbs/shizhangzi.md |
| warning | herb | duplicate_title | knowledge/herbs/shizhangzi.md | knowledge/herbs/shijunzi.md, knowledge/herbs/shizhangzi.md |
| warning | herb | duplicate_title | knowledge/herbs/sumu.md | knowledge/herbs/sumu.md, knowledge/herbs/suomu.md |
| warning | herb | duplicate_title | knowledge/herbs/suomu.md | knowledge/herbs/sumu.md, knowledge/herbs/suomu.md |
| warning | herb | duplicate_title | knowledge/herbs/tubiechong.md | knowledge/herbs/tubiechong.md, knowledge/herbs/zhechong.md |
| warning | herb | duplicate_title | knowledge/herbs/zhechong.md | knowledge/herbs/tubiechong.md, knowledge/herbs/zhechong.md |
| warning | herb | duplicate_title | knowledge/herbs/xuejie.md | knowledge/herbs/xuejie.md, knowledge/herbs/xuhuang.md |
| warning | herb | duplicate_title | knowledge/herbs/xuhuang.md | knowledge/herbs/xuejie.md, knowledge/herbs/xuhuang.md |
| warning | herb | duplicate_title | knowledge/herbs/yanhucuo.md | knowledge/herbs/yanhucuo.md, knowledge/herbs/yanhusuo.md |
| warning | herb | duplicate_title | knowledge/herbs/yanhusuo.md | knowledge/herbs/yanhucuo.md, knowledge/herbs/yanhusuo.md |
| warning | herb | duplicate_title | knowledge/herbs/yubaifu.md | knowledge/herbs/yubaifu.md, knowledge/herbs/yubaizi.md |
| warning | herb | duplicate_title | knowledge/herbs/yubaizi.md | knowledge/herbs/yubaifu.md, knowledge/herbs/yubaizi.md |
| warning | herb | duplicate_title | knowledge/herbs/zirantong.md | knowledge/herbs/zirantong.md, knowledge/herbs/zirun.md |
| warning | herb | duplicate_title | knowledge/herbs/zirun.md | knowledge/herbs/zirantong.md, knowledge/herbs/zirun.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/cuanzhu.md | knowledge/acupoints/cuanzhu.md, knowledge/acupoints/zanzhu.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/zanzhu.md | knowledge/acupoints/cuanzhu.md, knowledge/acupoints/zanzhu.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/fengchi.md | knowledge/acupoints/fengchi.md, knowledge/acupoints/fengchi_gb.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/fengchi_gb.md | knowledge/acupoints/fengchi.md, knowledge/acupoints/fengchi_gb.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/fuliu.md | knowledge/acupoints/fuliu.md, knowledge/acupoints/fuliu_k.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/fuliu_k.md | knowledge/acupoints/fuliu.md, knowledge/acupoints/fuliu_k.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/futu.md | knowledge/acupoints/futu.md, knowledge/acupoints/futu_li.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/futu_li.md | knowledge/acupoints/futu.md, knowledge/acupoints/futu_li.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/jian Shi.md | knowledge/acupoints/jian Shi.md, knowledge/acupoints/jianshi.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/jianshi.md | knowledge/acupoints/jian Shi.md, knowledge/acupoints/jianshi.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/jingming.md | knowledge/acupoints/jingming.md, knowledge/acupoints/jingming_bl.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/jingming_bl.md | knowledge/acupoints/jingming.md, knowledge/acupoints/jingming_bl.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/ligou.md | knowledge/acupoints/ligou.md, knowledge/acupoints/ligou_lv.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/ligou_lv.md | knowledge/acupoints/ligou.md, knowledge/acupoints/ligou_lv.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/naohu.md | knowledge/acupoints/naohu.md, knowledge/acupoints/naokong_bl.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/naokong_bl.md | knowledge/acupoints/naohu.md, knowledge/acupoints/naokong_bl.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/qimen.md | knowledge/acupoints/qimen.md, knowledge/acupoints/qimen_lv.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/qimen_lv.md | knowledge/acupoints/qimen.md, knowledge/acupoints/qimen_lv.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/qiuxu.md | knowledge/acupoints/qiuxu.md, knowledge/acupoints/qiuxu_gb.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/qiuxu_gb.md | knowledge/acupoints/qiuxu.md, knowledge/acupoints/qiuxu_gb.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/sanjiaoju.md | knowledge/acupoints/sanjiaoju.md, knowledge/acupoints/sanjiaoshu.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/sanjiaoshu.md | knowledge/acupoints/sanjiaoju.md, knowledge/acupoints/sanjiaoshu.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/taichong.md | knowledge/acupoints/taichong.md, knowledge/acupoints/taichong_lv.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/taichong_lv.md | knowledge/acupoints/taichong.md, knowledge/acupoints/taichong_lv.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/taixi.md | knowledge/acupoints/taixi.md, knowledge/acupoints/taixi_k.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/taixi_k.md | knowledge/acupoints/taixi.md, knowledge/acupoints/taixi_k.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/tianzhu.md | knowledge/acupoints/tianzhu.md, knowledge/acupoints/tianzhu_bl.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/tianzhu_bl.md | knowledge/acupoints/tianzhu.md, knowledge/acupoints/tianzhu_bl.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/xiabai.md | knowledge/acupoints/xiabai.md, knowledge/acupoints/xiamen.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/xiamen.md | knowledge/acupoints/xiabai.md, knowledge/acupoints/xiamen.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/xiawan.md | knowledge/acupoints/xiawan.md, knowledge/acupoints/xiwan.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/xiwan.md | knowledge/acupoints/xiawan.md, knowledge/acupoints/xiwan.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/xingjian.md | knowledge/acupoints/xingjian.md, knowledge/acupoints/xingjian_lv.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/xingjian_lv.md | knowledge/acupoints/xingjian.md, knowledge/acupoints/xingjian_lv.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/xuanzhong.md | knowledge/acupoints/xuanzhong.md, knowledge/acupoints/xuanzhong_gb.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/xuanzhong_gb.md | knowledge/acupoints/xuanzhong.md, knowledge/acupoints/xuanzhong_gb.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/yangguan.md | knowledge/acupoints/yangguan.md, knowledge/acupoints/yaoyangguan.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/yaoyangguan.md | knowledge/acupoints/yangguan.md, knowledge/acupoints/yaoyangguan.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/yingu.md | knowledge/acupoints/yingu.md, knowledge/acupoints/yingu_k.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/yingu_k.md | knowledge/acupoints/yingu.md, knowledge/acupoints/yingu_k.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/yinjiao.md | knowledge/acupoints/yinjiao.md, knowledge/acupoints/yinjiao_du.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/yinjiao_du.md | knowledge/acupoints/yinjiao.md, knowledge/acupoints/yinjiao_du.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/yongquan.md | knowledge/acupoints/yongquan.md, knowledge/acupoints/yongquan_k.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/yongquan_k.md | knowledge/acupoints/yongquan.md, knowledge/acupoints/yongquan_k.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/zhaohai.md | knowledge/acupoints/zhaohai.md, knowledge/acupoints/zhaohai_k.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/zhaohai_k.md | knowledge/acupoints/zhaohai.md, knowledge/acupoints/zhaohai_k.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/zhishi.md | knowledge/acupoints/zhishi.md, knowledge/acupoints/zhishi_bl.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/zhishi_bl.md | knowledge/acupoints/zhishi.md, knowledge/acupoints/zhishi_bl.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/zulinqi.md | knowledge/acupoints/zulinqi.md, knowledge/acupoints/zulinqi_gb.md |
| warning | acupoint | duplicate_title | knowledge/acupoints/zulinqi_gb.md | knowledge/acupoints/zulinqi.md, knowledge/acupoints/zulinqi_gb.md |
| review | herb | low_score_verified_needs_review | knowledge/herbs/baiguo.md | P8-D verified via QUALITY_OVERRIDES (score=50, threshold=50) |
| review | herb | low_score_verified_needs_review | knowledge/herbs/baihuasheshecao.md | P8-D verified via QUALITY_OVERRIDES (score=59, threshold=50) |
| review | herb | low_score_verified_needs_review | knowledge/herbs/banlangen.md | P8-D verified via QUALITY_OVERRIDES (score=53, threshold=50) |
