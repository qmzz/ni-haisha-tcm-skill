# baihuasheshecao 手工复核记录

- **复核时间：** 2026-07-06
- **当前文件：** `knowledge/herbs/baihuasheshecao.md`
- **队列位置：** `data/review_queue.jsonl` 第 12 行
- **条目：** 白花蛇舌草

## 当前文件概况

当前条目为 `trace_status: verified`，frontmatter 指向 `倪海夏-汉唐中医方剂讲解.json` 第 58 页。正文还包含多个“来源摘录”片段，其中部分片段只是“白花/白花蛇”等邻近词或 OCR 片段，不足以支撑白花蛇舌草专门内容。

## 查到的来源 / 引用摘要

1. `data/review_queue.jsonl`
   - `review_status=needs_review`
   - `quality_score=59`
   - 候选为 exact-name「白花蛇舌草」命中
2. `data/herb_sources.jsonl`
   - 同一候选：`倪海夏-汉唐中医方剂讲解.json` 第 58 页
   - 语境为批评肝炎/胆结石治疗中使用半边莲、白花蛇舌草等清热药
3. `data/herb_index.jsonl` / `data/knowledge_completeness.jsonl`
   - `trace_status=verified`
   - `source_quality_level=verified_direct`
   - completeness 仍缺 `properties`、`meridian`
4. `data/source_fts.sqlite`
   - FTS MATCH 对长词无额外命中；只读 LIKE 可复现第 58 页 exact-name 片段

## 修改点

- 在 P5 来源追溯状态增加 P8 手工复核说明。
- 在正文增加“来源边界说明（P8 手工复核）”，限定该引用只支撑提及，不支撑本草学字段。

## 保留边界

- 保留 `trace_status: verified` 作为“内部语料 exact-name 提及可追溯”。
- 不把现有来源扩大为对白花蛇舌草功效、主治或来源字段的验证。
- 不删除既有摘录，但明确其质量边界。

## 下一步

需要对“神农本草经”来源字段、功效主治、性味归经另行引入权威来源或更直接内部来源进行核验。
