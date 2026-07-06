# baijiangcao 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/baijiangcao.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 7 行
- **条目：** 败酱草

## 当前文件概况

文件为 verified 药材条目，frontmatter 有 `性味: 辛苦微寒`、`功效: 清热解毒，消痈排脓，祛瘀止痛` 与 `source_refs`。P11 队列标记缺失字段为 `meridian`。

## 来源 / FTS 摘要

`herb_index` 与 `knowledge_completeness` 均为 `verified_direct`，但 `meridian=null`。FTS 检索“败酱草”命中《神农本草经》216-217 页，内容集中在本经原文、鹿肠别名、腹膜炎/肠痈/脓疡等讲解，未见明确归经字段。

## 核查结论

现有来源支撑败酱草条目提及及部分功效语境，但不直接支撑归经。不能凭通用中药知识补 `meridian`。

## 修改/不修改理由

本轮未改知识正文。缺失字段属于来源未直接支撑项，按 P11 要求“不作无来源扩写”。

## 未决问题

若后续要补归经，应引入可核验的药典/现代中药学或经典本草来源，并单独记录 source_ref。