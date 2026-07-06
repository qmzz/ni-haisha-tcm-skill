# mengshi 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/mengshi.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 107 行
- **条目：** 礞石

## 当前文件概况

当前条目为 herb，trace_status 为 `verified`。p11 缺失字段为 `properties, meridian`。正文主要收录倪师谈顽痰、礞石滚痰丸、控涎丹、天南星等片段。

## 来源 / FTS 摘要

source_refs 指向 02 神农本草经 page 278。FTS 仅命中“礞石滚痰丸”这一方名语境，后文实际讲解重心转为天南星的味苦、温、有大毒及祛风湿顽痰。

## 是否直接支撑缺失字段

不直接支撑。现有来源只旁及“礞石滚痰丸”，未给出礞石本药性味或归经。

## 修改 / 不修改理由

不修改正文；当前内容是来源摘录式记录，虽边界偏宽，但没有新增未验证医学断语。不能据此补 properties/meridian。

## 未决问题

需另找礞石本草专条或外部权威来源；建议后续将当前 source boundary 标记为 contextual_mention，而非支撑缺字段的 verified_direct。
