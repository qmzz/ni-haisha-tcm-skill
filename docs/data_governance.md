# Data Governance

## 数据来源

第一来源：

```text
project/nihaixia/*.json
```

所有知识补全必须来自：

- 原始 JSON
- 现有知识文件
- 明确可追溯来源
- 人工复核记录

不得凭模型记忆扩写医学内容。

## 状态定义

- `no_source_found`：暂未找到来源。
- `candidate`：有来源候选，但未人工确认。
- `needs_review`：候选存在但质量、上下文或异名关系需复核。
- `verified`：人工确认来源有效。

## 质量评分

候选来源包含：

```json
{
  "quality_score": 80,
  "match_reason": ["matched_exact_name"],
  "risk_flags": [],
  "needs_review_reason": "候选来源需人工复核"
}
```

质量评分用于排序和复核优先级，不等于医学真实性判定。

## Alias 治理

alias 只用于扩大检索召回。

```text
alias hit → candidate / needs_review
```

不能自动提升为 verified。
