#!/usr/bin/env python3
"""方剂结构化索引测试。"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class FormulaIndexTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, "scripts/build_formula_sources.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable, "scripts/build_formula_index.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)

    def test_formula_index_created(self):
        path = ROOT / "data" / "formula_index.jsonl"
        self.assertTrue(path.exists())
        with path.open(encoding="utf-8") as f:
            records = [json.loads(line) for line in f]
        self.assertGreaterEqual(len(records), 100)

    def test_guizhi_tang_index_has_source_refs(self):
        path = ROOT / "data" / "formula_index.jsonl"
        with path.open(encoding="utf-8") as f:
            records = [json.loads(line) for line in f]
        record = next(r for r in records if r["formula_id"] == "guizhi_tang")
        self.assertEqual(record["name"], "桂枝汤")
        self.assertEqual(record["trace_status"], "candidate")
        self.assertTrue(record["source_refs"])
        self.assertIn("source_file", record["source_refs"][0])
        self.assertIn("quote", record["source_refs"][0])


if __name__ == "__main__":
    unittest.main()
