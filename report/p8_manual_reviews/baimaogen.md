# baimaogen 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/baimaogen.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 9 行
- **条目：** 白茅根

## 当前文件概况

文件为 verified 药材条目，正文已有来源、分类、性味、功效、主治、剂量、禁忌和讲解。P11 队列标记缺失 `meridian`。

## 来源 / FTS 摘要

FTS 检索“白茅根”命中《神农本草经》214 页，包含“味甘，寒，无毒”“利小便”“利水、止血”等讲解。`herb_index` 与 `knowledge_completeness` 也记录 verified，但 `meridian=null`。

## 核查结论

现有来源可支撑白茅根条目和部分性味/功效语境，但未直接给出归经。不能凭模型记忆补 `meridian`。

## 修改/不修改理由

本轮未改知识正文。虽然 source_ref 的 frontmatter quote 较短且正文有更完整摘录，但当前任务重点是 P11 缺字段；归经无直接来源支撑，故不补。

## 未决问题

后续可在清理 source_ref quote 时同步引用更完整的 214 页片段；归经仍需外部权威来源或明确内部来源。