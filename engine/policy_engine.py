"""Policy and approval-gate engine for local decision support."""

from __future__ import annotations

from typing import Any, Dict, Mapping

GUARDRAILS = [
    "Uses only user-provided local context.",
    "Does not claim live system access.",
    "Does not persist memory automatically.",
    "Does not execute external actions.",
    "High-risk domain outputs are decision support, not final specialist determinations.",
]

POLICIES = {
    "security": ["access", "privileged", "breach", "zero trust", "finding"],
    "audit": ["audit", "evidence", "control", "sign-off", "traceability"],
    "ai-governance": ["ai", "llm", "model", "data owner", "privacy", "evaluation"],
    "change-control": ["change", "rollback", "test", "release", "validation"],
    "privacy": ["personal", "pii", "retention", "consent", "cross-border"],
    "vendor-risk": ["vendor", "supplier", "contract", "lock-in", "exit"],
}


def evaluate_policy(input_context: Mapping[str, Any], policy: str = "security") -> Dict[str, Any]:
    try:
        from decision_intelligence_engine import build_decision_packet
    except ImportError:
        from .decision_intelligence_engine import build_decision_packet

    packet = build_decision_packet(input_context)
    text = " ".join(packet["facts"] + packet["assumptions"] + packet["missing_evidence"]).lower()
    terms = POLICIES.get(policy, POLICIES["security"])
    hits = [term for term in terms if term in text]
    readiness = max(0, min(100, 75 - len(packet["missing_evidence"]) * 6 - max(0, len(hits) - 2) * 5))
    controls = [{"control": term, "status": "Triggered" if term in hits else "Not detected"} for term in terms]
    return _with_invariants(
        "Policy Evaluation",
        {"policy": policy, "readiness": readiness, "triggered_terms": hits, "controls": controls},
        packet,
        "Close triggered policy evidence gaps before approval.",
    )


def approval_gates(input_context: Mapping[str, Any]) -> Dict[str, Any]:
    try:
        from decision_intelligence_engine import build_decision_packet
    except ImportError:
        from .decision_intelligence_engine import build_decision_packet

    packet = build_decision_packet(input_context)
    risk = packet["scorecard"]["board_risk"]["value"]
    gates = [
        {"role": "accountable_owner", "required": True, "reason": "Every decision needs a named owner."},
        {"role": "approver", "required": risk >= 45, "reason": "Board or high-risk decisions require explicit approval."},
        {"role": "contributor", "required": True, "reason": "Evidence owners must confirm missing evidence."},
        {"role": "informed", "required": True, "reason": "Affected stakeholders need a communication path."},
        {"role": "human_only", "required": risk >= 65, "reason": "High-risk decisions stay outside autonomous execution."},
    ]
    return _with_invariants("Approval Gates", {"gates": gates, "board_risk": risk}, packet, "Assign required approval gates before drafting execution steps.")


def governance_readiness(input_context: Mapping[str, Any]) -> Dict[str, Any]:
    security = evaluate_policy(input_context, "security")
    audit = evaluate_policy(input_context, "audit")
    change = evaluate_policy(input_context, "change-control")
    readiness = round((security["policy_evaluation"]["readiness"] + audit["policy_evaluation"]["readiness"] + change["policy_evaluation"]["readiness"]) / 3)
    return {
        "artifact": "Governance Readiness",
        "governance_readiness": {"score": readiness, "security": security["policy_evaluation"], "audit": audit["policy_evaluation"], "change_control": change["policy_evaluation"]},
        "facts": security["facts"],
        "assumptions": security["assumptions"],
        "hypotheses": security["hypotheses"],
        "missing_evidence": security["missing_evidence"],
        "confidence": security["confidence"],
        "recommended_action": {"recommendation": "Use the lowest-readiness control domain as the next evidence gate.", "owner": "CIO office", "timebox": "Before approval"},
        "guardrails": GUARDRAILS,
    }


def _with_invariants(artifact: str, payload: Dict[str, Any], packet: Mapping[str, Any], recommendation: str) -> Dict[str, Any]:
    key = artifact.lower().replace(" ", "_").replace("-", "_")
    return {
        "artifact": artifact,
        key: payload,
        "facts": packet["facts"],
        "assumptions": packet["assumptions"],
        "hypotheses": packet["hypotheses"],
        "missing_evidence": packet["missing_evidence"],
        "confidence": packet["confidence"],
        "recommended_action": {"recommendation": recommendation, "owner": "CIO office", "timebox": "Before approval"},
        "guardrails": GUARDRAILS,
    }
