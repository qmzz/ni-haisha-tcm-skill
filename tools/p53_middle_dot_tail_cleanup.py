import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_DIR = ROOT / "knowledge"
REPORT_PATH = ROOT / "report" / "p53_middle_dot_tail_cleanup.md"

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

MIDDLE_DOT_TAIL_RE = re.compile(r"[ \t]*\u00b7{6,}")


def clean_text(text: str) -> tuple[str, int]:
    count = len(MIDDLE_DOT_TAIL_RE.findall(text))
    return MIDDLE_DOT_TAIL_RE.sub("", text), count


def clean_value(value: Any) -> tuple[Any, int]:
    if isinstance(value, str):
        return clean_text(value)
    if isinstance(value, list):
        changed_items = []
        total = 0
        for item in value:
            cleaned, count = clean_value(item)
            total += count
            changed_items.append(cleaned)
        return changed_items, total
    if isinstance(value, dict):
        changed_dict = {}
        total = 0
        for key, item in value.items():
            cleaned, count = clean_value(item)
            total += count
            changed_dict[key] = cleaned
        return changed_dict, total
    return value, 0


def clean_jsonl_file(path: Path) -> tuple[bool, int, int]:
    changed = False
    changed_rows = 0
    total = 0
    output_lines = []

    for line in path.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        cleaned, count = clean_value(row)
        if cleaned != row:
            changed = True
            changed_rows += 1
        total += count
        output_lines.append(json.dumps(cleaned, ensure_ascii=False))

    if changed:
        path.write_text("\n".join(output_lines) + "\n", encoding="utf-8", newline="\n")
    return changed, changed_rows, total


def main() -> None:
    markdown_changes = []
    jsonl_changes = []
    total_removed = 0

    for path in sorted(KNOWLEDGE_DIR.rglob("*.md")):
        original = path.read_text(encoding="utf-8")
        updated, count = clean_text(original)
        if updated == original:
            continue
        path.write_text(updated, encoding="utf-8", newline="\n")
        total_removed += count
        markdown_changes.append((path.relative_to(ROOT).as_posix(), count))

    for path in ACTIVE_JSONL_FILES:
        changed, changed_rows, count = clean_jsonl_file(path)
        if not changed:
            continue
        total_removed += count
        jsonl_changes.append((path.relative_to(ROOT).as_posix(), changed_rows, count))

    lines = [
        "# P53 Middle Dot Tail Cleanup",
        "",
        "Removed high-confidence truncated table-of-contents tails made of long middle-dot runs from active content.",
        "Only runs of six or more middle dots were removed; ordinary single middle dots in titles and names were left unchanged.",
        "Needs-review evidence queues outside the active JSONL registry set were left unchanged.",
        "",
        f"- Markdown files changed: {len(markdown_changes)}",
        f"- JSONL files changed: {len(jsonl_changes)}",
        f"- Middle-dot tails removed: {total_removed}",
        "",
        "## Markdown Changes",
    ]
    for rel, count in markdown_changes:
        lines.append(f"- `{rel}`: {count} middle-dot tails")

    lines.extend(["", "## JSONL Changes"])
    for rel, rows, count in jsonl_changes:
        lines.append(f"- `{rel}`: {rows} rows, {count} middle-dot tails")

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
