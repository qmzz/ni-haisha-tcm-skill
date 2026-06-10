import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "report"
REPORT_PATH = ROOT / "report" / "p56_fffd_ocr_dequadruple_cleanup.md"

# Patterns for OCR artifacts in report excerpts
FFFD_RE = re.compile(r"\ufffd+")
QUADRUPLE_RE = re.compile(r"(\S)\1{3,}")
LONG_DOT_RE = re.compile(r"\.{10,}")
MIDDLE_DOT_LONG_RE = re.compile(r"[\u00b7\u2022\u2219\u25cf]{6,}")


def clean_text(text: str) -> tuple[str, int]:
    count = 0
    count += len(FFFD_RE.findall(text))
    count += len(QUADRUPLE_RE.findall(text))
    count += len(LONG_DOT_RE.findall(text))
    count += len(MIDDLE_DOT_LONG_RE.findall(text))
    updated = FFFD_RE.sub("", text)
    updated = QUADRUPLE_RE.sub(r"\1", updated)
    updated = LONG_DOT_RE.sub("", updated)
    updated = MIDDLE_DOT_LONG_RE.sub("", updated)
    return updated, count


def clean_json_report(path: Path) -> tuple[bool, int, int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    changed_items = 0
    total = 0

    items = data.get("items", [])
    for item in items:
        if "excerpt" in item and isinstance(item["excerpt"], str):
            cleaned, count = clean_text(item["excerpt"])
            if cleaned != item["excerpt"]:
                item["excerpt"] = cleaned
                changed = True
                changed_items += 1
                total += count

    if "summary" in data and isinstance(data["summary"], str):
        cleaned, count = clean_text(data["summary"])
        if cleaned != data["summary"]:
            data["summary"] = cleaned
            changed = True
            total += count

    if changed:
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    return changed, changed_items, total


def clean_md_report(path: Path) -> tuple[bool, int]:
    original = path.read_text(encoding="utf-8")
    cleaned, count = clean_text(original)
    if cleaned == original:
        return False, 0
    path.write_text(cleaned, encoding="utf-8", newline="\n")
    return True, count


def main() -> None:
    json_changes = []
    md_changes = []
    total_removed = 0

    for path in sorted(REPORT_DIR.rglob("*.json")):
        changed, items_changed, count = clean_json_report(path)
        if not changed:
            continue
        total_removed += count
        json_changes.append((path.relative_to(ROOT).as_posix(), items_changed, count))

    for path in sorted(REPORT_DIR.rglob("*.md")):
        # skip the report we generate
        if path == REPORT_PATH:
            continue
        changed, count = clean_md_report(path)
        if not changed:
            continue
        total_removed += count
        md_changes.append((path.relative_to(ROOT).as_posix(), count))

    lines = [
        "# P56 FFFD / OCR De-quadruple Cleanup",
        "",
        "Cleaned U+FFFD replacement characters, quadrupled OCR text artifacts,",
        "long ASCII dot separator runs, and long middle-dot runs from report files.",
        "Core content (data/, knowledge/) was already clean; only report/ had residual artifacts.",
        "",
        f"- JSON report files changed: {len(json_changes)}",
        f"- Markdown report files changed: {len(md_changes)}",
        f"- Total artifacts removed: {total_removed}",
        "",
        "## JSON Report Changes",
    ]
    for rel, items, count in json_changes:
        lines.append(f"- `{rel}`: {items} items, {count} artifacts")

    lines.extend(["", "## Markdown Report Changes"])
    for rel, count in md_changes:
        lines.append(f"- `{rel}`: {count} artifacts")

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()