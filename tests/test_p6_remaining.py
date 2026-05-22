#!/usr/bin/env python3
"""P6-B/C/D/E completion tests."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class P6RemainingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, "scripts/p6_seed_second_batch_decisions.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable, "scripts/build_verified_sources.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable, "scripts/standardize_verified_frontmatter.py", "--apply"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable, "scripts/build_p6_no_source_report.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable, "scripts/check_frontmatter_schema.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)

    def run_tool(self, name, payload):
        result = subprocess.run(
            [sys.executable, "tools/tcm_tools.py", name, json.dumps(payload, ensure_ascii=False)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(result.stdout)

    def test_p6_b_verified_expanded(self):
        rows = [json.loads(line) for line in (ROOT / "data" / "verified_sources.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        self.assertEqual(len(rows), 117)
        counts = {}
        for row in rows:
            counts[row["kind"]] = counts.get(row["kind"], 0) + 1
        self.assertEqual(counts, {"acupoint": 40, "formula": 40, "herb": 37})

    def test_p6_c_no_source_report(self):
        report = (ROOT / "report" / "p6_no_source_report.md").read_text(encoding="utf-8")
        self.assertIn("未决 no_source_found：184", report)
        self.assertIn("不自动提升为 verified", report)

    def test_p6_d_agent_tools(self):
        summary = self.run_tool("tcm_trace_summary", {"query": "大柴胡汤"})
        self.assertEqual(summary["trace_status"], "verified")
        self.assertIn("summary", summary)
        stats = self.run_tool("tcm_verified_stats", {})
        self.assertEqual(stats["verified_count"], 117)
        self.assertEqual(stats["by_kind"]["formula"], 40)
        no_source = self.run_tool("tcm_no_source_report", {})
        self.assertTrue(no_source["available"])

    def test_p6_frontmatter_audit(self):
        report = (ROOT / "report" / "frontmatter_audit.md").read_text(encoding="utf-8")
        self.assertIn("missing_required: 821", report)


if __name__ == "__main__":
    unittest.main()
