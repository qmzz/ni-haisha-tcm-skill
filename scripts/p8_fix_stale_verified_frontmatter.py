#!/usr/bin/env python3
"""P8-A-fix: detect and optionally repair stale verified frontmatter.

A stale verified frontmatter means the markdown file says `trace_status: verified`
but the item is not present in data/verified_sources.jsonl. This is a governance
consistency issue; the repair downgrades only governance metadata to the index
status (usually candidate). It does not modify medical body content.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from internal.frontmatter import parse_frontmatter  # noqa: E402

KINDS = {
    "formula": {"folder": ROOT / "knowledge" / "formulas", "index": ROOT / "data" / "formula_index.jsonl", "id_key": "formula_id"},
    "herb": {"folder": ROOT / "knowledge" / "herbs", "index": ROOT / "data" / "herb_index.jsonl", "id_key": "herb_id"},
    "acupoint": {"folder": ROOT / "knowledge" / "acupoints", "index": ROOT / "data" / "acupoint_index.jsonl", "id_key": "acupoint_id"},
}


def load_jsonl(path: Path) -> List[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_verified_keys() -> set[tuple[str, str]]:
    return {(row.get("kind"), row.get("item_id")) for row in load_jsonl(ROOT / "data" / "verified_sources.jsonl")}


def load_index_status() -> dict[tuple[str, str], str]:
    out = {}
    for kind, cfg in KINDS.items():
        for row in load_jsonl(cfg["index"]):
            item_id = row.get(cfg["id_key"]) or Path(row.get("file", "")).stem
            if item_id:
                out[(kind, str(item_id))] = row.get("trace_status") or "candidate"
    return out


def split_frontmatter(text: str):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end < 0:
        return None, text
    return text[4:end], text[end:]


def replace_scalar(fm: str, key: str, value: str) -> str:
    prefix = f"{key}:"
    lines = fm.splitlines()
    for idx, line in enumerate(lines):
        if line.strip().startswith(prefix):
            lines[idx] = f"{key}: {value}"
            return "\n".join(lines)
    lines.append(f"{key}: {value}")
    return "\n".join(lines)


def find_stale() -> List[dict]:
    verified = load_verified_keys()
    index_status = load_index_status()
    rows = []
    for kind, cfg in KINDS.items():
        for path in sorted(cfg["folder"].glob("*.md")):
            if "index" in path.name:
                continue
            text = path.read_text(encoding="utf-8")
            fm, _ = parse_frontmatter(text)
            item_id = path.stem
            key = (kind, item_id)
            if fm.get("trace_status") == "verified" and key not in verified:
                rows.append({
                    "kind": kind,
                    "item_id": item_id,
                    "file": str(path.relative_to(ROOT)),
                    "frontmatter_trace_status": "verified",
                    "target_trace_status": index_status.get(key, "candidate"),
                    "action": "downgrade_frontmatter_trace_status_only",
                    "source_policy": "governance_metadata_only_not_medical_content",
                })
    return rows


def apply_fix(rows: List[dict]) -> List[str]:
    changed = []
    for row in rows:
        path = ROOT / row["file"]
        text = path.read_text(encoding="utf-8")
        raw_fm, rest = split_frontmatter(text)
        if raw_fm is None:
            continue
        fm = replace_scalar(raw_fm, "trace_status", row["target_trace_status"])
        fm = replace_scalar(fm, "review_status", row["target_trace_status"])
        fm = replace_scalar(fm, "reviewer", '"p8_stale_verified_frontmatter_fix"')
        new_text = "---\n" + fm.rstrip() + rest
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed.append(row["file"])
    return changed


def write_report(rows: List[dict], changed: List[str]) -> None:
    lines = [
        "# P8-A stale verified frontmatter 修复报告",
        "",
        "## 定位",
        "",
        "本报告记录 frontmatter 标记为 verified、但未进入 `data/verified_sources.jsonl` registry 的治理不一致条目。修复仅调整治理元数据，不修改医学正文，不把 candidate 自动提升为 verified。",
        "",
        f"- stale_verified_frontmatter: {len(rows)}",
        f"- changed_files: {len(changed)}",
        "",
        "| kind | item_id | file | target_trace_status | action |",
        "|------|---------|------|---------------------|--------|",
    ]
    for row in rows:
        lines.append(f"| {row['kind']} | {row['item_id']} | {row['file']} | {row['target_trace_status']} | {row['action']} |")
    lines.extend([
        "",
        "## 边界",
        "",
        "- 本修复只处理治理元数据一致性。",
        "- 不新增 source_refs，不改医学正文。",
        "- 如需 verified，必须通过人工白名单和 registry 流程进入 `data/verified_sources.jsonl`。",
        "",
    ])
    out = ROOT / "report" / "p8_stale_verified_fix_report.md"
    out.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    apply = "--apply" in sys.argv
    rows = find_stale()
    changed = apply_fix(rows) if apply else []
    write_report(rows, changed)
    print(json.dumps({"apply": apply, "stale_count": len(rows), "changed_files": changed, "report": "report/p8_stale_verified_fix_report.md"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
