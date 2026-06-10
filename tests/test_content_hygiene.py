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

    def test_active_jsonl_have_no_pdf_footer_residue(self):
        hits = []
        patterns = [
            re.compile(r"V[0-9]+-[0-9]{1,8}"),
            re.compile(r"05-10-18"),
            re.compile(r"\u5b50\u90e8\u00b7\u9ec4\u5e1d\u5185\u7ecf"),
            re.compile(r"\u00b7[0-9]{1,4}\u00b7"),
            re.compile(r"\u7b2c\s*[0-9]+\s*\u9875\s*\u5171\s*[0-9]+\s*\u9875"),
            re.compile(r"\u5b88\u5019\u8bda\u5b9e\u56fd\u5b66\u4e66\u5e97"),
            re.compile(r"\u5185\u90e8\u4e2d\u533b\u6559\u6750\u7cfb\u5217"),
            re.compile(r'"}\s*,\s*\{"page_num"'),
            re.compile(r'"}\s*,\s*\{"page_'),
            re.compile(r"\u00b7{6,}\s*[0-9]{1,4}"),
            re.compile(r"\u00b7{6,}"),
            re.compile(r"\.{6,}\s*[0-9]{1,4}"),
            re.compile(r"\.{10,}(?=(?:[\"\r\n]|$))"),
            re.compile(r"\.{10,}"),
        ]
        files = [
            ROOT / "data" / "acupoint_index.jsonl",
            ROOT / "data" / "acupoint_sources.jsonl",
            ROOT / "data" / "formula_index.jsonl",
            ROOT / "data" / "formula_sources.jsonl",
            ROOT / "data" / "herb_index.jsonl",
            ROOT / "data" / "herb_sources.jsonl",
            ROOT / "data" / "review_decisions.jsonl",
            ROOT / "data" / "review_queue.jsonl",
            ROOT / "data" / "verified_sources.jsonl",
        ]

        def walk_strings(value):
            if isinstance(value, str):
                yield value
            elif isinstance(value, dict):
                for item in value.values():
                    yield from walk_strings(item)
            elif isinstance(value, list):
                for item in value:
                    yield from walk_strings(item)

        for path in files:
            for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                row = json.loads(line)
                for value in walk_strings(row):
                    for pattern in patterns:
                        if pattern.search(value):
                            hits.append((str(path.relative_to(ROOT)), line_no, pattern.pattern))
        self.assertEqual(hits, [])

    def test_knowledge_markdown_has_no_high_confidence_pdf_residue(self):
        hits = []
        patterns = [
            re.compile(r"V[0-9]+-[0-9]{1,8}"),
            re.compile(r"05-10-18"),
            re.compile(r"\u5b50\u90e8\u00b7\u9ec4\u5e1d\u5185\u7ecf"),
            re.compile(r"\u00b7[0-9]{1,4}\u00b7"),
            re.compile(r"\u00b7{6,}\s*[0-9]{1,4}"),
            re.compile(r"\u00b7{6,}"),
            re.compile(r"\.{6,}\s*[0-9]{1,4}"),
            re.compile(r"\.{10,}(?=(?:[\"\r\n]|$))"),
            re.compile(r"\.{10,}"),
        ]
        for path in (ROOT / "knowledge").rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            for pattern in patterns:
                if pattern.search(text):
                    hits.append((str(path.relative_to(ROOT)), pattern.pattern))
        self.assertEqual(hits, [])



    def test_report_files_have_no_ocr_residue(self):
        hits = []
        patterns = [
            re.compile(chr(0xFFFD) + r'{1,}'),
            re.compile(r'(\S)\1{3,}'),
            re.compile(r'\.{10,}'),
            re.compile(r'[\u00b7\u2022\u2219\u25cf]{6,}'),
        ]
        for path in (ROOT / 'report').rglob('*.*'):
            if path.suffix not in ('.md', '.json'):
                continue
            text = path.read_text(encoding='utf-8')
            for pattern in patterns:
                if pattern.search(text):
                    hits.append((str(path.relative_to(ROOT)), pattern.pattern))
        self.assertEqual(hits, [])


if __name__ == "__main__":
    unittest.main()
