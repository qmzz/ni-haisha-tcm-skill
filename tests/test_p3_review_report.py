#!/usr/bin/env python3
"""P3-A review queue filter and report tests."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class P3ReviewReportTest(unittest.TestCase):
    def test_review_queue_cli_filters_kind_status_limit_json(self):
        result = subprocess.run(
            [sys.executable, "cli.py", "review-queue", "--kind", "herb", "--status", "no_source_found", "--limit", "3", "--json"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        data = json.loads(result.stdout)
        self.assertEqual(len(data["items"]), 3)
        self.assertTrue(all(item["kind"] == "herb" for item in data["items"]))
        self.assertTrue(all(item["review_status"] == "no_source_found" for item in data["items"]))

    def test_build_review_report(self):
        result = subprocess.run(
            [sys.executable, "scripts/build_review_report.py"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("review_report.md", result.stdout)
        report = ROOT / "report" / "review_report.md"
        self.assertTrue(report.exists())
        text = report.read_text(encoding="utf-8")
        self.assertIn("复核队列总数", text)
        self.assertIn("formula / needs_review", text)
        self.assertIn("herb / no_source_found", text)


if __name__ == "__main__":
    unittest.main()
