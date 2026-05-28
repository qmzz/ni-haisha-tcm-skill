#!/usr/bin/env python3
"""P25/P5-A review verified_contextual rows.

Conservative mechanical triage:
- Promote to verified_direct only when the quote has clear direct markers near the item name.
- Demote to needs_review when quote is empty, obvious TOC/JSON/OCR fragment, or does not mention the item name.
- Keep verified_contextual otherwise.

This audits trace relation quality only; it does not judge medical truth.
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p25_verified_contextual_review.md"
POLICY = "source_quality_is_traceability_only_not_medical_validation"

INDEX_FILES = [
    ("herb", "herb_id", DATA / "herb_index.jsonl"),
    ("acupoint", "acupoint_id", DATA / "acupoint_index.jsonl"),
]

BAD_PATTERNS = [
    re.compile(r"\{\s*\"page_num\""),
    re.compile(r"\.\.\.\.\."),
    re.compile(r"第\s*\d+\s*页\s*共"),
    re.compile(r"【【|】】|����"),
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def quote_text(row: dict[str, Any]) -> str:
    refs = row.get("source_refs") or []
    return "\n".join((r.get("quote") or "") for r in refs[:3]).strip()


def has_bad_quote(quote: str) -> bool:
    if not quote or len(quote.strip()) < 20:
        return True
    return any(p.search(quote) for p in BAD_PATTERNS)


def near_name(quote: str, name: str, window: int = 80) -> str:
    pos = quote.find(name)
    if pos < 0:
        return ""
    return quote[max(0, pos - window): pos + len(name) + window]


def is_direct(kind: str, name: str, quote: str) -> bool:
    if not name or name not in quote:
        return False
    snippet = near_name(quote, name, 100)
    if kind == "herb":
        markers = [
            f"【{name}", f"、{name}", f"，{name}", f" {name}",
            f"{name}为", f"{name}是", f"{name}味", f"{name}性", f"{name}主",
            "【性味】", "【主治】", "【本经原文】", "【禁忌】", "【用量】",
        ]
        return any(m in snippet for m in markers)
    if kind == "acupoint":
        markers = [
            f"{name}穴", f"叫{name}", f"就是{name}", f"称{name}", f"、{name}", f"，{name}",
            "下针", "针", "灸", "寸", "穴道", "经", "络穴", "俞", "募穴",
        ]
        return any(m in snippet for m in markers)
    return False


def review_row(row: dict[str, Any]) -> tuple[str, str]:
    kind = row.get("kind") or ""
    name = row.get("name") or ""
    quote = quote_text(row)
    if has_bad_quote(quote):
        return "needs_review", "empty_or_dirty_quote"
    if name not in quote:
        return "needs_review", "quote_does_not_mention_item_name"
    if is_direct(kind, name, quote):
        return "verified_direct", "direct_marker_near_item_name"
    return "verified_contextual", "mention_without_direct_marker"


def main() -> int:
    verified = load_jsonl(DATA / "verified_sources.jsonl")
    decisions = []
    counter = Counter()
    by_kind = defaultdict(Counter)
    verified_by_key = {}

    for row in verified:
        if row.get("source_quality_level") == "verified_contextual":
            new_level, reason = review_row(row)
            old_level = row.get("source_quality_level")
            if new_level != old_level:
                row["source_quality_level"] = new_level
                row["source_quality_policy"] = POLICY
                row["p5a_review_reason"] = reason
                decisions.append({
                    "kind": row.get("kind"),
                    "item_id": row.get("item_id"),
                    "name": row.get("name"),
                    "from": old_level,
                    "to": new_level,
                    "reason": reason,
                })
            else:
                row["p5a_review_reason"] = reason
            counter[row.get("source_quality_level")] += 1
            by_kind[row.get("kind")][row.get("source_quality_level")] += 1
        verified_by_key[(row.get("kind"), row.get("item_id"))] = row

    write_jsonl(DATA / "verified_sources.jsonl", verified)

    # Sync indexes from verified registry.
    for kind, id_key, path in INDEX_FILES:
        rows = load_jsonl(path)
        for row in rows:
            key = (kind, row.get(id_key))
            if key in verified_by_key:
                v = verified_by_key[key]
                row["trace_status"] = "verified"
                row["source_quality_level"] = v.get("source_quality_level")
                row["source_quality_policy"] = POLICY
                if v.get("p5a_review_reason"):
                    row["p5a_review_reason"] = v["p5a_review_reason"]
                row["source_refs"] = v.get("source_refs", row.get("source_refs", []))
        write_jsonl(path, rows)

    # Sync completeness from verified registry.
    rows = load_jsonl(DATA / "knowledge_completeness.jsonl")
    for row in rows:
        key = (row.get("kind"), row.get("item_id"))
        if key in verified_by_key:
            v = verified_by_key[key]
            row["trace_status"] = "verified"
            row["verified_in_registry"] = True
            row["source_quality_level"] = v.get("source_quality_level")
            row["source_quality_policy"] = POLICY
            if v.get("p5a_review_reason"):
                row["p5a_review_reason"] = v["p5a_review_reason"]
    write_jsonl(DATA / "knowledge_completeness.jsonl", rows)

    report_lines = [
        "# P25 / P5-A verified_contextual Review",
        "",
        "本报告记录对 `verified_contextual` 的机械保守复核。",
        "",
        "> 边界：只评估来源片段与条目名的关系质量，不判断医学真实性、临床适用性或疗效。",
        "",
        "## Summary",
        "",
        f"- Changed rows: {len(decisions)}",
        "",
        "## Contextual bucket after review",
        "",
        "| kind | level | count |",
        "|---|---|---:|",
    ]
    for kind, c in sorted(by_kind.items()):
        for level, count in sorted(c.items()):
            report_lines.append(f"| {kind} | `{level}` | {count} |")
    report_lines += ["", "## Decisions", ""]
    if decisions:
        for d in decisions:
            report_lines.append(f"- `{d['kind']}:{d['item_id']}` {d['name']} — `{d['from']}` → `{d['to']}` ({d['reason']})")
    else:
        report_lines.append("No changes.")
    REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "changed": len(decisions),
        "decisions_by_to": dict(Counter(d["to"] for d in decisions)),
        "contextual_after_by_kind": {k: dict(v) for k, v in by_kind.items()},
        "report": str(REPORT.relative_to(ROOT)),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
