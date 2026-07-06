# jianghuang 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/jianghuang.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 71 行
- **条目：** 姜黄

## 当前文件概况

当前条目为 herb，frontmatter `trace_status: verified`，有 `source_refs`。正文来源摘录实际围绕《伤寒论》“干姜黄连黄芩人参汤”，p11 缺失 `properties` 与 `meridian`。

## 来源 / FTS 摘要

- `herb_index.jsonl` / `verified_sources.jsonl`：`source_quality_level=verified_direct`，引用 `桂林古本伤寒杂病论 .json`，page_num 为 null。
- 主引用里的“姜黄”来自“干姜黄芩黄连人参汤/干姜黄连黄芩人参汤”的连续字串，不是药材“姜黄”。
- `herb_sources.jsonl` 有 5 个候选命中，但均应警惕干姜、黄芩、黄连相邻字串误切。
- `source_fts.sqlite` 只读检索“姜黄”无命中。

## 是否直接支撑缺失字段

- properties：不支撑。
- meridian：不支撑。

## 修改 / 不修改理由

本轮不补写字段。当前 verified 来源属于 false positive / 分词串联污染，不应支撑姜黄条目任何医学字段。

## 未决问题

- 建议后续协同降级 `trace_status` 或重入 no_source/external source 流程，并清理 Markdown、`herb_index`、`verified_sources` 中的误引用。

## R19 action

- 已执行最小修复：清理 `knowledge/herbs/jianghuang.md` 中“干姜黄连黄芩人参汤”跨词误切的错误 `source_refs` 与无关来源摘录。
- 已同步注册表：`herb_index.jsonl`、`knowledge_completeness.jsonl` 降级为 `trace_status=no_source_found`、`source_quality_level=no_source`，并从 `verified_sources.jsonl` 移除。
- 已加入 no-source / external-source 后续队列；未补写 `properties` 或 `meridian`。
