#!/usr/bin/env python3
"""
倪海厦中医辨证辅助引擎（扩展版）
基于六经辨证、八纲辨证、脏腑辨证提供学习参考
覆盖 50+ 方剂

知识来源：倪海厦人纪系列 - 伤寒论、金匮要略、黄帝内经
"""

import json
from pathlib import Path
from typing import List, Dict, Optional

try:
    from internal.safety_guard import DISCLAIMER, build_missing_questions, check_red_flags
except ImportError:  # 兼容直接从 internal 目录运行的情况
    from safety_guard import DISCLAIMER, build_missing_questions, check_red_flags


class DiagnosisEngine:
    """中医诊断引擎（扩展版）"""

    def __init__(self):
        self.knowledge_dir = Path(__file__).parent.parent / "knowledge"
        self.data_dir = Path(__file__).parent.parent / "data"

        # 加载症状-方剂映射
        try:
            with open(self.data_dir / "symptom_formula.json", 'r') as f:
                self.symptom_formula = json.load(f)
        except FileNotFoundError:
            self.symptom_formula = {"symptoms": {}}

        # 六经辨证知识库（50+方剂）
        self.six_stages = {
            "taiyang": {
                "name": "太阳病",
                "description": "表证，邪在肌表",
                "symptoms": ["发热", "恶寒", "头痛", "项强", "脉浮", "身痛", "骨节痛", "鼻鸣干呕"],
                "subtypes": {
                    "zhongfeng": {"name": "太阳中风", "key_symptoms": ["发热", "恶寒", "汗出", "脉浮缓"], "formula": "桂枝汤", "formula_id": "guizhi_tang"},
                    "shanghan": {"name": "太阳伤寒", "key_symptoms": ["发热", "恶寒", "无汗", "脉浮紧"], "formula": "麻黄汤", "formula_id": "mahuang_tang"},
                    "daqinglong": {"name": "太阳伤寒兼里热", "key_symptoms": ["发热", "恶寒", "无汗", "烦躁", "脉浮紧"], "formula": "大青龙汤", "formula_id": "dahuoluo_tang"},
                    "xiaochilong": {"name": "外寒内饮", "key_symptoms": ["发热", "恶寒", "咳喘", "痰多清稀"], "formula": "小青龙汤", "formula_id": "xiaoqinglong_tang"},
                    "gegen": {"name": "太阳兼经输不利", "key_symptoms": ["发热", "恶寒", "项背强几几", "无汗"], "formula": "葛根汤", "formula_id": "ge_gen_tang"},
                    "gegen_jiashu": {"name": "太阳兼经输不利有汗", "key_symptoms": ["发热", "恶寒", "项背强几几", "汗出"], "formula": "桂枝加葛根汤", "formula_id": "guizhi_jiagetang"},
                    "guizhi_jiahoupo": {"name": "太阳中风兼喘", "key_symptoms": ["发热", "恶风", "汗出", "咳喘"], "formula": "桂枝加厚朴杏子汤", "formula_id": "guizhi_houpuxingzi"},
                    "guizhi_jiafuzi": {"name": "太阳阳虚", "key_symptoms": ["恶风", "汗出不止", "小便难", "四肢微急"], "formula": "桂枝加附子汤", "formula_id": "guizhi_fuzi"},
                    "maxing_shigan": {"name": "邪热壅肺", "key_symptoms": ["咳喘", "发热", "口渴", "痰黄"], "formula": "麻杏甘石汤", "formula_id": "maxing_shigan"},
                    "wusan": {"name": "太阳蓄水", "key_symptoms": ["发热", "口渴", "小便不利", "脉浮"], "formula": "五苓散", "formula_id": "wuling_san"},
                }
            },
            "yangming": {
                "name": "阳明病",
                "description": "里热证，邪热炽盛",
                "symptoms": ["发热", "大汗", "口渴", "脉洪大", "潮热", "谵语", "腹满痛", "便秘", "不恶寒反恶热"],
                "subtypes": {
                    "jingzheng": {"name": "阳明经证", "key_symptoms": ["大热", "大汗", "大渴", "脉洪大"], "formula": "白虎汤", "formula_id": "baihu_tang"},
                    "fuzheng": {"name": "阳明腑实", "key_symptoms": ["潮热", "谵语", "腹满痛", "便秘"], "formula": "大承气汤", "formula_id": "dachengqi_tang"},
                    "fuzheng_qing": {"name": "阳明腑实轻证", "key_symptoms": ["腹胀满", "谵语", "大便硬"], "formula": "小承气汤", "formula_id": "xiaochengqi_tang"},
                    "fuzheng_weijishi": {"name": "阳明腑实胃热", "key_symptoms": ["心烦", "腹胀满", "大便不通"], "formula": "调胃承气汤", "formula_id": "tiaoweichengqi"},
                    "qirensun": {"name": "阳明热盛气津两伤", "key_symptoms": ["大热", "大汗", "大渴", "脉洪大无力"], "formula": "白虎加人参汤", "formula_id": "baihu_renshen"},
                    "zhizi_chi": {"name": "热扰胸膈", "key_symptoms": ["虚烦不得眠", "心中懊憹"], "formula": "栀子豉汤", "formula_id": "zhizi_chi"},
                    "maziren": {"name": "脾约", "key_symptoms": ["大便硬", "小便数"], "formula": "麻子仁丸", "formula_id": "maimendong_tang"},
                }
            },
            "shaoyang": {
                "name": "少阳病",
                "description": "半表半里证",
                "symptoms": ["往来寒热", "胸胁苦满", "默默不欲饮食", "心烦喜呕", "口苦", "咽干", "目眩", "耳聋"],
                "subtypes": {
                    "xiaochaihu": {"name": "少阳证", "key_symptoms": ["往来寒热", "胸胁苦满", "口苦", "咽干", "目眩"], "formula": "小柴胡汤", "formula_id": "xiaochaihu_tang"},
                    "dachaihu": {"name": "少阳兼阳明", "key_symptoms": ["往来寒热", "心下急", "郁郁微烦", "便秘"], "formula": "大柴胡汤", "formula_id": "dachaihu_tang"},
                    "chaihu_guizhi": {"name": "少阳兼太阳", "key_symptoms": ["发热", "恶寒", "支节烦痛", "微呕"], "formula": "柴胡桂枝汤", "formula_id": "chaihu_guizhi"},
                    "chaihu_guizhi_ganjiang": {"name": "少阳兼水饮", "key_symptoms": ["胸胁满微结", "小便不利", "渴而不呕"], "formula": "柴胡桂枝干姜汤", "formula_id": "chaihu_longgu"},
                    "chaihu_jialonggu": {"name": "少阳兼烦惊", "key_symptoms": ["胸满", "烦惊", "谵语", "小便不利"], "formula": "柴胡加龙骨牡蛎汤", "formula_id": "chaihu_longgu"},
                }
            },
            "taiyin": {
                "name": "太阴病",
                "description": "脾虚寒湿证",
                "symptoms": ["腹满", "吐", "食不下", "自利", "口不渴", "时腹自痛"],
                "subtypes": {
                    "pihan": {"name": "太阴脾寒", "key_symptoms": ["腹满而吐", "食不下", "自利益甚", "时腹自痛"], "formula": "理中汤", "formula_id": "lizhong_tang"},
                    "fuzi_lizhong": {"name": "太阴虚寒重证", "key_symptoms": ["腹痛剧烈", "畏寒肢冷", "下利清谷"], "formula": "附子理中丸", "formula_id": "lizhong_wan"},
                    "xiaojianzhong": {"name": "中焦虚寒", "key_symptoms": ["腹中急痛", "喜温喜按", "心悸而烦"], "formula": "小建中汤", "formula_id": "xiaojianzhong_tang"},
                    "huangqi_jianzhong": {"name": "气虚虚劳", "key_symptoms": ["腹中急痛", "气短乏力", "自汗"], "formula": "黄芪建中汤", "formula_id": "huangqi_jianzhong"},
                    "danggui_jianzhong": {"name": "血虚虚劳", "key_symptoms": ["腹中急痛", "面色萎黄", "心悸"], "formula": "当归建中汤", "formula_id": "danggui_jianzhong"},
                    "wuma_wan": {"name": "虚寒腹痛", "key_symptoms": ["绕脐腹痛", "冷汗出", "手足厥冷"], "formula": "乌头桂枝汤", "formula_id": "danggui_sini"},
                }
            },
            "shaoyin": {
                "name": "少阴病",
                "description": "心肾虚衰证",
                "symptoms": ["脉微细", "但欲寐", "四肢厥冷", "下利清谷", "无热恶寒", "心烦", "不寐"],
                "subtypes": {
                    "hanhua": {"name": "少阴寒化", "key_symptoms": ["无热恶寒", "四肢厥冷", "下利清谷", "脉微细"], "formula": "四逆汤", "formula_id": "sini_tang"},
                    "rehua": {"name": "少阴热化", "key_symptoms": ["心烦", "不得卧", "口燥咽干", "脉细数"], "formula": "黄连阿胶汤", "formula_id": "huanglian_ejiao"},
                    "shen_yangxu": {"name": "少阴阳虚水泛", "key_symptoms": ["小便不利", "四肢沉重疼痛", "腹痛下利"], "formula": "真武汤", "formula_id": "zhenwu_tang"},
                    "tongmai_sini": {"name": "少阴寒化重证", "key_symptoms": ["下利清谷", "脉微欲绝", "身反不恶寒"], "formula": "通脉四逆汤", "formula_id": "tongmai_sini"},
                    "shaoyao_gancao": {"name": "筋脉拘急", "key_symptoms": ["脚挛急", "腹挛急"], "formula": "芍药甘草汤", "formula_id": "shaoyao_gancao"},
                    "si_ni_san": {"name": "阳郁厥逆", "key_symptoms": ["手足厥冷", "但身热", "咳悸"], "formula": "四逆散", "formula_id": "sini_san"},
                    "danggui_sini": {"name": "血虚寒厥", "key_symptoms": ["手足厥寒", "脉细欲绝", "腰腿冷痛"], "formula": "当归四逆汤", "formula_id": "danggui_sini"},
                    "danggui_sini_wuzhuyu": {"name": "血虚寒厥兼久寒", "key_symptoms": ["手足厥寒", "脉细欲绝", "呕吐腹痛"], "formula": "当归四逆加吴茱萸生姜汤", "formula_id": "danggui_sini"},
                }
            },
            "jueyin": {
                "name": "厥阴病",
                "description": "寒热错杂证",
                "symptoms": ["消渴", "气上撞心", "心中疼热", "饥而不欲食", "食则吐蛔", "下之利不止", "巅顶痛", "吐涎"],
                "subtypes": {
                    "hanre_cuozha": {"name": "厥阴寒热错杂", "key_symptoms": ["消渴", "气上撞心", "心中疼热", "饥而不欲食", "食则吐蛔"], "formula": "乌梅丸", "formula_id": "wumei_wan"},
                    "wuzhuyu_tang": {"name": "肝寒犯胃", "key_symptoms": ["巅顶痛", "干呕吐涎沫", "手足厥冷"], "formula": "吴茱萸汤", "formula_id": "danggui_sini"},
                    "jueyin_banxia": {"name": "上热下寒", "key_symptoms": ["手足厥冷", "喉痹", "唾脓血", "泄利不止"], "formula": "麻黄升麻汤", "formula_id": "mahuang_shengma"},
                }
            },
            "zabing": {
                "name": "杂病",
                "description": "金匮要略杂病",
                "symptoms": ["胸痹", "痰饮", "水肿", "黄疸", "淋证", "带下", "痛经", "失眠", "痹证", "梅核气"],
                "subtypes": {
                    "xiongbi": {"name": "胸阳不振", "key_symptoms": ["胸痹", "短气", "胸背痛"], "formula": "瓜蒌薤白白酒汤", "formula_id": "gualou_xiebai"},
                    "xiongbi_tan": {"name": "胸阳不振痰浊", "key_symptoms": ["胸痹", "不得卧", "心痛彻背"], "formula": "瓜蒌薤白半夏汤", "formula_id": "gualou_xiebai"},
                    "tanyin": {"name": "中阳不足痰饮", "key_symptoms": ["胸胁支满", "目眩", "心悸", "气短"], "formula": "苓桂术甘汤", "formula_id": "fuling_guizhi"},
                    "yushui": {"name": "阳虚水肿", "key_symptoms": ["一身悉肿", "恶风", "小便不利"], "formula": "越婢汤", "formula_id": "yuebi_tang"},
                    "huangdan": {"name": "阳黄", "key_symptoms": ["面目发黄", "如橘色", "小便黄"], "formula": "茵陈蒿汤", "formula_id": "yinchen_hao"},
                    "linzheng": {"name": "热淋", "key_symptoms": ["小便淋沥", "涩痛", "短赤"], "formula": "八正散", "formula_id": "yuebi_zhu"},
                    "mopi": {"name": "气滞痰凝", "key_symptoms": ["咽中如有炙脔"], "formula": "半夏厚朴汤", "formula_id": "banxia_houpo"},
                    "shimian": {"name": "阴虚火旺失眠", "key_symptoms": ["虚烦不眠", "心悸", "盗汗"], "formula": "酸枣仁汤", "formula_id": "wumei_wan"},
                    "wenjing": {"name": "虚寒瘀血", "key_symptoms": ["月经不调", "久不受孕", "少腹冷痛"], "formula": "温经汤", "formula_id": "wenjing_tang"},
                    "zhigancao": {"name": "气阴两虚", "key_symptoms": ["心动悸", "脉结代", "虚羸少气"], "formula": "炙甘草汤", "formula_id": "zhigancao_tang"},
                    "baixi": {"name": "风湿相搏", "key_symptoms": ["骨节疼烦", "掣痛不得屈伸"], "formula": "甘草附子汤", "formula_id": "gancao_fuzi"},
                    "zhujing": {"name": "血虚", "key_symptoms": ["面色萎黄", "月经量少", "头晕目眩"], "formula": "四物汤", "formula_id": "danggui_sini"},
                    "shenqiwan": {"name": "肾阳虚", "key_symptoms": ["腰膝酸冷", "小便不利", "脚软"], "formula": "肾气丸", "formula_id": "shenqi_wan"},
                    "banxia_xiexin": {"name": "寒热错杂痞", "key_symptoms": ["心下痞", "但满不痛", "呕吐"], "formula": "半夏泻心汤", "formula_id": "banxia_xiexin"},
                    "xie_xin": {"name": "热痞", "key_symptoms": ["心下痞", "按之濡", "口渴", "心烦"], "formula": "大黄黄连泻心汤", "formula_id": "dahuang_huanglian"},
                    "taohe_chengqi": {"name": "下焦蓄血", "key_symptoms": ["少腹急结", "其人如狂"], "formula": "桃核承气汤", "formula_id": "taohe_chengqi"},
                }
            }
        }

        # 八纲辨证
        self.eight_principles = {
            "biao_li": {
                "biao": ["发热", "恶寒", "头痛", "身痛", "脉浮", "鼻鸣干呕"],
                "li": ["腹满", "便秘", "烦躁", "谵语", "脉沉", "潮热", "腹满痛"]
            },
            "han_re": {
                "han": ["恶寒", "喜温", "口不渴", "小便清长", "大便溏薄", "四肢厥冷", "下利清谷"],
                "re": ["发热", "喜凉", "口渴", "小便短赤", "大便秘结", "大热", "大汗"]
            },
            "xu_shi": {
                "xu": ["神疲", "乏力", "气短", "懒言", "脉虚", "脉微细", "自汗", "但欲寐"],
                "shi": ["烦躁", "谵语", "腹痛拒按", "脉实", "腹满痛", "便秘", "潮热"]
            }
        }

        # 方剂推荐知识库（50+方剂）
        self.formula_details = {
            "桂枝汤": {"source": "伤寒论", "ingredients": "桂枝9g、白芍9g、生姜9g、大枣3枚、炙甘草6g", "dosage": "水煎服，温覆取微汗", "contraindications": "无汗者不宜", "ni_comment": "伤寒论第一方，调和营卫之祖方"},
            "麻黄汤": {"source": "伤寒论", "ingredients": "麻黄9g、桂枝6g、杏仁9g、炙甘草3g", "dosage": "水煎服，先煮麻黄去上沫", "contraindications": "有汗者不宜", "ni_comment": "太阳伤寒表实证主方"},
            "大青龙汤": {"source": "伤寒论", "ingredients": "麻黄12g、桂枝6g、杏仁9g、炙甘草6g、生姜9g、大枣3枚、石膏15g", "dosage": "水煎服，取微汗", "contraindications": "汗多者不宜", "ni_comment": "外寒内热兼烦躁"},
            "小青龙汤": {"source": "伤寒论", "ingredients": "麻黄9g、桂枝9g、干姜9g、细辛3g、五味子6g、白芍9g、半夏9g、炙甘草6g", "dosage": "水煎服", "contraindications": "阴虚燥咳者不宜", "ni_comment": "外寒内饮咳喘痰多"},
            "葛根汤": {"source": "伤寒论", "ingredients": "葛根12g、麻黄9g、桂枝6g、白芍6g、炙甘草6g、生姜9g、大枣3枚", "dosage": "水煎服", "contraindications": "有汗者不宜", "ni_comment": "项背强几几无汗者"},
            "小柴胡汤": {"source": "伤寒论", "ingredients": "柴胡12g、黄芩9g、人参9g、半夏9g、生姜9g、大枣4枚、炙甘草9g", "dosage": "水煎服", "contraindications": "太阳表证忌用", "ni_comment": "和解少阳第一方"},
            "大柴胡汤": {"source": "伤寒论", "ingredients": "柴胡12g、黄芩9g、白芍9g、半夏9g、生姜15g、大枣4枚、枳实9g、大黄6g", "dosage": "水煎服", "contraindications": "纯虚证不宜", "ni_comment": "少阳兼阳明腑实"},
            "白虎汤": {"source": "伤寒论", "ingredients": "石膏30g、知母9g、炙甘草3g、粳米9g", "dosage": "水煎服，石膏先煎", "contraindications": "脾胃虚寒者不宜", "ni_comment": "阳明经证主方，清热生津"},
            "白虎加人参汤": {"source": "伤寒论", "ingredients": "石膏30g、知母9g、炙甘草3g、粳米9g、人参9g", "dosage": "水煎服", "contraindications": "无热者不宜", "ni_comment": "热盛伤津兼气虚"},
            "大承气汤": {"source": "伤寒论", "ingredients": "大黄12g、芒硝9g、厚朴15g、枳实9g", "dosage": "先煮朴实，后下大黄，芒硝冲服", "contraindications": "无实热者不宜", "ni_comment": "峻下热结第一方"},
            "小承气汤": {"source": "伤寒论", "ingredients": "大黄9g、厚朴6g、枳实6g", "dosage": "水煎服", "contraindications": "无实热者不宜", "ni_comment": "阳明腑实轻证"},
            "调胃承气汤": {"source": "伤寒论", "ingredients": "大黄12g、芒硝9g、炙甘草6g", "dosage": "大黄、甘草水煎，芒硝冲服", "contraindications": "无实热者不宜", "ni_comment": "胃热燥结，心烦口渴"},
            "理中汤": {"source": "伤寒论", "ingredients": "人参9g、干姜9g、白术9g、炙甘草9g", "dosage": "水煎服", "contraindications": "热证不宜", "ni_comment": "太阴病主方，温中散寒"},
            "四逆汤": {"source": "伤寒论", "ingredients": "附子9g、干姜6g、炙甘草6g", "dosage": "附子先煎，水煎服", "contraindications": "热证禁用", "ni_comment": "回阳救逆第一方"},
            "通脉四逆汤": {"source": "伤寒论", "ingredients": "附子15g、干姜9g、炙甘草6g", "dosage": "附子先煎，水煎服", "contraindications": "热证禁用", "ni_comment": "少阴寒化重证，回阳力更强"},
            "真武汤": {"source": "伤寒论", "ingredients": "附子9g、茯苓9g、白术6g、生姜9g、白芍9g", "dosage": "附子先煎，水煎服", "contraindications": "阴虚火旺者不宜", "ni_comment": "温阳利水代表方"},
            "乌梅丸": {"source": "伤寒论", "ingredients": "乌梅300枚、细辛18g、干姜30g、黄连48g、附子18g、蜀椒12g、桂枝18g、人参18g、黄柏18g、当归12g", "dosage": "丸剂或汤剂", "contraindications": "纯热证不宜", "ni_comment": "厥阴病主方，寒热并用"},
            "五苓散": {"source": "伤寒论", "ingredients": "猪苓9g、泽泻15g、白术9g、茯苓9g、桂枝6g", "dosage": "散剂或汤剂", "contraindications": "津液不足者不宜", "ni_comment": "利水渗湿第一方"},
            "黄连阿胶汤": {"source": "伤寒论", "ingredients": "黄连12g、黄芩6g、白芍6g、阿胶9g、鸡子黄2枚", "dosage": "水煎，入阿胶鸡子黄搅匀", "contraindications": "寒证不宜", "ni_comment": "阴虚火旺失眠第一方"},
            "半夏泻心汤": {"source": "伤寒论", "ingredients": "半夏12g、黄芩9g、干姜9g、人参9g、黄连3g、大枣4枚、炙甘草9g", "dosage": "水煎服", "contraindications": "纯虚纯实不宜", "ni_comment": "心下痞寒热错杂"},
            "炙甘草汤": {"source": "伤寒论", "ingredients": "炙甘草12g、生姜9g、人参6g、生地48g、桂枝9g、阿胶6g、麦冬12g、麻仁9g、大枣30枚", "dosage": "水煎服，阿胶烊化", "contraindications": "无虚证不宜", "ni_comment": "心动悸脉结代第一方"},
            "小建中汤": {"source": "伤寒论", "ingredients": "桂枝9g、白芍18g、生姜9g、大枣4枚、炙甘草6g、饴糖30g", "dosage": "水煎，饴糖烊化", "contraindications": "实热证不宜", "ni_comment": "虚劳腹痛第一方"},
            "栀子豉汤": {"source": "伤寒论", "ingredients": "栀子12g、豆豉9g", "dosage": "水煎服", "contraindications": "中焦虚寒者不宜", "ni_comment": "虚烦不得眠第一方"},
            "麻杏甘石汤": {"source": "伤寒论", "ingredients": "麻黄9g、杏仁9g、炙甘草6g、石膏18g", "dosage": "水煎服，石膏先煎", "contraindications": "风寒咳喘不宜", "ni_comment": "肺热咳喘第一方"},
            "当归四逆汤": {"source": "伤寒论", "ingredients": "当归9g、桂枝9g、白芍9g、细辛3g、炙甘草6g、通草6g、大枣25枚", "dosage": "水煎服", "contraindications": "热证不宜", "ni_comment": "血虚寒厥手足厥寒"},
            "四逆散": {"source": "伤寒论", "ingredients": "柴胡6g、枳实6g、白芍6g、炙甘草6g", "dosage": "水煎服或散剂", "contraindications": "纯寒纯热不宜", "ni_comment": "阳郁气滞四肢厥冷"},
            "瓜蒌薤白白酒汤": {"source": "金匮要略", "ingredients": "瓜蒌实1枚、薤白9g、白酒适量", "dosage": "水酒煎服", "contraindications": "阴虚火旺不宜", "ni_comment": "胸痹第一方"},
            "瓜蒌薤白半夏汤": {"source": "金匮要略", "ingredients": "瓜蒌实1枚、薤白9g、半夏9g、白酒适量", "dosage": "水酒煎服", "contraindications": "阴虚火旺不宜", "ni_comment": "胸痹痰浊重证"},
            "苓桂术甘汤": {"source": "金匮要略", "ingredients": "茯苓12g、桂枝9g、白术6g、炙甘草6g", "dosage": "水煎服", "contraindications": "阴虚火旺不宜", "ni_comment": "温阳化饮健脾利湿"},
            "茵陈蒿汤": {"source": "金匮要略", "ingredients": "茵陈18g、栀子12g、大黄6g", "dosage": "水煎服", "contraindications": "阴黄不宜", "ni_comment": "阳黄第一方"},
            "温经汤": {"source": "金匮要略", "ingredients": "吴茱萸9g、当归6g、白芍6g、川芎6g、人参6g、桂枝6g、阿胶6g、牡丹皮6g、生姜6g、甘草6g、半夏6g、麦冬12g", "dosage": "水煎服，阿胶烊化", "contraindications": "实热证不宜", "ni_comment": "妇人月经不调不孕第一方"},
            "半夏厚朴汤": {"source": "金匮要略", "ingredients": "半夏9g、厚朴9g、茯苓12g、生姜9g、苏叶6g", "dosage": "水煎服", "contraindications": "阴虚燥咳不宜", "ni_comment": "梅核气第一方"},
            "酸枣仁汤": {"source": "金匮要略", "ingredients": "酸枣仁15g、甘草3g、知母6g、茯苓6g、川芎6g", "dosage": "水煎服", "contraindications": "无虚热不宜", "ni_comment": "虚劳虚烦不眠第一方"},
            "越婢汤": {"source": "金匮要略", "ingredients": "麻黄9g、石膏18g、生姜9g、大枣4枚、炙甘草6g", "dosage": "水煎服", "contraindications": "无风水者不宜", "ni_comment": "风水水肿第一方"},
            "防己黄芪汤": {"source": "金匮要略", "ingredients": "防己9g、黄芪9g、白术6g、甘草3g、生姜3片、大枣1枚", "dosage": "水煎服", "contraindications": "实证不宜", "ni_comment": "风水表虚水肿"},
            "肾气丸": {"source": "金匮要略", "ingredients": "干地黄24g、山药12g、山茱萸12g、泽泻9g、牡丹皮9g、茯苓9g、桂枝3g、附子3g", "dosage": "丸剂", "contraindications": "阴虚火旺不宜", "ni_comment": "补肾阳代表方"},
            "甘草附子汤": {"source": "伤寒论", "ingredients": "甘草6g、附子9g、白术6g、桂枝12g", "dosage": "附子先煎，水煎服", "contraindications": "热证不宜", "ni_comment": "风湿相搏骨节疼"},
            "竹叶石膏汤": {"source": "伤寒论", "ingredients": "竹叶6g、石膏30g、半夏9g、麦冬12g、人参6g、炙甘草6g、粳米9g", "dosage": "水煎服", "contraindications": "无热者不宜", "ni_comment": "伤寒后余热未清，气阴两伤"},
            "吴茱萸汤": {"source": "伤寒论", "ingredients": "吴茱萸9g、人参9g、生姜18g、大枣4枚", "dosage": "水煎服", "contraindications": "热证不宜", "ni_comment": "厥阴头痛干呕吐涎沫"},
            "大黄黄连泻心汤": {"source": "伤寒论", "ingredients": "大黄6g、黄连3g", "dosage": "开水渍服", "contraindications": "虚寒不宜", "ni_comment": "心下痞按之濡"},
            "桃核承气汤": {"source": "伤寒论", "ingredients": "桃仁9g、大黄12g、桂枝6g、炙甘草6g、芒硝6g", "dosage": "水煎，芒硝冲服", "contraindications": "无瘀血者不宜", "ni_comment": "下焦蓄血其人如狂"},
            "葛根芩连汤": {"source": "伤寒论", "ingredients": "葛根15g、黄芩9g、黄连9g、炙甘草6g", "dosage": "水煎服", "contraindications": "寒证不宜", "ni_comment": "协热下利第一方"},
            "柴胡桂枝干姜汤": {"source": "伤寒论", "ingredients": "柴胡12g、桂枝9g、干姜6g、瓜蒌根9g、黄芩9g、牡蛎6g、炙甘草6g", "dosage": "水煎服", "contraindications": "纯热证不宜", "ni_comment": "少阳兼水饮"},
        }

    def analyze(self, symptoms: List[str]) -> Dict:
        """分析症状，返回辨证辅助结果和相关方剂参考"""
        safety_result = check_red_flags(symptoms)
        missing_questions = build_missing_questions(symptoms)

        eight_principles_result = self._determine_eight_principles(symptoms)
        six_stage_result = self._match_six_stages(symptoms)
        formula_recommendation = self._recommend_formula(six_stage_result, symptoms)
        analysis = self._generate_analysis(symptoms, eight_principles_result, six_stage_result)

        return {
            "disclaimer": DISCLAIMER,
            "safety": safety_result,
            "symptoms": symptoms,
            "eight_principles": eight_principles_result,
            "six_stages": six_stage_result,
            "formula": formula_recommendation,
            "missing_questions": missing_questions,
            "analysis": analysis
        }

    def _determine_eight_principles(self, symptoms: List[str]) -> Dict:
        """八纲辨证"""
        biao_score = sum(1 for s in symptoms if any(k in s for k in self.eight_principles["biao_li"]["biao"]))
        li_score = sum(1 for s in symptoms if any(k in s for k in self.eight_principles["biao_li"]["li"]))

        han_score = sum(1 for s in symptoms if any(k in s for k in self.eight_principles["han_re"]["han"]))
        re_score = sum(1 for s in symptoms if any(k in s for k in self.eight_principles["han_re"]["re"]))

        xu_score = sum(1 for s in symptoms if any(k in s for k in self.eight_principles["xu_shi"]["xu"]))
        shi_score = sum(1 for s in symptoms if any(k in s for k in self.eight_principles["xu_shi"]["shi"]))

        yin_score = han_score + xu_score
        yang_score = re_score + shi_score

        text = " ".join(symptoms)

        # 组合规则优先：避免把“发热”简单等同于热证。
        if all(k in text for k in ["恶寒", "无汗"]) and ("脉浮紧" in text or "浮紧" in text):
            han_re = "寒证"
            han_re_note = "恶寒、无汗、脉浮紧同见，按表寒组合优先判断"
        elif all(k in text for k in ["大热", "大汗", "口渴"]):
            han_re = "热证"
            han_re_note = "大热、大汗、口渴同见，按热证组合判断"
        elif "恶寒" in text and re_score <= han_score + 1:
            han_re = "寒证"
            han_re_note = "恶寒权重优先，发热不单独作为热证依据"
        else:
            han_re = "寒证" if han_score > re_score else "热证"
            han_re_note = "按寒热症状计分判断"

        confidence = min(1.0, (max(biao_score, li_score) + max(han_score, re_score) + max(xu_score, shi_score)) / (max(len(symptoms), 1) * 3))

        return {
            "yin_yang": "阴证" if yin_score > yang_score else "阳证",
            "biao_li": "表证" if biao_score > li_score else "里证",
            "han_re": han_re,
            "han_re_note": han_re_note,
            "xu_shi": "虚证" if xu_score > shi_score else "实证",
            "confidence": confidence
        }

    def _match_six_stages(self, symptoms: List[str]) -> Dict:
        """六经辨证匹配"""
        best_match = None
        best_score = 0
        best_subtype = None

        for stage_key, stage_data in self.six_stages.items():
            # 主症匹配
            main_symptoms = stage_data["symptoms"]
            match_count = sum(1 for s in symptoms if any(m in s for m in main_symptoms))
            stage_score = match_count / len(main_symptoms)

            # 检查亚型
            for subtype_key, subtype_data in stage_data.get("subtypes", {}).items():
                subtype_symptoms = subtype_data["key_symptoms"]
                subtype_count = sum(1 for s in symptoms if any(sym in s for sym in subtype_symptoms))
                subtype_score = subtype_count / len(subtype_symptoms)

                if subtype_score > 0.4 and subtype_score >= best_score:
                    best_score = subtype_score
                    best_match = {
                        "stage": stage_key,
                        "name": stage_data["name"],
                        "description": stage_data["description"],
                        "subtype": subtype_data
                    }
                    best_subtype = subtype_data

            # 即使没有匹配到亚型，主症匹配也可以
            if stage_score > 0.3 and stage_score > best_score and not best_subtype:
                best_match = {
                    "stage": stage_key,
                    "name": stage_data["name"],
                    "description": stage_data["description"]
                }
                best_score = stage_score

        return best_match or {"stage": "unknown", "name": "未明确", "description": "需要更多症状信息"}

    def _recommend_formula(self, six_stage_result: Dict, symptoms: List[str]) -> Dict:
        """给出相关方剂参考"""
        if six_stage_result.get("subtype"):
            subtype = six_stage_result["subtype"]
            formula_name = subtype.get("formula", "未知")
            formula_id = subtype.get("formula_id", "")

            # 查找方剂详情
            details = self.formula_details.get(formula_name, {})

            return {
                "name": formula_name,
                "formula_id": formula_id,
                "reason": f"根据{six_stage_result['name']} - {subtype['name']}推荐",
                "source": details.get("source", ""),
                "ingredients": details.get("ingredients", ""),
                "dosage": details.get("dosage", ""),
                "contraindications": details.get("contraindications", ""),
                "ni_comment": details.get("ni_comment", ""),
                "modifications": self._suggest_modifications(formula_name, symptoms),
                "alternative_formulas": self._find_alternatives(six_stage_result, symptoms)
            }
        elif six_stage_result.get("stage") and six_stage_result["stage"] != "unknown":
            # 匹配到六经但未匹配到具体亚型
            stage_key = six_stage_result["stage"]
            stage_data = self.six_stages.get(stage_key, {})
            subtypes = stage_data.get("subtypes", {})
            suggestions = list(subtypes.keys())[:3]
            return {
                "name": "需进一步辨证",
                "reason": f"已识别{six_stage_result['name']}，需更多症状确定具体方剂",
                "suggestions": [subtypes[s]["formula"] for s in suggestions if s in subtypes]
            }
        else:
            # 尝试用症状-方剂映射
            symptom_match = self._match_by_symptoms(symptoms)
            if symptom_match:
                return symptom_match

            return {
                "name": "无法推荐",
                "reason": "症状信息不足，无法进行六经辨证",
                "suggestions": ["请详细描述症状", "建议面诊中医师"]
            }

    def _suggest_modifications(self, formula_name: str, symptoms: List[str]) -> List[str]:
        """建议方剂加减"""
        mods = []
        modification_rules = {
            "桂枝汤": [
                (["项背", "强"], "项背强几几：加葛根 → 桂枝加葛根汤"),
                (["喘"], "喘：加厚朴、杏仁 → 桂枝加厚朴杏子汤"),
                (["漏汗"], "阳虚漏汗：加附子 → 桂枝加附子汤"),
            ],
            "麻黄汤": [
                (["烦躁"], "烦躁：加石膏 → 大青龙汤"),
                (["项背"], "项背强几几：加葛根 → 葛根汤"),
            ],
            "小柴胡汤": [
                (["渴"], "渴：去半夏加天花粉"),
                (["腹中痛"], "腹中痛：去黄芩加白芍"),
                (["胁下痞鞭"], "胁下痞鞭：去大枣加牡蛎"),
            ],
            "四逆汤": [
                (["脉微欲绝"], "脉微欲绝：加重附子干姜 → 通脉四逆汤"),
                (["烦躁"], "烦躁：加人参、猪胆汁 → 通脉四逆加猪胆汁汤"),
            ],
            "理中汤": [
                (["脐上筑"], "脐上筑：去白术加桂枝"),
                (["吐多"], "吐多：去白术加生姜"),
                (["下利重"], "下利重：仍用白术"),
            ],
        }

        for keyword_list, modification in modification_rules.get(formula_name, []):
            if any(any(k in s for k in keyword_list) for s in symptoms):
                mods.append(modification)

        return mods

    def _find_alternatives(self, six_stage_result: Dict, symptoms: List[str]) -> List[str]:
        """查找替代方剂"""
        alternatives = []
        stage_key = six_stage_result.get("stage", "")
        stage_data = self.six_stages.get(stage_key, {})

        for subtype_key, subtype_data in stage_data.get("subtypes", {}).items():
            if subtype_data.get("formula") != six_stage_result.get("subtype", {}).get("formula"):
                alternatives.append(f"{subtype_data['formula']}（{subtype_data['name']}）")
                if len(alternatives) >= 2:
                    break

        return alternatives

    def _match_by_symptoms(self, symptoms: List[str]) -> Optional[Dict]:
        """通过症状-方剂映射推荐"""
        formula_scores = {}

        for symptom in symptoms:
            if symptom in self.symptom_formula.get("symptoms", {}):
                for formula in self.symptom_formula["symptoms"][symptom]["formulas"]:
                    fname = formula["name"]
                    if fname not in formula_scores:
                        formula_scores[fname] = {"score": 0, "reasons": []}
                    weight = 3 if formula["compatibility"] == "primary" else 1
                    formula_scores[fname]["score"] += weight
                    formula_scores[fname]["reasons"].append(f"{symptom} → {formula.get('note', '')}")

        if formula_scores:
            best = max(formula_scores, key=lambda x: formula_scores[x]["score"])
            details = self.formula_details.get(best, {})
            return {
                "name": best,
                "reason": f"根据症状匹配（得分：{formula_scores[best]['score']}）",
                "matched_symptoms": formula_scores[best]["reasons"][:5],
                "ingredients": details.get("ingredients", ""),
                "dosage": details.get("dosage", ""),
                "ni_comment": details.get("ni_comment", "")
            }
        return None

    def _generate_analysis(self, symptoms: List[str], eight_principles: Dict, six_stages: Dict) -> str:
        """生成分析说明"""
        parts = []
        parts.append(f"【八纲】{eight_principles['yin_yang']}、{eight_principles['biao_li']}、{eight_principles['han_re']}、{eight_principles['xu_shi']}")

        if six_stages.get("name") != "未明确":
            parts.append(f"【六经】{six_stages['name']} - {six_stages.get('description', '')}")
            if six_stages.get("subtype"):
                parts.append(f"【证型】{six_stages['subtype']['name']}")
                parts.append(f"【方剂】{six_stages['subtype'].get('formula', '')}")

        parts.append(f"【置信度】{eight_principles.get('confidence', 0):.1%}")

        return "\n".join(parts)


