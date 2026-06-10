#!/usr/bin/env python3
"""P46: remove OCR/footer residue from active data registry JSONL files."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p46_jsonl_registry_residue_cleanup.md"

DATA_FILES = [
    DATA / "acupoint_index.jsonl",
    DATA / "acupoint_sources.jsonl",
    DATA / "formula_index.jsonl",
    DATA / "formula_sources.jsonl",
    DATA / "herb_index.jsonl",
    DATA / "herb_sources.jsonl",
    DATA / "review_decisions.jsonl",
    DATA / "review_queue.jsonl",
    DATA / "verified_sources.jsonl",
]

REPLACEMENT_RE = re.compile("\ufffd+")
REPEATED_CJK_RE = re.compile(r"([\u4e00-\u9fff])\1{2,}")
REPEATED_BRACKETS = ["\u3010", "\u3011", "\u300a", "\u300b"]
REPEATED_PUNCT = ["\uff0c", "\u3002", "\uff0e", "\u3001", "\uff1b", "\uff1a"]

TARGETED_REPLACEMENTS = [
    ("\u52a0\u52a0\u52a0\u4e00\u4e9b", "\u52a0\u4e00\u4e9b"),
    ("\u9aa8\u9aa8\u9aa8\u3002", "\u9aa8\u3002"),
    ("\u866b\u866b\u866b\u3002", "\u866b\u3002"),
    ("\u901a\u901a\u901a", "\u901a"),
    ("\u901a\u901a\u901a\n\u7b2c", "\u901a\n\u7b2c"),
    ("\u52e4\u52e4\u52e4\u52e4\u6c42\u6c42\u6c42\u6c42\u53e4\u53e4\u53e4\u53e4\u8a13\u8a13\u8a13\u8a13", "\u52e4\u6c42\u53e4\u8a13"),
    ("\u535a\u535a\u535a\u535a\u91c7\u91c7\u91c7\u91c7\u773e\u773e\u773e\u773e\u65b9\u65b9\u65b9\u65b9", "\u535a\u91c7\u773e\u65b9"),
    ("\u5c0f\u5c0f\u5c0f\u5c0f\u6842\u6842\u6842\u6842\u679d\u679d\u679d\u679d", "\u5c0f\u6842\u679d"),
    ("\u7fa4\u7fa4\u7fa4\u7fa4\u9f99\u9f99\u9f99\u9f99\u65e0\u65e0\u65e0\u65e0\u9996\u9996\u9996\u9996", "\u7fa4\u9f99\u65e0\u9996"),
    ("\u6821\u6821\u6821\u6821\u6392\u6392\u6392\u6392", "\u6821\u6392"),
]

OCR_FOOTER_BLOCK = re.compile(
    r"\s*\u52e4\u6c42\u53e4\u8a13\s+\u535a\u91c7\u773e\u65b9\s+\u5c0f\u6842\u679d[\u00b7\u2022\uff0e]*\u7fa4\u9f99\u65e0\u9996.*"
)
OCR_FOOTER_FRAGMENT = re.compile(
    r"(\u52e4\u6c42\u53e4\u8a13\s+\u535a\u91c7\u773e\u65b9|\u5c0f\u6842\u679d[\u00b7\u2022\uff0e]*\u7fa4\u9f99\u65e0\u9996.*\u6821\u6392.*)"
)
BINARY_BARCODE = re.compile(r"11110000[.\s]*")
XIAOPAI = re.compile(r"\s*\u6821\u6392(?P<suffix>[\"'}]*)$")
VERSION_STAMP = re.compile(r"\s*V100415(?:\.\d+)?(?:\s+\d+)?(?P<suffix>[\"'}]*)$")
ORG_FOOTER_PATTERNS = [
    re.compile(r"\s*\u00b7\d+\u00b7\s*\u4e16\u548c\u7ecf\u5178\u6559\u80b2\u00b7\u7ecf\u53f2\u5b50\u96c6\s*"),
    re.compile(r"\s*\d{2}-\d{2}-\d{2}\s+\u4e16\u548c\u7ecf\u5178\u6559\u80b2\u00b7\u7ecf\u53f2\u5b50\u96c6\s*"),
    re.compile(r"\s*\u4e16\u548c\u7ecf\u5178\u6559\u80b2\u00b7\u7ecf\u53f2\u5b50\u96c6\s*"),
]
SLOGAN_FOOTER = re.compile(
    r"\s*\u4e0a\u4ee5\u7597\u541b\u4eb2\u4e4b\u75be,\u4e0b\u4ee5\u6551\u8d2b[\u8d31\u8ce4]\u4e4b\u5384,\u4e2d\u4ee5\u4fdd\u8eab\u957f\u5168\u3002\u7cbe\u8fdb\u5b66\u4e60\u4e3a\u5f80\u5723\u7ee7\u7edd\u5b66(?:\s*\u7b2c\d+\u9875\u5171\d+\u9875)?(?P<suffix>[\"'}]*)$"
)
SLOGAN_TAIL = re.compile(
    r"\s*(?:,?\u4e2d\u4ee5\u4fdd\u8eab\u957f\u5168\u3002)?\u7cbe\u8fdb\u5b66\u4e60\u4e3a\u5f80\u5723\u7ee7\u7edd\u5b66(?P<suffix>[\"'}]*)$"
)
PAGE_COUNT_FOOTER = re.compile(r"\s*\u7b2c\d+\u9875\u5171\d+\u9875(?P<suffix>[\"'}]*)$")


def keep_suffix(match: re.Match[str]) -> str:
    return match.groupdict().get("suffix", "")


def has_ocr_repeat_trigger(text: str) -> bool:
    if REPLACEMENT_RE.search(text):
        return True
    if any(old in text for old, _ in TARGETED_REPLACEMENTS):
        return True
    if any(re.search(re.escape(ch) + r"{2,}", text) for ch in REPEATED_BRACKETS):
        return True
    return any(re.search(re.escape(ch) + r"{3,}", text) for ch in REPEATED_PUNCT)


def normalize_ocr_repeats(text: str) -> str:
    if not has_ocr_repeat_trigger(text):
        return text
    text = REPLACEMENT_RE.sub("", text)
    for old, new in TARGETED_REPLACEMENTS:
        text = text.replace(old, new)
    for ch in REPEATED_BRACKETS:
        text = re.sub(re.escape(ch) + r"{2,}", ch, text)
    for ch in REPEATED_PUNCT:
        text = re.sub(re.escape(ch) + r"{3,}", ch, text)
    return REPEATED_CJK_RE.sub(r"\1", text)


def clean_string(value: str) -> tuple[str, bool]:
    original = value
    value = normalize_ocr_repeats(value)
    value = OCR_FOOTER_BLOCK.sub("", value)
    value = OCR_FOOTER_FRAGMENT.sub("", value)
    value = BINARY_BARCODE.sub("", value)
    value = XIAOPAI.sub(keep_suffix, value)
    value = VERSION_STAMP.sub(keep_suffix, value)
    for pattern in ORG_FOOTER_PATTERNS:
        value = pattern.sub(" ", value)
    value = SLOGAN_FOOTER.sub(keep_suffix, value)
    value = SLOGAN_TAIL.sub(keep_suffix, value)
    value = PAGE_COUNT_FOOTER.sub(keep_suffix, value)
    if value != original:
        value = value.rstrip()
    return value, value != original


def clean_value(value: Any) -> tuple[Any, int]:
    if isinstance(value, str):
        updated, changed = clean_string(value)
        return updated, int(changed)
    if isinstance(value, list):
        changed_count = 0
        updated_items = []
        for item in value:
            updated, changed = clean_value(item)
            updated_items.append(updated)
            changed_count += changed
        return updated_items, changed_count
    if isinstance(value, dict):
        changed_count = 0
        updated_obj: dict[str, Any] = {}
        for key, item in value.items():
            updated, changed = clean_value(item)
            updated_obj[key] = updated
            changed_count += changed
        return updated_obj, changed_count
    return value, 0


def clean_jsonl(path: Path) -> dict[str, Any] | None:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    changed_rows = 0
    changed_strings = 0
    updated_rows = []
    for row in rows:
        updated, changed = clean_value(row)
        if changed:
            changed_rows += 1
            changed_strings += changed
        updated_rows.append(updated)
    if changed_rows == 0:
        return None
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in updated_rows) + "\n", encoding="utf-8")
    return {
        "file": path.relative_to(ROOT).as_posix(),
        "changed_rows": changed_rows,
        "changed_strings": changed_strings,
    }


def write_report(changes: list[dict[str, Any]]) -> None:
    lines = [
        "# P46 JSONL Registry Residue Cleanup",
        "",
        "Removed OCR/footer residue from active data registry JSONL files.",
        "Historical report files and explicit needs-review evidence queues were intentionally left unchanged.",
        "",
        f"- JSONL files changed: {len(changes)}",
    ]
    if changes:
        lines.extend(["", "## JSONL Changes"])
        for row in changes:
            lines.append(f"- `{row['file']}`: {row['changed_rows']} rows, {row['changed_strings']} strings")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    changes = []
    for path in DATA_FILES:
        result = clean_jsonl(path)
        if result:
            changes.append(result)
    write_report(changes)
    print(json.dumps({"jsonl_files_changed": len(changes), "report": REPORT.relative_to(ROOT).as_posix()}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
