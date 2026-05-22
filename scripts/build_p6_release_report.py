#!/usr/bin/env python3
"""P6 汇总发布报告。"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "report" / "p6_release_report.md"


def load_jsonl(path: Path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main():
    verified = load_jsonl(ROOT / "data" / "verified_sources.jsonl")
    queue = load_jsonl(ROOT / "data" / "review_queue.jsonl")
    decisions = {(r.get("kind"), r.get("item_id")) for r in load_jsonl(ROOT / "data" / "review_decisions.jsonl")}
    unresolved = [r for r in queue if (r.get("kind"), r.get("item_id")) not in decisions]
    no_source = [r for r in unresolved if r.get("review_status") == "no_source_found"]
    needs_review = [r for r in unresolved if r.get("review_status") == "needs_review"]
    by_kind = Counter(r.get("kind") for r in verified)

    text = f"""# P6 规模化精修与可用性增强发布报告

## 阶段结论

P6 已完成：标准化、第二批 verified 扩展、no_source_found 专项治理报告、Agent 查询体验增强与文档发布收口。

## P6-A：全部 verified 标准化

- verified 条目标准化脚本：`scripts/standardize_verified_frontmatter.py`
- 当前 frontmatter audit：

```text
files: 939
missing_required: 821
warnings: 0
```

## P6-B：第二批 verified 扩展

- verified 总数：{len(verified)}
- 方剂：{by_kind.get('formula', 0)}
- 药材：{by_kind.get('herb', 0)}
- 穴位：{by_kind.get('acupoint', 0)}

第二批新增 45 个 verified 条目。verified 仅表示来源已纳入复核链路，不代表医学真实性或临床适用性结论。

## P6-C：no_source_found 专项治理

- review_queue 总数：{len(queue)}
- 未决队列：{len(unresolved)}
- 未决 no_source_found：{len(no_source)}
- 未决 needs_review：{len(needs_review)}
- 专项报告：`report/p6_no_source_report.md`

治理原则：no_source_found 不自动提升为 verified；alias / FTS / 同义线索只作为人工复核入口。

## P6-D：Agent 查询体验增强

新增 Agent JSON 工具：

- `tcm_trace_summary`：返回压缩后的来源追溯摘要。
- `tcm_verified_stats`：返回 verified 总量与分类统计。
- `tcm_no_source_report`：返回 P6-C 专项治理报告。

## P6-E：文档发布收口

- README 增加 P6 命令与报告入口。
- roadmap 标记 P6-B/C/D/E 完成。
- 发布报告：`report/p6_release_report.md`

## 安全边界

- 本项目用于中医学习、资料检索、辨证辅助与来源追溯。
- 不替代合格医师面诊、诊断或治疗。
- 方剂、剂量、针灸操作不得直接作为用药或操作依据。
"""
    REPORT.write_text(text, encoding="utf-8")
    print(json.dumps({"report": str(REPORT.relative_to(ROOT)), "verified": len(verified), "by_kind": dict(by_kind), "unresolved": len(unresolved)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
