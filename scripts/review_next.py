#!/usr/bin/env python3
"""输出下一批待复核条目。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data" / "review_queue.jsonl"
DECISIONS = ROOT / "data" / "review_decisions.jsonl"


def opt(name, default=None):
    if name not in sys.argv:
        return default
    idx = sys.argv.index(name)
    if idx + 1 >= len(sys.argv):
        return default
    return sys.argv[idx + 1]


def load_jsonl(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def main():
    kind = opt("--kind")
    status = opt("--status")
    limit = int(opt("--limit", 10))
    decided = {(d.get("kind"), d.get("item_id")) for d in load_jsonl(DECISIONS)}
    items = []
    for item in load_jsonl(QUEUE):
        if kind and item.get("kind") != kind:
            continue
        if status and item.get("review_status") != status:
            continue
        if (item.get("kind"), item.get("item_id")) in decided:
            continue
        items.append(item)
    print(json.dumps({"count": len(items), "items": items[:limit]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
