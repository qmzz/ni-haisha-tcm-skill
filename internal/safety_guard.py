#!/usr/bin/env python3
"""
安全边界模块。

本模块只做风险提示与输出约束，不提供医学诊断结论。
原则：宁可保守提醒，也不把 Skill 包装成可替代医师的诊断/治疗系统。
"""

from typing import Dict, List

DISCLAIMER = (
    "本系统仅用于中医理论学习、资料检索和辨证思路参考，"
    "不能替代合格医师的面诊、诊断或治疗。方剂、剂量、针灸等信息不得直接作为用药或操作依据。"
)

# 通用医学红旗症状。用于安全拦截，不作为中医知识扩写。
RED_FLAG_RULES = [
    ("胸痛", "胸痛可能涉及急症风险"),
    ("胸闷", "胸闷伴气短、胸痛时需警惕急症"),
    ("呼吸困难", "呼吸困难属于高风险症状"),
    ("气促", "气促明显时需及时就医"),
    ("意识不清", "意识障碍属于高风险症状"),
    ("昏迷", "昏迷属于急症"),
    ("抽搐", "抽搐属于高风险症状"),
    ("高热不退", "持续高热需及时就医"),
    ("咯血", "咯血需及时就医"),
    ("便血", "便血需及时就医"),
    ("呕血", "呕血需及时就医"),
    ("剧烈腹痛", "剧烈腹痛需排除急腹症"),
    ("中风", "疑似中风需立即就医"),
    ("口角歪斜", "口角歪斜需警惕卒中"),
    ("一侧肢体无力", "一侧肢体无力需警惕卒中"),
    ("孕妇", "孕产妇用药和针灸需专业医师评估"),
    ("婴儿", "婴幼儿病情变化快，需专业医师评估"),
    ("幼儿", "儿童用药需专业医师评估"),
]


def check_red_flags(symptoms: List[str]) -> Dict:
    """检查输入症状是否包含需要优先就医的风险信号。"""
    text = " ".join(symptoms)
    hits = []
    for keyword, reason in RED_FLAG_RULES:
        if keyword in text:
            hits.append({"keyword": keyword, "reason": reason})

    return {
        "risk_level": "high" if hits else "low",
        "red_flags": hits,
        "should_stop_formula": bool(hits),
        "disclaimer": DISCLAIMER,
    }


def build_missing_questions(symptoms: List[str]) -> List[str]:
    """根据经方辨证常见关键点生成补充问诊问题。

    问题只用于补充信息，不直接推导新知识。
    """
    text = " ".join(symptoms)
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
