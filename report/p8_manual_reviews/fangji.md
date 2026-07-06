# fangji 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/fangji.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 41 行
- **条目：** 防己

## 当前文件概况

文件为 P17 content quality verified 条目，P11 标记缺失 `meridian`。frontmatter source_ref 与正文开头仍有龙胆草段尾，但来源摘录中也包含防己直接条目片段。

## 来源 / FTS 摘要

FTS 检索“防己”命中《神农本草经》91 页，直接条目提到木防己、辛、寒凉、通腠理、利膀胱小便、下焦湿热等。未见明确归经字段。另有防风/防己黄芪汤相关语境。

## 核查结论

不补 `meridian`。现有条目有直接防己来源，但 source_ref 前部混有龙胆草，应后续清理 source boundary。

## 修改/不修改理由

本轮未改正文。归经无直接来源；同时需要先清理 source_ref 再做结构字段同步。

## 未决问题

建议后续将 source_ref 改为从“一百九十四这个防己...”起的干净片段。