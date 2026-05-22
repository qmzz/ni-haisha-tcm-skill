#!/usr/bin/env python3
"""P2 review / verified / trace workflow tests."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from internal.trace_service import TraceService


class P2TraceWorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for script in ["scripts/init_review_decisions.py", "scripts/build_verified_sources.py"]:
            subprocess.run([sys.executable, script], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)

    def test_review_decisions_created(self):
        path = ROOT / "data" / "review_decisions.jsonl"
        self.assertTrue(path.exists())
        with path.open(encoding="utf-8") as f:
            records = [json.loads(line) for line in f]
        self.assertEqual(len(records), 15)
        self.assertTrue(all(r["decision"] == "verified" for r in records))

    def test_verified_sources_created(self):
        path = ROOT / "data" / "verified_sources.jsonl"
        self.assertTrue(path.exists())
        with path.open(encoding="utf-8") as f:
            records = [json.loads(line) for line in f]
        self.assertEqual(len(records), 15)
        self.assertTrue(any(r["kind"] == "formula" and r["name"] == "桂枝汤" for r in records))
        self.assertTrue(any(r["kind"] == "herb" and r["name"] == "麻黄" for r in records))
        self.assertTrue(any(r["kind"] == "acupoint" and r["name"] == "百会" for r in records))

    def test_trace_prefers_exact_verified_match(self):
        result = TraceService().trace("麻黄")
        self.assertEqual(result["trace_status"], "verified")
        self.assertEqual(result["matches"][0]["kind"], "herb")
        self.assertEqual(result["matches"][0]["name"], "麻黄")

    def test_trace_cli_json(self):
        result = subprocess.run(
            [sys.executable, "cli.py", "trace", "桂枝汤", "--json"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        data = json.loads(result.stdout)
        self.assertEqual(data["trace_status"], "verified")
        self.assertEqual(data["matches"][0]["name"], "桂枝汤")


if __name__ == "__main__":
    unittest.main()
