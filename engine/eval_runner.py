"""Local regression eval runner for The Autonomous CIO."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

GUARDRAILS = [
    "Uses only user-provided local context.",
    "Does not claim live system access.",
    "Does not persist memory automatically.",
    "Does not execute external actions.",
    "High-risk domain outputs are decision support, not final specialist determinations.",
]


def run_evals(eval_dir: str = "engine/evals") -> Dict[str, Any]:
    try:
        from decision_intelligence_engine import build_decision_packet
    except ImportError:
        from .decision_intelligence_engine import build_decision_packet

    root = Path(eval_dir)
    cases = _load_cases(root)
    results = []
    for case in cases:
        packet = build_decision_packet(case["input"])
        score = packet["scorecard"][case.get("score_name", "decision_readiness")]["value"]
        low, high = case.get("expected_score_range", [0, 100])
        passed = packet["request_type"] == case.get("expected_request_type", packet["request_type"]) and low <= score <= high and _guardrails_ok(packet)
        results.append({"id": case.get("id"), "passed": passed, "request_type": packet["request_type"], "score": score, "expected_range": [low, high]})
    passed_count = sum(1 for item in results if item["passed"])
    return {
        "artifact": "CIO OS Eval Report",
        "eval_report": {"eval_dir": str(root), "case_count": len(results), "passed_count": passed_count, "failed_count": len(results) - passed_count, "results": results},
        "facts": [f"Ran {len(results)} eval case(s)."],
        "assumptions": [],
        "hypotheses": ["Eval cases are local deterministic regression checks."],
        "missing_evidence": [],
        "confidence": "High" if passed_count == len(results) else "Medium",
        "recommended_action": {"recommendation": "Review failed eval cases before release.", "owner": "CIO office", "timebox": "Before packaging"},
        "guardrails": GUARDRAILS,
    }


def eval_report(eval_dir: str = "engine/evals") -> Dict[str, Any]:
    return run_evals(eval_dir)


def _load_cases(root: Path) -> list[dict[str, Any]]:
    cases = []
    for file_path in sorted(root.glob("*.json")):
        data = json.loads(file_path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and isinstance(data.get("cases"), list):
            cases.extend(data["cases"])
        elif isinstance(data, list):
            cases.extend(data)
    if not cases:
        raise FileNotFoundError(f"no eval cases found in {root}")
    return cases


def _guardrails_ok(packet: Dict[str, Any]) -> bool:
    text = " ".join(packet.get("guardrails", [])).lower()
    return "does not claim live system access" in text and "does not execute external actions" in text
