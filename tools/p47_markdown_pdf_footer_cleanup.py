#!/usr/bin/env python3
"""P47: remove legacy PDF footer residue from active knowledge Markdown."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "knowledge"
REPORT = ROOT / "report" / "p47_markdown_pdf_footer_cleanup.md"

PDF_VERSION_TAIL = re.compile(r"\s*V\d+-\d{8}(?:（[^）\n]*(?:）\s*\d*)?)?(?P<suffix>(?:\\?[\"'])*)$")
SPACED_PAGE_COUNT_TAIL = re.compile(r"\s*第\s*\d+\s*页\s*共\s*\d+\s*页(?P<suffix>(?:\\?[\"'])*)$")
BOOKSTORE_FOOTER = re.compile(
    r"\s*守候诚实国学书店\s*第\s*\d+\s*页\s*共\s*\d+\s*页\s*内部中医教材系列\s*"
)


def keep_suffix(match: re.Match[str]) -> str:
    return match.groupdict().get("suffix", "")


def clean_line(line: str) -> tuple[str, bool]:
    original = line
    line = BOOKSTORE_FOOTER.sub(" ", line)
    line = SPACED_PAGE_COUNT_TAIL.sub(keep_suffix, line)
    line = PDF_VERSION_TAIL.sub(keep_suffix, line)
    if line != original:
        line = line.rstrip()
    return line, line != original


def clean_markdown(path: Path) -> dict[str, object] | None:
    original = path.read_text(encoding="utf-8")
    changed_lines = 0
    updated_lines = []
    for line in original.splitlines():
        updated, changed = clean_line(line)
        if changed:
            changed_lines += 1
        updated_lines.append(updated)
    updated = "\n".join(updated_lines) + ("\n" if original.endswith("\n") else "")
    if updated == original:
        return None
    path.write_text(updated, encoding="utf-8")
    return {"file": path.relative_to(ROOT).as_posix(), "changed_lines": changed_lines}


def write_report(changes: list[dict[str, object]]) -> None:
    lines = [
        "# P47 Markdown PDF Footer Cleanup",
        "",
        "Removed legacy PDF footer residue from active knowledge Markdown files.",
        "The cleanup is limited to line-tail version stamps, spaced page counters,",
        "and the bookstore/internal-textbook footer.",
        "",
        f"- Markdown files changed: {len(changes)}",
    ]
    if changes:
        lines.extend(["", "## Markdown Changes"])
        for row in changes:
            lines.append(f"- `{row['file']}`: {row['changed_lines']} lines")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    changes = []
    for path in sorted(KNOWLEDGE.rglob("*.md")):
        result = clean_markdown(path)
        if result:
            changes.append(result)
    write_report(changes)
    print(json.dumps({"markdown_files_changed": len(changes), "report": REPORT.relative_to(ROOT).as_posix()}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
