#!/usr/bin/env python3
"""P5-C core acupoint verified expansion tests."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = {
    "内关",
    "外关",
    "关元",
    "气海",
    "神阙",
    "大椎",
    "命门",
    "太冲",
    "涌泉",
    "中脘",
    "天枢",
    "肺俞",
    "心俞",
    "肝俞",
    "脾俞",
    "肾俞",
    "太溪",
    "列缺",
    "尺泽",
    "委中",
}


class P5CoreAcupointsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for script in [
            "scripts/p5_seed_core_acupoint_decisions.py",
            "scripts/build_verified_sources.py",
        ]:
            subprocess.run([sys.executable, script], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)

    def test_core_acupoints_verified(self):
        rows = [json.loads(line) for line in (ROOT / "data" / "verified_sources.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        names = {r["name"] for r in rows if r["kind"] == "acupoint"}
        self.assertTrue(CORE.issubset(names))
        self.assertGreaterEqual(len(names), 25)

    def test_acupoint_decisions_include_safety_note_and_quality(self):
        rows = [json.loads(line) for line in (ROOT / "data" / "review_decisions.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        row = next(r for r in rows if r.get("item_id") == "neiguan")
        self.assertEqual(row["decision"], "verified")
        self.assertGreaterEqual(row.get("quality_score", 0), 75)
        self.assertIn("不作为针灸操作指导", row.get("notes", ""))


if __name__ == "__main__":
    unittest.main()
