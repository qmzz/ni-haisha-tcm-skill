#!/usr/bin/env python3
"""P24 trim obvious repeated-character OCR tails from herb markdown quotes.

This is mechanical hygiene only. It removes tail fragments that start at obvious
OCR duplicated chapter headings, e.g. 二二二二...【【【【本本... It does not add new
medical content.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "report" / "p24_ocr_tail_trim.md"
PATTERNS = [
    re.compile(r"\s+[一二三四五六七八九十〇○零]{2,}[、、，,].*?【【【【.*", re.S),
    re.compile(r"\s+[一二三四五六七八九十〇○零]{2,}[、、，,].*", re.S),
    re.compile(r"\s+二二二二.*?【【【【.*", re.S),
    re.compile(r"\s+二二二二.*", re.S),
]
TARGETS = sorted((ROOT / "knowledge" / "herbs").glob("*.md"))


def trim_tail(line: str) -> tuple[str, bool]:
    original = line
    for pat in PATTERNS:
        line = pat.sub("", line)
    return line.rstrip(), line != original


def main() -> int:
    changed = []
    for path in TARGETS:
        text = path.read_text(encoding="utf-8")
        lines = []
        local = 0
        for line in text.splitlines():
            new_line, did = trim_tail(line)
            if did:
                local += 1
            lines.append(new_line)
        if local:
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            changed.append({"file": str(path.relative_to(ROOT)), "trimmed_lines": local})
    report_lines = [
        "# P24 OCR Tail Trim",
        "",
        "机械清理明显 OCR 重复字尾巴，不新增医学内容。",
        "",
        f"- Changed files: {len(changed)}",
        "",
    ]
    report_lines.extend(f"- `{r['file']}`: {r['trimmed_lines']} lines" for r in changed)
    REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print(json.dumps({"changed_files": len(changed), "changed": changed, "report": str(REPORT.relative_to(ROOT))}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
