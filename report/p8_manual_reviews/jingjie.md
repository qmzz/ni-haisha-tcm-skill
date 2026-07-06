# jingjie 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/jingjie.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 74 行
- **条目：** 荆芥

## 当前文件概况

当前条目为 herb，frontmatter `trace_status: verified`，有 `source_refs`。p11 缺失字段为 `meridian`。正文含多个 02 神农本草经讲解片段，讲假苏/荆芥、味辛性温、发表、祛风理血、发汗退热、皮肤痒疥癣等。

## 来源 / FTS 摘要

- `herb_index.jsonl` / `verified_sources.jsonl` 当前主引用为 `倪海厦人纪系列之神农本草经.json` page 152，但该页是索引/目录式词表，不是直接讲解。
- `herb_sources.jsonl` 当前 `source_hits=[]`，与 verified registry 不一致。
- `source_fts.sqlite` 只读检索“荆芥”有正文命中：`02【视频同步文稿】人-神农本草经（可打印）.json` page 231，内容包括皮肤痒、疥癣、发表等；另有索引页和方剂讲解命中。

## 是否直接支撑缺失字段

- meridian：不支撑。现有正文来源可支撑“味辛性温”等性味/功效语境，但未见明确归经。

## 修改 / 不修改理由

不修改 Markdown 或 index。缺失字段只有归经，内部来源未直接写归经；不得推断补写。另，当前 frontmatter 主 `source_refs` 应后续从目录页替换为 page 231 的直接讲解来源。

## 未决问题

- 后续可同步/修正来源引用边界：优先使用 02 神农本草经 page 231 的直接讲解片段，而不是 `倪海厦人纪系列之神农本草经.json` page 152 目录页。
- 归经仍需外部权威来源或直接原文，不应由本轮补写。
