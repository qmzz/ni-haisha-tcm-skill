# guadi 手工复核记录

- **复核时间：** 2026-07-07
- **当前文件：** `knowledge/herbs/guadi.md`
- **队列位置：** `data/p11_content_quality_queue.jsonl` 第 52 行
- **条目：** 瓜蒂

## 当前文件概况

当前条目为 herb，frontmatter `trace_status: verified`，有 `source_refs`，正文含完整倪师讲解摘录。`knowledge_completeness` 显示 `properties=true`、`meridian=false`。

## 来源 / FTS 摘要

- `herb_index.jsonl` / `verified_sources.jsonl`：`source_quality_level=verified_direct`，引用 `02【视频同步文稿】人-神农本草经（可打印）.json` page 174。
- 引用直接出现瓜蒂，含“味苦寒”“主大水，身面四肢浮肿”“吐法”“瓜蒂散”等讲解。
- `herb_sources.jsonl` 有候选命中 1 条。
- `source_fts.sqlite` 只读检索“瓜蒂”有多条命中，包括同步文稿 page 174、金匮要略 page 70、人纪神农本草经 page 73。

## 是否直接支撑缺失字段

- meridian：不支撑。已查来源可支撑性味与功效/用法，但未见明确归经。

## 修改 / 不修改理由

不修改 Markdown 或 index。p11 缺的是 meridian，而原始来源未直接写归经；不得据药性理论推断补写。

## 未决问题

- 无需补写归经；若后续外部权威来源提供归经，应单独标注外部来源，不应混入 verified_direct 内部语料字段。

