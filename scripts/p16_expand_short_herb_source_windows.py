#!/usr/bin/env python3
"""P16-B: Expand remaining short herb source excerpts from original JSON windows.

Rules:
- Use only original JSON source files under ../nihaixia and current title/source refs.
- Extract a wider window around the herb title when current body is still short.
- Insert as 来源摘录 continuation under 倪师讲解.
- Do not infer structured fields such as 归经.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = ROOT.parent / "nihaixia"
AUDIT = ROOT / "data" / "p9_quality_audit.jsonl"
REPORT = ROOT / "report" / "p16_short_herb_source_window_expansion.md"


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


def fm_title(fm: str, path: Path) -> str:
    m = re.search(r'^title:\s*"?([^"\n]+)"?', fm, re.M)
    return m.group(1).strip() if m else path.stem


def fm_source_files(fm: str) -> List[str]:
    return re.findall(r'^\s*source_file:\s*"([^"]+)"', fm, re.M)


def load_source_pages(source_file: str) -> List[Tuple[int, str]]:
    p = SRC_ROOT / source_file
    if not p.exists():
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return []
    pages = data if isinstance(data, list) else [data]
    out = []
    for i, obj in enumerate(pages, start=1):
        if isinstance(obj, dict):
            text = obj.get("text") or obj.get("content") or json.dumps(obj, ensure_ascii=False)
            page = int(obj.get("page_num") or obj.get("page") or i)
        else:
            text = str(obj)
            page = i
        out.append((page, text))
    return out


def clean(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"第\s*\d+\s*页\s*共\s*\d+\s*页", "", text).strip()
    return text


def split_quote(text: str) -> List[str]:
    text = clean(text)
    text = re.sub(r"(。|；|！|？)\s+", r"\1\n", text)
    text = re.sub(r"\s+(【(?:本经原文|性味|主治|用量|禁忌|产地|别录|大明|倪注)】)", r"\n\1", text)
    parts = [p.strip() for p in text.splitlines() if p.strip()]
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


def extract_window(title: str, source_files: List[str]) -> Tuple[str, int, str] | None:
    for sf in source_files:
        for page, text in load_source_pages(sf):
            idx = text.find(title)
            if idx == -1:
                continue
            start = max(0, idx - 180)
            end = min(len(text), idx + len(title) + 900)
            win = clean(text[start:end])
            if len(win) >= 180:
                return sf, page, win
    # fallback: all json files
    for p in SRC_ROOT.glob("*.json"):
        for page, text in load_source_pages(p.name):
            idx = text.find(title)
            if idx == -1:
                continue
            start = max(0, idx - 180)
            end = min(len(text), idx + len(title) + 900)
            win = clean(text[start:end])
            if len(win) >= 180:
                return p.name, page, win
    return None


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


def already_has_window(body: str) -> bool:
    return "P16 扩展摘录" in body


def append_to_commentary(body: str, source_file: str, page: int, quote: str) -> str:
    parts = split_quote(quote)
    if not parts:
        return body
    block = ["", f"> P16 扩展摘录（{source_file}，page {page}）："]
    block.extend([f"> {p}" for p in parts[:12]])
    block.append("")
    marker = "## 🌿 倪师讲解"
    pos = body.find(marker)
    if pos == -1:
        return body.rstrip() + "\n\n" + marker + "\n" + "\n".join(block) + "\n"
    # append before trailing document separator if exists after commentary
    tail_pos = body.rfind("\n---")
    if tail_pos > pos:
        return body[:tail_pos].rstrip() + "\n" + "\n".join(block) + "\n" + body[tail_pos:]
    return body.rstrip() + "\n" + "\n".join(block) + "\n"


def process_file(path: Path, apply: bool) -> Dict:
    original = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(original)
    before = visible_lines(body)
    if already_has_window(body):
        return {"file": str(path.relative_to(ROOT)), "changed": False, "reason": "already_expanded", "before": before, "after": before}
    title = fm_title(fm, path)
    source_files = fm_source_files(fm)
    hit = extract_window(title, source_files)
    if not hit:
        return {"file": str(path.relative_to(ROOT)), "changed": False, "reason": "no_window", "before": before, "after": before}
    sf, page, quote = hit
    new_body = append_to_commentary(body, sf, page, quote)
    after = visible_lines(new_body)
    changed = new_body != body and after > before
    if apply and changed:
        path.write_text(fm + new_body, encoding="utf-8")
    return {"file": str(path.relative_to(ROOT)), "changed": changed, "reason": "expanded" if changed else "unchanged", "before": before, "after": after, "source_file": sf, "page": page}


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
    not_changed = [r for r in results if not r["changed"]]

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# P16-B 短正文药材原始来源窗口扩展报告",
        "",
        f"- apply: {args.apply}",
        f"- input_body_short: {len(rows)}",
        f"- expanded_files: {len(changed)}",
        f"- source_limited_files: {len(not_changed)}",
        "",
        "## 原则",
        "",
        "- 仅从原始 JSON 中围绕条目中文名截取更宽来源窗口。",
        "- 扩展内容只作为 `P16 扩展摘录`，不整理成无依据的结构字段。",
        "- 不补 `归经`，不恢复空壳。",
        "",
        "## 扩展文件",
        "",
    ]
    for r in changed:
        lines.append(f"- `{r['file']}`: {r['before']} -> {r['after']} ({r.get('source_file')}, page {r.get('page')})")
    lines.extend(["", "## 未扩展文件", ""])
    for r in not_changed:
        lines.append(f"- `{r['file']}`: {r['reason']}, visible_lines={r['after']}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({"apply": args.apply, "input_body_short": len(rows), "expanded_files": len(changed), "source_limited_files": len(not_changed), "report": str(REPORT.relative_to(ROOT))}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
