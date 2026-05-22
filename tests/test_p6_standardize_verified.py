#!/usr/bin/env python3
"""P6-A standardize all verified entries tests."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class P6StandardizeVerifiedTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, "scripts/standardize_verified_frontmatter.py", "--apply"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable, "scripts/check_frontmatter_schema.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)

    def test_all_verified_entries_have_standard_fields(self):
        rows = [json.loads(line) for line in (ROOT / "data" / "verified_sources.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        self.assertGreaterEqual(len(rows), 72)
        for row in rows:
            text = (ROOT / row["file"]).read_text(encoding="utf-8")
            self.assertIn("review_status: verified", text)
            self.assertIn("safety_disclaimer_required: true", text)
            self.assertIn("content_scope:", text)
            self.assertIn("<!-- P5_STANDARD_NOTICE_START -->", text)
            self.assertIn("不构成诊断、处方、用药、针灸操作或治疗建议", text)
            self.assertIn("title:", text.split("---", 2)[1])

    def test_frontmatter_audit_verified_reduction(self):
        report = (ROOT / "report" / "frontmatter_audit.md").read_text(encoding="utf-8")
        self.assertIn("missing_required: 821", report)


if __name__ == "__main__":
    unittest.main()
