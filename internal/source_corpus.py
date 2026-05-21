#!/usr/bin/env python3
"""原始 PDF 提取 JSON 检索模块。

用途：
- 统一读取 `project/nihaixia/` 下的结构化 JSON；
- 为知识补全、方剂/药材/穴位查询提供可追溯原文片段；
- 严格避免凭模型记忆扩写内容。

默认路径：当前仓库的兄弟目录 `../nihaixia`。
可通过环境变量 `NIHAIXIA_SOURCE_DIR` 覆盖。
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional


@dataclass
class SourceHit:
    source_file: str
    page_num: Optional[int]
    quote: str
    char_start: int
    char_end: int

    def to_dict(self) -> Dict:
        return {
            "source_file": self.source_file,
            "page_num": self.page_num,
            "quote": self.quote,
            "char_start": self.char_start,
            "char_end": self.char_end,
        }


class SourceCorpus:
    """读取和检索原始 JSON 语料。"""

    def __init__(self, source_dir: Optional[Path] = None):
        if source_dir is None:
            env_dir = os.environ.get("NIHAIXIA_SOURCE_DIR")
            if env_dir:
                source_dir = Path(env_dir)
            else:
                source_dir = Path(__file__).resolve().parents[2] / "nihaixia"
        self.source_dir = Path(source_dir)
        self._json_cache: Dict[Path, Dict] = {}

    def available(self) -> bool:
        return self.source_dir.exists() and any(self.source_dir.glob("*.json"))

    def files(self) -> List[Path]:
        return sorted(self.source_dir.glob("*.json"))

    def manifest(self) -> List[Dict]:
        """返回原始 JSON 文件清单与基础统计。"""
        items = []
        for path in self.files():
            try:
                data = self._load_json(path)
                text = self._full_text(data)
                pages = self._pages(data)
                items.append({
                    "source_file": path.name,
                    "path": str(path),
                    "bytes": path.stat().st_size,
                    "chars": len(text),
                    "pages": len(pages) if pages else data.get("total_pages") or data.get("pages"),
                    "keys": list(data.keys()) if isinstance(data, dict) else [],
                })
            except Exception as exc:  # 保留异常，避免一个坏文件阻断全部索引
                items.append({
                    "source_file": path.name,
                    "path": str(path),
                    "error": f"{type(exc).__name__}: {exc}",
                })
        return items

    def search(self, keyword: str, limit: int = 10, context: int = 80) -> List[SourceHit]:
        """简单关键词检索，返回带来源文件和页码的原文片段。"""
        keyword = keyword.strip()
        if not keyword:
            return []

        hits: List[SourceHit] = []
        for path in self.files():
            data = self._load_json(path)
            pages = self._pages(data)
            if pages:
                for page in pages:
                    text = page.get("text") or page.get("content") or ""
                    page_num = page.get("page_num") or page.get("page")
                    hits.extend(self._search_text(path.name, text, keyword, context, page_num))
                    if len(hits) >= limit:
                        return hits[:limit]
            else:
                text = self._full_text(data)
                hits.extend(self._search_text(path.name, text, keyword, context, None))
                if len(hits) >= limit:
                    return hits[:limit]
        return hits[:limit]

    def _load_json(self, path: Path) -> Dict:
        if path not in self._json_cache:
            with path.open("r", encoding="utf-8") as f:
                self._json_cache[path] = json.load(f)
        return self._json_cache[path]

    def _pages(self, data: Dict) -> List[Dict]:
        pages = data.get("pages") if isinstance(data, dict) else None
        if isinstance(pages, list):
            return [p for p in pages if isinstance(p, dict)]
        return []

    def _full_text(self, data: Dict) -> str:
        if not isinstance(data, dict):
            return ""
        return data.get("full_text") or data.get("text") or ""

    def _search_text(
        self,
        source_file: str,
        text: str,
        keyword: str,
        context: int,
        page_num: Optional[int],
    ) -> Iterable[SourceHit]:
        start = 0
        while True:
            idx = text.find(keyword, start)
            if idx < 0:
                break
            left = max(0, idx - context)
            right = min(len(text), idx + len(keyword) + context)
            quote = text[left:right].replace("\n", " ").strip()
            yield SourceHit(
                source_file=source_file,
                page_num=page_num,
                quote=quote,
                char_start=idx,
                char_end=idx + len(keyword),
            )
            start = idx + len(keyword)
