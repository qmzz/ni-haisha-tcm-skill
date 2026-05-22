#!/usr/bin/env python3
"""P5-A：扩展核心方剂 verified review decisions。"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

CORE_FORMULAS = [
    "guizhi_jiagetang",
    "guizhi_houpuxingzi",
    "guizhi_fuzi",
    "getang",
    "dahuoluo_tang",
    "xiaoqinglong_tang",
    "maxing_shigan",
    "wuling_san",
    "zhuling_tang",
    "zhizi_chi",
    "baihu_renshen",
    "tiaoweichengqi",
    "xiaochengqi_tang",
    "taohe_chengqi",
    "didang_tang",
    "sini_tang",
    "lizhong_tang",
    "zhenwu_tang",
    "linggui_zhugan",
    "banxia_xiexin",
]


def load_jsonl(path: Path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def main():
    index = {r["formula_id"]: r for r in load_jsonl(DATA / "formula_index.jsonl")}
    decisions_path = DATA / "review_decisions.jsonl"
    existing = load_jsonl(decisions_path)
    by_key = {(r.get("kind"), r.get("item_id")): r for r in existing}
    today = date.today().isoformat()
    added = 0
    skipped = 0
    for item_id in CORE_FORMULAS:
        item = index.get(item_id)
        if not item:
            skipped += 1
            continue
        refs = item.get("source_refs") or []
        if not refs:
            skipped += 1
            continue
        ref = refs[0]
        if ref.get("quality_score", 0) < 70:
            skipped += 1
            continue
        key = ("formula", item_id)
        by_key[key] = {
            "kind": "formula",
            "item_id": item_id,
            "name": item.get("name"),
            "file": item.get("file"),
            "decision": "verified",
            "source_file": ref.get("source_file"),
            "page_num": ref.get("page_num"),
            "quote": ref.get("quote"),
            "reviewer": "p5_core_formula_seed",
            "reviewed_at": today,
            "notes": "P5-A 核心方剂 verified 扩展；候选来源质量分>=70，后续仍可人工二次复核。",
            "quality_score": ref.get("quality_score"),
            "match_reason": ref.get("match_reason"),
            "risk_flags": ref.get("risk_flags"),
        }
        added += 1
    with decisions_path.open("w", encoding="utf-8") as out:
        for row in sorted(by_key.values(), key=lambda r: (r.get("kind") or "", r.get("item_id") or "")):
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"wrote {decisions_path}")
    print(f"core formulas processed: {len(CORE_FORMULAS)}, added_or_updated: {added}, skipped: {skipped}, total_decisions: {len(by_key)}")


if __name__ == "__main__":
    main()
