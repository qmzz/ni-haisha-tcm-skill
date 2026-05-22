# P8-B 方剂 verified 扩展报告

## 阶段定位

P8-B 优先推进方剂知识库数据完备化。本批采用小批量人工白名单，只读取 `data/formula_index.jsonl` 中既有首选 `source_ref`，不凭模型记忆补医学内容。

## 本批结果

- whitelist: 69
- added: 63
- skipped_existing: 6
- errors: 0
- formula_verified_after: 113
- verified_total_after: 210

## 新增方剂

| item_id | name | source_file | page_num | quality_score | threshold |
|---------|------|-------------|----------|---------------|-----------|
| zhigancao_tang | 炙甘草汤 | 04【视频同步文稿】人-伤寒论（可打印）.json | 121 | 99 | 95 |
| wumei_wan | 乌梅丸 | 04【视频同步文稿】人-伤寒论（可打印）.json | 12 | 100 | 95 |
| sini_san | 四逆散 | 倪海厦人纪系列之伤寒论.json | 186 | 100 | 95 |
| shizao_tang | 十枣汤 | 04【视频同步文稿】人-伤寒论（可打印）.json | 102 | 100 | 95 |
| shengjiang_xiexin | 生姜泻心汤 | 倪海厦人纪系列之伤寒论.json | 116 | 100 | 95 |
| kujiu_tang | 苦酒汤 | 04【视频同步文稿】人-伤寒论（可打印）.json | 173 | 100 | 95 |
| banxia_san | 半夏散及汤 | 04【视频同步文稿】人-伤寒论（可打印）.json | 173 | 100 | 95 |
| shenqi_wan | 肾气丸 | 05【视频同步文稿】人-金匮要略（可打印）.json | 220 | 100 | 95 |
| jiaoai_tang | 胶艾汤 | 05【视频同步文稿】人-金匮要略（可打印）.json | 384 | 100 | 95 |
| fuling_xingren | 茯苓杏仁甘草汤 | 05【视频同步文稿】人-金匮要略（可打印）.json | 161 | 100 | 95 |
| tingli_dazao | 葶苈大枣泻肺汤 | 05【视频同步文稿】人-金匮要略（可打印）.json | 142 | 100 | 95 |
| gancao_fenmi | 甘草粉蜜汤 | 05【视频同步文稿】人-金匮要略（可打印）.json | 377 | 100 | 95 |
| yiyi_fuzi | 薏苡附子败酱散 | 倪海厦人纪系列之金匮要略.json | 58 | 100 | 95 |
| zaojia_wan | 皂荚丸 | 05【视频同步文稿】人-金匮要略（可打印）.json | 137 | 100 | 95 |
| zhizhu_san | 蜘蛛散 | 05【视频同步文稿】人-金匮要略（可打印）.json | 375 | 100 | 95 |
| xiayu_xue | 下瘀血汤 | 05【视频同步文稿】人-金匮要略（可打印）.json | 394 | 100 | 95 |
| puhui_san | 蒲灰散 | 05【视频同步文稿】人-金匮要略（可打印）.json | 284 | 100 | 95 |
| fangji_fuling | 防己茯苓汤 | 05【视频同步文稿】人-金匮要略（可打印）.json | 284 | 100 | 95 |
| zeqi_tang | 泽漆汤 | 05【视频同步文稿】人-金匮要略（可打印）.json | 139 | 99 | 95 |
| yuebi_tang | 越婢汤 | 05【视频同步文稿】人-金匮要略（可打印）.json | 145 | 99 | 95 |
| yuebi_zhu | 越婢加术汤 | 05【视频同步文稿】人-金匮要略（可打印）.json | 281 | 99 | 95 |
| fuling_guizhi | 茯苓桂枝甘草大枣汤 | 04【视频同步文稿】人-伤寒论（可打印）.json | 51 | 99 | 95 |
| guizhi_gancao | 桂枝甘草汤 | 倪海厦人纪系列之伤寒论.json | 51 | 99 | 95 |
| mahuang_fuzi_gancao | 麻黄附子甘草汤 | 倪海厦人纪系列之伤寒论.json | 207 | 99 | 95 |
| baitouweng_jiaoai | 白头翁加甘草阿胶汤 | 金匮要略.json | None | 100 | 95 |
| baizhu_fuzi | 白术附子汤 | 桂林古本伤寒杂病论 .json | None | 74 | 70 |
| dahuang_gansui | 大黄甘遂汤 | 05【视频同步文稿】人-金匮要略（可打印）.json | 412 | 99 | 95 |
| danggui_jianzhong | 当归建中汤 | 金匮要略.json | None | 96 | 95 |
| fuling_rongyan | 茯苓戎盐汤 | 05【视频同步文稿】人-金匮要略（可打印）.json | 252 | 100 | 95 |
| gancao_fuzi | 甘草附子汤 | 倪海厦人纪系列之伤寒论.json | 54 | 99 | 95 |
| gancao_ganjiang | 甘草干姜汤 | 倪海厦人纪系列之伤寒论.json | 30 | 96 | 95 |
| gancao_mahuang | 甘草麻黄汤 | 05【视频同步文稿】人-金匮要略（可打印）.json | 282 | 99 | 95 |
| ganjiang_fuzi | 干姜附子汤 | 04【视频同步文稿】人-伤寒论（可打印）.json | 49 | 99 | 95 |
| guizhi_dahuang | 桂枝加大黄汤 | 倪海厦人纪系列之伤寒论.json | 170 | 99 | 95 |
| honglanhua_jiu | 红蓝花酒 | 金匮要略.json | None | 100 | 95 |
| houpo_shengjiang | 厚朴生姜半夏甘草人参汤 | 04【视频同步文稿】人-伤寒论（可打印）.json | 53 | 99 | 95 |
| huashi_baiyu | 滑石白鱼散 | 05【视频同步文稿】人-金匮要略（可打印）.json | 252 | 100 | 95 |
| jishibai_san | 鸡屎白散 | 金匮要略.json | None | 100 | 95 |
| juzhi_jiang | 橘枳姜汤 | 倪海夏-汉唐中医方剂讲解.json | 125 | 74 | 70 |
| lizhong_wan | 理中丸 | 05【视频同步文稿】人-金匮要略（可打印）.json | 16 | 80 | 80 |
| mahuang_lianqiao | 麻黄连轺赤小豆汤 | 桂林古本伤寒杂病论 .json | None | 74 | 70 |
| mahuang_shengma | 麻黄升麻汤 | 倪海厦人纪系列之伤寒论.json | 199 | 99 | 95 |
| maimendong_tang | 麦门冬汤 | 05【视频同步文稿】人-金匮要略（可打印）.json | 141 | 99 | 95 |
| muli_zexie | 牡蛎泽泻散 | 桂林古本伤寒杂病论 .json | None | 80 | 80 |
| neibu_danggui | 内补当归建中汤 | 金匮要略.json | None | 96 | 95 |
| painong_san | 排脓散 | 05【视频同步文稿】人-金匮要略（可打印）.json | 370 | 99 | 95 |
| painong_tang | 排脓汤 | 倪海厦人纪系列之金匮要略.json | 151 | 100 | 95 |
| sanwu_huangqin | 三物黄芩汤 | 金匮要略.json | None | 99 | 95 |
| shaoyao_gancao_fuzi | 芍药甘草附子汤 | 倪海厦人纪系列之伤寒论.json | 54 | 99 | 95 |
| shechuangzi_san | 蛇床子散 | 倪海厦人纪系列之金匮要略.json | 414 | 100 | 95 |
| shegan_mahuang | 射干麻黄汤 | 倪海厦人纪系列之金匮要略.json | 142 | 99 | 95 |
| taohua_tang | 桃花汤 | 04【视频同步文稿】人-伤寒论（可打印）.json | 171 | 99 | 95 |
| tongmai_sini | 通脉四逆汤 | 倪海厦人纪系列之伤寒论.json | 184 | 99 | 95 |
| wangbuliuxing | 王不留行散 | 05【视频同步文稿】人-金匮要略（可打印）.json | 369 | 99 | 95 |
| wenjing_tang | 温经汤 | 倪海厦人纪系列之金匮要略.json | 409 | 99 | 95 |
| xiaoer_gan | 小儿疳虫蚀齿方 | 金匮要略.json | None | 96 | 95 |
| xiaojianzhong_tang | 小建中汤 | 05【视频同步文稿】人-金匮要略（可打印）.json | 122 | 99 | 95 |
| xingzi_tang | 杏子汤 | 金匮要略.json | None | 100 | 95 |
| xuanfu_daihe | 旋覆代赭汤 | 倪海厦人纪系列之伤寒论.json | 119 | 99 | 95 |
| zhishi_shaoyao | 枳实芍药散 | 金匮要略.json | None | 100 | 95 |
| zhishi_zhizi | 枳实栀子豉汤 | 桂林古本伤寒杂病论 .json | None | 77 | 70 |
| zhupi_dawan | 竹皮大丸 | 金匮要略.json | None | 100 | 95 |
| zhuye_shigao | 竹叶石膏汤 | 倪海厦人纪系列之伤寒论.json | 138 | 93 | 90 |

## 边界

- verified 仅表示来源追溯链路通过复核，不代表医学真实性或临床适用性。
- 本批不修改医学正文，只通过既有标准化脚本补治理 frontmatter 与安全边界。
- candidate 不等于 verified；未进入本白名单的条目保持原状态。
- 少数低分尾部条目使用显式 QUALITY_OVERRIDES，仅表示人工纳入追溯链路复核，不代表医学判断。
