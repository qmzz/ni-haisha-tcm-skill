#!/usr/bin/env python3
"""方剂来源候选索引测试。"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class FormulaSourcesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, "scripts/build_formula_sources.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)

    def test_formula_sources_file_created(self):
        path = ROOT / "data" / "formula_sources.jsonl"
        self.assertTrue(path.exists())
        with path.open(encoding="utf-8") as f:
            records = [json.loads(line) for line in f]
        self.assertGreaterEqual(len(records), 100)

    def test_guizhi_tang_has_traceable_source_candidate(self):
        path = ROOT / "data" / "formula_sources.jsonl"
        with path.open(encoding="utf-8") as f:
            records = [json.loads(line) for line in f]
        record = next(r for r in records if r["formula_id"] == "guizhi_tang")
        self.assertEqual(record["name"], "桂枝汤")
        self.assertTrue(record["source_hits"])
        first = record["source_hits"][0]
        self.assertIn("桂枝汤", first["quote"])
        self.assertTrue(first["source_file"])


if __name__ == "__main__":
    unittest.main()
