#!/usr/bin/env python3
"""P3-B alias-aware source matching tests."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class P3AliasMatchingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for script in [
            "scripts/build_formula_sources.py",
            "scripts/build_formula_index.py",
            "scripts/build_herb_sources.py",
            "scripts/build_herb_index.py",
            "scripts/build_review_queue.py",
        ]:
            subprocess.run([sys.executable, script], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)

    def test_alias_registry_exists(self):
        path = ROOT / "data" / "aliases.json"
        self.assertTrue(path.exists())
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertIn("herb", data)
        self.assertIn("白豆蔻", data["herb"])

    def test_herb_alias_hit_records_matched_keyword(self):
        with (ROOT / "data" / "herb_sources.jsonl").open(encoding="utf-8") as f:
            records = [json.loads(line) for line in f]
        record = next(r for r in records if r["name"] == "白豆蔻")
        self.assertIn("豆蔻", record["searched_keywords"])
        self.assertTrue(record["source_hits"])
        self.assertIn("matched_keyword", record["source_hits"][0])

    def test_formula_alias_hit_records_matched_keyword(self):
        with (ROOT / "data" / "formula_sources.jsonl").open(encoding="utf-8") as f:
            records = [json.loads(line) for line in f]
        record = next(r for r in records if r["name"] == "白术附子汤")
        self.assertIn("术附汤", record["searched_keywords"])
        self.assertTrue(record["source_hits"])
        self.assertIn("matched_keyword", record["source_hits"][0])


if __name__ == "__main__":
    unittest.main()
