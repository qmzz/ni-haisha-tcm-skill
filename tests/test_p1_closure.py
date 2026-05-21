#!/usr/bin/env python3
"""P1 收口：CLI 来源查询与 review queue 测试。"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class P1ClosureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        commands = [
            "scripts/build_formula_sources.py",
            "scripts/build_formula_index.py",
            "scripts/build_herb_sources.py",
            "scripts/build_herb_index.py",
            "scripts/build_acupoint_sources.py",
            "scripts/build_acupoint_index.py",
            "scripts/build_review_queue.py",
        ]
        for script in commands:
            subprocess.run([sys.executable, script], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)

    def test_herb_source_cli_json(self):
        result = subprocess.run(
            [sys.executable, "cli.py", "herb-source", "麻黄", "--json"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        data = json.loads(result.stdout)
        self.assertEqual(data["kind"], "药材")
        self.assertTrue(data["matches"])
        self.assertEqual(data["matches"][0]["name"], "麻黄")

    def test_acupoint_source_cli_json(self):
        result = subprocess.run(
            [sys.executable, "cli.py", "acupoint-source", "百会", "--json"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        data = json.loads(result.stdout)
        self.assertEqual(data["kind"], "穴位")
        self.assertTrue(data["matches"])
        self.assertEqual(data["matches"][0]["name"], "百会")

    def test_review_queue_created(self):
        path = ROOT / "data" / "review_queue.jsonl"
        self.assertTrue(path.exists())
        with path.open(encoding="utf-8") as f:
            records = [json.loads(line) for line in f]
        self.assertGreaterEqual(len(records), 180)
        self.assertTrue(any(r["review_status"] == "no_source_found" for r in records))
        self.assertTrue(any(r["review_status"] == "needs_review" for r in records))


if __name__ == "__main__":
    unittest.main()
