#!/usr/bin/env python3
"""P7-E/P7-F release closure tests."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class P7ReleaseClosureTest(unittest.TestCase):
    def run_cli_json(self, *args):
        result = subprocess.run(
            [sys.executable, "cli.py", *args, "--json"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(result.stdout)

    def test_cli_lookup_explain_dashboard_batch_trace(self):
        lookup = self.run_cli_json("lookup", "白头翁汤")
        self.assertEqual(lookup["trace"]["trace_status"], "verified")
        self.assertIn("safety_boundary", lookup)

        explained = self.run_cli_json("explain-trace", "白头翁汤")
        self.assertEqual(explained["trace_status"], "verified")
        self.assertIn("来源治理状态", explained["boundary"])

        dashboard = self.run_cli_json("review-dashboard")
        self.assertGreaterEqual(dashboard["verified"]["count"], 147)
        self.assertGreaterEqual(dashboard["verified"]["by_kind"]["acupoint"], 50)
        self.assertGreaterEqual(dashboard["verified"]["by_kind"]["formula"], 50)
        self.assertGreaterEqual(dashboard["verified"]["by_kind"]["herb"], 47)

        batch = self.run_cli_json("batch-trace", "桂枝汤,白头翁汤")
        self.assertEqual(batch["count"], 2)
        self.assertTrue(all("trace_status" in item for item in batch["items"]))

    def test_p7_release_report_and_docs(self):
        subprocess.run([sys.executable, "scripts/build_p7_release_report.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        report = (ROOT / "report" / "p7_release_report.md").read_text(encoding="utf-8")
        self.assertIn("P7-E：CLI / 文档产品化", report)
        self.assertRegex(report, r"总数：(?:147|171|209|210|240|369|374)")
        self.assertIn("acupoint_name_variant: 63", report)

        roadmap = (ROOT / "docs" / "roadmap.md").read_text(encoding="utf-8")
        self.assertIn("[x] P7-E", roadmap)
        self.assertIn("[x] P7-F", roadmap)

        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("[1.1.0] - 2026-05-22", changelog)


if __name__ == "__main__":
    unittest.main()
