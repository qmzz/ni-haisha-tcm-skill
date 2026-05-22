#!/usr/bin/env python3
"""P5-B core herb verified expansion tests."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = {
    "白芍",
    "生姜",
    "大枣",
    "半夏",
    "黄芩",
    "黄连",
    "附子",
    "人参",
    "干姜",
    "细辛",
    "杏仁",
    "柴胡",
    "茯苓",
    "白术",
    "泽泻",
    "牡蛎",
    "龙骨",
}


class P5CoreHerbsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for script in [
            "scripts/p5_seed_core_herb_decisions.py",
            "scripts/build_verified_sources.py",
        ]:
            subprocess.run([sys.executable, script], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)

    def test_core_herbs_verified(self):
        rows = [json.loads(line) for line in (ROOT / "data" / "verified_sources.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        herb_names = {r["name"] for r in rows if r["kind"] == "herb"}
        self.assertTrue(CORE.issubset(herb_names))
        self.assertGreaterEqual(len(herb_names), 22)

    def test_herb_decisions_include_quality_metadata(self):
        rows = [json.loads(line) for line in (ROOT / "data" / "review_decisions.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        row = next(r for r in rows if r.get("item_id") == "baishao")
        self.assertEqual(row["decision"], "verified")
        self.assertGreaterEqual(row.get("quality_score", 0), 80)
        self.assertIn("match_reason", row)


if __name__ == "__main__":
    unittest.main()
