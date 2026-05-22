#!/usr/bin/env python3
"""导出人工复核模板 JSONL。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data" / "review_queue.jsonl"
OUT = ROOT / "data" / "review_decisions.template.jsonl"


def opt(name, default=None):
    if name not in sys.argv:
        return default
    idx = sys.argv.index(name)
    if idx + 1 >= len(sys.argv):
        return default
    return sys.argv[idx + 1]


def main():
    kind = opt("--kind")
    status = opt("--status")
    limit = int(opt("--limit", 50))
    rows = []
    with QUEUE.open(encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            if kind and item.get("kind") != kind:
                continue
            if status and item.get("review_status") != status:
                continue
            rows.append({
                "kind": item.get("kind"),
                "item_id": item.get("item_id"),
                "name": item.get("name"),
                "decision": "pending",
                "source_ref": None,
                "reviewer_note": item.get("reason"),
            })
            if len(rows) >= limit:
                break
    with OUT.open("w", encoding="utf-8") as out:
        for row in rows:
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"wrote {OUT}")
    print(f"items: {len(rows)}")


if __name__ == "__main__":
    main()
