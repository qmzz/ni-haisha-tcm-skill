#!/usr/bin/env python3
"""P4-D/E/F tests."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class P4DEFTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
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

    def test_agent_review_stats_tool(self):
        data = self.run_tool("tcm_review_stats", {})
        self.assertIn("review_queue_count", data)
        self.assertIn("counts", data)

    def test_agent_fts_tool(self):
        data = self.run_tool("tcm_search_sources_fts", {"query": "桂枝汤", "limit": 1})
        self.assertIn("hits", data)

    def test_agent_compare_tool(self):
        data = self.run_tool("tcm_compare_formulas", {"names": ["桂枝汤", "麻黄汤"]})
        self.assertEqual(data["kind"], "formula")
        self.assertEqual(len(data["items"]), 2)

    def test_frontmatter_audit_report(self):
        report = ROOT / "report" / "frontmatter_audit.md"
        self.assertTrue(report.exists())
        text = report.read_text(encoding="utf-8")
        self.assertIn("Frontmatter Audit", text)

    def test_docs_exist(self):
        for path in [
            "docs/agent_integration.md",
            "docs/review_workflow.md",
            "docs/safety_boundary.md",
            "docs/data_governance.md",
            "docs/frontmatter_schema.md",
        ]:
            self.assertTrue((ROOT / path).exists())


if __name__ == "__main__":
    unittest.main()
