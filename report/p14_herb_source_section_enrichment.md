# P14 药材正文来源摘录补强报告

- apply: True
- queue_items: 80
- changed_files: 0
- by_change: `{}`

## 原则

- 只使用现有 `source_refs.quote`。
- 不凭模型记忆补中药性味、归经、剂量或禁忌。
- quote 未明确提供 `归经` 时，不补归经。

## 变更文件

