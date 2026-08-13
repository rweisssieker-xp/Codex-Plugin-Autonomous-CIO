"""Draft action payloads without executing external work."""

from __future__ import annotations

from typing import Any, Dict, Mapping

GUARDRAILS = [
    "Uses only user-provided local context.",
    "Does not claim live system access.",
    "Does not persist memory automatically.",
    "Does not execute external actions.",
    "High-risk domain outputs are decision support, not final specialist determinations.",
]


def draft_actions(input_context: Mapping[str, Any], draft_type: str = "email") -> Dict[str, Any]:
    try:
        from decision_intelligence_engine import build_decision_packet
    except ImportError:
        from .decision_intelligence_engine import build_decision_packet

    packet = build_decision_packet(input_context)
    drafts = []
    actions = packet.get("draft_next_steps", {}).get("next_24h", []) + packet.get("draft_next_steps", {}).get("next_7d", [])
    for idx, action in enumerate(actions[:6], start=1):
        drafts.append(_draft(draft_type, idx, action, packet))
    return {
        "artifact": "Action Drafts",
        "draft_type": draft_type,
        "drafts": drafts,
        "facts": packet["facts"],
        "assumptions": packet["assumptions"],
        "hypotheses": packet["hypotheses"],
        "missing_evidence": packet["missing_evidence"],
        "confidence": packet["confidence"],
        "recommended_action": {"recommendation": "Review and approve drafts manually before using any external system.", "owner": "CIO office", "timebox": "Before sending or creating tickets"},
        "guardrails": GUARDRAILS,
    }


def _draft(draft_type: str, idx: int, action: str, packet: Mapping[str, Any]) -> Dict[str, Any]:
    subject = f"Decision follow-up: {packet.get('request_type', 'CIO review')} #{idx}"
    if draft_type == "teams":
        return {"draft_id": f"TEAMS-{idx:03d}", "channel_hint": "leadership-review", "message": f"{subject}\n{action}\nDecision needed: {packet.get('decision_needed', '')}", "executed": False}
    if draft_type == "topdesk":
        return {"draft_id": f"TOPDESK-{idx:03d}", "change_title": subject, "brief_description": action, "impact": packet.get("request_type", ""), "executed": False}
    if draft_type == "github":
        return {"draft_id": f"GITHUB-{idx:03d}", "issue_title": subject, "issue_body": action, "labels": ["decision-support", "draft"], "executed": False}
    if draft_type == "board-pack":
        return {"draft_id": f"BOARD-{idx:03d}", "section": "Next Actions", "content": action, "executed": False}
    return {"draft_id": f"EMAIL-{idx:03d}", "to": "", "subject": subject, "body": f"{action}\n\nMissing evidence:\n- " + "\n- ".join(packet.get("missing_evidence", [])[:5]), "executed": False}
