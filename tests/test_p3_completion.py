#!/usr/bin/env python3
"""P3-C/D/E completion tests."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class P3CompletionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for script in [
            "scripts/build_sqlite_fts.py",
            "scripts/build_quality_report.py",
        ]:
            subprocess.run([sys.executable, script], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)

    def test_fts_cli_json(self):
        result = subprocess.run(
            [sys.executable, "cli.py", "fts-search", "桂枝汤", "--limit", "2", "--json"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        data = json.loads(result.stdout)
        self.assertTrue(data["available"])
        self.assertTrue(data["hits"])
        self.assertIn("search_mode", data["hits"][0])

    def test_review_next_cli_json(self):
        result = subprocess.run(
            [sys.executable, "cli.py", "review-next", "--kind", "herb", "--status", "needs_review", "--limit", "2", "--json"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        data = json.loads(result.stdout)
        self.assertLessEqual(len(data["items"]), 2)
        self.assertTrue(all(item["kind"] == "herb" for item in data["items"]))

    def test_review_export_cli_json(self):
        result = subprocess.run(
            [sys.executable, "cli.py", "review-export", "--kind", "herb", "--status", "no_source_found", "--limit", "3", "--json"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        data = json.loads(result.stdout)
        self.assertEqual(data["count"], 3)
        template = ROOT / "data" / "review_decisions.template.jsonl"
        self.assertTrue(template.exists())
        self.assertEqual(len(template.read_text(encoding="utf-8").strip().splitlines()), 3)

    def test_quality_report(self):
        report = ROOT / "report" / "quality_report.md"
        self.assertTrue(report.exists())
        text = report.read_text(encoding="utf-8")
        self.assertIn("来源候选覆盖率", text)
        self.assertIn("candidate 不等于 verified", text)


if __name__ == "__main__":
    unittest.main()
