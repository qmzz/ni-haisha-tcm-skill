#!/usr/bin/env python3
"""根据复核决策生成 verified 来源索引。

输入：data/review_decisions.jsonl
输出：data/verified_sources.jsonl
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def main():
    in_path = DATA_DIR / "review_decisions.jsonl"
    out_path = DATA_DIR / "verified_sources.jsonl"
    if not in_path.exists():
        raise SystemExit("missing data/review_decisions.jsonl, run: python3 scripts/init_review_decisions.py")

    verified = []
    with in_path.open(encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            if item.get("decision") != "verified":
                continue
            if not item.get("source_file") or not item.get("quote"):
                continue
            verified.append({
                "kind": item["kind"],
                "item_id": item["item_id"],
                "name": item["name"],
                "file": item.get("file"),
                "trace_status": "verified",
                "source_refs": [{
                    "source_file": item["source_file"],
                    "page_num": item.get("page_num"),
                    "quote": item["quote"],
                    "reviewer": item.get("reviewer"),
                    "reviewed_at": item.get("reviewed_at"),
                }],
                "notes": item.get("notes"),
            })

    with out_path.open("w", encoding="utf-8") as out:
        for item in verified:
            out.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"wrote {out_path}")
    print(f"verified sources: {len(verified)}")


if __name__ == "__main__":
    main()
