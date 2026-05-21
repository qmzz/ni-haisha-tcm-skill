#!/usr/bin/env python3
"""原始 JSON 来源检索回归测试。"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from internal.source_corpus import SourceCorpus


class SourceCorpusTest(unittest.TestCase):
    def test_source_corpus_available(self):
        corpus = SourceCorpus()
        self.assertTrue(corpus.available(), f"source dir unavailable: {corpus.source_dir}")
        self.assertGreaterEqual(len(corpus.files()), 1)

    def test_source_search_returns_traceable_hits(self):
        corpus = SourceCorpus()
        hits = corpus.search("桂枝汤", limit=3)
        self.assertTrue(hits)
        first = hits[0].to_dict()
        self.assertTrue(first["source_file"])
        self.assertIn("桂枝汤", first["quote"])
        self.assertIn("char_start", first)


if __name__ == "__main__":
    unittest.main()
