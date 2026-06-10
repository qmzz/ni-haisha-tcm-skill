#!/usr/bin/env python3
"""P45: Remove page footer artifacts, version stamps, org watermarks, and U+FFFD."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "knowledge"
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p45_footer_artifact_cleanup.md"

# Full OCR footer block
OCR_FOOTER_BLOCK = re.compile(
    r"\s*\u52e4\u6c42\u53e4\u8a13\s+\u535a\u91c7\u773e\u65b9\s+\u5c0f\u6842\u679d[\u00b7\u2022\uff0e]*\u7fa4\u9f99\u65e0\u9996.*"
)
# OCR footer fragments split across lines
OCR_FOOTER_FRAGMENT = re.compile(
    r"(\u52e4\u6c42\u53e4\u8a13\s+\u535a\u91c7\u773e\u65b9|\u5c0f\u6842\u679d[\u00b7\u2022\uff0e]*\u7fa4\u9f99\u65e0\u9996.*\u6821\u6392.*)"
)
# 11110000 barcode
BINARY_BARCODE = re.compile(r"11110000[.\s]*")
# typesetting mark at end, preserving optional closing quote/braces
XIAOPAI = re.compile(r"\s*\u6821\u6392(?P<suffix>[\"'}]*)$")
# version stamp at end, preserving optional closing quote/braces
VERSION_STAMP = re.compile(r"\s*V100415\.\d+(?:\s+\d+)?(?P<suffix>[\"'}]*)$")
# education org footer variants
ORG_FOOTER_PATTERNS = [
    re.compile(r"\s*\u00b7\d+\u00b7\s*\u4e16\u548c\u7ecf\u5178\u6559\u80b2\u00b7\u7ecf\u53f2\u5b50\u96c6\s*"),
    re.compile(r"\s*\d{2}-\d{2}-\d{2}\s+\u4e16\u548c\u7ecf\u5178\u6559\u80b2\u00b7\u7ecf\u53f2\u5b50\u96c6\s*"),
    re.compile(r"\s*\u4e16\u548c\u7ecf\u5178\u6559\u80b2\u00b7\u7ecf\u53f2\u5b50\u96c6\s*"),
]
# slogan + optional page count footer, preserving optional closing quote/braces
SLOGAN_FOOTER = re.compile(
    r"\s*\u4e0a\u4ee5\u7597\u541b\u4eb2\u4e4b\u75be,\u4e0b\u4ee5\u6551\u8d2b[\u8d31\u8ce4]\u4e4b\u5384,\u4e2d\u4ee5\u4fdd\u8eab\u957f\u5168\u3002\u7cbe\u8fdb\u5b66\u4e60\u4e3a\u5f80\u5723\u7ee7\u7edd\u5b66(?:\s*\u7b2c\d+\u9875\u5171\d+\u9875)?(?P<suffix>[\"'}]*)$"
)
SLOGAN_TAIL = re.compile(
    r"\s*(?:,?\u4e2d\u4ee5\u4fdd\u8eab\u957f\u5168\u3002)?\u7cbe\u8fdb\u5b66\u4e60\u4e3a\u5f80\u5723\u7ee7\u7edd\u5b66(?P<suffix>[\"'}]*)$"
)
# standalone page count at end of line, preserving optional closing quote/braces
PAGE_COUNT_FOOTER = re.compile(r"\s*\u7b2c\d+\u9875\u5171\d+\u9875(?P<suffix>[\"'}]*)$")
# standalone page number only when it is the whole line
STANDALONE_PAGE_NUM = re.compile(r"^\s*\u7b2c\d+\u9875\s*$")


def keep_suffix(match: re.Match[str]) -> str:
    return match.groupdict().get("suffix", "")
def clean_line(line: str) -> tuple[str, bool]:
    original = line
    m = OCR_FOOTER_BLOCK.search(line)
    if m:
        line = line[:m.start()] + line[m.end():]
    line = OCR_FOOTER_FRAGMENT.sub("", line)
    line = BINARY_BARCODE.sub("", line)
    line = XIAOPAI.sub(keep_suffix, line)
    line = VERSION_STAMP.sub(keep_suffix, line)
    for pat in ORG_FOOTER_PATTERNS:
        line = pat.sub(" ", line)
    line = SLOGAN_FOOTER.sub(keep_suffix, line)
    line = SLOGAN_TAIL.sub(keep_suffix, line)
    line = PAGE_COUNT_FOOTER.sub(keep_suffix, line)
    line = STANDALONE_PAGE_NUM.sub("", line)
    if line != original:
        line = line.rstrip()
    return line, line != original


def clean_markdown(path: Path) -> dict | None:
    original = path.read_text(encoding="utf-8")
    lines = original.splitlines()
    changed_lines = 0
    new_lines = []
    for line in lines:
        new_line, changed = clean_line(line)
        if changed:
            changed_lines += 1
        new_lines.append(new_line)
    updated = "\n".join(new_lines) + ("\n" if original.endswith("\n") else "")
    if updated == original:
        return None
    path.write_text(updated, encoding="utf-8")
    return {"file": str(path.relative_to(ROOT).as_posix()), "changed_lines": changed_lines}


def clean_jsonl_value(value):
    if isinstance(value, str):
        orig = value
        value = value.replace("\ufffd", "")
        value = BINARY_BARCODE.sub("", value)
        value = XIAOPAI.sub(keep_suffix, value)
        value = VERSION_STAMP.sub(keep_suffix, value)
        for pat in ORG_FOOTER_PATTERNS:
            value = pat.sub(" ", value)
        value = SLOGAN_FOOTER.sub(keep_suffix, value)
        value = SLOGAN_TAIL.sub(keep_suffix, value)
        value = PAGE_COUNT_FOOTER.sub(keep_suffix, value)
        return value, value != orig
    if isinstance(value, list):
        changed = False
        result = []
        for item in value:
            new_item, c = clean_jsonl_value(item)
            result.append(new_item)
            changed = changed or c
        return result, changed
    if isinstance(value, dict):
        changed = False
        result = {}
        for k, v in value.items():
            new_v, c = clean_jsonl_value(v)
            result[k] = new_v
            changed = changed or c
        return result, changed
    return value, False


def clean_jsonl(path: Path) -> dict | None:
    if not path.exists():
        return None
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    changed_rows = 0
    new_rows = []
    for row in rows:
        new_row, changed = clean_jsonl_value(row)
        if changed:
            changed_rows += 1
        new_rows.append(new_row)
    if changed_rows == 0:
        return None
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in new_rows) + "\n", encoding="utf-8")
    return {"file": str(path.relative_to(ROOT).as_posix()), "changed_rows": changed_rows}


def write_report(md_changes, jsonl_changes):
    lines = [
        "# P45 Footer Artifact Cleanup",
        "",
        "Removed page footer OCR artifacts, publisher version stamps, education org watermarks,",
        "slogan footers, standalone page numbers, and U+FFFD replacement characters.",
        "",
        f"- Markdown files changed: {len(md_changes)}",
        f"- JSONL files changed: {len(jsonl_changes)}",
    ]
    if md_changes:
        lines.extend(["", "## Markdown Changes"])
        for r in md_changes:
            lines.append(f"- `{r['file']}`: {r['changed_lines']} lines")
    if jsonl_changes:
        lines.extend(["", "## JSONL Changes"])
        for r in jsonl_changes:
            lines.append(f"- `{r['file']}`: {r['changed_rows']} rows")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    md_changes = []
    for p in sorted(KNOWLEDGE.rglob("*.md")):
        r = clean_markdown(p)
        if r:
            md_changes.append(r)
    jsonl_targets = [DATA / "herb_sources.jsonl", DATA / "verified_sources.jsonl", DATA / "review_decisions.jsonl"]
    jsonl_changes = []
    for p in jsonl_targets:
        r = clean_jsonl(p)
        if r:
            jsonl_changes.append(r)
    write_report(md_changes, jsonl_changes)
    print(json.dumps({"markdown_files_changed": len(md_changes), "jsonl_files_changed": len(jsonl_changes)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
