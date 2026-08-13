"""Evidence quality scoring for provided decision context."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, Mapping

GUARDRAILS = [
    "Uses only user-provided local context.",
    "Does not claim live system access.",
    "Does not persist memory automatically.",
    "Does not execute external actions.",
    "High-risk domain outputs are decision support, not final specialist determinations.",
]


def score_evidence_quality(input_context: Mapping[str, Any]) -> Dict[str, Any]:
    try:
        from decision_intelligence_engine import build_decision_packet
    except ImportError:
        from .decision_intelligence_engine import build_decision_packet

    packet = build_decision_packet(input_context)
    nodes = packet.get("evidence_graph", {}).get("nodes", [])
    scored = []
    for node in nodes:
        label = str(node.get("label", ""))
        source_type = str(node.get("type", "claim"))
        source_weight = _source_weight(source_type, label)
        freshness_days = _freshness_days(label)
        directness = 25 if source_type == "fact" else 12 if source_type == "assumption" else 6
        conflict_score = 30 if any(term in label.lower() for term in ("contradict", "but ", "however", "unclear")) else 0
        completeness = 20 if len(label) > 40 else 10
        score = max(0, min(100, source_weight + directness + completeness - conflict_score - max(0, freshness_days - 45) // 3))
        scored.append(
            {
                "claim": label,
                "source_type": source_type,
                "evidence_quality_score": score,
                "freshness_days": freshness_days,
                "source_weight": source_weight,
                "conflict_score": conflict_score,
                "directness": directness,
                "completeness": completeness,
            }
        )
    avg = round(sum(item["evidence_quality_score"] for item in scored) / len(scored), 1) if scored else 0
    return {
        "artifact": "Evidence Quality Score",
        "evidence_quality": {"average_score": avg, "items": scored},
        "facts": packet["facts"],
        "assumptions": packet["assumptions"],
        "hypotheses": packet["hypotheses"],
        "missing_evidence": packet["missing_evidence"],
        "confidence": packet["confidence"],
        "recommended_action": packet["recommended_action"],
        "guardrails": GUARDRAILS,
    }


def _source_weight(source_type: str, label: str) -> int:
    if source_type == "fact":
        return 35
    if source_type == "assumption":
        return 15
    if "missing" in source_type:
        return 5
    if any(term in label.lower() for term in ("owner", "evidence", "approved", "signed")):
        return 25
    return 18


def _freshness_days(text: str) -> int:
    for token in text.replace(",", " ").split():
        try:
            return max(0, (date.today() - datetime.strptime(token[:10], "%Y-%m-%d").date()).days)
        except Exception:
            continue
    return 0
