#!/usr/bin/env python3
"""
倪海厦经方推荐器
基于伤寒论和金匮要略的方剂匹配系统

知识来源：倪海厦人纪系列 - 伤寒论、金匮要略、汉唐中医方剂讲解
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class FormulaRecommender:
    """经方推荐器"""
    
    def __init__(self):
        self.knowledge_dir = Path(__file__).parent.parent / "knowledge"
        self.data_dir = Path(__file__).parent.parent / "data"
        
        # 伤寒论 113 方核心方剂库（倪海厦讲解版）
        self.formulas = {
            # === 太阳病篇 ===
            "guizhi_tang": {
                "name": "桂枝汤",
                "source": "伤寒论",
                "category": "太阳病",
                "pattern": "太阳中风证",
                "key_symptoms": ["发热", "恶寒", "汗出", "脉浮缓", "头痛", "鼻鸣干呕"],
                "ingredients": [
                    {"name": "桂枝", "amount": "9g", "role": "君"},
                    {"name": "白芍", "amount": "9g", "role": "臣"},
                    {"name": "生姜", "amount": "9g", "role": "佐"},
                    {"name": "大枣", "amount": "3 枚", "role": "佐"},
                    {"name": "炙甘草", "amount": "6g", "role": "使"}
                ],
                "dosage": "水煎服，日三服",
                "ni_comment": "伤寒论第一方，调和营卫之祖方。桂枝辛温解肌，白芍酸寒敛阴，一散一收，调和营卫。",
                "modifications": [
                    {"symptom": "项背强几几", "add": ["葛根"], "formula": "桂枝加葛根汤"},
                    {"symptom": "喘", "add": ["厚朴", "杏仁"], "formula": "桂枝加厚朴杏子汤"},
                    {"symptom": "阳虚漏汗", "add": ["附子"], "formula": "桂枝加附子汤"}
                ]
            },
            "mahuang_tang": {
                "name": "麻黄汤",
                "source": "伤寒论",
                "category": "太阳病",
                "pattern": "太阳伤寒证",
                "key_symptoms": ["发热", "恶寒", "无汗", "脉浮紧", "头痛", "身痛", "腰痛", "骨节疼痛", "喘"],
                "ingredients": [
                    {"name": "麻黄", "amount": "9g", "role": "君"},
                    {"name": "桂枝", "amount": "6g", "role": "臣"},
                    {"name": "杏仁", "amount": "9g", "role": "佐"},
                    {"name": "炙甘草", "amount": "3g", "role": "使"}
                ],
                "dosage": "水煎服，温覆取汗",
                "ni_comment": "太阳伤寒表实证主方。麻黄发汗解表，桂枝助阳化气，杏仁降气平喘，甘草调和诸药。",
                "modifications": [
                    {"symptom": "烦躁", "add": ["石膏"], "formula": "大青龙汤"},
                    {"symptom": "项背强几几", "add": ["葛根"], "formula": "葛根汤"}
                ]
            },
            "dahuoluo_tang": {
                "name": "大青龙汤",
                "source": "伤寒论",
                "category": "太阳病",
                "pattern": "太阳伤寒兼里热证",
                "key_symptoms": ["发热", "恶寒", "无汗", "烦躁", "脉浮紧"],
                "ingredients": [
                    {"name": "麻黄", "amount": "12g", "role": "君"},
                    {"name": "桂枝", "amount": "6g", "role": "臣"},
                    {"name": "杏仁", "amount": "9g", "role": "佐"},
                    {"name": "生姜", "amount": "9g", "role": "佐"},
                    {"name": "大枣", "amount": "3 枚", "role": "佐"},
                    {"name": "炙甘草", "amount": "6g", "role": "使"},
                    {"name": "石膏", "amount": "15g", "role": "臣"}
                ],
                "dosage": "水煎服，取微汗",
                "ni_comment": "外寒内热之证。麻黄汤加石膏清里热，姜枣调和营卫。烦躁是关键症状。",
                "modifications": []
            },
            "xiaochaihu_tang": {
                "name": "小柴胡汤",
                "source": "伤寒论",
                "category": "少阳病",
                "pattern": "少阳证",
                "key_symptoms": ["往来寒热", "胸胁苦满", "默默不欲饮食", "心烦喜呕", "口苦", "咽干", "目眩"],
                "ingredients": [
                    {"name": "柴胡", "amount": "12g", "role": "君"},
                    {"name": "黄芩", "amount": "9g", "role": "臣"},
                    {"name": "人参", "amount": "9g", "role": "佐"},
                    {"name": "半夏", "amount": "9g", "role": "佐"},
                    {"name": "生姜", "amount": "9g", "role": "佐"},
                    {"name": "大枣", "amount": "3 枚", "role": "佐"},
                    {"name": "炙甘草", "amount": "6g", "role": "使"}
                ],
                "dosage": "水煎服，日三服",
                "ni_comment": "少阳病主方，和解表里之祖方。柴胡透邪外出，黄芩清泄少阳，人参扶正祛邪。",
                "modifications": [
                    {"symptom": "胸中烦而不呕", "remove": ["半夏", "人参"], "add": ["瓜蒌"], "formula": "小柴胡汤去半夏人参加瓜蒌"},
                    {"symptom": "渴", "remove": ["半夏"], "add": ["天花粉"], "formula": "小柴胡汤去半夏加天花粉"}
                ]
            },
            # === 阳明病篇 ===
            "baihu_tang": {
                "name": "白虎汤",
                "source": "伤寒论",
                "category": "阳明病",
                "pattern": "阳明经证",
                "key_symptoms": ["大热", "大汗", "大渴", "脉洪大"],
                "ingredients": [
                    {"name": "石膏", "amount": "30g", "role": "君"},
                    {"name": "知母", "amount": "12g", "role": "臣"},
                    {"name": "粳米", "amount": "15g", "role": "佐"},
                    {"name": "炙甘草", "amount": "6g", "role": "使"}
                ],
                "dosage": "水煎服，米熟汤成",
                "ni_comment": "阳明经证主方，清热生津。石膏大清里热，知母滋阴润燥，粳米甘草护胃。",
                "modifications": [
                    {"symptom": "气津两伤", "add": ["人参"], "formula": "白虎加人参汤"}
                ]
            },
            "tiaohechengqi_tang": {
                "name": "调胃承气汤",
                "source": "伤寒论",
                "category": "阳明病",
                "pattern": "阳明腑证轻证",
                "key_symptoms": ["发热", "便秘", "腹满", "谵语"],
                "ingredients": [
                    {"name": "大黄", "amount": "12g", "role": "君"},
                    {"name": "芒硝", "amount": "9g", "role": "臣"},
                    {"name": "炙甘草", "amount": "6g", "role": "使"}
                ],
                "dosage": "水煎服，温顿服之",
                "ni_comment": "阳明腑实轻证。大黄芒硝泻下通便，甘草缓急和胃。",
                "modifications": []
            },
            # === 太阴病篇 ===
            "lizhong_tang": {
                "name": "理中汤",
                "source": "伤寒论",
                "category": "太阴病",
                "pattern": "太阴脾寒证",
                "key_symptoms": ["腹满而吐", "食不下", "自利益甚", "时腹自痛", "口不渴"],
                "ingredients": [
                    {"name": "人参", "amount": "9g", "role": "君"},
                    {"name": "干姜", "amount": "9g", "role": "臣"},
                    {"name": "白术", "amount": "9g", "role": "佐"},
                    {"name": "炙甘草", "amount": "6g", "role": "使"}
                ],
                "dosage": "水煎服，日三服",
                "ni_comment": "太阴病主方，温中散寒。干姜温中散寒，人参白术健脾益气。",
                "modifications": []
            },
            # === 少阴病篇 ===
            "sini_tang": {
                "name": "四逆汤",
                "source": "伤寒论",
                "category": "少阴病",
                "pattern": "少阴寒化证",
                "key_symptoms": ["无热恶寒", "四肢厥冷", "下利清谷", "脉微细", "但欲寐"],
                "ingredients": [
                    {"name": "附子", "amount": "15g", "role": "君"},
                    {"name": "干姜", "amount": "9g", "role": "臣"},
                    {"name": "炙甘草", "amount": "6g", "role": "使"}
                ],
                "dosage": "水煎服，附子先煎",
                "ni_comment": "少阴寒化主方，回阳救逆。附子大辛大热，回阳救逆第一品药。",
                "modifications": []
            },
            "huanglian ejiao_tang": {
                "name": "黄连阿胶汤",
                "source": "伤寒论",
                "category": "少阴病",
                "pattern": "少阴热化证",
                "key_symptoms": ["心烦", "不得卧", "口燥咽干", "脉细数"],
                "ingredients": [
                    {"name": "黄连", "amount": "12g", "role": "君"},
                    {"name": "黄芩", "amount": "6g", "role": "臣"},
                    {"name": "白芍", "amount": "9g", "role": "佐"},
                    {"name": "阿胶", "amount": "9g", "role": "佐"},
                    {"name": "鸡子黄", "amount": "2 枚", "role": "佐"}
                ],
                "dosage": "水煎服，阿胶烊化，鸡子黄冲服",
                "ni_comment": "少阴热化主方，滋阴降火。黄连黄芩清心火，阿胶鸡子黄滋肾阴。",
                "modifications": []
            },
            # === 厥阴病篇 ===
            "wumei_wan": {
                "name": "乌梅丸",
                "source": "伤寒论",
                "category": "厥阴病",
                "pattern": "厥阴寒热错杂证",
                "key_symptoms": ["消渴", "气上撞心", "心中疼热", "饥而不欲食", "食则吐蛔"],
                "ingredients": [
                    {"name": "乌梅", "amount": "30g", "role": "君"},
                    {"name": "细辛", "amount": "6g", "role": "臣"},
                    {"name": "干姜", "amount": "9g", "role": "臣"},
                    {"name": "黄连", "amount": "9g", "role": "臣"},
                    {"name": "当归", "amount": "9g", "role": "佐"},
                    {"name": "附子", "amount": "9g", "role": "佐"},
                    {"name": "蜀椒", "amount": "6g", "role": "佐"},
                    {"name": "桂枝", "amount": "9g", "role": "佐"},
                    {"name": "人参", "amount": "9g", "role": "佐"},
                    {"name": "黄柏", "amount": "9g", "role": "佐"}
                ],
                "dosage": "蜜丸，每服 10 丸",
                "ni_comment": "厥阴病主方，寒热并用。乌梅酸收敛肝，黄连黄柏清热，附子干姜温阳。",
                "modifications": []
            },
            # === 金匮要略方 ===
            "shenqi_wan": {
                "name": "肾气丸",
                "source": "金匮要略",
                "category": "杂病",
                "pattern": "肾阳虚证",
                "key_symptoms": ["腰膝酸软", "畏寒肢冷", "小便不利", "舌淡胖", "脉沉弱"],
                "ingredients": [
                    {"name": "干地黄", "amount": "24g", "role": "君"},
                    {"name": "山药", "amount": "12g", "role": "臣"},
                    {"name": "山茱萸", "amount": "12g", "role": "臣"},
                    {"name": "泽泻", "amount": "9g", "role": "佐"},
                    {"name": "茯苓", "amount": "9g", "role": "佐"},
                    {"name": "牡丹皮", "amount": "9g", "role": "佐"},
                    {"name": "桂枝", "amount": "3g", "role": "佐"},
                    {"name": "附子", "amount": "3g", "role": "佐"}
                ],
                "dosage": "蜜丸，每服 15 丸",
                "ni_comment": "补肾阳之祖方。六味地黄丸加桂附，阴中求阳，少火生气。",
                "modifications": []
            }
        }
        
        # 症状 - 方剂映射
        self.symptom_formula_map = self._build_symptom_map()
    
    def _build_symptom_map(self) -> Dict:
        """构建症状 - 方剂映射"""
        symptom_map = {}
        
        for formula_key, formula in self.formulas.items():
            for symptom in formula["key_symptoms"]:
                if symptom not in symptom_map:
                    symptom_map[symptom] = []
                symptom_map[symptom].append(formula_key)
        
        return symptom_map
    
    def recommend(self, symptoms: List[str], pattern: Optional[str] = None) -> Dict:
        """
        给出相关方剂参考
        
        Args:
            symptoms: 症状列表
            pattern: 证型（可选）
            
        Returns:
            方剂推荐结果
        """
        # 1. 基础方剂匹配
        matched_formulas = self._match_formulas(symptoms)
        
        if not matched_formulas:
            return {
                "success": False,
                "message": "未找到匹配的方剂",
                "suggestions": ["请提供更多症状信息", "建议咨询专业中医师"]
            }
        
        # 2. 排序（按匹配度）
        matched_formulas.sort(key=lambda x: x["match_score"], reverse=True)
        
        # 3. 首选方剂
        best_formula = matched_formulas[0]
        formula_data = self.formulas[best_formula["key"]]
        
        # 4. 随证加减
        modifications = self._suggest_modifications(formula_data, symptoms)
        
        # 5. 剂量调整（倪海厦经验）
        dosage_notes = self._generate_dosage_notes(formula_data)
        
        return {
            "success": True,
            "formula": {
                "name": formula_data["name"],
                "source": formula_data["source"],
                "category": formula_data["category"],
                "pattern": formula_data["pattern"],
                "match_score": best_formula["match_score"]
            },
            "ingredients": formula_data["ingredients"],
            "dosage": formula_data["dosage"],
            "ni_comment": formula_data.get("ni_comment", ""),
            "modifications": modifications,
            "dosage_notes": dosage_notes,
            "alternatives": [self.formulas[f["key"]] for f in matched_formulas[1:3]] if len(matched_formulas) > 1 else []
        }
    
    def _match_formulas(self, symptoms: List[str]) -> List[Dict]:
        """匹配方剂"""
        matched = []
        
        for formula_key, formula in self.formulas.items():
            # 计算症状匹配数
            match_count = sum(1 for s in symptoms if any(key_sym in s for key_sym in formula["key_symptoms"]))
            match_score = match_count / len(formula["key_symptoms"])
            
            if match_score > 0.3:  # 30% 匹配度阈值
                matched.append({
                    "key": formula_key,
                    "match_score": match_score,
                    "matched_symptoms": [s for s in symptoms if any(key_sym in s for key_sym in formula["key_symptoms"])]
                })
        
        return matched
    
    def _suggest_modifications(self, formula: Dict, symptoms: List[str]) -> List[str]:
        """建议方剂加减"""
        modifications = []
        
        for mod in formula.get("modifications", []):
            if any(sym in s for s in symptoms for sym in mod["symptom"]):
                add_str = " + ".join(mod.get("add", []))
                remove_str = " - ".join(mod.get("remove", []))
                
                if add_str and remove_str:
                    modifications.append(f"{mod['symptom']}：加{add_str}，减{remove_str} → {mod['formula']}")
                elif add_str:
                    modifications.append(f"{mod['symptom']}：加{add_str} → {mod['formula']}")
                elif remove_str:
                    modifications.append(f"{mod['symptom']}：减{remove_str} → {mod['formula']}")
        
        return modifications
    
    def _generate_dosage_notes(self, formula: Dict) -> List[str]:
        """生成剂量说明（倪海厦经验）"""
        notes = []
        
        # 特殊煎煮方法
        if "附子" in [i["name"] for i in formula["ingredients"]]:
            notes.append("⚠️ 附子有毒，需先煎 30 分钟以上")
        
        if "阿胶" in [i["name"] for i in formula["ingredients"]]:
            notes.append("阿胶烊化（用热水溶化后兑入药液）")
        
        if "鸡子黄" in [i["name"] for i in formula["ingredients"]]:
            notes.append("鸡子黄冲服（药液稍凉后打入蛋黄搅匀）")
        
        if "芒硝" in [i["name"] for i in formula["ingredients"]]:
            notes.append("芒硝冲服（用药液溶化后服）")
        
        # 服用注意
        if "麻黄" in [i["name"] for i in formula["ingredients"]]:
            notes.append("服麻黄汤后温覆取汗，但不可大汗淋漓")
        
        return notes
    
    def query_formula(self, name: str) -> Dict:
        """
        查询方剂详情
        
        Args:
            name: 方剂名
            
        Returns:
            方剂详情
        """
        # 模糊匹配
        for key, formula in self.formulas.items():
            if name in formula["name"] or formula["name"] in name:
                return {
                    "success": True,
                    "formula": formula
                }
        
        return {
            "success": False,
            "message": f"未找到方剂：{name}",
            "available_formulas": list(set(f["name"] for f in self.formulas.values()))
        }


if __name__ == "__main__":
    # 测试方剂推荐器
    recommender = FormulaRecommender()
    
    # 测试用例 1：太阳中风
    print("=" * 60)
    print("测试 1：太阳中风证")
    print("=" * 60)
    result = recommender.recommend(["发热", "恶寒", "汗出", "脉浮缓"])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 测试用例 2：太阳伤寒
    print("\n" + "=" * 60)
    print("测试 2：太阳伤寒证")
    print("=" * 60)
    result = recommender.recommend(["发热", "恶寒", "无汗", "脉浮紧", "头痛"])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 测试用例 3：少阳证
    print("\n" + "=" * 60)
    print("测试 3：少阳证")
    print("=" * 60)
    result = recommender.recommend(["往来寒热", "胸胁苦满", "口苦", "咽干"])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 测试用例 4：方剂查询
    print("\n" + "=" * 60)
    print("测试 4：查询桂枝汤")
    print("=" * 60)
    result = recommender.query_formula("桂枝汤")
    print(json.dumps(result, ensure_ascii=False, indent=2))
