#!/usr/bin/env python3
"""P10-B: alias 查询闭环测试。"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class P10BAliasQueryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Build alias index
        subprocess.run([sys.executable, "scripts/build_alias_index.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)

    def test_alias_index_exists(self):
        path = ROOT / "data" / "alias_index.jsonl"
        self.assertTrue(path.exists())
        rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
        self.assertGreaterEqual(len(rows), 50)
        # Should have herb and acupoint aliases
        kinds = {r["kind"] for r in rows}
        self.assertIn("herb", kinds)
        self.assertIn("acupoint", kinds)

    def test_herb_alias_redirect(self):
        """艾舍(aishe) 应该通过 alias_of 跳转到 艾叶(aoye)。"""
        result = subprocess.run(
            [sys.executable, "tools/tcm_tools.py", "tcm_trace", '{"query":"aishe"}'],
            cwd=ROOT, check=True, capture_output=True, text=True,
        )
        data = json.loads(result.stdout)
        self.assertEqual(data["trace_status"], "verified")
        self.assertIn("alias_redirect", data)
        self.assertEqual(data["alias_redirect"]["to"], "aoye")

    def test_acupoint_alias_redirect(self):
        """赞竹(zanzhu) 应该通过 alias 跳转到 攒竹(cuanzhu)。"""
        result = subprocess.run(
            [sys.executable, "tools/tcm_tools.py", "tcm_trace", '{"query":"zanzhu"}'],
            cwd=ROOT, check=True, capture_output=True, text=True,
        )
        data = json.loads(result.stdout)
        self.assertEqual(data["trace_status"], "verified")
        self.assertIn("alias_redirect", data)
        self.assertEqual(data["alias_redirect"]["to"], "cuanzhu")

    def test_standard_name_no_redirect(self):
        """标准名查询不应触发 alias redirect。"""
        result = subprocess.run(
            [sys.executable, "tools/tcm_tools.py", "tcm_trace", '{"query":"huangbo"}'],
            cwd=ROOT, check=True, capture_output=True, text=True,
        )
        data = json.loads(result.stdout)
        self.assertEqual(data["trace_status"], "verified")
        self.assertNotIn("alias_redirect", data)

    def test_unknown_query_no_alias(self):
        """未知查询不应有 alias redirect。"""
        result = subprocess.run(
            [sys.executable, "tools/tcm_tools.py", "tcm_trace", '{"query":"xyz_unknown"}'],
            cwd=ROOT, check=True, capture_output=True, text=True,
        )
        data = json.loads(result.stdout)
        self.assertNotIn("alias_redirect", data)

    def test_lookup_with_alias(self):
        """tcm_lookup 应该能通过 alias 查到标准条目。"""
        result = subprocess.run(
            [sys.executable, "tools/tcm_tools.py", "tcm_lookup", '{"query":"aishe"}'],
            cwd=ROOT, check=True, capture_output=True, text=True,
        )
        data = json.loads(result.stdout)
        self.assertEqual(data["trace"]["trace_status"], "verified")
        self.assertIn("alias_redirect", data["trace"])


if __name__ == "__main__":
    unittest.main()
