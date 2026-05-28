#!/usr/bin/env python3
"""统一来源追溯服务。

优先级：
1. data/verified_sources.jsonl
2. data/*_index.jsonl 中的 candidate refs
3. data/review_queue.jsonl
4. 原始 JSON keyword search fallback
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from internal.source_corpus import SourceCorpus

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

INDEX_CONFIG = [
    ("formula", "formula_id", DATA_DIR / "formula_index.jsonl"),
    ("herb", "herb_id", DATA_DIR / "herb_index.jsonl"),
    ("acupoint", "acupoint_id", DATA_DIR / "acupoint_index.jsonl"),
]


def _load_jsonl(path: Path) -> List[Dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def _matches(record: Dict, query: str, id_key: str = "item_id") -> bool:
    return query == record.get(id_key) or query == record.get("name") or query in record.get("name", "")


class TraceService:
    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = data_dir

    def trace(self, query: str, limit: int = 5) -> Dict:
        query = query.strip()
        if not query:
            return {"query": query, "trace_status": "empty_query", "matches": []}

        # P10-B: alias resolution
        alias_match = self._resolve_alias(query)
        if alias_match:
            target_id = alias_match.get("target_id")
            # Redirect trace to target
            result = self._trace_core(target_id, limit)
            result["alias_redirect"] = {
                "from": query,
                "to": target_id,
                "alias_of": alias_match.get("alias_id"),
                "note": f"命中 alias，自动跳转至标准条目 {target_id}"
            }
            return result

        return self._trace_core(query, limit)

    def _trace_core(self, query: str, limit: int) -> Dict:
        verified = self._trace_verified(query)
        if verified:
            return {"query": query, "trace_status": "verified", "source_quality_level": self._rollup_quality(verified), "matches": verified[:limit]}

        candidates = self._trace_candidates(query)
        if candidates:
            candidate_matches = [m for m in candidates if m.get("trace_status") == "candidate"]
            no_source_matches = [m for m in candidates if m.get("trace_status") == "no_source_found"]
            other_matches = [m for m in candidates if m.get("trace_status") not in {"candidate", "no_source_found"}]

            if candidate_matches:
                return {"query": query, "trace_status": "candidate", "source_quality_level": self._rollup_quality(candidate_matches), "matches": candidate_matches[:limit]}
            if other_matches:
                status = other_matches[0].get("trace_status") or "candidate"
                return {"query": query, "trace_status": status, "source_quality_level": self._rollup_quality(other_matches), "matches": other_matches[:limit]}

            # `*_index.jsonl` also contains no_source_found inventory rows.  They
            # are useful for resolving the canonical file/name, but must not be
            # promoted to `candidate`: candidate means there are source_refs that
            # still need human review.  Empty no-source rows should stay explicit.
            return {"query": query, "trace_status": "no_source_found", "source_quality_level": "no_source", "matches": no_source_matches[:limit]}

        review_items = self._trace_review_queue(query)
        if review_items:
            return {"query": query, "trace_status": "needs_review", "source_quality_level": self._rollup_quality(review_items) or "needs_review", "matches": review_items[:limit]}

        corpus = SourceCorpus()
        hits = [h.to_dict() for h in corpus.search(query, limit=limit, context=100)]
        return {"query": query, "trace_status": "source_search" if hits else "no_source_found", "source_quality_level": "source_search" if hits else "no_source", "matches": hits}


    def _rollup_quality(self, rows: List[Dict]) -> str:
        levels = [r.get("source_quality_level") for r in rows if r.get("source_quality_level")]
        if not levels:
            return ""
        priority = [
            "verified_direct",
            "verified_alias",
            "verified_contextual",
            "candidate_direct",
            "candidate_alias",
            "candidate_contextual",
            "needs_review",
            "source_search",
            "no_source",
        ]
        for level in priority:
            if level in levels:
                return level
        return levels[0]

    def _resolve_alias(self, query: str) -> Optional[Dict]:
        """P10-B: 检查 alias_index，返回 alias 映射。"""
        aliases = _load_jsonl(self.data_dir / "alias_index.jsonl")
        for a in aliases:
            if query == a.get("alias_id") or query == a.get("alias_title"):
                return a
        return None

    def _trace_verified(self, query: str) -> List[Dict]:
        records = _load_jsonl(self.data_dir / "verified_sources.jsonl")
        matches = [r for r in records if _matches(r, query)]
        exact = [m for m in matches if query == m.get("name") or query == m.get("item_id")]
        return exact or matches

    def _trace_candidates(self, query: str) -> List[Dict]:
        matches = []
        for kind, id_key, path in INDEX_CONFIG:
            for record in _load_jsonl(path):
                if _matches(record, query, id_key=id_key):
                    trace_status = record.get("trace_status", "candidate")
                    source_refs = record.get("source_refs", [])
                    if trace_status == "candidate" and not source_refs:
                        trace_status = "no_source_found"
                    matches.append({
                        "kind": kind,
                        "item_id": record.get(id_key),
                        "name": record.get("name"),
                        "file": record.get("file"),
                        "trace_status": trace_status,
                        "source_refs": source_refs,
                        "source_quality_level": record.get("source_quality_level"),
                    })
        exact = [m for m in matches if query == m.get("name") or query == m.get("item_id")]
        return exact or matches

    def _trace_review_queue(self, query: str) -> List[Dict]:
        records = _load_jsonl(self.data_dir / "review_queue.jsonl")
        return [r for r in records if _matches(r, query)]
