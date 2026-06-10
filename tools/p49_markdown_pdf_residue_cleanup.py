import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_DIR = ROOT / "knowledge"
REPORT_PATH = ROOT / "report" / "p49_markdown_pdf_residue_cleanup.md"

PDF_VERSION_RE = re.compile(
    r'[ \t]*V[0-9]+-[0-9]{1,8}(?:（[^）\n]*）)?(?:[ \t]*[0-9]{1,4})?"?'
)
DOT_PAGE_RE = re.compile(r"[ \t]*\u00b7[0-9]{1,4}\u00b7[ \t]*")


def normalize_text(text: str) -> tuple[str, dict[str, int]]:
    counts = {
        "pdf_version": len(PDF_VERSION_RE.findall(text)),
        "dot_page_marker": len(DOT_PAGE_RE.findall(text)),
    }
    text = PDF_VERSION_RE.sub("", text)
    text = DOT_PAGE_RE.sub(" ", text)
    return text, counts


def main() -> None:
    changed = []
    totals = {"pdf_version": 0, "dot_page_marker": 0}
    for path in sorted(KNOWLEDGE_DIR.rglob("*.md")):
        original = path.read_text(encoding="utf-8")
        updated, counts = normalize_text(original)
        if updated == original:
            continue
        path.write_text(updated, encoding="utf-8", newline="\n")
        for key, value in counts.items():
            totals[key] += value
        changed.append((path.relative_to(ROOT).as_posix(), counts))

    lines = [
        "# P49 Markdown PDF Residue Cleanup",
        "",
        "Removed high-confidence PDF version fragments and dot-wrapped page markers from knowledge Markdown files.",
        "Compact page references like `page 263` were left unchanged because many are source citations or transcript content.",
        "",
        f"- Markdown files changed: {len(changed)}",
        f"- PDF version fragments removed: {totals['pdf_version']}",
        f"- Dot page markers removed: {totals['dot_page_marker']}",
        "",
        "## Markdown Changes",
    ]
    for rel, counts in changed:
        lines.append(
            f"- `{rel}`: {counts['pdf_version']} version fragments, "
            f"{counts['dot_page_marker']} dot page markers"
        )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
