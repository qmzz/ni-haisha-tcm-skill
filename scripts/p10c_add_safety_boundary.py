#!/usr/bin/env python3
"""P10-C safety boundary 全覆盖。

为所有知识文件添加统一的 safety_boundary 声明。
- herb: 学习资料声明
- acupoint: 学习资料 + 非针灸指导声明
- formula: 学习资料声明（已覆盖，补充缺失）

不修改医学正文，只追加安全边界声明。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from internal.frontmatter import parse_frontmatter

KINDS = {
    "herb": ROOT / "knowledge" / "herbs",
    "acupoint": ROOT / "knowledge" / "acupoints",
    "formula": ROOT / "knowledge" / "formulas",
}

# 安全边界模板
SAFETY_BOUNDARY_TEMPLATE = """## 学习与安全边界

**本条目仅供中医学习参考，不构成诊断或治疗建议。**

- 内容来源于倪海厦老师教学资料，用于中医知识传承与学习
- 不能替代专业医师的辨证论治
- 如有健康问题，请咨询执业中医师
{extra}"""

ACUPOINT_EXTRA = """\n- **本条目仅作学习与来源追溯，不作为针灸操作指导**
- 针灸操作需由专业医师在正规医疗机构进行
- 自行针刺存在感染、气胸、神经损伤等风险
"""


def has_safety_boundary(text: str) -> bool:
    """检查是否已有安全边界声明"""
    markers = [
        "学习与安全边界",
        "不构成诊断",
        "不能替代",
        "仅供中医学习",
        "不作为针灸操作指导",
    ]
    return any(m in text for m in markers)


def add_safety_boundary(path: Path, kind: str) -> bool:
    """为单个文件添加安全边界，返回是否修改"""
    text = path.read_text(encoding="utf-8")
    
    if has_safety_boundary(text):
        return False
    
    fm, body = parse_frontmatter(text)
    if body is None:
        body = text
    
    extra = ACUPOINT_EXTRA if kind == "acupoint" else ""
    safety_section = SAFETY_BOUNDARY_TEMPLATE.format(extra=extra)
    
    # 追加到文件末尾
    new_text = text.rstrip() + "\n\n" + safety_section + "\n"
    
    path.write_text(new_text, encoding="utf-8")
    return True


def main():
    stats: Dict[str, Dict[str, int]] = {}
    
    for kind, folder in KINDS.items():
        added = 0
        skipped = 0
        
        for path in sorted(folder.glob("*.md")):
            if "index" in path.name:
                continue
            
            if add_safety_boundary(path, kind):
                added += 1
            else:
                skipped += 1
        
        stats[kind] = {"added": added, "skipped": skipped}
    
    print(json.dumps(stats, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
