#!/usr/bin/env python3
"""P6-B：第二批高价值条目 verified 决策种子。

原则：
- 只从现有 index 的首选 source_ref 取引用；
- 只验证“来源匹配/可追溯”，不判定医学真实性；
- 采用人工维护的二批白名单，避免把全部 candidate 自动提升为 verified。
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
        "threshold": 70,
        "reviewer": "p6_second_batch_formula_seed",
        "items": [
            "dachaihu_tang",
            "chaihu_guizhi",
            "chaihu_longgu",
            "huanglian_ejiao",
            "danggui_sini",
            "yinchen_hao",
            "gancao_xiexin",
            "fuzi_xiexin",
            "getang_banxia",
            "guizhi_shaoyao",
            "guizhi_qu_shaoyao",
            "fangji_huangqi",
            "gualou_xiebai",
            "houpo_mahuang",
            "danggui_shengjiang",
        ],
    },
    "herb": {
        "index": "herb_index.jsonl",
        "id_key": "herb_id",
        "threshold": 80,
        "reviewer": "p6_second_batch_herb_seed",
        "items": [
            "danggui",
            "fangji",
            "geda",
            "houpo",
            "mangxiao",
            "baizhi",
            "beimu",
            "chuanxiong",
            "chenpi",
            "tinglizi",
            "wumei",
            "xiebai",
            "yinchen",
            "zhishi",
            "zhimu",
        ],
    },
    "acupoint": {
        "index": "acupoint_index.jsonl",
        "id_key": "acupoint_id",
        "threshold": 75,
        "reviewer": "p6_second_batch_acupoint_seed",
        "items": [
            "fengchi",
            "fengfu",
            "yingxiang",
            "renzhong",
            "chengjiang",
            "jiache",
            "xiaguan",
            "jianjing",
            "jianyu",
            "quze",
            "shaohai",
            "shenmen",
            "laogong",
            "houxi",
            "yanglingquan",
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
                "notes": "P6-B 第二批 verified 扩展；仅确认来源可追溯，不作为医学真实性或临床适用性判定。" + (" 穴位内容仅作学习与来源追溯，不作为针灸操作指导。" if kind == "acupoint" else ""),
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
