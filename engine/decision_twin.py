"""Interactive decision twin scenarios."""

from __future__ import annotations

from typing import Any, Dict, Mapping

GUARDRAILS = [
    "Uses only user-provided local context.",
    "Does not claim live system access.",
    "Does not persist memory automatically.",
    "Does not execute external actions.",
    "High-risk domain outputs are decision support, not final specialist determinations.",
]

SCENARIO_DELTAS = {
    "approve": {"readiness": -5, "risk": 12, "value": 8, "reversibility": "Low"},
    "defer": {"readiness": 15, "risk": -14, "value": -4, "reversibility": "High"},
    "stop": {"readiness": 5, "risk": -25, "value": -18, "reversibility": "Medium"},
    "re-scope": {"readiness": 12, "risk": -10, "value": 4, "reversibility": "Medium"},
    "fund": {"readiness": 10, "risk": -6, "value": 12, "reversibility": "Medium"},
    "rollback": {"readiness": 4, "risk": -18, "value": -8, "reversibility": "High"},
}


def run_decision_twin(input_context: Mapping[str, Any], scenario: str) -> Dict[str, Any]:
    try:
        from decision_intelligence_engine import build_decision_packet
    except ImportError:
        from .decision_intelligence_engine import build_decision_packet

    packet = build_decision_packet(input_context)
    base = packet["scorecard"]
    delta = SCENARIO_DELTAS.get(scenario, SCENARIO_DELTAS["defer"])
    projected = {
        "decision_readiness": _bounded(base["decision_readiness"]["value"] + delta["readiness"]),
        "board_risk": _bounded(base["board_risk"]["value"] + delta["risk"]),
        "value_leakage": _bounded(base["value_leakage"]["value"] - delta["value"]),
        "evidence_confidence": _bounded(base["evidence_confidence"]["value"] + max(delta["readiness"] // 2, -5)),
        "autonomy_readiness": _bounded(base["autonomy_readiness"]["value"] + delta["readiness"] // 2 - max(delta["risk"], 0) // 3),
    }
    return {
        "artifact": "Interactive Decision Twin",
        "scenario": scenario,
        "base_scores": {key: value["value"] for key, value in base.items()},
        "projected_scores": projected,
        "score_deltas": {key: projected[key] - base[key]["value"] for key in projected},
        "risk_chain_deltas": _risk_deltas(packet, scenario),
        "missing_evidence_changes": _missing_changes(packet, scenario),
        "decision_reversibility": delta["reversibility"],
        "facts": packet["facts"],
        "assumptions": packet["assumptions"],
        "hypotheses": packet["hypotheses"],
        "missing_evidence": packet["missing_evidence"],
        "confidence": packet["confidence"],
        "recommended_action": packet["recommended_action"],
        "guardrails": GUARDRAILS,
    }


def _risk_deltas(packet: Mapping[str, Any], scenario: str) -> list[dict[str, str]]:
    changes = []
    for item in packet.get("risk_chain", [])[:5]:
        direction = "reduced" if scenario in {"defer", "stop", "rollback", "re-scope"} else "increased"
        changes.append({"signal": str(item.get("signal", "")), "scenario_effect": direction, "watch": str(item.get("business_impact", ""))})
    return changes


def _missing_changes(packet: Mapping[str, Any], scenario: str) -> list[str]:
    if scenario in {"defer", "re-scope", "fund"}:
        return [f"Can close evidence gap: {item}" for item in packet.get("missing_evidence", [])[:5]]
    return [f"Must accept or explicitly waive: {item}" for item in packet.get("missing_evidence", [])[:5]]


def _bounded(value: int) -> int:
    return max(0, min(100, int(value)))
