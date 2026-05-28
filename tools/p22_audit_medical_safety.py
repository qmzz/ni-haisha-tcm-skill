#!/usr/bin/env python3
"""P22/P2 audit medical safety coverage.

Read-only audit for safety boundaries in tools, markdown knowledge files, and data rows.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "report" / "p22_medical_safety_audit.md"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def has_any(text: str, keywords: list[str]) -> bool:
    return any(k in text for k in keywords)


def run_tool(tool: str, payload: dict[str, Any]) -> dict[str, Any]:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "tcm_tools.py"), tool, json.dumps(payload, ensure_ascii=False)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(proc.stdout)


def main() -> int:
    knowledge_dirs = {
        "formula": ROOT / "knowledge" / "formulas",
        "herb": ROOT / "knowledge" / "herbs",
        "acupoint": ROOT / "knowledge" / "acupoints",
    }
    coverage = {}
    missing_safety = []
    missing_contra = []
    caution_placeholders = []

    for kind, folder in knowledge_dirs.items():
        files = sorted(p for p in folder.glob("*.md") if "index" not in p.name)
        safety_count = 0
        contra_count = 0
        for p in files:
            text = p.read_text(encoding="utf-8")
            if has_any(text, ["安全边界", "不构成诊断", "不作为", "不能替代"]):
                safety_count += 1
            else:
                missing_safety.append(str(p.relative_to(ROOT)))
            if kind in {"formula", "herb"} and has_any(text, ["禁忌", "注意事项", "慎用", "不宜"]):
                contra_count += 1
                if "禁忌与慎用（待考）" in text:
                    caution_placeholders.append(str(p.relative_to(ROOT)))
            elif kind in {"formula", "herb"}:
                missing_contra.append(str(p.relative_to(ROOT)))
        coverage[kind] = {
            "total": len(files),
            "with_safety_boundary": safety_count,
            "with_contra_or_caution_text": contra_count if kind in {"formula", "herb"} else None,
        }

    completeness = load_jsonl(ROOT / "data" / "knowledge_completeness.jsonl")
    completeness_missing_safety = [
        f"{r.get('kind')}:{r.get('item_id')}" for r in completeness if not r.get("has_safety_boundary")
    ]

    emergency = run_tool("tcm_safety_check", {"text": "胸痛,呼吸困难"})
    special = run_tool("tcm_safety_check", {"text": "孕妇咳嗽怎么吃小青龙汤"})
    diagnosis_block = run_tool("tcm_diagnose_assist", {"symptoms": ["咳嗽", "小青龙汤怎么吃"]})
    policy = run_tool("tcm_safety_policy", {})

    tool_checks = {
        "emergency_blocks": emergency.get("risk_level") == "high" and emergency.get("blocked") is True,
        "special_or_intent_blocks": special.get("risk_level") == "medium" and special.get("blocked") is True,
        "diagnosis_blocks_treatment_intent": diagnosis_block.get("stopped") is True,
        "policy_exposes_p2_version": policy.get("policy_version") == "p2-2026-05-28",
    }

    hard_failures = []
    if missing_safety:
        hard_failures.append(f"knowledge files missing safety boundary: {len(missing_safety)}")
    if completeness_missing_safety:
        hard_failures.append(f"completeness rows missing has_safety_boundary: {len(completeness_missing_safety)}")
    if not all(tool_checks.values()):
        hard_failures.append("tool safety checks failed")

    lines = [
        "# P22 / P2 Medical Safety Audit",
        "",
        "Read-only audit for medical safety coverage after P2 changes.",
        "",
        "> 边界：本报告审计安全提示、红旗分流和输出约束，不判断医学真实性或临床疗效。",
        "",
        "## Summary",
        "",
        f"- Hard failures: {len(hard_failures)}",
        f"- Markdown files missing safety boundary: {len(missing_safety)}",
        f"- completeness rows missing safety boundary: {len(completeness_missing_safety)}",
        f"- Formula/herb files without explicit 禁忌/注意/慎用 text: {len(missing_contra)}",
        f"- Trace-safe caution placeholders: {len(caution_placeholders)}",
        "",
        "## Knowledge safety boundary coverage",
        "",
        "| kind | total | with_safety_boundary | with_contra_or_caution_text |",
        "|---|---:|---:|---:|",
    ]
    for kind, row in coverage.items():
        contra = row["with_contra_or_caution_text"]
        lines.append(f"| {kind} | {row['total']} | {row['with_safety_boundary']} | {contra if contra is not None else '-'} |")

    lines += [
        "",
        "## Tool safety checks",
        "",
        "| check | result |",
        "|---|---|",
    ]
    for k, v in tool_checks.items():
        lines.append(f"| `{k}` | {'PASS' if v else 'FAIL'} |")

    lines += [
        "",
        "## Remaining soft gaps",
        "",
        "Soft gap means the global safety boundary exists, but the individual formula/herb file lacks explicit contraindication/caution wording.",
        "",
    ]
    if missing_contra:
        for item in missing_contra[:80]:
            lines.append(f"- `{item}`")
        if len(missing_contra) > 80:
            lines.append(f"- ... {len(missing_contra) - 80} more")
    else:
        lines.append("No soft gaps found.")

    if hard_failures:
        lines += ["", "## Hard failures", ""]
        lines.extend(f"- {x}" for x in hard_failures)

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({
        "hard_failures": hard_failures,
        "coverage": coverage,
        "missing_safety_boundary": len(missing_safety),
        "completeness_missing_safety": len(completeness_missing_safety),
        "soft_missing_contra_or_caution": len(missing_contra),
        "trace_safe_caution_placeholders": len(caution_placeholders),
        "tool_checks": tool_checks,
        "report": str(REPORT.relative_to(ROOT)),
    }, ensure_ascii=False, indent=2))
    return 0 if not hard_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
