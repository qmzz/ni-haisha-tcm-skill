#!/usr/bin/env python3
"""P19 reconcile verified source registry and completeness rows.

This script fixes contradictions between:
- data/knowledge_completeness.jsonl
- data/verified_sources.jsonl
- data/herb_index.jsonl
- Markdown frontmatter

Rules:
1. If Markdown frontmatter is verified and has non-empty source_refs, add/sync it
   into verified_sources and herb_index.
2. If Markdown frontmatter is not verified/no source_refs, do not promote it;
   downgrade the stale knowledge_completeness row to the frontmatter/index state.

This is trace registry synchronization only. It does not validate medical truth or
rewrite medical claims.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REVIEWED_AT = "2026-05-27"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---", 4)
    return text[4:end] if end >= 0 else ""


def scalar(fm: str, key: str) -> str:
    m = re.search(rf'^\s*{re.escape(key)}\s*:\s*(.*?)\s*$', fm, re.M)
    if not m:
        return ""
    return m.group(1).strip().strip('"\'')


def source_refs(fm: str) -> list[dict[str, Any]]:
    if re.search(r'^\s*source_refs:\s*\[\]\s*$', fm, re.M):
        return []
    refs: list[dict[str, Any]] = []
    starts = [m.start() for m in re.finditer(r'^\s*-\s+source_file:\s*"[^"]+"\s*$', fm, re.M)]
    for idx, start in enumerate(starts):
        end = starts[idx + 1] if idx + 1 < len(starts) else len(fm)
        block = fm[start:end]
        sf = re.search(r'^\s*-\s+source_file:\s*"(?P<v>[^"]+)"\s*$', block, re.M)
        pg = re.search(r'^\s+page_num:\s*(?P<v>\d+|null)\s*$', block, re.M)
        qt = re.search(r'^\s+quote:\s*"(?P<v>.*?)"\s*$', block, re.M | re.S)
        if not sf or not qt:
            continue
        page_raw = pg.group("v") if pg else "null"
        refs.append({
            "source_file": sf.group("v"),
            "page_num": None if page_raw == "null" else int(page_raw),
            "quote": qt.group("v"),
            "reviewer": "p19_registry_sync",
            "reviewed_at": REVIEWED_AT,
        })
    return refs


def main() -> int:
    completeness = load_jsonl(DATA / "knowledge_completeness.jsonl")
    verified_rows = load_jsonl(DATA / "verified_sources.jsonl")
    verified_by_key = {(row.get("kind"), row.get("item_id")): row for row in verified_rows}
    herb_rows = load_jsonl(DATA / "herb_index.jsonl")
    herb_by_id = {row.get("herb_id"): row for row in herb_rows}

    added = 0
    downgraded = 0
    updated_herb_index = 0
    touched_ids: set[str] = set()

    for row in completeness:
        if row.get("kind") != "herb":
            continue
        key = (row.get("kind"), row.get("item_id"))
        if row.get("trace_status") != "verified" or key in verified_by_key:
            continue

        path = ROOT / row["file"]
        fm = frontmatter(path.read_text(encoding="utf-8"))
        fm_trace = scalar(fm, "trace_status")
        fm_review = scalar(fm, "review_status")
        refs = source_refs(fm)
        herb_id = row["item_id"]

        if fm_trace == "verified" and refs:
            new_row = {
                "kind": "herb",
                "item_id": herb_id,
                "name": row["name"],
                "file": row["file"],
                "trace_status": "verified",
                "source_refs": refs,
                "notes": "P19 registry sync from verified Markdown frontmatter; traceability only, not medical validation.",
            }
            verified_rows.append(new_row)
            verified_by_key[key] = new_row
            added += 1
            if herb_id in herb_by_id:
                herb_by_id[herb_id]["trace_status"] = "verified"
                herb_by_id[herb_id]["source_refs"] = refs
                herb_by_id[herb_id].pop("source_scope", None)
                herb_by_id[herb_id].pop("external_reference_required", None)
                updated_herb_index += 1
            touched_ids.add(herb_id)
        else:
            # Completeness row is stale; follow Markdown/frontmatter and index.
            index_row = herb_by_id.get(herb_id, {})
            status = fm_trace or index_row.get("trace_status") or "no_source_found"
            row["trace_status"] = status
            row["frontmatter_trace_status"] = fm_trace or status
            row["verified_in_registry"] = False
            row["review_status"] = fm_review or index_row.get("trace_status") or status
            row["quality_tier"] = "needs_source" if status == "no_source_found" else "needs_review"
            row["has_source_refs"] = bool(refs)
            row["source_policy"] = "p19_reconciled_to_frontmatter_not_verified"
            downgraded += 1
            touched_ids.add(herb_id)

    verified_rows.sort(key=lambda r: (str(r.get("kind")), str(r.get("item_id"))))
    write_jsonl(DATA / "verified_sources.jsonl", verified_rows)
    write_jsonl(DATA / "herb_index.jsonl", herb_rows)
    write_jsonl(DATA / "knowledge_completeness.jsonl", completeness)

    print(json.dumps({
        "added_verified_sources": added,
        "downgraded_stale_completeness": downgraded,
        "updated_herb_index": updated_herb_index,
        "touched_ids": sorted(touched_ids),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
