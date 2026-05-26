#!/usr/bin/env bash
set -euo pipefail

cd /app/working/workspaces/default/project/ni-haisha-tcm-skill

rm -f tmp_fix_patch_artifacts.py

python3 scripts/p12_candidate_batch.py --apply >/tmp/p12.log
python3 scripts/build_verified_sources.py >/tmp/build.log
python3 scripts/apply_verified_frontmatter.py --apply >/tmp/apply.log
python3 scripts/standardize_verified_frontmatter.py --apply >/tmp/std.log
python3 scripts/p8_fix_stale_verified_frontmatter.py --apply >/tmp/stale.log
python3 scripts/p9_fix_verified_source_refs.py >/tmp/p9refs.log
python3 scripts/p9_fix_empty_titles.py >/tmp/titles.log
python3 scripts/p11_e_mark_no_source_scope.py --apply >/tmp/p11e.log
python3 scripts/p13_clean_body_placeholders.py --apply >/tmp/p13body.log
python3 scripts/p13_clean_frontmatter_placeholders.py --apply >/tmp/p13fm.log
python3 scripts/check_frontmatter_schema.py >/tmp/fm.log
python3 scripts/build_p8_knowledge_audit.py >/tmp/audit.log
python3 scripts/p9_quality_audit.py >/tmp/p9a.log
python3 scripts/p9_f_review_decisions.py >/tmp/p9f.log
python3 scripts/p9_quality_audit.py >/tmp/p9a2.log
python3 scripts/p9_build_review_queue.py >/tmp/p9q.log
python3 scripts/build_alias_index.py >/tmp/alias.log
python3 scripts/p11_build_content_quality_queue.py >/tmp/p11q.log
python3 scripts/p11_finalize_closure.py >/tmp/closure.log
python3 -m unittest discover -s tests -p 'test_*.py'

echo placeholders=$(grep -RIlE '待考|待补充|暂无|待完善|TODO|待查|待定|待确认|未提供明确|现有 verified 来源未提供' knowledge | wc -l) json_frags=$(grep -RIl '"}, {"' knowledge | wc -l) page_text=$(grep -RIl 'page_num.*text' knowledge | wc -l)

set -a
. /app/working.secret/github.env
set +a

git add -A
git commit -m "feat: P13 清理知识条目占位内容并补齐 P12 seed 稳定性"
git push https://${GITHUB_TOKEN}@github.com/qmzz/ni-haisha-tcm-skill.git HEAD:main
