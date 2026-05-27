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
        capture_output=True,
        check=True,
    )
    return json.loads(proc.stdout)


class TcmToolSmokeTests(unittest.TestCase):
    def test_safety_check_blocks_red_flags(self):
        data = run_tool("tcm_safety_check", {"text": "胸痛,呼吸困难"})
        self.assertTrue(data["high_risk"])
        self.assertTrue(data["safety"]["should_stop_formula"])
        self.assertGreaterEqual(len(data["red_flags"]), 2)

    def test_lookup_verified_formula(self):
        data = run_tool("tcm_lookup", {"query": "桂枝汤"})
        self.assertEqual(data["kind"], "formula")
        self.assertEqual(data["trace"]["trace_status"], "verified")
        self.assertTrue(data["markdown"])

    def test_no_source_index_row_is_not_promoted_to_candidate(self):
        data = run_tool("tcm_trace", {"query": "薄荷"})
        self.assertEqual(data["trace_status"], "no_source_found")
        self.assertTrue(data["matches"])
        self.assertEqual(data["matches"][0]["kind"], "herb")

    def test_candidate_with_source_refs_stays_candidate(self):
        data = run_tool("tcm_trace", {"query": "白豆蔻"})
        self.assertEqual(data["trace_status"], "candidate")
        self.assertTrue(data["matches"])
        self.assertTrue(data["matches"][0].get("source_refs"))

    def test_diagnosis_uses_canonical_formula_id_for_trace(self):
        data = run_tool("tcm_diagnose_assist", {"symptoms": ["发热", "恶寒", "项背强几几", "无汗"]})
        self.assertFalse(data["stopped"])
        self.assertEqual(data["formula"]["name"], "葛根汤")
        self.assertEqual(data["formula"]["formula_id"], "getang")
        self.assertEqual(data["formula_trace"]["trace_status"], "verified")
        self.assertEqual(data["formula_trace"]["query"], "getang")

    def test_diagnosis_does_not_trace_wrong_formula_when_id_unknown(self):
        data = run_tool("tcm_diagnose_assist", {"symptoms": ["大便硬", "小便数"]})
        self.assertFalse(data["stopped"])
        self.assertEqual(data["formula"]["name"], "麻子仁丸")
        self.assertEqual(data["formula"]["formula_id"], "")
        self.assertNotEqual(
            (data["formula_trace"].get("matches") or [{}])[0].get("item_id"),
            "maimendong_tang",
        )


if __name__ == "__main__":
    unittest.main()
