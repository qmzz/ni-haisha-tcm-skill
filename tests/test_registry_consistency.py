import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class RegistryConsistencyTests(unittest.TestCase):
    def test_all_verified_completeness_rows_exist_in_verified_registry(self):
        verified_sources = load_jsonl(ROOT / "data" / "verified_sources.jsonl")
        registry_keys = {(row.get("kind"), row.get("item_id")) for row in verified_sources}
        completeness = load_jsonl(ROOT / "data" / "knowledge_completeness.jsonl")
        missing = [
            (row.get("kind"), row.get("item_id"), row.get("name"))
            for row in completeness
            if row.get("trace_status") == "verified" and (row.get("kind"), row.get("item_id")) not in registry_keys
        ]
        self.assertEqual(missing, [])

    def test_verified_herb_index_rows_have_source_refs(self):
        herb_rows = load_jsonl(ROOT / "data" / "herb_index.jsonl")
        bad = [
            (row.get("herb_id"), row.get("name"))
            for row in herb_rows
            if row.get("trace_status") == "verified" and not row.get("source_refs")
        ]
        self.assertEqual(bad, [])

    def test_no_source_herb_index_rows_have_no_source_refs(self):
        herb_rows = load_jsonl(ROOT / "data" / "herb_index.jsonl")
        bad = [
            (row.get("herb_id"), row.get("name"))
            for row in herb_rows
            if row.get("trace_status") == "no_source_found" and row.get("source_refs")
        ]
        self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main()
