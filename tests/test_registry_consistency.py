import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class RegistryConsistencyTests(unittest.TestCase):
    def test_all_verified_completeness_rows_exist_in_verified_registry(self):
        verified_sources = load_jsonl(ROOT / "data" / "verified_sources.jsonl")
        registry_keys = {(row.get("kind"), row.get("item_id")) for row in verified_sources}
        completeness = load_jsonl(ROOT / "data" / "knowledge_completeness.jsonl")
        missing = [
            (row.get("kind"), row.get("item_id"), row.get("name"))
            for row in completeness
            if row.get("trace_status") == "verified" and (row.get("kind"), row.get("item_id")) not in registry_keys
        ]
        self.assertEqual(missing, [])

    def test_verified_herb_index_rows_have_source_refs(self):
        herb_rows = load_jsonl(ROOT / "data" / "herb_index.jsonl")
        bad = [
            (row.get("herb_id"), row.get("name"))
            for row in herb_rows
            if row.get("trace_status") == "verified" and not row.get("source_refs")
        ]
        self.assertEqual(bad, [])

    def test_no_source_herb_index_rows_have_no_source_refs(self):
        herb_rows = load_jsonl(ROOT / "data" / "herb_index.jsonl")
        bad = [
            (row.get("herb_id"), row.get("name"))
            for row in herb_rows
            if row.get("trace_status") == "no_source_found" and row.get("source_refs")
        ]
        self.assertEqual(bad, [])

    def test_trace_registry_rows_have_source_quality_level(self):
        files = [
            ROOT / "data" / "verified_sources.jsonl",
            ROOT / "data" / "formula_index.jsonl",
            ROOT / "data" / "herb_index.jsonl",
            ROOT / "data" / "acupoint_index.jsonl",
            ROOT / "data" / "knowledge_completeness.jsonl",
            ROOT / "data" / "review_queue.jsonl",
        ]
        missing = []
        for path in files:
            for idx, row in enumerate(load_jsonl(path), 1):
                if not row.get("source_quality_level"):
                    missing.append((path.name, idx, row.get("kind"), row.get("item_id") or row.get("name")))
        self.assertEqual(missing, [])

    def test_no_source_rows_are_quality_no_source(self):
        files = [ROOT / "data" / "herb_index.jsonl", ROOT / "data" / "acupoint_index.jsonl"]
        bad = []
        for path in files:
            for row in load_jsonl(path):
                if row.get("trace_status") == "no_source_found" and row.get("source_quality_level") != "no_source":
                    bad.append((path.name, row.get("name"), row.get("source_quality_level")))
        self.assertEqual(bad, [])

    def test_source_quality_conflict_audit_is_clean(self):
        import subprocess
        import sys

        proc = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "p21_audit_source_quality_conflicts.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_no_unresolved_candidate_alias_in_indexes(self):
        files = [
            (ROOT / "data" / "formula_index.jsonl", "formula_id"),
            (ROOT / "data" / "herb_index.jsonl", "herb_id"),
            (ROOT / "data" / "acupoint_index.jsonl", "acupoint_id"),
        ]
        unresolved = []
        for path, id_key in files:
            for row in load_jsonl(path):
                if row.get("source_quality_level") == "candidate_alias":
                    unresolved.append((path.name, row.get(id_key), row.get("name")))
        self.assertEqual(unresolved, [])

    def test_medical_safety_audit_has_no_hard_failures(self):
        import subprocess
        import sys

        proc = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "p22_audit_medical_safety.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_all_completeness_rows_have_safety_boundary(self):
        rows = load_jsonl(ROOT / "data" / "knowledge_completeness.jsonl")
        missing = [(r.get("kind"), r.get("item_id")) for r in rows if not r.get("has_safety_boundary")]
        self.assertEqual(missing, [])

    def test_herb_files_have_caution_text(self):
        missing = []
        for path in sorted((ROOT / "knowledge" / "herbs").glob("*.md")):
            if "index" in path.name:
                continue
            text = path.read_text(encoding="utf-8")
            if not any(k in text for k in ["禁忌", "慎用", "不宜", "注意"]):
                missing.append(path.name)
        self.assertEqual(missing, [])

    def test_trace_safe_placeholders_are_not_fabricated(self):
        import subprocess
        import sys

        proc = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "p22_audit_medical_safety.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        data = __import__("json").loads(proc.stdout)
        self.assertEqual(data["soft_missing_contra_or_caution"], 0)
        self.assertGreater(data["trace_safe_caution_placeholders"], 0)

    def test_p5a_contextual_review_leaves_small_contextual_bucket(self):
        rows = load_jsonl(ROOT / "data" / "verified_sources.jsonl")
        contextual = [r for r in rows if r.get("source_quality_level") == "verified_contextual"]
        needs_review = [r for r in rows if r.get("source_quality_level") == "needs_review"]
        self.assertLessEqual(len(contextual), 20)
        self.assertLessEqual(len(needs_review), 40)

    def test_needs_review_rows_have_p5a_reason(self):
        rows = load_jsonl(ROOT / "data" / "verified_sources.jsonl")
        missing = [
            (r.get("kind"), r.get("item_id"))
            for r in rows
            if r.get("source_quality_level") == "needs_review" and not r.get("p5a_review_reason")
        ]
        self.assertEqual(missing, [])

    def test_no_needs_review_remaining_in_verified_registry(self):
        rows = load_jsonl(ROOT / "data" / "verified_sources.jsonl")
        remaining = [(r.get("kind"), r.get("item_id")) for r in rows if r.get("source_quality_level") == "needs_review"]
        self.assertEqual(remaining, [])


if __name__ == "__main__":
    unittest.main()
