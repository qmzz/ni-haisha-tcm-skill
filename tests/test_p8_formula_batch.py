#!/usr/bin/env python3
"""P8 stale frontmatter fix and formula verified batch tests."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class P8FormulaBatchTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, "scripts/p8_fix_stale_verified_frontmatter.py", "--apply"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable, "scripts/p8_seed_formula_verified_batch.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable, "scripts/build_verified_sources.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable, "scripts/standardize_verified_frontmatter.py", "--apply"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable, "scripts/check_frontmatter_schema.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable, "scripts/build_p8_knowledge_audit.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)

    def test_stale_verified_frontmatter_fixed(self):
        report = (ROOT / "report" / "p8_stale_verified_fix_report.md").read_text(encoding="utf-8")
        self.assertIn("frontmatter 标记 verified 但未进入 registry：0", (ROOT / "report" / "p8_knowledge_audit.md").read_text(encoding="utf-8"))
        self.assertIn("stale_verified_frontmatter: 0", report)
        text = (ROOT / "knowledge" / "herbs" / "taoren.md").read_text(encoding="utf-8")
        self.assertIn("trace_status: candidate", text)

    def test_formula_verified_batch_counts(self):
        rows = [json.loads(line) for line in (ROOT / "data" / "verified_sources.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        counts = {}
        for row in rows:
            counts[row["kind"]] = counts.get(row["kind"], 0) + 1
        self.assertEqual(len(rows), 171)
        self.assertEqual(counts, {"acupoint": 50, "formula": 74, "herb": 47})
        self.assertTrue(any(row["item_id"] == "zhigancao_tang" for row in rows))

    def test_formula_batch_report_and_audit(self):
        report = (ROOT / "report" / "p8_formula_verified_batch_report.md").read_text(encoding="utf-8")
        self.assertIn("formula_verified_after: 74", report)
        self.assertIn("verified_total_after: 171", report)
        audit = (ROOT / "report" / "frontmatter_audit.md").read_text(encoding="utf-8")
        self.assertIn("missing_required: 767", audit)


if __name__ == "__main__":
    unittest.main()
