#!/usr/bin/env python3
"""P7-A/P7-B no_source 与 alias 治理测试。"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class P7NoSourceAliasTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, "scripts/p7_classify_no_source.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable, "scripts/p7_build_alias_review.py", "--apply-safe"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)

    def test_no_source_classification_outputs(self):
        path = ROOT / "data" / "no_source_classification.jsonl"
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        self.assertEqual(len(rows), 184)
        categories = {row["category"] for row in rows}
        self.assertIn("alias_candidate", categories)
        self.assertIn("acupoint_name_variant", categories)
        report = (ROOT / "report" / "p7_no_source_classification.md").read_text(encoding="utf-8")
        self.assertIn("no_source_found 条目：184", report)
        self.assertIn("分类结果不等于 verified", report)

    def test_alias_review_outputs(self):
        path = ROOT / "data" / "alias_review.jsonl"
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        self.assertGreaterEqual(len(rows), 4)
        self.assertTrue(any(row["decision"] == "safe_alias" for row in rows))
        report = (ROOT / "report" / "p7_alias_review.md").read_text(encoding="utf-8")
        self.assertIn("alias hit 只能进入 candidate / needs_review", report)

    def test_safe_aliases_present(self):
        aliases = json.loads((ROOT / "data" / "aliases.json").read_text(encoding="utf-8"))
        self.assertIn("刺桐皮", aliases["herb"].get("海桐皮", []))
        self.assertIn("韶脑", aliases["herb"].get("樟脑", []))
        self.assertIn("地丁", aliases["herb"].get("紫花地丁", []))
        self.assertIn("四神聪穴", aliases["acupoint"].get("四神聪", []))


if __name__ == "__main__":
    unittest.main()
