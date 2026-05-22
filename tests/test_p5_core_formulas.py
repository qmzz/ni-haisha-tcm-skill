#!/usr/bin/env python3
"""P5-A core formula verified expansion tests."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = {
    "桂枝加葛根汤",
    "桂枝加厚朴杏子汤",
    "桂枝附子汤",
    "葛根汤",
    "大青龙汤",
    "小青龙汤",
    "麻杏石甘汤",
    "五苓散",
    "猪苓汤",
    "栀子豉汤",
    "白虎加人参汤",
    "调胃承气汤",
    "小承气汤",
    "桃核承气汤",
    "抵当汤",
    "四逆汤",
    "理中汤",
    "真武汤",
    "苓桂术甘汤",
    "半夏泻心汤",
}


class P5CoreFormulasTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for script in [
            "scripts/p5_seed_core_formula_decisions.py",
            "scripts/build_verified_sources.py",
        ]:
            subprocess.run([sys.executable, script], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)

    def test_core_formulas_verified(self):
        rows = [json.loads(line) for line in (ROOT / "data" / "verified_sources.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        formula_names = {r["name"] for r in rows if r["kind"] == "formula"}
        self.assertTrue(CORE.issubset(formula_names))
        self.assertGreaterEqual(len(formula_names), 25)

    def test_decisions_include_quality_metadata(self):
        rows = [json.loads(line) for line in (ROOT / "data" / "review_decisions.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        row = next(r for r in rows if r.get("item_id") == "getang")
        self.assertEqual(row["decision"], "verified")
        self.assertGreaterEqual(row.get("quality_score", 0), 70)
        self.assertIn("match_reason", row)


if __name__ == "__main__":
    unittest.main()
