#!/usr/bin/env python3
"""P48: remove legacy PDF footer and embedded page-boundary residue from active JSONL."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p48_jsonl_pdf_footer_cleanup.md"

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

PDF_VERSION_BEFORE_BOUNDARY = re.compile(
    r"\s*V\d+-\d{1,8}(?:（[^）\n]*(?:）\s*\d*)?)?(?=\"}\s*,\s*\{\"page_)"
)
PDF_VERSION_TAIL = re.compile(
    r"\s*V\d+-\d{1,8}(?:（[^）\n]*(?:）\s*\d*)?)?(?P<suffix>(?:\\?[\"'])*)$"
)
SPACED_PAGE_COUNT_TAIL = re.compile(r"\s*第\s*\d+\s*页\s*共\s*\d+\s*页(?P<suffix>(?:\\?[\"'])*)$")
BOOKSTORE_FOOTER = re.compile(
    r"\s*守候诚实国学书店\s*第\s*\d+\s*页\s*共\s*\d+\s*页\s*内部中医教材系列\s*"
)
PAGE_JSON_BOUNDARY = re.compile(
    r'"}\s*,\s*\{"page_num"\s*:\s*(?:\d+|null)\s*,\s*"text"\s*:\s*"'
)
TRUNCATED_PAGE_JSON_BOUNDARY_TAIL = re.compile(r"\s*\"}\s*,\s*\{\"page_[^\"]*(?P<suffix>[\"']*)$")


def keep_suffix(match: re.Match[str]) -> str:
    return match.groupdict().get("suffix", "")


def clean_string(value: str) -> tuple[str, bool]:
    original = value
    value = BOOKSTORE_FOOTER.sub(" ", value)
    value = PDF_VERSION_BEFORE_BOUNDARY.sub("", value)
    value = PAGE_JSON_BOUNDARY.sub(" ", value)
    value = TRUNCATED_PAGE_JSON_BOUNDARY_TAIL.sub(keep_suffix, value)

    lines = []
    for line in value.splitlines():
        line = SPACED_PAGE_COUNT_TAIL.sub(keep_suffix, line)
        line = PDF_VERSION_TAIL.sub(keep_suffix, line)
        lines.append(line.rstrip())
    value = "\n".join(lines)

    if value != original:
        value = re.sub(r"[ \t]{2,}", " ", value).rstrip()
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
        "# P48 JSONL PDF Footer Cleanup",
        "",
        "Removed legacy PDF footer residue and embedded page-boundary JSON fragments",
        "from active JSONL registries. Explicit needs-review evidence queues were left unchanged.",
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
    print(json.dumps({"jsonl_files_changed": len(changes), "report": REPORT.relative_to(ROOT).as_posix()}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
