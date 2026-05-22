#!/usr/bin/env python3
"""初始化 P2 verified 试点复核决策。

从 P1 生成的 *_index.jsonl 中抽取少量高价值条目的首选来源，生成：
- data/review_decisions.jsonl

注意：这里是 P2 试点种子，后续可人工编辑 decision/quote/source_file/page_num。
"""

import json
from datetime import date
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

PILOT_ITEMS = {
    "formula": ["guizhi_tang", "mahuang_tang", "baihu_tang", "xiaochaihu_tang", "dachengqi_tang"],
    "herb": ["mahuang", "guizhi", "gancao", "shigao", "dahuang"],
    "acupoint": ["baihui", "zusanli", "hegu", "quchi", "sanyinjiao"],
}

CONFIG = {
    "formula": {"path": DATA_DIR / "formula_index.jsonl", "id_key": "formula_id"},
    "herb": {"path": DATA_DIR / "herb_index.jsonl", "id_key": "herb_id"},
    "acupoint": {"path": DATA_DIR / "acupoint_index.jsonl", "id_key": "acupoint_id"},
}


def load_index(kind: str) -> Dict[str, Dict]:
    cfg = CONFIG[kind]
    records = {}
    with cfg["path"].open(encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            records[record[cfg["id_key"]]] = record
    return records


def build_decisions() -> List[Dict]:
    decisions = []
    today = date.today().isoformat()
    for kind, ids in PILOT_ITEMS.items():
        index = load_index(kind)
        id_key = CONFIG[kind]["id_key"]
        for item_id in ids:
            item = index[item_id]
            refs = item.get("source_refs") or []
            ref = refs[0] if refs else {}
            decisions.append({
                "kind": kind,
                "item_id": item_id,
                "name": item.get("name"),
                "file": item.get("file"),
                "decision": "verified" if ref else "no_source",
                "source_file": ref.get("source_file"),
                "page_num": ref.get("page_num"),
                "quote": ref.get("quote"),
                "reviewer": "p2_pilot_seed",
                "reviewed_at": today,
                "notes": "P2 试点 verified 条目；来源仍应支持人工二次复核。",
            })
    return decisions


def main():
    DATA_DIR.mkdir(exist_ok=True)
    out_path = DATA_DIR / "review_decisions.jsonl"
    decisions = build_decisions()
    with out_path.open("w", encoding="utf-8") as out:
        for item in decisions:
            out.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"wrote {out_path}")
    print(f"review decisions: {len(decisions)}")


if __name__ == "__main__":
    main()
