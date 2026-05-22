# P8-A stale verified frontmatter 修复报告

## 定位

本报告记录 frontmatter 标记为 verified、但未进入 `data/verified_sources.jsonl` registry 的治理不一致条目。修复仅调整治理元数据，不修改医学正文，不把 candidate 自动提升为 verified。

- stale_verified_frontmatter: 0
- changed_files: 0

| kind | item_id | file | target_trace_status | action |
|------|---------|------|---------------------|--------|

## 边界

- 本修复只处理治理元数据一致性。
- 不新增 source_refs，不改医学正文。
- 如需 verified，必须通过人工白名单和 registry 流程进入 `data/verified_sources.jsonl`。
