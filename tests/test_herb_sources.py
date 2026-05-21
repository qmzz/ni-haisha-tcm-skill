#!/usr/bin/env python3
"""药材来源候选与索引测试。"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class HerbSourcesIndexTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, "scripts/build_herb_sources.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable, "scripts/build_herb_index.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)

    def test_herb_sources_created(self):
        path = ROOT / "data" / "herb_sources.jsonl"
        self.assertTrue(path.exists())
        with path.open(encoding="utf-8") as f:
            records = [json.loads(line) for line in f]
        self.assertGreaterEqual(len(records), 400)
        self.assertGreaterEqual(sum(1 for r in records if r["source_hits"]), 250)

    def test_mahuang_has_traceable_source_candidate(self):
        path = ROOT / "data" / "herb_index.jsonl"
        self.assertTrue(path.exists())
        with path.open(encoding="utf-8") as f:
            records = [json.loads(line) for line in f]
        record = next(r for r in records if r["herb_id"] == "mahuang")
        self.assertEqual(record["name"], "麻黄")
        self.assertEqual(record["trace_status"], "candidate")
        self.assertTrue(record["source_refs"])
        self.assertIn("麻黄", record["source_refs"][0]["quote"])


if __name__ == "__main__":
    unittest.main()
