#!/usr/bin/env python3
"""构建穴位结构化索引。

输出：data/acupoint_index.jsonl
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict

ROOT = Path(__file__).resolve().parents[1]
ACUPOINT_DIR = ROOT / "knowledge" / "acupoints"
DATA_DIR = ROOT / "data"


def first_heading(text: str) -> str:
    m = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
    return m.group(1).strip() if m else ""


def clean_title(title: str) -> str:
    title = re.sub(r"\s*\([^)]*\)\s*$", "", title).strip()
    if title.endswith("穴") and len(title) > 1:
        title = title[:-1]
    return title


def extract_bold_field(text: str, field: str) -> str:
    m = re.search(rf"\*\*{re.escape(field)}：\*\*\s*([^\n]+)", text)
    return m.group(1).strip() if m else ""


def load_sources() -> Dict[str, Dict]:
    path = DATA_DIR / "acupoint_sources.jsonl"
    if not path.exists():
        raise SystemExit("missing data/acupoint_sources.jsonl, run: python3 scripts/build_acupoint_sources.py")
    items = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            items[record["acupoint_id"]] = record
    return items


def main():
    DATA_DIR.mkdir(exist_ok=True)
    source_map = load_sources()
    out_path = DATA_DIR / "acupoint_index.jsonl"
    count = 0
    with out_path.open("w", encoding="utf-8") as out:
        for path in sorted(ACUPOINT_DIR.glob("*.md")):
            if "index" in path.name:
                continue
            text = path.read_text(encoding="utf-8")
            acupoint_id = path.stem
            title = first_heading(text) or acupoint_id
            source_hits = source_map.get(acupoint_id, {}).get("source_hits", [])
            record = {
                "acupoint_id": acupoint_id,
                "name": clean_title(title),
                "display_name": title,
                "file": str(path.relative_to(ROOT)),
                "meridian": extract_bold_field(text, "归经"),
                "location": extract_bold_field(text, "定位"),
                "attributes": extract_bold_field(text, "属性"),
                "trace_status": "candidate" if source_hits else "no_source_found",
                "source_refs": source_hits[:3],
            }
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1
    print(f"wrote {out_path}")
    print(f"acupoint records: {count}")


if __name__ == "__main__":
    main()
