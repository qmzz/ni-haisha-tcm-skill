# P56 FFFD / OCR De-quadruple Cleanup

Cleaned U+FFFD replacement characters, quadrupled OCR text artifacts,
long ASCII dot separator runs, and long middle-dot runs from report files.
Core content (data/, knowledge/) was already clean; only report/ had residual artifacts.

- JSON report files changed: 0
- Markdown report files changed: 31
- Total artifacts removed: 236

## JSON Report Changes

## Markdown Report Changes
- `report/alias_candidates.md`: 4 artifacts
- `report/frontmatter_audit.md`: 4 artifacts
- `report/p10d_nsf_alias_hits.md`: 6 artifacts
- `report/p10d_nsf_hits.md`: 5 artifacts
- `report/p11_b_usage_fill_report.md`: 4 artifacts
- `report/p11_c_acupoint_verified_batch_report.md`: 5 artifacts
- `report/p11_c_herb_verified_batch_report.md`: 5 artifacts
- `report/p11_closure.md`: 5 artifacts
- `report/p11_content_quality_queue.md`: 9 artifacts
- `report/p11_d_acupoint_verified_batch_report.md`: 5 artifacts
- `report/p12_candidate_batch_report.md`: 6 artifacts
- `report/p44_ocr_repeat_normalization.md`: 17 artifacts
- `report/p45_footer_artifact_cleanup.md`: 4 artifacts
- `report/p5_refinement_report.md`: 9 artifacts
- `report/p6_no_source_report.md`: 9 artifacts
- `report/p7_alias_review.md`: 5 artifacts
- `report/p7_no_source_classification.md`: 10 artifacts
- `report/p7_release_report.md`: 4 artifacts
- `report/p8_acupoint_no_source_variant.md`: 4 artifacts
- `report/p8_e_3_auto_candidates.md`: 10 artifacts
- `report/p8_e_closure.md`: 3 artifacts
- `report/p8_e_no_source_expand_hits.md`: 7 artifacts
- `report/p8_formula_verified_batch_report.md`: 6 artifacts
- `report/p8_herb_verified_batch_report.md`: 6 artifacts
- `report/p8_knowledge_audit.md`: 13 artifacts
- `report/p8_no_source_inventory.md`: 12 artifacts
- `report/p8_stale_verified_fix_report.md`: 5 artifacts
- `report/p9_quality_audit.md`: 8 artifacts
- `report/quality_report.md`: 8 artifacts
- `report/review_progress.md`: 6 artifacts
- `report/review_report.md`: 32 artifacts
