#!/usr/bin/env python3
"""检查知识文件 frontmatter schema。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from internal.frontmatter import audit_file

KINDS = {
    "formula": ROOT / "knowledge" / "formulas",
    "herb": ROOT / "knowledge" / "herbs",
    "acupoint": ROOT / "knowledge" / "acupoints",
}


def main():
    rows = []
    for kind, folder in KINDS.items():
        for path in sorted(folder.glob("*.md")):
            if "index" in path.name:
                continue
            row = audit_file(path, kind)
            row["file"] = str(path.relative_to(ROOT))
            rows.append(row)
    report = ROOT / "report" / "frontmatter_audit.md"
    report.parent.mkdir(exist_ok=True)
    missing_count = sum(1 for r in rows if r["missing"])
    warning_count = sum(1 for r in rows if r["warnings"])
    lines = ["# Frontmatter Audit", "", f"- files: {len(rows)}", f"- missing_required: {missing_count}", f"- warnings: {warning_count}", "", "| file | kind | missing | warnings |", "|------|------|---------|----------|"]
    for row in rows:
        if row["missing"] or row["warnings"]:
            lines.append(f"| {row['file']} | {row['kind']} | {', '.join(row['missing'])} | {', '.join(row['warnings'])} |")
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {report}")
    print(json.dumps({"files": len(rows), "missing_required": missing_count, "warnings": warning_count}, ensure_ascii=False))


if __name__ == "__main__":
    main()
