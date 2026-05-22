#!/usr/bin/env python3
"""P4-A：导入人工复核模板到 review_decisions.jsonl。"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DECISIONS = DATA / "review_decisions.jsonl"


def load_jsonl(path: Path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: python3 scripts/review_import.py <template.jsonl>")
    input_path = Path(sys.argv[1])
    if not input_path.is_absolute():
        input_path = ROOT / input_path
    existing = load_jsonl(DECISIONS)
    by_key = {(r.get("kind"), r.get("item_id")): r for r in existing}
    imported = 0
    skipped = 0
    for row in load_jsonl(input_path):
        decision = row.get("decision")
        if decision in {None, "", "pending"}:
            skipped += 1
            continue
        key = (row.get("kind"), row.get("item_id"))
        normalized = dict(row)
        normalized.setdefault("reviewed_at", date.today().isoformat())
        normalized.setdefault("reviewer", "manual")
        source_ref = normalized.pop("source_ref", None)
        if source_ref:
            normalized.setdefault("source_file", source_ref.get("source_file"))
            normalized.setdefault("page_num", source_ref.get("page_num"))
            normalized.setdefault("quote", source_ref.get("quote"))
        by_key[key] = normalized
        imported += 1
    with DECISIONS.open("w", encoding="utf-8") as out:
        for row in sorted(by_key.values(), key=lambda r: (r.get("kind") or "", r.get("item_id") or "")):
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"wrote {DECISIONS}")
    print(f"imported: {imported}, skipped_pending: {skipped}, total: {len(by_key)}")


if __name__ == "__main__":
    main()
