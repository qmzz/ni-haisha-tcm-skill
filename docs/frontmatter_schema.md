# Frontmatter Schema

知识文件 frontmatter 用于表达追溯状态与治理元数据，不承载新的医学结论。

## 最小字段

```yaml
---
title: 桂枝汤
kind: formula
trace_status: verified
---
```

`kind` 可取：

- `formula`
- `herb`
- `acupoint`

`trace_status` 可取：

- `verified`：人工复核通过，且应有 `source_refs`
- `candidate`：有候选来源但未人工确认
- `needs_review`：候选存在但需要复核
- `no_source_found`：暂未找到来源

## verified 推荐字段

```yaml
---
title: 桂枝汤
kind: formula
trace_status: verified
source_refs:
  - source_file: 04【视频同步文稿】人-伤寒论（可打印）.json
    page_num: 11
    quote: 太阳中风...桂枝汤主之
aliases:
  - 桂枝汤方
review:
  status: verified
  reviewed_at: 2026-05-22
  reviewer: manual
safety:
  medical_disclaimer_required: true
---
```

## 原则

- 不自动把 candidate 提升为 verified。
- 不通过 frontmatter 自动改写医学正文。
- `verified` 必须可以追溯到原始 JSON 或人工复核记录。
- 医学相关输出仍必须包含安全免责声明。
