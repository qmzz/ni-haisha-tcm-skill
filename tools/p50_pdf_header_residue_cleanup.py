import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_DIR = ROOT / "knowledge"
REPORT_PATH = ROOT / "report" / "p50_pdf_header_residue_cleanup.md"

ACTIVE_JSONL_FILES = [
    ROOT / "data" / "acupoint_index.jsonl",
    ROOT / "data" / "acupoint_sources.jsonl",
    ROOT / "data" / "formula_index.jsonl",
    ROOT / "data" / "formula_sources.jsonl",
    ROOT / "data" / "herb_index.jsonl",
    ROOT / "data" / "herb_sources.jsonl",
    ROOT / "data" / "review_decisions.jsonl",
    ROOT / "data" / "review_queue.jsonl",
    ROOT / "data" / "verified_sources.jsonl",
]

HEADER_PAIR_RE = re.compile(r"[ \t]*05-10-18[ \t\r\n]+\u5b50\u90e8\u00b7\u9ec4\u5e1d\u5185\u7ecf[ \t\r\n]*")
DATE_RE = re.compile(r"[ \t]*05-10-18[ \t]*")
BOOK_HEADER_RE = re.compile(r"[ \t]*\u5b50\u90e8\u00b7\u9ec4\u5e1d\u5185\u7ecf[ \t]*")
DOT_PAGE_RE = re.compile(r"[ \t]*\u00b7[0-9]{1,4}\u00b7[ \t]*")


def separator_replacement(match: re.Match[str]) -> str:
    return "\n" if "\n" in match.group(0) else " "


def clean_text(text: str) -> tuple[str, dict[str, int]]:
    counts = {
        "date_book_header": len(HEADER_PAIR_RE.findall(text)),
        "date_header": 0,
        "book_header": 0,
        "dot_page_marker": len(DOT_PAGE_RE.findall(text)),
    }
    text = HEADER_PAIR_RE.sub(separator_replacement, text)
    counts["date_header"] = len(DATE_RE.findall(text))
    text = DATE_RE.sub(" ", text)
    counts["book_header"] = len(BOOK_HEADER_RE.findall(text))
    text = BOOK_HEADER_RE.sub(" ", text)
    text = DOT_PAGE_RE.sub(" ", text)
    return text, counts


def merge_counts(target: dict[str, int], counts: dict[str, int]) -> None:
    for key, value in counts.items():
        target[key] = target.get(key, 0) + value


def clean_value(value: Any) -> tuple[Any, dict[str, int]]:
    counts = {"date_book_header": 0, "date_header": 0, "book_header": 0, "dot_page_marker": 0}
    if isinstance(value, str):
        return clean_text(value)
    if isinstance(value, list):
        changed_items = []
        for item in value:
            cleaned, item_counts = clean_value(item)
            merge_counts(counts, item_counts)
            changed_items.append(cleaned)
        return changed_items, counts
    if isinstance(value, dict):
        changed_dict = {}
        for key, item in value.items():
            cleaned, item_counts = clean_value(item)
            merge_counts(counts, item_counts)
            changed_dict[key] = cleaned
        return changed_dict, counts
    return value, counts


def clean_jsonl_file(path: Path) -> tuple[bool, int, int, dict[str, int]]:
    changed = False
    changed_rows = 0
    changed_strings = 0
    totals = {"date_book_header": 0, "date_header": 0, "book_header": 0, "dot_page_marker": 0}
    output_lines = []

    for line in path.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        cleaned, row_counts = clean_value(row)
        merge_counts(totals, row_counts)
        if cleaned != row:
            changed = True
            changed_rows += 1
            changed_strings += sum(1 for value in row_counts.values() if value)
        output_lines.append(json.dumps(cleaned, ensure_ascii=False))

    if changed:
        path.write_text("\n".join(output_lines) + "\n", encoding="utf-8", newline="\n")
    return changed, changed_rows, changed_strings, totals


def main() -> None:
    markdown_changes = []
    jsonl_changes = []
    totals = {"date_book_header": 0, "date_header": 0, "book_header": 0, "dot_page_marker": 0}

    for path in sorted(KNOWLEDGE_DIR.rglob("*.md")):
        original = path.read_text(encoding="utf-8")
        updated, counts = clean_text(original)
        if updated == original:
            continue
        path.write_text(updated, encoding="utf-8", newline="\n")
        merge_counts(totals, counts)
        markdown_changes.append((path.relative_to(ROOT).as_posix(), counts))

    for path in ACTIVE_JSONL_FILES:
        changed, changed_rows, changed_strings, counts = clean_jsonl_file(path)
        if not changed:
            continue
        merge_counts(totals, counts)
        jsonl_changes.append((path.relative_to(ROOT).as_posix(), changed_rows, changed_strings, counts))

    lines = [
        "# P50 PDF Header Residue Cleanup",
        "",
        "Removed high-confidence PDF date/book headers and dot-wrapped page markers from active content.",
        "Needs-review evidence queues outside the active JSONL registry set were left unchanged.",
        "Compact page references like `page 263` were left unchanged because many are source citations or transcript content.",
        "",
        f"- Markdown files changed: {len(markdown_changes)}",
        f"- JSONL files changed: {len(jsonl_changes)}",
        f"- Date/book header pairs removed: {totals['date_book_header']}",
        f"- Standalone date headers removed: {totals['date_header']}",
        f"- Standalone book headers removed: {totals['book_header']}",
        f"- Dot page markers removed: {totals['dot_page_marker']}",
        "",
        "## Markdown Changes",
    ]
    for rel, counts in markdown_changes:
        lines.append(
            f"- `{rel}`: {counts['date_book_header']} date/book pairs, "
            f"{counts['date_header']} dates, {counts['book_header']} book headers, "
            f"{counts['dot_page_marker']} dot page markers"
        )

    lines.extend(["", "## JSONL Changes"])
    for rel, rows, strings, counts in jsonl_changes:
        lines.append(
            f"- `{rel}`: {rows} rows, {strings} pattern groups, "
            f"{counts['date_book_header']} date/book pairs, {counts['date_header']} dates, "
            f"{counts['book_header']} book headers, {counts['dot_page_marker']} dot page markers"
        )

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
