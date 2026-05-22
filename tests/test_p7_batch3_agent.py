#!/usr/bin/env python3
"""P7-C/P7-D tests."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class P7Batch3AgentOrchestrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, "scripts/p7_seed_verified_batch3.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable, "scripts/build_verified_sources.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable, "scripts/standardize_verified_frontmatter.py", "--apply"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
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

    def test_p7_c_verified_batch3_counts(self):
        rows = [json.loads(line) for line in (ROOT / "data" / "verified_sources.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        self.assertEqual(len(rows), 147)
        counts = {}
        for row in rows:
            counts[row["kind"]] = counts.get(row["kind"], 0) + 1
        self.assertEqual(counts, {"acupoint": 50, "formula": 50, "herb": 47})
        self.assertTrue(any(row["name"] == "白头翁汤" for row in rows))

    def test_p7_d_lookup_and_explain_trace(self):
        lookup = self.run_tool("tcm_lookup", {"query": "白头翁汤"})
        self.assertEqual(lookup["trace"]["trace_status"], "verified")
        self.assertIn("safety_boundary", lookup)
        explained = self.run_tool("tcm_explain_trace", {"query": "白头翁汤"})
        self.assertEqual(explained["trace_status"], "verified")
        self.assertIn("来源治理状态", explained["boundary"])

    def test_p7_d_dashboard_and_batch_trace(self):
        dashboard = self.run_tool("tcm_review_dashboard", {})
        self.assertEqual(dashboard["verified"]["count"], 147)
        self.assertIn("review_queue", dashboard)
        batch = self.run_tool("tcm_batch_trace", {"queries": ["桂枝汤", "白头翁汤"]})
        self.assertEqual(batch["count"], 2)
        self.assertEqual(batch["items"][1]["trace_status"], "verified")

    def test_frontmatter_audit_after_p7_c(self):
        report = (ROOT / "report" / "frontmatter_audit.md").read_text(encoding="utf-8")
        self.assertIn("missing_required: 791", report)


if __name__ == "__main__":
    unittest.main()
