#!/usr/bin/env python3
"""verified frontmatter pilot tests."""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class VerifiedFrontmatterTest(unittest.TestCase):
    def test_verified_frontmatter_written_for_pilot_formula(self):
        text = (ROOT / "knowledge/formulas/guizhi_tang.md").read_text(encoding="utf-8")
        self.assertIn("trace_status: verified", text[:1200])
        self.assertIn("source_refs:", text[:1200])
        self.assertIn("桂枝汤", text[:1200])

    def test_frontmatter_apply_is_idempotent_after_apply(self):
        result = subprocess.run(
            [sys.executable, "scripts/apply_verified_frontmatter.py", "--dry-run"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn('"changed_count": 0', result.stdout)


if __name__ == "__main__":
    unittest.main()
