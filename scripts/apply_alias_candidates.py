#!/usr/bin/env python3
"""将中高置信 alias_candidates 合并进 data/aliases.json。"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ALIASES = DATA / "aliases.json"
CANDIDATES = DATA / "alias_candidates.jsonl"


def load_jsonl(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def main():
    aliases = json.loads(ALIASES.read_text(encoding="utf-8")) if ALIASES.exists() else {}
    added = 0
    for row in load_jsonl(CANDIDATES):
        if row.get("confidence") not in {"high", "medium"}:
            continue
        kind = row["kind"]
        name = row["name"]
        alias = row["alias"]
        aliases.setdefault(kind, {}).setdefault(name, [])
        if alias not in aliases[kind][name]:
            aliases[kind][name].append(alias)
            added += 1
    ALIASES.write_text(json.dumps(aliases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {ALIASES}")
    print(f"added aliases: {added}")


if __name__ == "__main__":
    main()
