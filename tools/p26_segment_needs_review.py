#!/usr/bin/env python3
"""P26/P5-B segment needs_review rows into actionable subqueues.

No medical content changes. This classifies rows by why the source relation is
not trustworthy enough for verified source-quality use.
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p26_needs_review_segmentation.md"
QUEUE = DATA / "p26_needs_review_segments.jsonl"

DIRTY_PATTERNS = [
    re.compile(r"\.\.\.\.\."),
    re.compile(r"\{\s*\"page_num\""),
    re.compile(r"第\s*\d+\s*页\s*共"),
    re.compile(r"【【|】】|����"),
    re.compile(r"[一二三四五六七八九十〇○零]{4,}[、、，,]"),
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def quote_text(row: dict[str, Any]) -> str:
    refs = row.get("source_refs") or []
    return "\n".join((r.get("quote") or "") for r in refs[:3]).strip()


def segment(row: dict[str, Any]) -> tuple[str, str]:
    name = row.get("name") or ""
    quote = quote_text(row)
    if not quote or len(quote.strip()) < 20:
        return "empty_quote", "source_refs missing or quote too short"
    if any(p.search(quote) for p in DIRTY_PATTERNS):
        return "dirty_quote", "quote appears to be OCR/TOC/JSON/page-fragment residue"
    if name and name not in quote:
        return "name_mismatch", "quote does not contain item name"
    return "weak_context", "quote mentions item but lacks direct source markers"


def main() -> int:
    rows = load_jsonl(DATA / "verified_sources.jsonl")
    queue = []
    counters = Counter()
    by_kind = defaultdict(Counter)
    for row in rows:
        if row.get("source_quality_level") != "needs_review":
            continue
        seg, reason = segment(row)
        row["p5b_review_segment"] = seg
        row["p5b_review_segment_reason"] = reason
        counters[seg] += 1
        by_kind[row.get("kind")][seg] += 1
        refs = row.get("source_refs") or []
        queue.append({
            "kind": row.get("kind"),
            "item_id": row.get("item_id"),
            "name": row.get("name"),
            "file": row.get("file"),
            "source_quality_level": row.get("source_quality_level"),
            "p5a_review_reason": row.get("p5a_review_reason"),
            "p5b_review_segment": seg,
            "p5b_review_segment_reason": reason,
            "source_file": refs[0].get("source_file") if refs else None,
            "page_num": refs[0].get("page_num") if refs else None,
            "quote_preview": quote_text(row).replace("\n", " ")[:240],
        })
    write_jsonl(DATA / "verified_sources.jsonl", rows)
    write_jsonl(QUEUE, queue)

    lines = [
        "# P26 / P5-B needs_review Segmentation",
        "",
        "本报告将 P5-A 降级出的 `needs_review` 条目按问题类型分成后续可执行队列。",
        "",
        "> 边界：只做来源关系分型，不改写医学内容，不判断医学真实性或疗效。",
        "",
        "## Summary",
        "",
        f"- needs_review rows segmented: {len(queue)}",
        "",
        "## By segment",
        "",
        "| segment | count |",
        "|---|---:|",
    ]
    for seg, count in sorted(counters.items()):
        lines.append(f"| `{seg}` | {count} |")
    lines += ["", "## By kind and segment", "", "| kind | segment | count |", "|---|---|---:|"]
    for kind, c in sorted(by_kind.items()):
        for seg, count in sorted(c.items()):
            lines.append(f"| {kind} | `{seg}` | {count} |")
    lines += [
        "",
        "## Next actions",
        "",
        "- `empty_quote`: 重新检索来源或降级为 no_source/needs_review 队列，不保留 verified 语义。",
        "- `dirty_quote`: 先做 OCR/TOC/JSON 片段清理，再重新检索。",
        "- `name_mismatch`: 检查 alias/重复二级条目/错配 source_refs，优先修 item_id 与来源关系。",
        "- `weak_context`: 人工判断是否可保留 contextual 或降级。",
        "",
        f"Queue file: `{QUEUE.relative_to(ROOT)}`",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({
        "segmented": len(queue),
        "by_segment": dict(counters),
        "by_kind": {k: dict(v) for k, v in by_kind.items()},
        "queue": str(QUEUE.relative_to(ROOT)),
        "report": str(REPORT.relative_to(ROOT)),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
