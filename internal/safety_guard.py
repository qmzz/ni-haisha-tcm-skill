#!/usr/bin/env python3
"""
医学安全边界模块。

本模块只做风险提示、分流与输出约束，不提供医学诊断结论。
原则：宁可保守提醒，也不把 Skill 包装成可替代医师的诊断/治疗系统。
"""

from __future__ import annotations

from typing import Dict, List

DISCLAIMER = (
    "本系统仅用于中医理论学习、资料检索和辨证思路参考，"
    "不能替代合格医师的面诊、诊断或治疗。方剂、剂量、针灸等信息不得直接作为用药或操作依据。"
)

SAFETY_POLICY_VERSION = "p2-2026-05-28"

# 高风险医学红旗：命中后停止方剂/针灸建议，提示及时就医。
EMERGENCY_RED_FLAG_RULES = [
    ("胸痛", "胸痛可能涉及心血管等急症风险"),
    ("胸闷", "胸闷伴气短、胸痛时需警惕急症"),
    ("呼吸困难", "呼吸困难属于高风险症状"),
    ("气促", "气促明显时需及时就医"),
    ("喘不过气", "明显呼吸受限需及时就医"),
    ("意识不清", "意识障碍属于高风险症状"),
    ("昏迷", "昏迷属于急症"),
    ("抽搐", "抽搐属于高风险症状"),
    ("惊厥", "惊厥属于高风险症状"),
    ("高热不退", "持续高热需及时就医"),
    ("持续高热", "持续高热需及时就医"),
    ("咯血", "咯血需及时就医"),
    ("便血", "便血需及时就医"),
    ("呕血", "呕血需及时就医"),
    ("大出血", "明显出血需及时就医"),
    ("剧烈腹痛", "剧烈腹痛需排除急腹症"),
    ("腹痛剧烈", "剧烈腹痛需排除急腹症"),
    ("中风", "疑似中风需立即就医"),
    ("卒中", "疑似卒中需立即就医"),
    ("口角歪斜", "口角歪斜需警惕卒中"),
    ("一侧肢体无力", "一侧肢体无力需警惕卒中"),
    ("偏瘫", "偏瘫需警惕卒中"),
    ("自杀", "自伤/自杀风险需立即联系急救或身边可信人员"),
    ("想死", "自伤/自杀风险需立即联系急救或身边可信人员"),
]

# 特殊人群：不一定都是急症，但不应给方剂、剂量、针灸操作参考。
SPECIAL_POPULATION_RULES = [
    ("孕妇", "孕产妇用药和针灸需专业医师评估"),
    ("怀孕", "孕产妇用药和针灸需专业医师评估"),
    ("妊娠", "孕产妇用药和针灸需专业医师评估"),
    ("产后", "产后体质与出血、感染等风险需专业评估"),
    ("哺乳", "哺乳期用药需专业医师评估"),
    ("婴儿", "婴幼儿病情变化快，需专业医师评估"),
    ("幼儿", "儿童用药需专业医师评估"),
    ("小孩", "儿童用药需专业医师评估"),
    ("儿童", "儿童用药需专业医师评估"),
    ("老人", "老年人常合并基础病和用药风险，需专业评估"),
    ("高龄", "高龄人群需专业评估"),
]

# 用户意图风险：防止把资料检索变成处方/操作指导。
TREATMENT_INTENT_RULES = [
    ("怎么吃", "涉及实际用药方法，本工具不能给出处方或服药指导"),
    ("吃多少", "涉及剂量，本工具不能给出处方或服药指导"),
    ("剂量", "涉及剂量，本工具不能给出处方或服药指导"),
    ("开方", "涉及处方，本工具不能替代医师开方"),
    ("处方", "涉及处方，本工具不能替代医师开方"),
    ("抓药", "涉及实际用药，本工具不能给出抓药建议"),
    ("服用", "涉及实际服药，本工具不能给出用药指导"),
    ("用药", "涉及实际用药，本工具不能给出用药指导"),
    ("针刺", "涉及针灸操作，本工具不能给出操作指导"),
    ("扎针", "涉及针灸操作，本工具不能给出操作指导"),
    ("艾灸", "涉及灸法操作，本工具不能给出操作指导"),
    ("穴位怎么扎", "涉及针灸操作，本工具不能给出操作指导"),
]


