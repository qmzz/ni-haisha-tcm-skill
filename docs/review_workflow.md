# Review Workflow

P4 后，复核闭环如下：

```text
review_queue.jsonl
  ↓ review-next / review-export
review_decisions.template.jsonl
  ↓ 人工编辑 decision/source_ref
review-import
  ↓
review_decisions.jsonl
  ↓ review-apply
verified_sources.jsonl + review_progress.md
```

## 命令

```bash
python3 cli.py review-next --kind herb --status needs_review --limit 10
python3 cli.py review-export --kind herb --status no_source_found --limit 50
python3 cli.py review-import data/review_decisions.template.jsonl
python3 cli.py review-apply
python3 cli.py review-stats
```

## decision 取值

- `pending`：默认，不导入。
- `verified`：人工确认来源有效。
- `rejected`：候选无效。
- `needs_more_context`：需要更多上下文。
- `alias_candidate`：疑似异名候选。

## 原则

- 只有 `verified` 且带来源字段的决策会进入 `verified_sources.jsonl`。
- `review-import` 会以 `kind + item_id` 覆盖旧决策。
- `review-apply` 可重复执行。
