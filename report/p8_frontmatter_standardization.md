# P8 Frontmatter 标准化报告

## 任务
为所有知识文件添加基础 frontmatter，确保所有 939 个文件都有完整的 `kind` 和 `trace_status` 字段。

## 结果

- **处理文件数**: 478
- **Verified 文件**: 461（已有完整 frontmatter）
- **新增基础 frontmatter**: 478
  - no_source_found: 184
  - needs_review: 4
  - unverified: 290

### Frontmatter 字段
```yaml
---
title: ""
kind: {herb|acupoint|formula}
trace_status: {verified|needs_review|no_source_found|unverified}
---
```

## 审计结果

- files: 939
- **missing_required: 0**（之前 565/503）
- warnings: 0

## 相关脚本

- `scripts/p8_add_basic_frontmatter.py`: 批量添加基础 frontmatter
  - 默认 dry-run
  - `--apply`: 实际写入
