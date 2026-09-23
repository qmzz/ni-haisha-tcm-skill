import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def run_tool(tool, payload):
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "tcm_tools.py"), tool, json.dumps(payload, ensure_ascii=False)],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    return json.loads(proc.stdout)

class TcmToolSmokeTests(unittest.TestCase):
    def test_search_formula(self):
        data = run_tool("tcm_search", {"query": "麻黄汤", "category": "formulas"})
        self.assertEqual(data["status"], "success")
        self.assertGreaterEqual(data["count"], 1)
        titles = [r["title"] for r in data["results"]]
        self.assertIn("麻黄汤", titles)

    def test_search_herb(self):
        data = run_tool("tcm_search", {"query": "附子", "category": "herbs"})
        self.assertEqual(data["status"], "success")
        self.assertGreaterEqual(data["count"], 1)

    def test_get_document_herb(self):
        data = run_tool("tcm_doc", {"category": "herbs", "name": "附子"})
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["title"], "附子")
        self.assertIn("## 🌿 神农本草原意与性味气味", data["content"])
        self.assertIn("## 🫀 倪师药性推演与破局心法", data["content"])

    def test_get_document_formula(self):
        data = run_tool("tcm_doc", {"category": "formulas", "name": "真武汤"})
        self.assertEqual(data["status"], "success")
        self.assertIn("## 📜 经方出处与原方配比", data["content"])

    def test_get_document_acupoint(self):
        data = run_tool("tcm_doc", {"category": "acupoints", "name": "足三里"})
        self.assertEqual(data["status"], "success")
        self.assertIn("## 📍 经络归属与精准取穴法", data["content"])

if __name__ == "__main__":
    unittest.main()
