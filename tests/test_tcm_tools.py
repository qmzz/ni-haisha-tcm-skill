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
    def test_safety_check_blocks_emergency_red_flags(self):
        data = run_tool("tcm_safety_check", {"text": "胸痛,呼吸困难"})
        self.assertEqual(data["risk_level"], "high")
        self.assertTrue(data["high_risk"])
        self.assertTrue(data["blocked"])
        self.assertTrue(data["safety"]["should_stop_formula"])
        self.assertGreaterEqual(len(data["safety"]["emergency_red_flags"]), 2)

    def test_safety_check_blocks_special_population_and_treatment_intent(self):
        data = run_tool("tcm_safety_check", {"text": "孕妇咳嗽怎么吃小青龙汤"})
        self.assertEqual(data["risk_level"], "medium")
        self.assertFalse(data["high_risk"])
        self.assertTrue(data["blocked"])
        self.assertTrue(data["safety"]["special_populations"])
        self.assertTrue(data["safety"]["treatment_intents"])
        self.assertIn("不得输出处方", data["safety"]["allowed_response_scope"])

    def test_diagnosis_stops_for_treatment_intent_even_without_emergency(self):
        data = run_tool("tcm_diagnose_assist", {"symptoms": ["咳嗽", "小青龙汤怎么吃"]})
        self.assertTrue(data["stopped"])
        self.assertEqual(data["safety"]["risk_level"], "medium")
        self.assertIn("停止输出方剂参考", data["reason"])

    def test_safety_policy_tool_exposes_p2_policy(self):
        data = run_tool("tcm_safety_policy", {})
        self.assertEqual(data["policy_version"], "p2-2026-05-28")
        self.assertIn("special_population", data["stop_formula_when"])
        self.assertIn("treatment_or_procedure_intent", data["stop_formula_when"])

    def test_lookup_verified_formula(self):
        data = run_tool("tcm_lookup", {"query": "桂枝汤"})
        self.assertEqual(data["kind"], "formula")
        self.assertEqual(data["trace"]["trace_status"], "verified")
        self.assertTrue(data["markdown"])

    def test_verified_registry_synced_herb_traces_verified(self):
        data = run_tool("tcm_trace", {"query": "薄荷"})
        self.assertEqual(data["trace_status"], "verified")
        self.assertTrue(data["matches"])
        self.assertEqual(data["matches"][0]["kind"], "herb")
        self.assertEqual(data["matches"][0]["item_id"], "bohe")
        self.assertTrue(data["matches"][0].get("source_refs"))

    def test_no_source_index_row_is_not_promoted_to_candidate(self):
        data = run_tool("tcm_trace", {"query": "川贝母"})
        self.assertEqual(data["trace_status"], "no_source_found")
        self.assertTrue(data["matches"])
        self.assertEqual(data["matches"][0]["kind"], "herb")
        self.assertEqual(data["matches"][0]["item_id"], "chuanyubeimu")

    def test_weak_alias_candidate_with_no_source_frontmatter_stays_no_source(self):
        data = run_tool("tcm_trace", {"query": "白豆蔻"})
        self.assertEqual(data["trace_status"], "no_source_found")
        self.assertEqual(data["source_quality_level"], "no_source")
        self.assertTrue(data["matches"])
        self.assertFalse(data["matches"][0].get("source_refs"))

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

    def test_source_quality_levels_tool_documents_boundary(self):
        data = run_tool("tcm_source_quality_levels", {})
        self.assertIn("资料链路可信度", data["boundary"])
        self.assertIn("verified_direct", data["suggested_verified_sublevels"])
        self.assertEqual(data["doc"], "docs/source_quality_levels.md")

    def test_trace_and_lookup_expose_source_quality_level(self):
        trace_data = run_tool("tcm_trace", {"query": "桂枝汤"})
        self.assertEqual(trace_data["trace_status"], "verified")
        self.assertIn(trace_data["source_quality_level"], {"verified_direct", "verified_contextual", "verified_alias"})
        self.assertIn("source_quality_level", trace_data["matches"][0])

        lookup_data = run_tool("tcm_lookup", {"query": "桂枝汤"})
        self.assertIn(lookup_data["source_quality_level"], {"verified_direct", "verified_contextual", "verified_alias"})
        self.assertIn("source_quality_level", lookup_data["trace"])

        explain_data = run_tool("tcm_explain_trace", {"query": "桂枝汤"})
        self.assertIn(explain_data["source_quality_level"], {"verified_direct", "verified_contextual", "verified_alias"})

        diag_data = run_tool("tcm_diagnose_assist", {"symptoms": ["发热", "恶寒", "汗出", "脉浮缓"]})
        self.assertFalse(diag_data["stopped"])
        self.assertIn(diag_data["formula_trace"]["source_quality_level"], {"verified_direct", "verified_contextual", "verified_alias"})

    def test_no_source_trace_reports_no_source_quality(self):
        trace_data = run_tool("tcm_trace", {"query": "川贝母"})
        self.assertEqual(trace_data["trace_status"], "no_source_found")
        self.assertEqual(trace_data["source_quality_level"], "no_source")


if __name__ == "__main__":
    unittest.main()
