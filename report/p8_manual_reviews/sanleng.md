# sanleng 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/sanleng.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 130 行
- **条目：** 三棱

## 当前文件概况

当前条目为 herb，trace_status 为 `verified`。p11 缺失字段为 `properties, meridian`。正文仅保留基础信息和来源摘录。

## 来源 / FTS 摘要

source_refs 指向倪海厦人纪系列之神农本草经 page 30，但该处是玉竹/萎蕤产地描述“地下茎粗大有三棱”，不是三棱药材专条。FTS 大量命中针灸“三棱针”、京三棱十八反等，均非本药专条。

## 是否直接支撑缺失字段

不支撑。当前来源属于名称形容词/器具/相邻语境 false positive，不支撑三棱性味归经。

## 修改 / 不修改理由

不修改正文；正文目前未扩写未验证医学内容。建议后续将 source boundary 降级为 false_positive。

## 未决问题

需要独立三棱药材来源；当前 verified_direct 应人工复核降级。
