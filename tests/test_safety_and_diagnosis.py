#!/usr/bin/env python3
"""基础回归测试：安全边界与典型辨证组合。

这些用例只验证系统行为，不新增医学知识。
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from internal.diagnosis_engine import DiagnosisEngine


class SafetyAndDiagnosisTest(unittest.TestCase):
    def test_taiyang_shanghan_is_cold_pattern(self):
        engine = DiagnosisEngine()
        result = engine.analyze(["发热", "恶寒", "无汗", "脉浮紧"])
        self.assertEqual(result["eight_principles"]["biao_li"], "表证")
        self.assertEqual(result["eight_principles"]["han_re"], "寒证")
        self.assertEqual(result["six_stages"]["subtype"]["name"], "太阳伤寒")
        self.assertEqual(result["formula"]["name"], "麻黄汤")

    def test_red_flags_stop_formula_reference(self):
        engine = DiagnosisEngine()
        result = engine.analyze(["胸痛", "呼吸困难", "发热"])
        self.assertEqual(result["safety"]["risk_level"], "high")
        self.assertIs(result["safety"]["should_stop_formula"], True)
        self.assertGreaterEqual(len(result["safety"]["red_flags"]), 2)

    def test_missing_questions_are_returned(self):
        engine = DiagnosisEngine()
        result = engine.analyze(["发热", "恶寒"])
        self.assertTrue(result["missing_questions"])


if __name__ == "__main__":
    unittest.main()
