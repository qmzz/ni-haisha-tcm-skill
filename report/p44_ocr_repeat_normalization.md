# P44 OCR Repeat Normalization

Mechanically normalized repeated OCR residue in active knowledge/registry files.
No new medical content was added; only lines/strings with strong OCR-repeat triggers were changed.

## Summary

- Knowledge Markdown files changed: 111
- JSONL registry files changed: 4
- Report files cleaned: 1 (p43_source_ref_residue_sync.md empty section)
- Remaining active-scope hits: 0

## Cleaning Rules Applied

Strong OCR-trigger patterns normalized:
- Replacement characters ()
- Repeated brackets: 【【 -> 【, 】】 -> 】, 《《 -> 《, 》》 -> 》
- Repeated punctuation (3+): ，，， -> ，, 。。。 -> 。, etc.
- Repeated CJK characters (3+ consecutive same): collapsed to single

Targeted OCR page-footer/text residue replacements:
- 加加加一些 -> 加一些
- 骨骨骨。 -> 骨。
- 虫虫虫。 -> 虫。
- 通通通 -> 通
- 通通通\n第 -> 通\n第
- 勤求古訓 -> 勤求古訓
- 博采眾方 -> 博采眾方
- 小桂枝·群龙无首 -> 小桂枝·群龙无首

## Intentionally Not Cleaned

The following were detected but intentionally left as-is because they appear to be
natural speech transcription patterns (repetition for emphasis), historical audit
samples, or source text numbering:
- 二二二、 in hehuanpi.md (possible OCR numbering, low confidence)
- 呃呃呃 in meiguihua.md (speech transcription)
- 痛痛痛 in ganlan.md (speech emphasis)
- Historical report/audit queue samples (p43, p5, p8, p12 reports)

## JSONL Files Changed

- data/verified_sources.jsonl: cleaned OCR repeat residue in source_ref.quote fields
- data/herb_index.jsonl: cleaned OCR repeat residue in source_ref.quote fields
- data/formula_index.jsonl: cleaned OCR repeat residue in source_ref.quote fields
- data/acupoint_index.jsonl: cleaned OCR repeat residue in source_ref.quote fields

## Tool

- tools/p44_normalize_ocr_repeats.py: reusable script for OCR repeat normalization

## Verification

- python -m py_compile tools/p44_normalize_ocr_repeats.py
- python tests/test_content_hygiene.py (4 tests OK)
- python tests/test_registry_consistency.py (17 tests OK)
- python tests/test_tcm_tools.py (14 tests OK)
