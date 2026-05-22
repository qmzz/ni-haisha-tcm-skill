#!/usr/bin/env python3
"""生成 review 进度报告。"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "review_progress.md"


def load(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def main():
    REPORT.parent.mkdir(exist_ok=True)
    queue = load(DATA / "review_queue.jsonl")
    decisions = load(DATA / "review_decisions.jsonl")
    verified = load(DATA / "verified_sources.jsonl")
    q = Counter((r.get("kind"), r.get("review_status")) for r in queue)
    d = Counter((r.get("kind"), r.get("decision")) for r in decisions)
    decided_keys = {(r.get("kind"), r.get("item_id")) for r in decisions}
    pending = [r for r in queue if (r.get("kind"), r.get("item_id")) not in decided_keys]
    lines = ["# Review 进度报告", "", f"- review_queue：{len(queue)}", f"- review_decisions：{len(decisions)}", f"- verified_sources：{len(verified)}", f"- pending_without_decision：{len(pending)}", "", "## Queue 分布", "", "| kind | status | count |", "|------|--------|------:|"]
    for (kind, status), count in sorted(q.items()):
        lines.append(f"| {kind} | {status} | {count} |")
    lines += ["", "## Decision 分布", "", "| kind | decision | count |", "|------|----------|------:|"]
    for (kind, decision), count in sorted(d.items()):
        lines.append(f"| {kind} | {decision} | {count} |")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
