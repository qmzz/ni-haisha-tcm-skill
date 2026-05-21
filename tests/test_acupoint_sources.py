#!/usr/bin/env python3
"""穴位来源候选与索引测试。"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class AcupointSourcesIndexTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, "scripts/build_acupoint_sources.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable, "scripts/build_acupoint_index.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)

    def test_acupoint_sources_created(self):
        path = ROOT / "data" / "acupoint_sources.jsonl"
        self.assertTrue(path.exists())
        with path.open(encoding="utf-8") as f:
            records = [json.loads(line) for line in f]
        self.assertGreaterEqual(len(records), 400)
        self.assertGreaterEqual(sum(1 for r in records if r["source_hits"]), 300)

    def test_baihui_has_traceable_source_candidate(self):
        path = ROOT / "data" / "acupoint_index.jsonl"
        self.assertTrue(path.exists())
        with path.open(encoding="utf-8") as f:
            records = [json.loads(line) for line in f]
        record = next(r for r in records if r["acupoint_id"] == "baihui")
        self.assertEqual(record["name"], "百会")
        self.assertEqual(record["trace_status"], "candidate")
        self.assertTrue(record["source_refs"])
        self.assertIn("百会", record["source_refs"][0]["quote"])


if __name__ == "__main__":
    unittest.main()
