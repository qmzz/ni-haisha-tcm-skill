import re
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ContentHygieneTests(unittest.TestCase):
    def test_mechanical_residue_removed(self):
        forbidden_literals = [
            "来源摘录：",
            "这味药，在经方中应用广泛",
            "这个穴位，在临床上应用非常广泛",
            "����",
        ]
        hits = []
        for path in (ROOT / "knowledge").rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            for literal in forbidden_literals:
                if literal in text:
                    hits.append((str(path.relative_to(ROOT)), literal))
        self.assertEqual(hits, [])

    def test_json_page_fragments_removed(self):
        hits = []
        pattern = re.compile(r'^>\s*,?\s*\{"page_num"\s*:')
        for path in (ROOT / "knowledge").rglob("*.md"):
            for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if pattern.match(line):
                    hits.append((str(path.relative_to(ROOT)), line_no))
        self.assertEqual(hits, [])

    def test_no_obvious_repeated_ocr_heading_tails(self):
        hits = []
        patterns = [
            re.compile(r"【【.*】】"),
            re.compile(r"[一二三四五六七八九〇○零]{4,}、"),
        ]
        for path in (ROOT / "knowledge").rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            for pattern in patterns:
                if pattern.search(text):
                    hits.append((str(path.relative_to(ROOT)), pattern.pattern))
        self.assertEqual(hits, [])

    def test_jsonl_source_refs_have_no_ocr_tail_residue(self):
        hits = []
        patterns = [
            re.compile(r"\uFFFD{2,}"),
            re.compile(r"【【"),
            re.compile(r"】】"),
            re.compile(r"[一二三四五六七八九十〇○零]{4,}[、，,]"),
        ]
        files = [
            ROOT / "data" / "verified_sources.jsonl",
            ROOT / "data" / "herb_index.jsonl",
            ROOT / "data" / "acupoint_index.jsonl",
            ROOT / "data" / "formula_index.jsonl",
        ]
        for path in files:
            for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                row = json.loads(line)
                item_id = row.get("item_id") or row.get("herb_id") or row.get("acupoint_id") or row.get("formula_id")
                for ref in row.get("source_refs") or []:
                    quote = ref.get("quote") or ""
                    for pattern in patterns:
                        if pattern.search(quote):
                            hits.append((str(path.relative_to(ROOT)), line_no, item_id, pattern.pattern))
        self.assertEqual(hits, [])


if __name__ == "__main__":
    unittest.main()
