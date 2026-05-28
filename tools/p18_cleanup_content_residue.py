#!/usr/bin/env python3
"""P18 lightweight content residue cleanup.

This script only performs mechanical cleanup that does not invent medical
content:
- remove pipeline label prefixes such as `来源摘录：` from blockquotes;
- remove obvious model-placeholder quote lines;
- remove OCR replacement-character noise (`����`);
- remove single-line JSON fragments accidentally pasted into markdown;
- prune empty markdown sections.

It deliberately does not rewrite medical claims or source quotes.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "knowledge"

PLACEHOLDER_PATTERNS = [
    re.compile(r'^>\s*["“]?「[^」]+」这味药，在经方中应用广泛\.\.\.["”]?\s*$'),
    re.compile(r'^>\s*["“]?「[^」]+」这个穴位，在临床上应用非常广泛\.\.\.["”]?\s*$'),
]
JSON_FRAGMENT_PATTERNS = [
    re.compile(r'^>\s*,?\s*\{"page_num"\s*:'),
    re.compile(r'^>\s*,?\s*\{"[^"{}]+"\s*:'),
]
HEADING_RE = re.compile(r'^(#{2,6})\s+\S')


def is_placeholder(line: str) -> bool:
    return any(p.search(line) for p in PLACEHOLDER_PATTERNS)


def is_json_fragment(line: str) -> bool:
    return any(p.search(line) for p in JSON_FRAGMENT_PATTERNS)


def prune_empty_sections(lines: list[str]) -> list[str]:
    """Remove empty markdown heading sections.

    A section is empty when the heading is followed only by blank lines until the
    next heading of the same or higher level (or EOF). We only remove the heading
    and its blank padding, leaving non-empty content untouched.
    """
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = HEADING_RE.match(line)
        if not m:
            out.append(line)
            i += 1
            continue

        level = len(m.group(1))
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1

        next_is_same_or_parent_heading = False
        if j >= len(lines):
            next_is_same_or_parent_heading = True
        else:
            m2 = HEADING_RE.match(lines[j])
            next_is_same_or_parent_heading = bool(m2 and len(m2.group(1)) <= level)

        if next_is_same_or_parent_heading:
            i = j
            continue

        out.append(line)
        i += 1
    return out


def clean_file(path: Path) -> dict[str, int]:
    text = path.read_text(encoding="utf-8")
    original = text
    stats = {
        "source_labels": text.count("来源摘录："),
        "placeholders": 0,
        "ocr_noise_lines": 0,
        "json_fragments": 0,
    }

    lines = []
    for line in text.splitlines():
        if is_placeholder(line):
            stats["placeholders"] += 1
            continue
        if is_json_fragment(line):
            stats["json_fragments"] += 1
            continue
        if "����" in line:
            stats["ocr_noise_lines"] += 1
            line = line.replace("����", "").rstrip()
            if not line.strip() or line.strip() == ">":
                continue
        line = line.replace("来源摘录：", "")
        lines.append(line)

    lines = prune_empty_sections(lines)
    new_text = "\n".join(lines).rstrip() + "\n"
    if new_text != original:
        path.write_text(new_text, encoding="utf-8")
    stats["changed"] = int(new_text != original)
    return stats


def main() -> int:
    totals = {"files": 0, "changed": 0, "source_labels": 0, "placeholders": 0, "ocr_noise_lines": 0, "json_fragments": 0}
    for path in sorted(KNOWLEDGE.rglob("*.md")):
        totals["files"] += 1
        stats = clean_file(path)
        for key in totals:
            if key != "files":
                totals[key] += stats.get(key, 0)
    print(totals)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
