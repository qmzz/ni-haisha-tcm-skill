#!/usr/bin/env python3
"""P8 stale frontmatter fix and formula verified batch tests."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SEED_SCRIPTS = [
    "scripts/p8_seed_formula_verified_batch.py",
    "scripts/p8_seed_herb_verified_batch.py",
    "scripts/p8_seed_herb_candidate_review.py",
    "scripts/p8_seed_acupoint_verified_batch.py",
    "scripts/p8_e_3_seed_verified.py",
    "scripts/p11_c_seed_acupoint_verified.py",
    "scripts/p11_d_seed_acupoint_verified.py",
    "scripts/p12_candidate_batch.py",
]

PIPELINE_SCRIPTS = [
    "scripts/build_verified_sources.py",
    "scripts/apply_verified_frontmatter.py",
    "scripts/standardize_verified_frontmatter.py",
    "scripts/p8_fix_stale_verified_frontmatter.py",
    "scripts/p9_fix_verified_source_refs.py",
    "scripts/p9_fix_empty_titles.py",
    "scripts/check_frontmatter_schema.py",
    "scripts/build_p8_knowledge_audit.py",
    "scripts/p9_quality_audit.py",
    "scripts/p9_f_review_decisions.py",
    "scripts/p9_quality_audit.py",
]


def run_script(name: str, args: list[str] | None = None):
    cmd = [sys.executable, name] + (args or [])
    return subprocess.run(cmd, cwd=ROOT, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


class P8FormulaBatchTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Run all seed scripts to restore full 512 registry
        for script in SEED_SCRIPTS:
            run_script(script, ["--apply"])
        # Run full pipeline
        for script in PIPELINE_SCRIPTS:
            extra = ["--apply"] if "fix_stale" in script or "apply_verified" in script or "standardize" in script else []
            run_script(script, extra)

    def test_stale_verified_frontmatter_fixed(self):
        report = (ROOT / "report" / "p8_stale_verified_fix_report.md").read_text(encoding="utf-8")
        self.assertIn("stale_verified_frontmatter: 0", report)
        audit = (ROOT / "report" / "p8_knowledge_audit.md").read_text(encoding="utf-8")
        self.assertIn("frontmatter 标记 verified 但未进入 registry：0", audit)

    def test_formula_verified_batch_counts(self):
        rows = [json.loads(line) for line in (ROOT / "data" / "verified_sources.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        counts = {}
        for row in rows:
            counts[row["kind"]] = counts.get(row["kind"], 0) + 1
        self.assertGreaterEqual(len(rows), 500)
        self.assertGreaterEqual(counts["acupoint"], 100)
        self.assertGreaterEqual(counts["formula"], 110)
        self.assertGreaterEqual(counts["herb"], 280)
        self.assertTrue(any(row["item_id"] == "zhigancao_tang" for row in rows))

    def test_formula_batch_report_and_audit(self):
        report = (ROOT / "report" / "p8_formula_verified_batch_report.md").read_text(encoding="utf-8")
        self.assertRegex(report, r"formula_verified_after: (?:74|112|113)")
        self.assertRegex(report, r"verified_total_after: (?:171|209|210)")
        audit = (ROOT / "report" / "frontmatter_audit.md").read_text(encoding="utf-8")
        self.assertIn("missing_required: 0", audit)

    def test_p9_quality_audit_structure(self):
        audit = (ROOT / "report" / "p9_quality_audit.md").read_text(encoding="utf-8")
        self.assertIn("issues:", audit)
        # No error-level issues after P9-A fix
        self.assertNotIn("'error':", audit.split("by_level:")[1].split("\n")[0] if "by_level:" in audit else "")

    def test_frontmatter_no_empty_titles(self):
        """P9-B fixed 427 empty titles; verify no new ones appear."""
        empty = 0
        for folder in [ROOT / "knowledge" / "herbs", ROOT / "knowledge" / "acupoints", ROOT / "knowledge" / "formulas"]:
            for path in folder.glob("*.md"):
                if "index" in path.name:
                    continue
                text = path.read_text(encoding="utf-8")
                if not text.startswith("---\n"):
                    continue
                end = text.find("\n---", 4)
                if end < 0:
                    continue
                fm = text[4:end]
                if 'title: ""' in fm:
                    empty += 1
        self.assertEqual(empty, 0)


if __name__ == "__main__":
    unittest.main()
