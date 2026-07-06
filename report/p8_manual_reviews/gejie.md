# gejie 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/gejie.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 49 行
- **条目：** 蛤蚧

## 当前文件概况

当前条目为 herb，frontmatter `trace_status: verified`，有 `source_refs`，正文含安全边界、基础信息、倪师讲解和 P16 扩展摘录。`knowledge_completeness` 显示缺失 `properties` 与 `meridian`。

## 来源 / FTS 摘要

- `herb_index.jsonl` / `verified_sources.jsonl`：`source_quality_level=verified_direct`，引用 `神农本草经.json`，page_num 为 null。
- 引用内容主要是石龙子/蜥蜴/守宫相关名物训诂，中间提到“广雅云：蛤蚧……蜥蜴也”。
- `herb_sources.jsonl` 有 2 个候选命中，均在 `神农本草经.json`，后一条已跨到木虻条目。
- `source_fts.sqlite` 只读检索“蛤蚧”命中 `神农本草经.json` page 26，同样是名物训诂语境。

## 是否直接支撑缺失字段

- properties：不支撑。未见蛤蚧性味原文。
- meridian：不支撑。未见蛤蚧归经原文。

## 修改 / 不修改理由

本轮不补写字段。现有来源可证明“蛤蚧”一词在语料中出现，但边界属于石龙子条目名物训诂，不足以支撑蛤蚧条目的性味、归经或现代药材内容。

## 未决问题

- P16 扩展摘录明显跨到木虻等相邻条目，建议后续做 source boundary 清理。
- verified 状态是否应保留为“名称命中”而非“条目直接来源”，需要后续统一规则。

