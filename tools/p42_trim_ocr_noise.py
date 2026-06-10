#!/usr/bin/env python3
"""Trim obvious OCR residue from knowledge markdown.

This is intentionally mechanical. It trims obvious replacement-character noise,
duplicated OCR heading tails such as `【【【【...】】】】`, and repeated numeral
chapter prefixes that were pasted into the middle of source excerpts. It does
not add any new medical content.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "knowledge"
REPORT = ROOT / "report" / "p42_ocr_noise_trim.md"

REPLACEMENT_RE = re.compile(r"\uFFFD{2,}")
DOUBLE_BRACKET_RE = re.compile(r"【【")
REPEATED_NUMERAL_RE = re.compile(r"[一二三四五六七八九〇○零]{4,}、")


def read_head_text(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    proc = subprocess.run(
        ["git", "-C", str(ROOT), "show", f"HEAD:{rel}"],
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    return proc.stdout


def trim_line(line: str) -> tuple[str, bool]:
    cut = len(line)
    for pat in (REPLACEMENT_RE, DOUBLE_BRACKET_RE, REPEATED_NUMERAL_RE):
        m = pat.search(line)
        if m:
            cut = min(cut, m.start())
    if cut < len(line):
        line = line[:cut]
        return line, True
    return line, False


def clean_file(path: Path) -> dict[str, int]:
    original = read_head_text(path)
    lines: list[str] = []
    changed_lines = 0
    for raw in original.splitlines():
        line, changed = trim_line(raw)
        if changed:
            changed_lines += 1
        lines.append(line)
    new_text = "\n".join(lines) + ("\n" if lines else "")
    if path.read_text(encoding="utf-8") != new_text:
        path.write_text(new_text, encoding="utf-8")
    return {"changed_lines": changed_lines, "changed_against_head": int(new_text != original)}


def main() -> int:
    changed = []
    for path in sorted(KNOWLEDGE.rglob("*.md")):
        stats = clean_file(path)
        if stats["changed_against_head"]:
            changed.append({"file": path.relative_to(ROOT).as_posix(), "trimmed_lines": stats["changed_lines"]})

    REPORT.write_text(
        "\n".join(
            [
                "# P42 OCR Noise Trim",
                "",
                "机械清理知识库中的明显 OCR 替换字符、重复章节头和双重书名号残留；保留 Markdown 正常空行与排版。",
                "",
                f"- Changed files: {len(changed)}",
                "",
                *[f"- `{row['file']}`: {row['trimmed_lines']} lines" for row in changed],
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"changed_files": len(changed), "changed": changed, "report": str(REPORT.relative_to(ROOT))}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
