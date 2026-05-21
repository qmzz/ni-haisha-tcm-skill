#!/usr/bin/env python3
"""构建原始 JSON 语料索引。

输出：data/source_manifest.json 与 data/source_pages.jsonl

注意：本脚本只索引原始文本，不做医学内容归纳，不生成新知识。
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from internal.source_corpus import SourceCorpus


def main():
    skill_dir = Path(__file__).resolve().parents[1]
    data_dir = skill_dir / "data"
    data_dir.mkdir(exist_ok=True)

    corpus = SourceCorpus()
    manifest = corpus.manifest()

    manifest_path = data_dir / "source_manifest.json"
    pages_path = data_dir / "source_pages.jsonl"

    manifest_path.write_text(json.dumps({
        "source_dir": str(corpus.source_dir),
        "files": manifest,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    count = 0
    with pages_path.open("w", encoding="utf-8") as out:
        for path in corpus.files():
            data = corpus._load_json(path)
            pages = corpus._pages(data)
            if pages:
                for page in pages:
                    text = page.get("text") or page.get("content") or ""
                    record = {
                        "source_file": path.name,
                        "page_num": page.get("page_num") or page.get("page"),
                        "chars": len(text),
                        "text": text,
                    }
                    out.write(json.dumps(record, ensure_ascii=False) + "\n")
                    count += 1
            else:
                text = corpus._full_text(data)
                record = {
                    "source_file": path.name,
                    "page_num": None,
                    "chars": len(text),
                    "text": text,
                }
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
                count += 1

    print(f"wrote {manifest_path}")
    print(f"wrote {pages_path} ({count} records)")


if __name__ == "__main__":
    main()
