#!/usr/bin/env python3
"""OpenClaw/QwenPaw tool wrapper tests."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TcmToolsTest(unittest.TestCase):
    def run_tool(self, tool, payload):
        result = subprocess.run(
            [sys.executable, "tools/tcm_tools.py", tool, json.dumps(payload, ensure_ascii=False)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(result.stdout)

    def test_safety_check_stops_red_flags(self):
        data = self.run_tool("tcm_safety_check", {"text": "胸痛,呼吸困难"})
        self.assertTrue(data["high_risk"])
        self.assertTrue(data["red_flags"])

    def test_trace_tool_returns_verified(self):
        data = self.run_tool("tcm_trace", {"query": "桂枝汤"})
        self.assertEqual(data["trace_status"], "verified")
        self.assertEqual(data["matches"][0]["name"], "桂枝汤")

    def test_diagnose_assist_has_formula_trace(self):
        data = self.run_tool("tcm_diagnose_assist", {"symptoms": ["发热", "恶寒", "无汗", "脉浮紧"]})
        self.assertFalse(data["stopped"])
        self.assertIn("formula_trace", data)
        self.assertIn(data["formula_trace"]["trace_status"], {"verified", "candidate", "source_search", "no_source_found"})

    def test_diagnose_assist_stops_high_risk(self):
        data = self.run_tool("tcm_diagnose_assist", {"symptoms": ["胸痛", "呼吸困难"]})
        self.assertTrue(data["stopped"])
        self.assertTrue(data["safety"]["high_risk"])


if __name__ == "__main__":
    unittest.main()