def _scan_rules(text: str, rules: List[tuple], category: str) -> List[Dict]:
    hits = []
    for keyword, reason in rules:
        if keyword in text:
            hits.append({"keyword": keyword, "reason": reason, "category": category})
    return hits


def normalize_symptoms(symptoms) -> List[str]:
    """Normalize string/list input into a list of non-empty text fragments."""
    if symptoms is None:
        return []
    if isinstance(symptoms, str):
        return [s.strip() for s in symptoms.replace("，", ",").split(",") if s.strip()]
    return [str(s).strip() for s in symptoms if str(s).strip()]


def check_red_flags(symptoms: List[str]) -> Dict:
    """检查输入是否包含需要优先就医或停止医学建议的风险信号。"""
    text = " ".join(normalize_symptoms(symptoms))
    emergency_hits = _scan_rules(text, EMERGENCY_RED_FLAG_RULES, "emergency_red_flag")
    special_hits = _scan_rules(text, SPECIAL_POPULATION_RULES, "special_population")
    intent_hits = _scan_rules(text, TREATMENT_INTENT_RULES, "treatment_or_procedure_intent")

    red_flags = emergency_hits + special_hits + intent_hits
    if emergency_hits:
        risk_level = "high"
        action = "urgent_medical_care"
    elif special_hits:
        risk_level = "medium"
        action = "professional_evaluation_required"
    elif intent_hits:
        risk_level = "medium"
        action = "do_not_provide_prescription_or_operation"
    else:
        risk_level = "low"
        action = "learning_reference_only"

    should_stop_formula = bool(emergency_hits or special_hits or intent_hits)
    should_stop_acupoint_operation = bool(emergency_hits or special_hits or intent_hits)

    return {
        "policy_version": SAFETY_POLICY_VERSION,
        "risk_level": risk_level,
        "action": action,
        "red_flags": red_flags,
        "emergency_red_flags": emergency_hits,
        "special_populations": special_hits,
        "treatment_intents": intent_hits,
        "should_stop_formula": should_stop_formula,
        "should_stop_acupoint_operation": should_stop_acupoint_operation,
        "allowed_response_scope": "只可做资料检索、来源追溯和一般性学习说明；不得输出处方、剂量、抓药、服药或针灸操作指导。",
        "disclaimer": DISCLAIMER,
    }


def safety_policy() -> Dict:
    """Return machine-readable P2 safety policy for Agent callers."""
    return {
        "policy_version": SAFETY_POLICY_VERSION,
        "boundary": DISCLAIMER,
        "stop_formula_when": [
            "emergency_red_flag",
            "special_population",
            "treatment_or_procedure_intent",
        ],
        "risk_levels": {
            "high": "出现急症红旗；停止方剂/穴位建议，提示及时就医。",
            "medium": "特殊人群或实际治疗意图；停止处方、剂量、针灸操作输出，仅保留学习与来源检索。",
            "low": "未命中内置风险；仍必须保留学习参考边界。",
        },
        "red_flag_keywords": [k for k, _ in EMERGENCY_RED_FLAG_RULES],
        "special_population_keywords": [k for k, _ in SPECIAL_POPULATION_RULES],
        "treatment_intent_keywords": [k for k, _ in TREATMENT_INTENT_RULES],
    }


def build_missing_questions(symptoms: List[str]) -> List[str]:
    """根据经方辨证常见关键点生成补充问诊问题。

    问题只用于补充信息，不直接推导新知识。
    """
    text = " ".join(normalize_symptoms(symptoms))
    questions = []
    checks = [
        (("汗", "无汗", "汗出", "自汗", "盗汗"), "是否有汗？是无汗、汗出、自汗还是盗汗？"),
        (("渴", "口渴", "不渴", "喜冷", "喜热"), "是否口渴？喜冷饮还是热饮？"),
        (("大便", "便秘", "下利", "腹泻", "溏"), "大便情况如何？便秘、下利还是正常？"),
        (("小便", "尿", "小便利", "小便不利", "短赤"), "小便情况如何？颜色、次数、有无不利？"),
        (("咳", "喘", "痰"), "有无咳嗽、喘、痰？痰色和痰量如何？"),
        (("舌", "苔"), "舌质、舌苔情况如何？"),
        (("脉",), "脉象如何？浮沉、迟数、虚实、紧缓？"),
    ]
    for keywords, question in checks:
        if not any(k in text for k in keywords):
            questions.append(question)
    return questions[:5]
