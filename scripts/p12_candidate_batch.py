#!/usr/bin/env python3
"""P12 一次性批量处理：剩余 164 条 candidate。

策略：
1. 对 161 条有原始资料名命中的 candidate 提取 source_refs
2. 对 3 条无命中的改为 no_source_found
3. 不凭模型记忆补写医学内容
4. 只从原始 JSON 提取上下文作为 quote
"""

from __future__ import annotations

import json
import re
import argparse
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SRC = Path("/app/working/workspaces/default/project/nihaixia")
REPORT = ROOT / "report" / "p12_candidate_batch_report.md"


def load_jsonl(path: Path) -> List[Dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def write_jsonl(path: Path, rows: List[Dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def parse_frontmatter(text: str) -> Tuple[Dict, str]:
    """Parse frontmatter into dict + body. Returns ({}, text) if no frontmatter."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    fm_text = text[4:end]
    body = text[end + 5:]
    fm = {}
    for line in fm_text.splitlines():
        m = re.match(r'^(\w[\w_]*):\s*"?([^"]*)"?\s*$', line)
        if m:
            fm[m.group(1)] = m.group(2)
    return fm, body


def load_source_texts() -> Dict[str, str]:
    """Load all source JSON files as searchable text."""
    texts = {}
    for f in SRC.glob("*.json"):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            if isinstance(data, list):
                texts[f.name] = [json.dumps(x, ensure_ascii=False) for x in data]
            elif isinstance(data, dict):
                texts[f.name] = [json.dumps(data, ensure_ascii=False)]
        except Exception:
            pass
    return texts


def find_quote_in_source(name: str, source_pages: List[str], context_chars: int = 300) -> Optional[Tuple[str, int, str]]:
    """Find a name in source pages, return (source_file, page_num, quote)."""
    for fname, pages in source_texts.items():
        for i, page in enumerate(pages):
            if name in page:
                idx = page.index(name)
                start = max(0, idx - context_chars)
                end = min(len(page), idx + len(name) + context_chars)
                quote = page[start:end].strip()
                # Try to find page number pattern
                page_num = i + 1
                # quality heuristics
                return fname, page_num, quote
    return None


def compute_quality_score(quote: str, name: str, kind: str) -> int:
    """Simple quality scoring based on quote content."""
    score = 60  # base for having a name match
    # bonus for longer quote
    if len(quote) > 200:
        score += 5
    if len(quote) > 400:
        score += 5
    # bonus for TCM-relevant keywords
    tcm_keywords = {
        "acupoint": ["下针", "针", "灸", "穴", "经", "寸", "主治", "治疗"],
        "herb": ["味", "性", "归经", "功效", "主治", "药", "煎", "服"],
        "formula": ["方", "汤", "剂", "组成", "主治", "服"],
    }
    for kw in tcm_keywords.get(kind, []):
        if kw in quote:
            score += 3
    # bonus for direct name presence
    if name in quote:
        score += 10
    # cap at 95 for this batch (not full quality check)
    return min(score, 95)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    global source_texts
    source_texts = load_source_texts()

    # Load current state
    kc_rows = load_jsonl(DATA / "knowledge_completeness.jsonl")
    candidates = [r for r in kc_rows if r.get("trace_status") == "candidate"]

    # Load aliases for name lookup
    aliases = {}
    alias_path = DATA / "aliases.json"
    if alias_path.exists():
        aliases = json.loads(alias_path.read_text(encoding="utf-8"))

    # Build alias -> canonical name map
    alias_names = {}
    for aid, info in aliases.items():
        if info.get("target_id"):
            alias_names[info["target_id"]] = info.get("alias_title", "")

    # Load name map from knowledge files
    name_map = {}
    for r in candidates:
        p = ROOT / r["file"]
        txt = p.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(txt)
        name_map[r["item_id"]] = fm.get("title", r["item_id"])

    # Process
    verified_adds = []
    needs_review = []
    no_source = []
    errors = []

    for r in candidates:
        iid = r["item_id"]
        kind = r["kind"]
        name = name_map.get(iid, iid)
        file_path = r["file"]

        # Search in sources
        hit = find_quote_in_source(name, None)
        if not hit:
            no_source.append({"kind": kind, "item_id": iid, "name": name, "file": file_path})
            continue

        src_file, page_num, quote = hit
        score = compute_quality_score(quote, name, kind)

        entry = {
            "kind": kind,
            "item_id": iid,
            "name": name,
            "file": file_path,
            "source_file": src_file,
            "page_num": page_num,
            "quote": quote[:500],
            "quality_score": score,
            "match_reason": ["name_in_source"],
            "risk_flags": [],
            "decision": "verified",
            "reviewer": "p12_candidate_batch",
            "reviewed_at": date.today().isoformat(),
            "notes": "P12 batch source_ref extraction from original JSON; name match found; verified = source traceability only, not medical validation.",
        }

        if score >= 75:
            verified_adds.append(entry)
        else:
            entry["decision"] = "needs_review"
            needs_review.append(entry)

    # Summary
    print(json.dumps({
        "apply": args.apply,
        "total_candidates": len(candidates),
        "verified_adds": len(verified_adds),
        "needs_review": len(needs_review),
        "no_source": len(no_source),
        "errors": len(errors),
    }, ensure_ascii=False, indent=2))

    # Apply verified decisions
    if args.apply:
        decisions = load_jsonl(DATA / "review_decisions.jsonl")
        existing = {(d.get("kind"), d.get("item_id"), d.get("decision")) for d in decisions}

        new_verified = []
        for v in verified_adds:
            key = (v["kind"], v["item_id"], "verified")
            if key not in existing:
                new_verified.append(v)

        if new_verified:
            decisions.extend(new_verified)
            write_jsonl(DATA / "review_decisions.jsonl", decisions)
            print(f"Added {len(new_verified)} verified decisions")

        # Update no_source items: change trace_status to no_source_found
        for ns in no_source:
            p = ROOT / ns["file"]
            txt = p.read_text(encoding="utf-8")
            txt = txt.replace("trace_status: candidate", "trace_status: no_source_found")
            txt = txt.replace("trace_status: unverified", "trace_status: no_source_found")
            txt = txt.replace("trace_status: needs_review", "trace_status: no_source_found")
            # Add scope markers if not present
            if "source_scope:" not in txt:
                txt = txt.replace("---\n\n# ", '---\nsource_scope: "not_in_nihaixia_source"\nexternal_reference_required: true\nno_source_policy: "keep_boundary_until_traceable_source"\n\n# ', 1)
                txt = txt.replace("---\n\n#", '---\nsource_scope: "not_in_nihaixia_source"\nexternal_reference_required: true\nno_source_policy: "keep_boundary_until_traceable_source"\n\n#', 1)
            p.write_text(txt, encoding="utf-8")

    # Write report
    REPORT.parent.mkdir(exist_ok=True)
    lines = [
        "# P12 Candidate 批量处理报告",
        "",
        f"- apply: {args.apply}",
        f"- total candidates: {len(candidates)}",
        f"- verified (score>=75): {len(verified_adds)}",
        f"- needs_review (score<75): {len(needs_review)}",
        f"- no_source_found: {len(no_source)}",
        "",
        "## 无原始资料命中（改为 no_source_found）",
        "",
    ]
    for ns in no_source:
        lines.append(f"- `{ns['kind']}` {ns['item_id']} ({ns['name']})")
    lines += [
        "",
        "## Verified 条目",
        "",
        "| kind | item_id | name | score | source_file | page |",
        "|------|---------|------|-------|-------------|------|",
    ]
    for v in verified_adds:
        lines.append(f"| {v['kind']} | {v['item_id']} | {v['name']} | {v['quality_score']} | {v['source_file']} | {v['page_num']} |")
    if needs_review:
        lines += [
            "",
            "## Needs Review",
            "",
            "| kind | item_id | name | score |",
            "|------|---------|------|-------|",
        ]
        for nr in needs_review:
            lines.append(f"| {nr['kind']} | {nr['item_id']} | {nr['name']} | {nr['quality_score']} |")
    lines += [
        "",
        "说明：verified 仅表示来源追溯链路通过，不代表医学真实性或临床适用性。",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    source_texts = {}
    main()
