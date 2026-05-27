import re
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


if __name__ == "__main__":
    unittest.main()
