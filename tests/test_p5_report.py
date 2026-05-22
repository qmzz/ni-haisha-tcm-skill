#!/usr/bin/env python3
"""P5 final report tests."""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class P5ReportTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, "scripts/build_p5_report.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)

    def test_p5_report_exists_and_has_metrics(self):
        report = ROOT / "report" / "p5_refinement_report.md"
        self.assertTrue(report.exists())
        text = report.read_text(encoding="utf-8")
        self.assertRegex(text, r"verified_sources：(?:72|117|147)")
        self.assertIn("样板标准化条目：10/10", text)
        self.assertIn("P5-A：核心方剂", text)
        self.assertIn("candidate 不等于 verified", text)

    def test_p5_release_notes_exists(self):
        notes = ROOT / "docs" / "p5_release_notes.md"
        self.assertTrue(notes.exists())
        text = notes.read_text(encoding="utf-8")
        self.assertIn("verified_sources:", text)
        self.assertIn("不提供针灸操作指导", text)


if __name__ == "__main__":
    unittest.main()
