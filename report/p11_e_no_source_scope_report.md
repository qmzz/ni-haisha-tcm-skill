# P11-E no_source_found scope 边界报告

- apply: True
- no_source_found total: 133
- changed_files: 0
- errors: 0

## 分类

- acupoint: 15
- herb: 118

## 边界策略

这些条目在当前倪海厦原始 JSON 与既有别名扩展检索中无明确命中。
本阶段不凭模型记忆补写医学正文，不改变 trace_status；仅补充 frontmatter scope 元数据。
若后续要提升，必须引入明确可追溯的外部来源。

新增/规范化 frontmatter:

```yaml
source_scope: "not_in_nihaixia_source"
external_reference_required: true
no_source_policy: "keep_boundary_until_traceable_source"
```

## 变更文件

