"""Local regression eval runner for The Autonomous CIO."""

from __future__ import annotations

import json
from datetime import datetime, timezone
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
        rubric = _decision_packet_rubric(packet)
        passed = (
            packet["request_type"] == case.get("expected_request_type", packet["request_type"])
            and low <= score <= high
            and _guardrails_ok(packet)
            and rubric["passed"]
        )
        results.append(
            {
                "id": case.get("id"),
                "passed": passed,
                "request_type": packet["request_type"],
                "expected_request_type": case.get("expected_request_type", packet["request_type"]),
                "score": score,
                "expected_range": [low, high],
                "rubric": rubric,
            }
        )
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


def run_orchestrator_evals(eval_dir: str = "engine/evals") -> Dict[str, Any]:
    try:
        from decision_intelligence_engine import run_skill_orchestrator
    except ImportError:
        from .decision_intelligence_engine import run_skill_orchestrator

    cases = _load_cases(Path(eval_dir))
    results = []
    for case in cases:
        output = run_skill_orchestrator(case["input"])
        orchestration = output["orchestration"]
        chain = orchestration["selected_skill_chain"]
        expected = case.get("expected_request_type", orchestration["detected_request_type"])
        required = _required_chain_members(expected)
        missing = [skill for skill in required if skill not in chain]
        passed = orchestration["detected_request_type"] == expected and not missing and _guardrails_ok(output)
        results.append(
            {
                "id": case.get("id"),
                "passed": passed,
                "detected_request_type": orchestration["detected_request_type"],
                "expected_request_type": expected,
                "selected_skill_chain": chain,
                "required_skills": required,
                "missing_required_skills": missing,
                "why": orchestration["why"],
            }
        )
    passed_count = sum(1 for item in results if item["passed"])
    return {
        "artifact": "Orchestrator Chain Eval Report",
        "orchestrator_eval_report": {
            "eval_dir": eval_dir,
            "case_count": len(results),
            "passed_count": passed_count,
            "failed_count": len(results) - passed_count,
            "results": results,
        },
        "facts": [f"Ran {len(results)} orchestrator chain eval case(s)."],
        "assumptions": [],
        "hypotheses": ["Skill-chain checks validate deterministic routing over local golden scenarios."],
        "missing_evidence": [],
        "confidence": "High" if passed_count == len(results) else "Medium",
        "recommended_action": {
            "recommendation": "Review any missing required skill-chain member before release.",
            "owner": "CIO office",
            "timebox": "Before marketplace packaging",
        },
        "guardrails": GUARDRAILS,
    }


def usage_benchmark(eval_dir: str = "engine/evals") -> Dict[str, Any]:
    try:
        from decision_intelligence_engine import build_decision_packet
    except ImportError:
        from .decision_intelligence_engine import build_decision_packet

    cases = _load_cases(Path(eval_dir))
    samples = []
    for case in cases:
        input_text = json.dumps(case["input"], ensure_ascii=False, sort_keys=True)
        packet = build_decision_packet(case["input"])
        output_text = json.dumps(packet, ensure_ascii=False, sort_keys=True)
        samples.append(
            {
                "id": case.get("id"),
                "request_type": packet["request_type"],
                "estimated_input_tokens": _estimate_tokens(input_text),
                "estimated_output_tokens": _estimate_tokens(output_text),
                "selected_skill_count": len(packet["selected_skill_chain"]),
                "missing_evidence_count": len(packet["missing_evidence"]),
                "board_question_count": len(packet["board_challenge_questions"]),
                "decision_readiness": packet["scorecard"]["decision_readiness"]["value"],
                "board_risk": packet["scorecard"]["board_risk"]["value"],
            }
        )
    summary = _usage_summary(samples)
    return {
        "artifact": "Usage Benchmark",
        "usage_benchmark": {
            "eval_dir": eval_dir,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "case_count": len(samples),
            "summary": summary,
            "estimated_input_tokens_avg": summary.get("estimated_input_tokens_avg"),
            "estimated_output_tokens_avg": summary.get("estimated_output_tokens_avg"),
            "estimated_total_tokens_avg": summary.get("estimated_total_tokens_avg"),
            "estimated_total_tokens_max": summary.get("estimated_total_tokens_max"),
            "samples": samples,
            "observed_usage_supplied": False,
            "note": "Token counts are deterministic local estimates. Attach Codex or Responses usage logs for observed usage.",
        },
        "facts": [f"Estimated usage for {len(samples)} golden scenario(s)."],
        "assumptions": ["Token estimates use a local characters-per-token heuristic."],
        "hypotheses": ["Observed Codex usage should be compared against these local estimates."],
        "missing_evidence": ["Observed Codex token usage logs are not supplied."],
        "confidence": "Medium",
        "recommended_action": {
            "recommendation": "Run real Codex sessions for the starter prompts and compare observed usage to this benchmark.",
            "owner": "CIO office",
            "timebox": "Before enterprise rollout",
        },
        "guardrails": GUARDRAILS,
    }


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


def _decision_packet_rubric(packet: Dict[str, Any]) -> Dict[str, Any]:
    checks = {
        "facts_separated": isinstance(packet.get("facts"), list),
        "assumptions_labeled": isinstance(packet.get("assumptions"), list),
        "hypotheses_labeled": isinstance(packet.get("hypotheses"), list),
        "missing_evidence_present": isinstance(packet.get("missing_evidence"), list),
        "decision_needed_clear": bool(packet.get("decision_needed")),
        "recommended_action_present": bool(packet.get("recommended_action", {}).get("recommendation")),
        "board_questions_present": len(packet.get("board_challenge_questions", [])) >= 3,
        "guardrails_present": _guardrails_ok(packet),
        "no_live_action_claim": "execute external actions" in " ".join(packet.get("guardrails", [])).lower(),
    }
    return {"passed": all(checks.values()), "checks": checks}


def _required_chain_members(request_type: str) -> list[str]:
    if request_type == "AI Approval":
        return ["ai-governance-intelligence", "governance-gap-predictor", "executive-decision-packet"]
    if request_type == "Crisis Command":
        return ["crisis-command-mode", "risk-chain-intelligence", "executive-decision-packet"]
    if request_type == "Transformation Value":
        return ["transformation-value-tracker", "value-leakage-intelligence", "executive-decision-packet"]
    if request_type == "Portfolio Decision":
        return ["enterprise-signal-ranking", "executive-truth-layer", "executive-decision-packet"]
    return ["enterprise-signal-ranking", "executive-truth-layer", "risk-chain-intelligence", "executive-decision-packet"]


def _estimate_tokens(text: str) -> int:
    return max(1, round(len(text) / 4))


def _usage_summary(samples: list[dict[str, Any]]) -> dict[str, Any]:
    if not samples:
        return {}
    input_tokens = [item["estimated_input_tokens"] for item in samples]
    output_tokens = [item["estimated_output_tokens"] for item in samples]
    total_tokens = [item["estimated_input_tokens"] + item["estimated_output_tokens"] for item in samples]
    return {
        "estimated_input_tokens_avg": round(sum(input_tokens) / len(input_tokens), 2),
        "estimated_output_tokens_avg": round(sum(output_tokens) / len(output_tokens), 2),
        "estimated_total_tokens_avg": round(sum(total_tokens) / len(total_tokens), 2),
        "estimated_total_tokens_max": max(total_tokens),
        "request_type_counts": _counts(item["request_type"] for item in samples),
    }


def _counts(values: Any) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        counts[str(value)] = counts.get(str(value), 0) + 1
    return counts
