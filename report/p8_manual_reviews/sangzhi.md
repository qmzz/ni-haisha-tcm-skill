# sangzhi 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/sangzhi.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 129 行
- **条目：** 桑枝

## 当前文件概况

当前条目为 herb，trace_status 为 `verified`。p11 缺失字段为 `meridian`。index 已有 `properties=微苦平`、`effects=祛风湿，利关节`。

## 来源 / FTS 摘要

source_refs 指向倪海厦人纪系列之神农本草经 page 68，但该页实际是桑螵蛸专条中“着生于桑枝上者”。FTS 另命中桂枝条“与桑枝附子牛膝威灵仙同用治关节疼痛”和金匮“桑枝、桂枝进入四肢”语境。

## 是否直接支撑缺失字段

不直接支撑归经。当前 source_ref 是桑螵蛸产地语境，不能支撑桑枝药性或归经；其他命中也只是用药/部位类旁及线索。

## 修改 / 不修改理由

不修改正文；但建议后续收紧 source boundary，避免把桑螵蛸专条误作桑枝来源。

## 未决问题

桑枝需独立来源；当前 verified_direct 可信度不足，建议后续降级或重建 source_refs。
