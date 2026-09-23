#!/usr/bin/env python3
"""OpenClaw 调用的倪海厦经方与知识库查询工具入口。

用法：
  python3 tools/tcm_tools.py tcm_query '{"query":"麻黄汤", "category":"formulas"}'
  python3 tools/tcm_tools.py tcm_search '{"query":"下焦寒湿 心悸"}'
  python3 tools/tcm_tools.py tcm_doc '{"category":"herbs", "name":"附子"}'
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from internal.knowledge_query import KnowledgeIndex

def _payload() -> Dict[str, Any]:
    if len(sys.argv) >= 3:
        try:
            return json.loads(sys.argv[2])
        except Exception:
            return {"query": sys.argv[2]}
    raw = sys.stdin.read().strip()
    return json.loads(raw) if raw else {}

def _print(data: Dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))

def tcm_search(payload: Dict[str, Any]) -> Dict[str, Any]:
    query = payload.get("query") or payload.get("text") or payload.get("keyword") or ""
    category = payload.get("category")
    limit = int(payload.get("limit", 5))
    index = KnowledgeIndex.get_instance()
    results = index.search(query, category=category, limit=limit)
    return {
        "status": "success",
        "query": query,
        "category": category,
        "count": len(results),
        "results": results
    }

def tcm_doc(payload: Dict[str, Any]) -> Dict[str, Any]:
    category = payload.get("category", "")
    name = payload.get("name") or payload.get("title") or payload.get("query") or ""
    index = KnowledgeIndex.get_instance()
    doc = index.get_document(category, name)
    if not doc:
        return {"status": "not_found", "message": f"未找到相关条目: {category}/{name}"}
    return {
        "status": "success",
        "category": doc["category"],
        "category_name": doc["category_name"],
        "title": doc["title"],
        "filename": doc["filename"],
        "path": doc["path"],
        "content": doc["content"]
    }

def main():
    if len(sys.argv) < 2:
        _print({"status": "error", "message": "Missing action"})
        sys.exit(1)
    
    action = sys.argv[1]
    payload = _payload()
    
    if action in ["tcm_search", "search", "query", "tcm_query"]:
        _print(tcm_search(payload))
    elif action in ["tcm_doc", "get_doc", "doc", "tcm_read"]:
        _print(tcm_doc(payload))
    else:
        # 默认回退为全文检索
        _print(tcm_search({"query": action}))

if __name__ == "__main__":
    main()
