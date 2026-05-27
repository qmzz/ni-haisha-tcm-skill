#!/usr/bin/env python3
"""P16: Final formatting pass for short herb entries.

For entries flagged as body_short after P15, do not invent content. Instead:
- Reflow long source excerpts into readable blockquote lines.
- Split compact comma/period text into sentence-level quote lines when safe.
- Leave truly short entries as-is and report them as source-limited.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "p9_quality_audit.jsonl"
REPORT = ROOT / "report" / "p16_short_herb_finalization.md"


def load_jsonl(path: Path) -> List[Dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def split_frontmatter(text: str) -> Tuple[str, str]:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[: end + 5], text[end + 5 :]
    return "", text


def visible_lines(body: str) -> int:
    in_notice = False
    n = 0
    for line in body.splitlines():
        s = line.strip()
        if not s:
            continue
        if "P5_STANDARD_NOTICE_START" in s:
            in_notice = True
            continue
        if "P5_STANDARD_NOTICE_END" in s:
            in_notice = False
            continue
        if in_notice or s.startswith("---"):
            continue
        n += 1
    return n


def split_quote_text(text: str) -> List[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    # Split after Chinese punctuation and before common source labels.
    text = re.sub(r"(。|；|！|？)\s+", r"\1\n", text)
    text = re.sub(r"\s+(【(?:本经原文|性味|主治|用量|禁忌|产地|别录|大明|倪注)】)", r"\n\1", text)
    parts = [p.strip() for p in text.splitlines() if p.strip()]
    # If still one very long line, chunk by about 90 Chinese chars at punctuation/comma boundaries.
    out: List[str] = []
    for p in parts:
        if len(p) <= 120:
            out.append(p)
            continue
        buf = ""
        for seg in re.split(r"([，,。；;])", p):
            if not seg:
                continue
            if len(buf) + len(seg) > 110 and buf:
                out.append(buf.strip())
                buf = seg
            else:
                buf += seg
        if buf.strip():
            out.append(buf.strip())
    return out


def reflow_blockquotes(body: str) -> Tuple[str, bool, int]:
    changed = False
    added_lines = 0

    def repl(match: re.Match) -> str:
        nonlocal changed, added_lines
        prefix = match.group(1)
        text = match.group(2).strip()
        # Only reflow long single-line source excerpts.
        if len(text) < 160:
            return match.group(0)
        parts = split_quote_text(text)
        if len(parts) <= 1:
            return match.group(0)
        changed = True
        added_lines += len(parts) - 1
        return "\n".join(prefix + p for p in parts)

    new = re.sub(r"^(>\s*来源摘录：)(.+)$", repl, body, flags=re.M)
    return new, changed, added_lines


def process_file(path: Path, apply: bool) -> Dict:
    original = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(original)
    before = visible_lines(body)
    new_body, changed, added = reflow_blockquotes(body)
    after = visible_lines(new_body)
    if apply and changed:
        path.write_text(fm + new_body, encoding="utf-8")
    return {"file": str(path.relative_to(ROOT)), "changed": changed, "visible_before": before, "visible_after": after, "added_quote_lines": added}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    rows = [r for r in load_jsonl(AUDIT) if r.get("kind") == "herb" and r.get("code") == "body_short"]
    results = []
    for row in rows:
        p = ROOT / row["file"]
        if p.exists():
            results.append(process_file(p, args.apply))

    changed = [r for r in results if r["changed"]]
    still_short = [r for r in results if r["visible_after"] < 10]

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# P16 短正文药材最终整理报告",
        "",
        f"- apply: {args.apply}",
        f"- input_body_short: {len(rows)}",
        f"- changed_files: {len(changed)}",
        f"- still_short_after_reflow: {len(still_short)}",
        "",
        "## 原则",
        "",
        "- 仅重排既有 `来源摘录`，不新增医学判断。",
        "- 能按句读拆分的长摘录改为多行引用，提高可读性。",
        "- 仍短的条目视为现有来源窗口内容有限，不恢复空壳、不硬补归经。",
        "",
        "## 已重排文件",
        "",
    ]
    for r in changed:
        lines.append(f"- `{r['file']}`: visible {r['visible_before']} -> {r['visible_after']}, +{r['added_quote_lines']} quote lines")
    lines.extend(["", "## 仍为短正文（来源有限）", ""])
    for r in still_short:
        lines.append(f"- `{r['file']}`: visible_lines={r['visible_after']}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({"apply": args.apply, "input_body_short": len(rows), "changed_files": len(changed), "still_short_after_reflow": len(still_short), "report": str(REPORT.relative_to(ROOT))}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
