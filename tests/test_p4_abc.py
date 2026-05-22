#!/usr/bin/env python3
"""P4-A/C/B review loop, quality score, alias candidate tests."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class P4ABCTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for script in [
            "scripts/build_alias_candidates.py",
            "scripts/apply_alias_candidates.py",
            "scripts/build_herb_sources.py",
            "scripts/build_herb_index.py",
            "scripts/build_review_queue.py",
            "scripts/build_review_progress.py",
            "scripts/build_quality_report.py",
        ]:
            subprocess.run([sys.executable, script], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)

    def test_source_hits_have_quality_fields(self):
        with (ROOT / "data" / "herb_sources.jsonl").open(encoding="utf-8") as f:
            records = [json.loads(line) for line in f]
        record = next(r for r in records if r.get("source_hits"))
        hit = record["source_hits"][0]
        self.assertIn("quality_score", hit)
        self.assertIn("match_reason", hit)
        self.assertIn("risk_flags", hit)
        self.assertIn("needs_review_reason", hit)

    def test_alias_candidates_generated(self):
        path = ROOT / "data" / "alias_candidates.jsonl"
        self.assertTrue(path.exists())
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        self.assertTrue(rows)
        self.assertTrue(all(row["status"] == "candidate_only" for row in rows))

    def test_review_import_pending_does_not_add_decision(self):
        decisions = ROOT / "data" / "review_decisions.jsonl"
        before_rows = [json.loads(line) for line in decisions.read_text(encoding="utf-8").splitlines() if line.strip()] if decisions.exists() else []
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".jsonl", delete=False) as f:
            temp_path = Path(f.name)
            f.write(json.dumps({"kind": "herb", "item_id": "temp", "name": "临时", "decision": "pending"}, ensure_ascii=False) + "\n")
        try:
            subprocess.run([sys.executable, "scripts/review_import.py", str(temp_path)], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
            after_rows = [json.loads(line) for line in decisions.read_text(encoding="utf-8").splitlines() if line.strip()] if decisions.exists() else []
            self.assertEqual(len(before_rows), len(after_rows))
            self.assertFalse(any(row.get("item_id") == "temp" for row in after_rows))
        finally:
            temp_path.unlink(missing_ok=True)

    def test_review_apply_outputs_progress(self):
        subprocess.run([sys.executable, "cli.py", "review-apply"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        self.assertTrue((ROOT / "report" / "review_progress.md").exists())


if __name__ == "__main__":
    unittest.main()
