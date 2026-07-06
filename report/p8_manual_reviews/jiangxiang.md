# jiangxiang 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/jiangxiang.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 72 行
- **条目：** 降香

## 当前文件概况

当前条目为 herb，frontmatter `trace_status: no_source_found`，有 `external_reference_required: true` 与 `no_source_policy: keep_boundary_until_traceable_source`。p11 缺失字段为 `[properties, meridian]`。缺失性味与归经，内部语料无命中；既有正文已写 FTS/LIKE 无命中。

## 来源 / FTS 摘要

- `herb_index.jsonl`：`source_quality_level=no_source`，`source_refs=[]`。
- `herb_sources.jsonl`：`status=no_source_found`，`source_hits=[]`。
- `no_source_classification.jsonl`：`review_status=no_source_found`。
- `source_fts.sqlite` 只读检索“降香”无命中。

## 是否直接支撑缺失字段

当前无内部来源直接支撑 p11 所列缺失字段；若 p11 未列缺失字段，现有医学字段也未被内部来源直接支撑。

## 修改 / 不修改理由

不修改正文，不从模型记忆或常识补写。no_source 条目只能保留边界或进入外部权威来源流程。

## 未决问题

- 后续如保留或提升现有医学字段，需逐条补充白名单外部权威 `source_refs`。
- 若正文存在“内容来源于倪海厦老师教学资料”或伪引语表达，应在后续边界治理中统一降噪。
