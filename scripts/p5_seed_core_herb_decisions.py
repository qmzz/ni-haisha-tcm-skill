#!/usr/bin/env python3
"""P5-B：扩展核心药材 verified review decisions。"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

CORE_HERBS = [
    "baishao",
    "shengjiang",
    "dazao",
    "banxia",
    "huangqin",
    "huanglian",
    "fuzi",
    "renshen",
    "ganjiang",
    "xixin",
    "xingren",
    "chaihu",
    "fuling",
    "baizhu",
    "zezie",
    "muli",
    "longgu",
]


def load_jsonl(path: Path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def main():
    index = {r["herb_id"]: r for r in load_jsonl(DATA / "herb_index.jsonl")}
    decisions_path = DATA / "review_decisions.jsonl"
    existing = load_jsonl(decisions_path)
    by_key = {(r.get("kind"), r.get("item_id")): r for r in existing}
    today = date.today().isoformat()
    added = 0
    skipped = []
    for item_id in CORE_HERBS:
        item = index.get(item_id)
        if not item:
            skipped.append({"item_id": item_id, "reason": "not_found"})
            continue
        refs = item.get("source_refs") or []
        if not refs:
            skipped.append({"item_id": item_id, "reason": "no_source_ref"})
            continue
        ref = refs[0]
        if ref.get("quality_score", 0) < 80:
            skipped.append({"item_id": item_id, "reason": "quality_below_80", "score": ref.get("quality_score")})
            continue
        key = ("herb", item_id)
        by_key[key] = {
            "kind": "herb",
            "item_id": item_id,
            "name": item.get("name"),
            "file": item.get("file"),
            "decision": "verified",
            "source_file": ref.get("source_file"),
            "page_num": ref.get("page_num"),
            "quote": ref.get("quote"),
            "reviewer": "p5_core_herb_seed",
            "reviewed_at": today,
            "notes": "P5-B 核心药材 verified 扩展；候选来源质量分>=80，后续仍可人工二次复核。",
            "quality_score": ref.get("quality_score"),
            "match_reason": ref.get("match_reason"),
            "risk_flags": ref.get("risk_flags"),
        }
        added += 1
    with decisions_path.open("w", encoding="utf-8") as out:
        for row in sorted(by_key.values(), key=lambda r: (r.get("kind") or "", r.get("item_id") or "")):
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"wrote {decisions_path}")
    print(f"core herbs processed: {len(CORE_HERBS)}, added_or_updated: {added}, skipped: {len(skipped)}, total_decisions: {len(by_key)}")
    if skipped:
        print(json.dumps({"skipped": skipped}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
