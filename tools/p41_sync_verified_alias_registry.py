#!/usr/bin/env python3
"""Sync verified alias rows into the verified source registry.

This only registers rows that are already marked as verified_alias in
knowledge_completeness and already carry source_refs in the corresponding
index file. It does not promote no-source rows or validate medical claims.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REVIEWED_AT = "2026-06-10"

INDEX_CONFIG = {
    "formula": (DATA / "formula_index.jsonl", "formula_id"),
    "herb": (DATA / "herb_index.jsonl", "herb_id"),
    "acupoint": (DATA / "acupoint_index.jsonl", "acupoint_id"),
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def main() -> int:
    completeness = load_jsonl(DATA / "knowledge_completeness.jsonl")
    registry = load_jsonl(DATA / "verified_sources.jsonl")
    registry_keys = {(row.get("kind"), row.get("item_id")) for row in registry}

    indexes: dict[str, dict[str, dict[str, Any]]] = {}
    for kind, (path, id_key) in INDEX_CONFIG.items():
        indexes[kind] = {str(row.get(id_key)): row for row in load_jsonl(path)}

    added: list[tuple[str, str]] = []
    skipped_missing_refs: list[tuple[str, str]] = []

    for row in completeness:
        kind = row.get("kind")
        item_id = row.get("item_id")
        key = (kind, item_id)
        if (
            row.get("trace_status") != "verified"
            or row.get("source_quality_level") != "verified_alias"
            or key in registry_keys
            or kind not in indexes
        ):
            continue

        index_row = indexes[kind].get(str(item_id), {})
        refs = index_row.get("source_refs") or row.get("source_refs") or []
        if not refs:
            skipped_missing_refs.append((str(kind), str(item_id)))
            continue

        registry.append({
            "kind": kind,
            "item_id": item_id,
            "name": row.get("name") or index_row.get("name"),
            "file": row.get("file") or index_row.get("file"),
            "trace_status": "verified",
            "source_refs": refs,
            "notes": "P41 registry sync for verified_alias row already resolved to a verified canonical source; traceability only, not medical validation.",
            "review_status": "trace_review_passed",
            "source_quality_level": "verified_alias",
            "source_quality_policy": "source_quality_is_traceability_only_not_medical_validation",
            "canonical_item_id": row.get("canonical_item_id") or index_row.get("canonical_item_id"),
            "p6b_resolution": row.get("p6b_resolution") or index_row.get("p6b_resolution"),
            "p41_synced_from": "knowledge_completeness_and_index",
            "reviewed_at": REVIEWED_AT,
        })
        registry_keys.add(key)
        added.append((str(kind), str(item_id)))

    registry.sort(key=lambda r: (str(r.get("kind")), str(r.get("item_id"))))
    write_jsonl(DATA / "verified_sources.jsonl", registry)
    print(json.dumps({
        "added_verified_alias_registry_rows": added,
        "skipped_missing_refs": skipped_missing_refs,
        "verified_sources_rows": len(registry),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
