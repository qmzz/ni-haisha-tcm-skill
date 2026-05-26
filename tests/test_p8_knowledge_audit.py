#!/usr/bin/env python3
"""P8-A knowledge completeness audit tests."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class P8KnowledgeAuditTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, "scripts/build_p8_knowledge_audit.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)

    def test_outputs_exist_and_cover_knowledge_base(self):
        data = ROOT / "data" / "knowledge_completeness.jsonl"
        report = ROOT / "report" / "p8_knowledge_audit.md"
        self.assertTrue(data.exists())
        self.assertTrue(report.exists())
        rows = [json.loads(line) for line in data.read_text(encoding="utf-8").splitlines() if line.strip()]
        self.assertEqual(len(rows), 939)
        counts = {}
        for row in rows:
            counts[row["kind"]] = counts.get(row["kind"], 0) + 1
        self.assertEqual(counts, {"formula": 113, "herb": 415, "acupoint": 411})

    def test_metrics_track_registry_and_content_gaps(self):
        rows = [json.loads(line) for line in (ROOT / "data" / "knowledge_completeness.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        verified_registry = sum(1 for row in rows if row["verified_in_registry"])
        self.assertGreaterEqual(verified_registry, 147)
        self.assertTrue(any(row["quality_tier"] == "seed" for row in rows))
        missing_any = any(row["missing_content_fields"] for row in rows)
        self.assertIsInstance(missing_any, bool)
        self.assertTrue(all(row["source_policy"] == "audit_only_not_medical_validation" for row in rows))

    def test_report_contains_p8_a_decision_inputs(self):
        text = (ROOT / "report" / "p8_knowledge_audit.md").read_text(encoding="utf-8")
        self.assertIn("P8-A 知识库完整度审计", text)
        self.assertRegex(text, r"verified 来源链路：(?:147|171|209|210|240|369|374|436|453|461|512|562)")
        self.assertRegex(text, r"frontmatter 标记 verified 但未进入 registry：[01]")
        self.assertIn("quality_tier` 只代表资料治理完备度", text)
        self.assertIn("方剂优先", text)


if __name__ == "__main__":
    unittest.main()
