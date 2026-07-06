# P8 Final Audit Summary

Date: 2026-07-07
Branch: `p8-manual-source-refinement`

## Scope

This final audit summarizes the current P8 manual source refinement state after the R19 high-confidence fixes. It does not introduce bulk knowledge-body changes. The audit treats `report/p8_manual_reviews/*.md` as the manual review-note corpus and checks whether the major P8 queues have corresponding review coverage.

## Verification

- Initial `git status --short --branch`: clean worktree on `p8-manual-source-refinement`.
- Test command: `.venv/bin/python -m pytest -q`.
- Test result: `38 passed in 5.23s`.

## Review Coverage

Manual review-note files: 382 files in `report/p8_manual_reviews/`.

| Queue | Data file | Rows | Unique `item_id` | Review-note coverage |
| --- | --- | ---: | ---: | ---: |
| review_queue | `data/review_queue.jsonl` | 218 | 218 | 218/218 |
| p36 external source queue | `data/p36_external_source_queue.jsonl` | 142 | 142 | 142/142 |
| p30 no-source classification | `data/p30_no_source_classification.jsonl` | 142 | 142 | 142/142 |
| p11 content quality queue | `data/p11_content_quality_queue.jsonl` | 216 | 216 | 216/216 |
| p26 needs-review segmentation | `data/p26_needs_review_segments.jsonl` | 160 | 160 | 160/160 |
| alias_review | `data/alias_review.jsonl` | 130 | 67 | 130/130 rows, 67/67 unique item IDs |
| p39 high-risk external review | `data/p39_high_risk_external_review_queue.jsonl` | 14 | 14 | 14/14 |

Notes:

- `report/p8_manual_source_refinement_plan.md` still describes the p36 queue as 137 rows, but the current data file contains 142 rows. The current audit uses the data file as authoritative.
- `report/review_progress.md` records `review_queue: 218`, matching the current `data/review_queue.jsonl` row count.

## Review Notes Total

- Total manual review notes present: 382.
- All specified queues have full `item_id` coverage by at least one manual note file.
- Coverage means review evidence has been recorded; it does not mean the corresponding knowledge Markdown, indexes, or registries have all been corrected.

## Key Commit Range

Recent key commits in this P8/R19 closing range:

- `fb94816 docs: update p8 r19 reviewed correction status`
- `f3d986e fix: apply p8 reviewed source-boundary corrections xiamen yangguan yinjiao_ren`
- `974adfa fix: apply p8 reviewed source-boundary corrections zhongshu ganlan jianghuang`
- `004d174 refine: manually review p26 segments mengchong-puhuang`
- `0713fe5 refine: manually review p26 segments lianqiao-meiguihua`
- `2c5426b refine: manually review p26 segments huangbo-kunbu`
- `9b918b1 refine: manually review p26 segments guiban-huangbai`
- `193f19a refine: manually review p26 segments ejiao-guanzhong`
- `4ea9142 refine: manually review p26 segments dangshen-duzhong`
- `5d330dd refine: manually review p26 segments bohe-danggui`
- `ad29485 refine: manually review p26 segments qucha-yutang`
- `9759175 refine: manually review p26 segments benshen-luozhen`
- `1f25362 refine: manually review p11 quality xiaoji-zisu`
- `5f795d8 refine: manually review p11 quality mengshi-xiangru`
- `91f1dbc docs(p8): update R15 manual review status jinyingzi-menghua`
- `a287eaf refine: manually review p11 quality leiwan-menghua`
- `63e699b refine: manually review p11 quality jinyingzi-leigongteng`

## High-Confidence Fixes Already Applied

R19 applied six narrow, review-backed fixes. These are the known actual body/registry changes, not just notes:

- `zhongshu`: removed the false-positive source context about “中枢神经/生命中枢”; downgraded Markdown, `acupoint_index`, and `knowledge_completeness` to `no_source_found/no_source`; removed from `verified_sources`.
- `ganlan`: removed the football/橄榄球 false-positive context; downgraded Markdown, `herb_index`, and `knowledge_completeness` to `no_source_found/no_source`; removed from `verified_sources`.
- `jianghuang`: removed the cross-token false positive from “干姜黄连黄芩人参汤”; downgraded Markdown, `herb_index`, and `knowledge_completeness` to `no_source_found/no_source`; removed from `verified_sources`.
- `xiamen`: fixed the channel/meridian inconsistency for the 侠白 alias entry from `足阳明胃经` to `手太阴肺经`; synced `knowledge/acupoints/xiamen.md` and `acupoint_index`. Alias merge/source-ref replacement was deliberately not done.
- `yangguan`: resolved the 阳关/腰阳关 context boundary issue in the narrow R19 correction set; synced the affected Markdown/index state according to the review note.
- `yinjiao_ren`: removed the incorrect canonical/verified-alias mapping to `yinjiao` 龈交; unified state to `no_source_found/no_source`; added it to no-source and external-source follow-up queues instead of promoting from p29 without quote-level recheck.

Earlier P8 manual review work also included a focused correction for `jinyingzi`, where adjacent-entry pollution was narrowed in the Markdown/quote evidence. Its index and `verified_sources` synchronization remain a follow-up item.

## Follow-up Candidates Identified But Not Completed

These are known candidates from review notes/status reports. They should be handled as separate, small-batch tasks with tests after each batch:

- Source-ref synchronization: many acupoint and herb records have better direct candidate context in notes, but current `source_refs` still point to dirty, adjacent, or weak windows.
- False-positive downgrade pass: examples include source boundaries that are only nearby terms, page/table residue, or cross-token matches; avoid demotion unless the quote-level evidence is clear.
- Alias and duplicate merge pass: examples include `huangbai`/`huangbo`, `gualou`/`gualue`, `luobuma`/`luobumaye`, and similar duplicate or alias-like pairs.
- Field synchronization pass: notes identify possible properties/meridian/toxicity/safety-field updates such as `qiancao`, `shegan`, `wuyi`, `xionghuang`, and `yinchen`, but these were not applied in this final audit.
- Cross-entry contamination cleanup: examples include adjacent source windows and serial pollution around herb entries; each cleanup needs quote-level confirmation.
- Registry `empty_quote` synchronization: p26 notes identify records with real Markdown/source content while registry-level quote state still looks empty or stale.
- High-risk p39 safety review: the 14 high-risk/restricted external-source rows have required safety-field templates and review notes, but no external medical content should be promoted until the required safety fields and source whitelist are satisfied.

## Current Risk Boundary

- The manual note corpus is complete for the specified queues, but most notes are evidence records only.
- Except for the narrow R19 fixes and the earlier `jinyingzi` cleanup, this phase did not batch-edit knowledge Markdown, indexes, `knowledge_completeness`, `verified_sources`, or registry files.
- p11 and p26 are fully covered by notes, but many rows still require later source-boundary correction, field synchronization, downgrade, or alias/duplicate resolution before registry state can be considered fully consistent.
- p30 and p36 coverage confirms no-source/external-source governance classification has notes, not that external source content has been added or validated.
- alias_review coverage confirms all alias rows have corresponding item notes; it does not authorize automatic alias promotion or canonical merging.
- p39 coverage confirms high-risk items are queued and reviewed at the template/evidence level; medical content promotion remains blocked until safety review requirements are explicitly met.

## Final Status

P8 manual review coverage for the requested queues is complete. The repository tests pass. The remaining work is not broad prose editing; it should be executed as targeted follow-up tasks that convert selected review notes into minimal, source-boundary-safe Markdown and registry updates.
