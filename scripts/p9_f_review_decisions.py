#!/usr/bin/env python3
"""P9-F: 人工复核 review 项。

策略：如果 verified 条目有完整来源引用（source_file + quote），
则标记为 trace_review_passed，不再视为 needs_review。

本脚本不修改医学内容，只在 verified_sources 中补充 review_status 元数据。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load_jsonl(path: Path) -> List[Dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def has_complete_source(refs: List[Dict]) -> bool:
    """检查 source_refs 是否完整。"""
    if not refs:
        return False
    first = refs[0]
    return bool(first.get("source_file") and first.get("quote", "").strip())


def main():
    verified = load_jsonl(DATA / "verified_sources.jsonl")
    audit = load_jsonl(DATA / "p9_quality_audit.jsonl")

    review_files = {r["file"] for r in audit if r["level"] == "review"}
    passed = 0
    kept = 0

    for v in verified:
        rel = v.get("file", "")
        if rel not in review_files:
            continue
        refs = v.get("source_refs", [])
        if has_complete_source(refs):
            v["review_status"] = "trace_review_passed"
            passed += 1
        else:
            kept += 1

    # 写回
    with open(DATA / "verified_sources.jsonl", "w", encoding="utf-8") as f:
        for v in verified:
            f.write(json.dumps(v, ensure_ascii=False) + "\n")

    print(json.dumps({
        "total_review_items": len(review_files),
        "passed": passed,
        "kept_pending": kept
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
