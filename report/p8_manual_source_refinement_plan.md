# P8 Manual Source Refinement Plan

Date: 2026-07-06
Branch: p8-manual-source-refinement
Owner: OpenClaw main assistant

## Objective

Synchronize the repository to latest upstream and perform slow, item-by-item refinement against original/source materials. The goal is precision, traceability, safety boundaries, and content quality, not bulk throughput.

## Non-goals

- Do not bulk-generate content from model memory.
- Do not use scripts to batch-modify knowledge content.
- Do not promote source quality without explicit source evidence.
- Do not rewrite medical safety cautions casually.

Scripts may only be used for read-only inventory, validation, tests, or locating candidate records. Actual knowledge edits must be manual, one item at a time.

## Current Repository State

- Synced local `main` to `origin/main` at `90b214a`.
- Created working branch: `p8-manual-source-refinement`.
- Knowledge inventory:
  - Herbs: 416
  - Formulas: 114
  - Cases: 51
  - Acupoints: 412
  - Concepts: 45

## Primary Queues

1. `data/p39_high_risk_external_review_queue.jsonl` — 14 high-risk/restricted herbs requiring human review.
2. `data/review_queue.jsonl` — 218 candidate/needs-review items.
3. `data/p36_external_source_queue.jsonl` — 137 external-source-required items.
4. `data/p11_content_quality_queue.jsonl` — 216 quality/source-boundary items.

## Manual Item Workflow

For each item:

1. Read the current knowledge file.
2. Read registry/source rows related to the item.
3. Locate original-source quote/window in source registry or source FTS.
4. Compare fields against the source text:
   - title/name/alias
   - category/type
   - indications/use cases
   - composition/dose/preparation if formula
   - safety/contraindications if herb/high-risk
   - source references and source quality level
5. Edit only what is supported by source evidence.
6. If source is insufficient, mark boundary explicitly instead of inventing.
7. Update a per-item review note with:
   - item id/name
   - files changed
   - source quote or registry row used
   - decision
   - unresolved issues
8. Run relevant tests/validation after each small batch.
9. Commit in small batches with clear commit message.

## First Batch Proposal

Start with high-risk review queue, because medical safety and legal/restricted status matter most:

- fanxieye / 番泻叶
- haima / 海马
- hamayou / 哈蟆油
- hongqu / 红曲
- jixueteng / 鸡血藤
- luhui / 芦荟
- madouling / 马兜铃
- mubiezi / 木鳖子
- pangolin-related if present
- pugongying / 蒲公英 if queue marks external risk
- quanxie / 全蝎
- shuizhi / 水蛭
- wugong / 蜈蚣
- xixin / 细辛

Actual list should be read from `data/p39_high_risk_external_review_queue.jsonl` before editing.

## Evidence Standard

- Prefer internal original corpus / verified source registry.
- If using external modern references, keep `external_source_required` or appropriate source-quality label unless policy permits promotion.
- Quote source snippets in review notes; do not paste large copyrighted text.
- High-risk herb safety requires conservative wording and explicit professional/medical boundary.

## Progress Log

- 2026-07-06: repository synced, branch created, baseline plan written.
