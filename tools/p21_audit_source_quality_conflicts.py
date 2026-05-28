#!/usr/bin/env python3
"""P21/P1 audit source-quality conflicts across registry, indexes, frontmatter.

Read-only audit. It reports conflicts and unresolved alias risks after P20 rollout.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p21_source_quality_conflict_audit.md"

INDEX_FILES = [
    ("formula", "formula_id", DATA / "formula_index.jsonl"),
    ("herb", "herb_id", DATA / "herb_index.jsonl"),
    ("acupoint", "acupoint_id", DATA / "acupoint_index.jsonl"),
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def frontmatter_status(path: Path) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---", 4)
    if end < 0:
        return ""
    fm = text[4:end]
    m = re.search(r'^\s*trace_status\s*:\s*(.+?)\s*$', fm, re.M)
    return m.group(1).strip().strip('"').strip("'") if m else ""


def main() -> int:
    verified = {(r.get("kind"), r.get("item_id")): r for r in load_jsonl(DATA / "verified_sources.jsonl")}
    completeness = {(r.get("kind"), r.get("item_id")): r for r in load_jsonl(DATA / "knowledge_completeness.jsonl")}
    conflicts: list[dict[str, Any]] = []
    no_source_resolutions: list[dict[str, Any]] = []

    for kind, id_key, path in INDEX_FILES:
        for row in load_jsonl(path):
            item_id = row.get(id_key)
            key = (kind, item_id)
            ver = verified.get(key)
            comp = completeness.get(key, {})
            fm_status = frontmatter_status(ROOT / row.get("file", ""))
            issues: list[str] = []

            if ver and ver.get("trace_status") == "verified" and row.get("trace_status") != "verified":
                issues.append(f"index={row.get('trace_status')} but registry=verified")
            if ver and ver.get("trace_status") == "verified" and comp.get("trace_status") != "verified":
                issues.append(f"completeness={comp.get('trace_status')} but registry=verified")
            # Frontmatter may still carry historical review_status=verified. After P5-B
            # source_quality_level is authoritative for trace relation quality; no_source/needs_review
            # rows are allowed to diverge from historical frontmatter review_status.
            if fm_status and row.get("trace_status") and fm_status != row.get("trace_status"):
                allowed_historical_verified = row.get("source_quality_level") in {"no_source", "needs_review"} and fm_status == "verified"
                allowed_alias_from_no_source = row.get("source_quality_level") == "verified_alias" and row.get("p6b_resolution") == "mapped_to_verified_canonical_as_alias" and fm_status == "no_source_found"
                if not (allowed_historical_verified or allowed_alias_from_no_source):
                    issues.append(f"frontmatter={fm_status} but index={row.get('trace_status')}")
            if ver and row.get("source_quality_level") != ver.get("source_quality_level"):
                issues.append(f"index_quality={row.get('source_quality_level')} but registry_quality={ver.get('source_quality_level')}")
            if ver and comp.get("source_quality_level") and comp.get("source_quality_level") != ver.get("source_quality_level"):
                issues.append(f"completeness_quality={comp.get('source_quality_level')} but registry_quality={ver.get('source_quality_level')}")
            if row.get("trace_status") == "no_source_found" and row.get("source_refs"):
                issues.append("no_source_found row has source_refs")
            if row.get("trace_status") == "no_source_found" and row.get("source_quality_level") != "no_source":
                issues.append(f"no_source_found quality={row.get('source_quality_level')}")

            if issues:
                conflicts.append({
                    "kind": kind,
                    "item_id": item_id,
                    "name": row.get("name"),
                    "file": row.get("file"),
                    "index_status": row.get("trace_status"),
                    "index_quality": row.get("source_quality_level"),
                    "frontmatter_status": fm_status,
                    "issues": issues,
                })

            if row.get("p1_resolution"):
                no_source_resolutions.append({
                    "kind": kind,
                    "item_id": item_id,
                    "name": row.get("name"),
                    "resolution": row.get("p1_resolution"),
                })

    alias_risks = []
    for kind, id_key, path in INDEX_FILES:
        for row in load_jsonl(path):
            level = row.get("source_quality_level", "")
            if level == "candidate_alias":
                alias_risks.append({
                    "kind": kind,
                    "item_id": row.get(id_key),
                    "name": row.get("name"),
                    "trace_status": row.get("trace_status"),
                    "source_quality_level": level,
                    "source_ref_count": len(row.get("source_refs") or []),
                })

    dist = Counter()
    for _, _, path in INDEX_FILES:
        for row in load_jsonl(path):
            dist[row.get("source_quality_level", "")] += 1

    lines = [
        "# P21 / P1 Source Quality Conflict Audit",
        "",
        "Read-only audit after P20 rollout.",
        "",
        "> 边界：本报告只审计来源治理状态，不判断医学真实性或临床适用性。",
        "",
        "## Summary",
        "",
        f"- Conflicts: {len(conflicts)}",
        f"- Alias-risk rows: {len(alias_risks)}",
        f"- P1 no-source resolutions: {len(no_source_resolutions)}",
        "",
        "## Index source_quality distribution",
        "",
        "| level | count |",
        "|---|---:|",
    ]
    for level, count in sorted(dist.items()):
        lines.append(f"| `{level}` | {count} |")

    lines += ["", "## Conflicts", ""]
    if conflicts:
        for item in conflicts:
            lines.append(f"- `{item['kind']}:{item['item_id']}` {item['name']} — {', '.join(item['issues'])}")
    else:
        lines.append("No conflicts found.")

    lines += ["", "## Alias risk rows", ""]
    if alias_risks:
        for item in alias_risks:
            lines.append(f"- `{item['kind']}:{item['item_id']}` {item['name']} — `{item['source_quality_level']}`, status `{item['trace_status']}`, refs {item['source_ref_count']}")
    else:
        lines.append("No unresolved alias-risk rows in index files.")

    lines += ["", "## P1 no-source resolutions", ""]
    if no_source_resolutions:
        for item in no_source_resolutions:
            lines.append(f"- `{item['kind']}:{item['item_id']}` {item['name']} — {item['resolution']}")
    else:
        lines.append("No P1 no-source resolutions recorded.")

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({
        "conflicts": len(conflicts),
        "alias_risks": len(alias_risks),
        "p1_no_source_resolutions": len(no_source_resolutions),
        "report": str(REPORT.relative_to(ROOT)),
    }, ensure_ascii=False, indent=2))
    return 0 if not conflicts else 1


if __name__ == "__main__":
    raise SystemExit(main())