if __name__ == "__main__":
    import json as js
    engine = DiagnosisEngine()

    test_cases = [
        (["发热", "恶寒", "汗出", "脉浮缓"], "太阳中风 - 桂枝汤"),
        (["发热", "恶寒", "无汗", "脉浮紧"], "太阳伤寒 - 麻黄汤"),
        (["大热", "大汗", "大渴", "脉洪大"], "阳明经证 - 白虎汤"),
        (["往来寒热", "胸胁苦满", "口苦", "目眩"], "少阳证 - 小柴胡汤"),
        (["腹满而吐", "食不下", "自利"], "太阴脾寒 - 理中汤"),
        (["四肢厥冷", "下利清谷", "脉微细"], "少阴寒化 - 四逆汤"),
        (["消渴", "气上撞心", "心中疼热"], "厥阴寒热错杂 - 乌梅丸"),
        (["失眠", "心烦", "口燥咽干"], "少阴热化 - 黄连阿胶汤"),
        (["胸痹", "短气", "胸背痛"], "胸阳不振 - 瓜蒌薤白白酒汤"),
        (["心动悸", "脉结代"], "气阴两虚 - 炙甘草汤"),
    ]

    for symptoms, expected in test_cases:
        result = engine.analyze(symptoms)
        print(f"\n{'='*60}")
        print(f"测试：{symptoms}")
        print(f"期望：{expected}")
        print(f"结果：{result['formula']['name']}")
        print(f"辨证：{result['analysis']}")
        if result['formula'].get('modifications'):
            print(f"加减：{result['formula']['modifications']}")
