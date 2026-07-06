# madouling 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/madouling.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 104 行
- **条目：** 马兜铃

## 当前文件概况

当前条目为 herb，trace_status 为 `verified`。p11 缺失字段为 `properties, meridian`。

## 来源 / FTS 摘要

source_refs 指向 02 神农本草经 page 226；LIKE 命中 page 226 与 05金匮约 page 61，内容是倪师讲解防己时顺带提及“马兜铃酸”“马兜铃本身就是中药”，属于防己分辨（木防己 vs 广防己）的语境，非独立马兜铃本草讲解。

## 是否直接支撑缺失字段

不直接支撑性味归经。来源仅涉及药名提及和防己鉴识语境，不含马兜铃性味、归经、功效的专门讲解。

## 修改 / 不修改理由

不修改正文；source boundary 为旁及提及，不可作为药材性味归经依据。

## 未决问题

需独立马兜铃讲解来源才能填补缺失字段；建议后续将 source border 收紧为 contextual_mention，不作为 verified_direct 全文验证。
