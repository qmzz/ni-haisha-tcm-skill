#!/usr/bin/env python3
"""P5-D sample frontmatter/body standardization tests."""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = [
    "knowledge/formulas/guizhi_tang.md",
    "knowledge/formulas/mahuang_tang.md",
    "knowledge/formulas/xiaochaihu_tang.md",
    "knowledge/formulas/wuling_san.md",
    "knowledge/formulas/banxia_xiexin.md",
    "knowledge/herbs/mahuang.md",
    "knowledge/herbs/guizhi.md",
    "knowledge/herbs/gancao.md",
    "knowledge/herbs/fuzi.md",
    "knowledge/herbs/banxia.md",
]


class P5SampleStandardizationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, "scripts/p5_standardize_sample_frontmatter.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable, "scripts/check_frontmatter_schema.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)

    def test_samples_have_standard_metadata(self):
        for rel in SAMPLES:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("review_status: verified", text)
            self.assertIn("safety_disclaimer_required: true", text)
            self.assertIn("content_scope:", text)
            self.assertIn("<!-- P5_STANDARD_NOTICE_START -->", text)
            self.assertIn("不构成诊断、处方、用药或治疗建议", text)

    def test_frontmatter_audit_improved_by_ten(self):
        report = (ROOT / "report" / "frontmatter_audit.md").read_text(encoding="utf-8")
        self.assertIn("missing_required: 929", report)

    def test_docs_exist(self):
        self.assertTrue((ROOT / "docs" / "p5_refinement_samples.md").exists())


if __name__ == "__main__":
    unittest.main()
