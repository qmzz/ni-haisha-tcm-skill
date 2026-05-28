# P28 / P5-C Remaining needs_review Source Repair

逐条对剩余 needs_review 进行原始 JSON 重检索与保守修复。

> 边界：只更新来源关系与 source_refs，不改写医学内容，不判断医学真实性或疗效。

- Processed: 34

## By target level

| target | count |
|---|---:|
| `verified_contextual` | 2 |
| `verified_direct` | 32 |

## Decisions

- `acupoint:benshen` 本神 — `needs_review` → `verified_direct` (raw_search_direct_hit; 01【视频同步文稿】人-针灸篇（可打印）.json p51)
- `acupoint:chengguang` 承光 — `needs_review` → `verified_direct` (raw_search_direct_hit; 01【视频同步文稿】人-针灸篇（可打印）.json p91)
- `acupoint:dachangshu` 大肠俞 — `needs_review` → `verified_direct` (raw_search_direct_hit; 01【视频同步文稿】人-针灸篇（可打印）.json p6)
- `acupoint:dicang` 地仓 — `needs_review` → `verified_direct` (raw_search_direct_hit; 01【视频同步文稿】人-针灸篇（可打印）.json p52)
- `acupoint:dingchuan` 定喘 — `needs_review` → `verified_direct` (raw_search_direct_hit; 01【视频同步文稿】人-针灸篇（可打印）.json p9)
- `acupoint:gaohuangshu` 膏肓俞 — `needs_review` → `verified_direct` (raw_search_direct_hit; 01【视频同步文稿】人-针灸篇（可打印）.json p103)
- `acupoint:guanmen` 关门 — `needs_review` → `verified_direct` (raw_search_direct_hit; 01【视频同步文稿】人-针灸篇（可打印）.json p52)
- `acupoint:jiaji` 夹脊 — `needs_review` → `verified_direct` (raw_search_direct_hit; 01【视频同步文稿】人-针灸篇（可打印）.json p138)
- `acupoint:luoque` 络却 — `needs_review` → `verified_direct` (raw_search_direct_hit; 01【视频同步文稿】人-针灸篇（可打印）.json p91)
- `acupoint:luozhen` 落枕 — `needs_review` → `verified_direct` (raw_search_direct_hit; 01【视频同步文稿】人-针灸篇（可打印）.json p49)
- `acupoint:qucha` 曲差 — `needs_review` → `verified_direct` (raw_search_direct_hit; 01【视频同步文稿】人-针灸篇（可打印）.json p90)
- `acupoint:quyuan` 曲垣 — `needs_review` → `verified_direct` (raw_search_direct_hit; 01【视频同步文稿】人-针灸篇（可打印）.json p86)
- `acupoint:shuitu` 水突 — `needs_review` → `verified_direct` (raw_search_direct_hit; 01【视频同步文稿】人-针灸篇（可打印）.json p53)
- `acupoint:tongtian` 通天 — `needs_review` → `verified_direct` (raw_search_direct_hit; 01【视频同步文稿】人-针灸篇（可打印）.json p91)
- `acupoint:wuchu` 五处 — `needs_review` → `verified_direct` (raw_search_direct_hit; 01【视频同步文稿】人-针灸篇（可打印）.json p91)
- `acupoint:xiabai` 侠白 — `needs_review` → `verified_direct` (raw_search_direct_hit; 01【视频同步文稿】人-针灸篇（可打印）.json p41)
- `acupoint:xiamen` 侠白 — `needs_review` → `verified_direct` (raw_search_direct_hit; 01【视频同步文稿】人-针灸篇（可打印）.json p41)
- `acupoint:xinhui` 囟会 — `needs_review` → `verified_direct` (raw_search_direct_hit; 01【视频同步文稿】人-针灸篇（可打印）.json p38)
- `acupoint:yishe` 意舍 — `needs_review` → `verified_direct` (raw_search_direct_hit; 01【视频同步文稿】人-针灸篇（可打印）.json p104)
- `acupoint:yutang` 玉堂 — `needs_review` → `verified_direct` (raw_search_direct_hit; 01【视频同步文稿】人-针灸篇（可打印）.json p32)
- `herb:banlangen` 板蓝根 — `needs_review` → `verified_contextual` (raw_search_contextual_hit; 05【视频同步文稿】人-金匮要略（可打印）.json p260)
- `herb:bingpian` 冰片 — `needs_review` → `verified_direct` (raw_search_direct_hit; 倪海厦人纪系列之神农本草经.json p67)
- `herb:bohe` 薄荷 — `needs_review` → `verified_direct` (raw_search_direct_hit; 倪海厦人纪系列之神农本草经.json p91)
- `herb:changshanmiao` 常山苗 — `needs_review` → `verified_direct` (raw_search_direct_hit; 02【视频同步文稿】人-神农本草经（可打印）.json p127)
- `herb:daqingye` 大青叶 — `needs_review` → `verified_direct` (raw_search_direct_hit; 02【视频同步文稿】人-神农本草经（可打印）.json p101)
- `herb:dengxincao` 灯心草 — `needs_review` → `verified_contextual` (raw_search_contextual_hit; 04【视频同步文稿】人-伤寒论（可打印）.json p143)
- `herb:dingxiang` 丁香 — `needs_review` → `verified_direct` (raw_search_direct_hit; 02【视频同步文稿】人-神农本草经（可打印）.json p131)
- `herb:heshouwu` 何首乌 — `needs_review` → `verified_direct` (raw_search_direct_hit; 02【视频同步文稿】人-神农本草经（可打印）.json p10)
- `herb:huajiao` 花椒 — `needs_review` → `verified_direct` (raw_search_direct_hit; 02【视频同步文稿】人-神农本草经（可打印）.json p143)
- `herb:hujiao` 胡椒 — `needs_review` → `verified_direct` (raw_search_direct_hit; 02【视频同步文稿】人-神农本草经（可打印）.json p58)
- `herb:longyanrou` 龙眼肉 — `needs_review` → `verified_direct` (raw_search_direct_hit; 02【视频同步文稿】人-神农本草经（可打印）.json p242)
- `herb:meiguihua` 玫瑰花 — `needs_review` → `verified_direct` (raw_search_direct_hit; 02【视频同步文稿】人-神农本草经（可打印）.json p121)
- `herb:mugua` 木瓜 — `needs_review` → `verified_direct` (raw_search_direct_hit; 02【视频同步文稿】人-神农本草经（可打印）.json p245)
- `herb:zhushagen` 朱砂根 — `needs_review` → `verified_direct` (raw_search_direct_hit; 02【视频同步文稿】人-神农本草经（可打印）.json p36)
