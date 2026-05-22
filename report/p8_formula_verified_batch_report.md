# P8-B 方剂 verified 扩展报告

## 阶段定位

P8-B 优先推进方剂知识库数据完备化。本批采用小批量人工白名单，只读取 `data/formula_index.jsonl` 中既有首选 `source_ref`，不凭模型记忆补医学内容。

## 本批结果

- whitelist: 30
- added: 24
- skipped_existing: 6
- errors: 0
- formula_verified_after: 74
- verified_total_after: 171

## 新增方剂

| item_id | name | source_file | page_num | quality_score |
|---------|------|-------------|----------|---------------|
| zhigancao_tang | 炙甘草汤 | 04【视频同步文稿】人-伤寒论（可打印）.json | 121 | 99 |
| wumei_wan | 乌梅丸 | 04【视频同步文稿】人-伤寒论（可打印）.json | 12 | 100 |
| sini_san | 四逆散 | 倪海厦人纪系列之伤寒论.json | 186 | 100 |
| shizao_tang | 十枣汤 | 04【视频同步文稿】人-伤寒论（可打印）.json | 102 | 100 |
| shengjiang_xiexin | 生姜泻心汤 | 倪海厦人纪系列之伤寒论.json | 116 | 100 |
| kujiu_tang | 苦酒汤 | 04【视频同步文稿】人-伤寒论（可打印）.json | 173 | 100 |
| banxia_san | 半夏散及汤 | 04【视频同步文稿】人-伤寒论（可打印）.json | 173 | 100 |
| shenqi_wan | 肾气丸 | 05【视频同步文稿】人-金匮要略（可打印）.json | 220 | 100 |
| jiaoai_tang | 胶艾汤 | 05【视频同步文稿】人-金匮要略（可打印）.json | 384 | 100 |
| fuling_xingren | 茯苓杏仁甘草汤 | 05【视频同步文稿】人-金匮要略（可打印）.json | 161 | 100 |
| tingli_dazao | 葶苈大枣泻肺汤 | 05【视频同步文稿】人-金匮要略（可打印）.json | 142 | 100 |
| gancao_fenmi | 甘草粉蜜汤 | 05【视频同步文稿】人-金匮要略（可打印）.json | 377 | 100 |
| yiyi_fuzi | 薏苡附子败酱散 | 倪海厦人纪系列之金匮要略.json | 58 | 100 |
| zaojia_wan | 皂荚丸 | 05【视频同步文稿】人-金匮要略（可打印）.json | 137 | 100 |
| zhizhu_san | 蜘蛛散 | 05【视频同步文稿】人-金匮要略（可打印）.json | 375 | 100 |
| xiayu_xue | 下瘀血汤 | 05【视频同步文稿】人-金匮要略（可打印）.json | 394 | 100 |
| puhui_san | 蒲灰散 | 05【视频同步文稿】人-金匮要略（可打印）.json | 284 | 100 |
| fangji_fuling | 防己茯苓汤 | 05【视频同步文稿】人-金匮要略（可打印）.json | 284 | 100 |
| zeqi_tang | 泽漆汤 | 05【视频同步文稿】人-金匮要略（可打印）.json | 139 | 99 |
| yuebi_tang | 越婢汤 | 05【视频同步文稿】人-金匮要略（可打印）.json | 145 | 99 |
| yuebi_zhu | 越婢加术汤 | 05【视频同步文稿】人-金匮要略（可打印）.json | 281 | 99 |
| fuling_guizhi | 茯苓桂枝甘草大枣汤 | 04【视频同步文稿】人-伤寒论（可打印）.json | 51 | 99 |
| guizhi_gancao | 桂枝甘草汤 | 倪海厦人纪系列之伤寒论.json | 51 | 99 |
| mahuang_fuzi_gancao | 麻黄附子甘草汤 | 倪海厦人纪系列之伤寒论.json | 207 | 99 |

## 边界

- verified 仅表示来源追溯链路通过复核，不代表医学真实性或临床适用性。
- 本批不修改医学正文，只通过既有标准化脚本补治理 frontmatter 与安全边界。
- candidate 不等于 verified；未进入本白名单的条目保持原状态。
