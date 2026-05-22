#!/usr/bin/env python3
"""异名 / 别名注册表。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
ALIASES_PATH = ROOT / "data" / "aliases.json"


def load_aliases() -> Dict[str, Dict[str, List[str]]]:
    if not ALIASES_PATH.exists():
        return {}
    with ALIASES_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def keywords_for(kind: str, name: str) -> List[str]:
    aliases = load_aliases().get(kind, {})
    result = [name]
    result.extend(aliases.get(name, []))
    # 去重且保序
    seen = set()
    deduped = []
    for item in result:
        item = item.strip()
        if item and item not in seen:
            seen.add(item)
            deduped.append(item)
    return deduped
