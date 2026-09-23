import os, glob, re, json
from pathlib import Path
from typing import Dict, List, Any, Optional

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_DIR = ROOT / "knowledge"

CATEGORIES = {
    "formulas": "经方",
    "herbs": "本草药材",
    "acupoints": "针灸穴位",
    "concepts": "核心气化概念",
    "diagnosis": "四诊与辨证",
    "cases": "实战医案"
}

class KnowledgeIndex:
    _instance = None
    _docs = [] # list of dict: {category, filename, title, path, content, tags}

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._build_index()
        return cls._instance

    def _build_index(self):
        self._docs = []
        for cat in CATEGORIES.keys():
            cat_dir = KNOWLEDGE_DIR / cat
            if not cat_dir.exists():
                continue
            for fpath in cat_dir.glob("*.md"):
                if fpath.name.endswith("_index.md") or fpath.name.endswith("_plan.md"):
                    continue
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
                        content = fp.read()
                    title = ""
                    for line in content.split("\n"):
                        if line.startswith("# "):
                            title = line.replace("# ", "").strip()
                            break
                    if not title:
                        title = fpath.stem
                    self._docs.append({
                        "category": cat,
                        "category_name": CATEGORIES[cat],
                        "filename": fpath.name,
                        "title": title,
                        "path": str(fpath),
                        "content": content
                    })
                except Exception:
                    pass

    def search(self, query: str, category: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
        query = query.strip()
        if not query:
            return []
        keywords = [k for k in re.split(r"[\s,，、]+", query) if k]
        results = []
        for doc in self._docs:
            if category and doc["category"] != category:
                continue
            score = 0
            # 标题完全匹配
            if query in doc["title"] or query == doc["filename"].replace(".md", ""):
                score += 100
            for kw in keywords:
                if kw in doc["title"]:
                    score += 30
                if kw in doc["filename"]:
                    score += 20
                # 内容命中次数
                c_count = doc["content"].count(kw)
                score += min(c_count * 2, 20)
            if score > 0:
                # 提取摘要/命中段落
                snippet = ""
                for kw in keywords:
                    idx = doc["content"].find(kw)
                    if idx != -1:
                        start = max(0, idx - 80)
                        end = min(len(doc["content"]), idx + 200)
                        snippet = doc["content"][start:end].replace("\n", " ") + "..."
                        break
                if not snippet:
                    snippet = doc["content"][:200].replace("\n", " ") + "..."
                results.append({
                    "category": doc["category"],
                    "category_name": doc["category_name"],
                    "filename": doc["filename"],
                    "title": doc["title"],
                    "score": score,
                    "snippet": snippet,
                    "path": doc["path"]
                })
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]

    def get_document(self, category: str, name_or_file: str) -> Optional[Dict[str, Any]]:
        for doc in self._docs:
            if category and doc["category"] != category:
                continue
            if name_or_file in doc["title"] or doc["filename"] == name_or_file or doc["filename"] == f"{name_or_file}.md":
                return doc
        return None

