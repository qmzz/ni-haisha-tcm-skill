#!/usr/bin/env python3
"""P7-C：第三批高确定性 verified 精修。

约束：
- 只使用现有 index 的首选 source_ref；
- 采用小批量人工白名单；
- verified 仅表示来源追溯链路通过，不代表医学真实性或临床适用性。
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

BATCH = {
    "formula": {
        "index": "formula_index.jsonl",
        "id_key": "formula_id",
        "threshold": 95,
        "reviewer": "p7_batch3_formula_seed",
        "items": [
            "baitouweng_tang",
            "banxia_houpo",
            "dahuang_huanglian",
            "fuling_gancao",
            "fuling_sini",
            "guizhi_fuling",
            "huangqi_jianzhong",
            "jiegeng_tang",
            "mahuang_fuzi_xixin",
            "shaoyao_gancao",
        ],
    },
    "herb": {
        "index": "herb_index.jsonl",
        "id_key": "herb_id",
        "threshold": 95,
        "reviewer": "p7_batch3_herb_seed",
        "items": [
            "aishe",
            "badou",
            "baifan",
            "baiji",
            "baitouweng",
            "baiziren",
            "biejia",
            "cangzhu",
            "cheqianzi",
            "duzhong",
        ],
    },
    "acupoint": {
        "index": "acupoint_index.jsonl",
        "id_key": "acupoint_id",
        "threshold": 80,
        "reviewer": "p7_batch3_acupoint_seed",
        "items": [
            "chengqi",
            "cuanzhu",
            "dadun",
            "daling",
            "danzhong",
            "geshu",
            "gongsun",
            "jianli",
            "jingming",
            "kongzui",
        ],
    },
}


def load_jsonl(path: Path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main():
    decisions_path = DATA / "review_decisions.jsonl"
    existing = load_jsonl(decisions_path)
    by_key = {(r.get("kind"), r.get("item_id")): r for r in existing}
    today = date.today().isoformat()
    summary = {}
    errors = []

    for kind, cfg in BATCH.items():
        index = {r[cfg["id_key"]]: r for r in load_jsonl(DATA / cfg["index"])}
        added = 0
        skipped = 0
        for item_id in cfg["items"]:
            item = index.get(item_id)
            if not item:
                errors.append({"kind": kind, "item_id": item_id, "error": "missing_index_item"})
                skipped += 1
                continue
            refs = item.get("source_refs") or []
            if not refs:
                errors.append({"kind": kind, "item_id": item_id, "error": "missing_source_ref"})
                skipped += 1
                continue
            ref = refs[0]
            if (ref.get("quality_score") or 0) < cfg["threshold"]:
                errors.append({"kind": kind, "item_id": item_id, "error": "quality_below_threshold", "quality_score": ref.get("quality_score")})
                skipped += 1
                continue
            by_key[(kind, item_id)] = {
                "kind": kind,
                "item_id": item_id,
                "name": item.get("name"),
                "file": item.get("file"),
                "decision": "verified",
                "source_file": ref.get("source_file"),
                "page_num": ref.get("page_num"),
                "quote": ref.get("quote"),
                "reviewer": cfg["reviewer"],
                "reviewed_at": today,
                "notes": "P7-C 第三批高确定性 verified 精修；仅确认来源可追溯，不作为医学真实性或临床适用性判定。" + (" 穴位内容仅作学习与来源追溯，不作为针灸操作指导。" if kind == "acupoint" else ""),
                "quality_score": ref.get("quality_score"),
                "match_reason": ref.get("match_reason"),
                "risk_flags": ref.get("risk_flags"),
            }
            added += 1
        summary[kind] = {"requested": len(cfg["items"]), "added_or_updated": added, "skipped": skipped}

    with decisions_path.open("w", encoding="utf-8") as out:
        for row in sorted(by_key.values(), key=lambda r: (r.get("kind") or "", r.get("item_id") or "")):
            out.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(json.dumps({"summary": summary, "errors": errors, "total_decisions": len(by_key)}, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
