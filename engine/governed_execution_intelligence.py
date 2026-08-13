"""Governed execution intelligence for local CIO decision support."""

from __future__ import annotations

from contextlib import contextmanager
from datetime import date, timedelta
import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, Mapping

try:
    from decision_intelligence_engine import build_decision_packet
    from decision_twin import run_decision_twin
    from memory_store import init_memory_db
except ImportError:
    from .decision_intelligence_engine import build_decision_packet
    from .decision_twin import run_decision_twin
    from .memory_store import init_memory_db


GUARDRAILS = [
    "Uses only user-provided local context.",
    "Does not claim live system access.",
    "Does not persist memory automatically.",
    "Does not execute external actions.",
    "Does not train or update an external model.",
    "High-risk domain outputs are decision support, not final specialist determinations.",
]


def build_enterprise_decision_ledger(db_path: str) -> Dict[str, Any]:
    init_memory_db(db_path)
    with _connect(db_path) as conn:
        ledger = {
            "decisions": _rows(conn, "select * from decisions order by id desc limit 50"),
            "assumptions": _rows(conn, "select * from assumptions order by id desc limit 50"),
            "evidence": _rows(conn, "select * from evidence order by id desc limit 50"),
            "outcomes": _rows(conn, "select * from outcomes order by id desc limit 50"),
            "reviews": _rows(conn, "select id,title,request_type,created_on from reviews order by id desc limit 25"),
        }
    return _result("Enterprise Decision Ledger", {"db_path": db_path, **ledger}, [f"Built ledger with {len(ledger['decisions'])} decision(s)."])


def trace_control_to_decision(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    text = _text(input_context)
    domains = []
    for domain, words in {
        "audit": ["audit", "control", "evidence"],
        "security": ["security", "privileged", "access"],
        "ai_governance": ["ai", "llm", "model", "data owner"],
        "privacy": ["privacy", "personal", "pii"],
        "change_control": ["change", "release", "rollback", "test"],
    }.items():
        if _hits(text, words):
            domains.append({"control_domain": domain, "decision_ref": packet.get("decision_needed", ""), "evidence_gap": _gap_for(domain, packet.get("missing_evidence", []))})
    if db_path:
        init_memory_db(db_path)
        with _connect(db_path) as conn:
            for item in domains:
                conn.execute("insert into control_decision_links(decision_ref,control_domain,evidence_gap,payload,created_on) values(?,?,?,?,?)", (item["decision_ref"], item["control_domain"], item["evidence_gap"], json.dumps(item, ensure_ascii=False), date.today().isoformat()))
    return _with_packet("Control-to-Decision Traceability", {"links": domains, "link_count": len(domains)}, packet, "Close control evidence links before final approval.")


def score_vendor_truth(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    text = _text(input_context)
    vendor_terms = _hits(text, ["vendor", "supplier", "milestone", "contract"])
    weak_terms = _hits(text, ["missed", "slipped", "delayed", "unknown", "no evidence"])
    score = max(0, min(100, 75 + vendor_terms * 3 - weak_terms * 14 - len(packet.get("missing_evidence", [])) * 3))
    payload = {"truth_score": score, "vendor_signal_count": vendor_terms, "weak_vendor_signal_count": weak_terms, "posture": "Trusted with evidence" if score >= 70 else "Needs challenge" if score >= 40 else "High challenge required"}
    if db_path:
        init_memory_db(db_path)
        with _connect(db_path) as conn:
            conn.execute("insert into vendor_truth_records(vendor_signal,truth_score,payload,created_on) values(?,?,?,?)", ("vendor_context", score, json.dumps(payload, ensure_ascii=False), date.today().isoformat()))
    return _with_packet("Vendor Truth Index", payload, packet, "Ask vendor for evidence-backed milestone and recovery proof.")


def detect_narrative_integrity(input_context: Mapping[str, Any]) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    text = _text(input_context)
    positive = _hits(text, ["on track", "under control", "no impact", "green", "broadly"])
    contradictions = []
    for signal in ["testing has not started", "budget reserve", "incomplete", "slipped", "over forecast", "missing evidence", "unknown"]:
        if signal in text:
            contradictions.append(signal)
    score = max(0, min(100, 85 - positive * 12 - len(contradictions) * 15))
    return _with_packet("Narrative Integrity Detector", {"integrity_score": score, "positive_narrative_signals": positive, "contradictions": contradictions, "posture": "Coherent" if score >= 70 else "Needs reframing" if score >= 40 else "Narrative risk high"}, packet, "Rewrite the executive narrative so uncertainty and evidence gaps are visible.")


def run_decision_simulation_arena(input_context: Mapping[str, Any]) -> Dict[str, Any]:
    scenarios = ["approve", "defer", "re-scope", "stop", "fund", "rollback"]
    results = [run_decision_twin(input_context, scenario) for scenario in scenarios]
    ranked = sorted(
        [{"scenario": item["scenario"], "decision_readiness": item["projected_scores"]["decision_readiness"], "board_risk": item["projected_scores"]["board_risk"], "decision_reversibility": item["decision_reversibility"]} for item in results],
        key=lambda row: (row["decision_readiness"], -row["board_risk"]),
        reverse=True,
    )
    packet = build_decision_packet(input_context)
    return _with_packet("Decision Simulation Arena", {"scenarios": ranked, "recommended_scenario": ranked[0]["scenario"] if ranked else "defer"}, packet, "Use the highest-readiness, lowest-risk scenario as the default challenge path.")


def build_delegation_planner(input_context: Mapping[str, Any]) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    drafts = []
    for idx, item in enumerate(packet.get("missing_evidence", [])[:5], start=1):
        owner = _owner_for(item)
        drafts.append({"draft_id": f"DEL-{idx:03d}", "owner": owner, "task": f"Close evidence gap: {item}", "evidence_needed": item, "due_on": (date.today() + timedelta(days=7)).isoformat(), "escalation_path": "CIO office -> Steering committee", "human_approval_required": True, "executed": False})
    for idx, item in enumerate(packet.get("draft_next_steps", {}).get("next_24h", [])[:3], start=len(drafts) + 1):
        owner = _owner_for(item)
        drafts.append({"draft_id": f"DEL-{idx:03d}", "owner": owner, "task": item, "evidence_needed": "Completion confirmation", "due_on": (date.today() + timedelta(days=2)).isoformat(), "escalation_path": "CIO office", "human_approval_required": True, "executed": False})
    return _with_packet("Autonomous Delegation Planner", {"delegations": drafts, "draft_count": len(drafts)}, packet, "Review delegation drafts manually before assigning work.")


def shadow_cost_of_inaction(input_context: Mapping[str, Any]) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    text = _text(input_context)
    costs = []
    for domain, words, impact in [
        ("audit", ["audit", "control", "evidence"], "audit finding or delayed sign-off"),
        ("security", ["security", "privileged", "access"], "unaccepted security exposure"),
        ("delivery", ["testing", "go-live", "milestone", "delayed"], "delivery failure or late rework"),
        ("finance", ["budget", "spend", "reserve", "forecast"], "unplanned funding pressure"),
        ("customer", ["customer", "billing", "outage"], "customer trust impact"),
    ]:
        if _hits(text, words):
            costs.append({"domain": domain, "inaction_cost": impact, "severity": "High" if domain in {"security", "audit"} else "Medium"})
    return _with_packet("Shadow Cost of Inaction", {"costs": costs, "cost_count": len(costs)}, packet, "Make the cost of not deciding explicit in the decision packet.")


@contextmanager
def _connect(db_path: str):
    conn = sqlite3.connect(Path(db_path))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def _rows(conn: sqlite3.Connection, query: str) -> list[dict[str, Any]]:
    return [dict(row) for row in conn.execute(query).fetchall()]


def _text(input_context: Mapping[str, Any]) -> str:
    return json.dumps(input_context, ensure_ascii=False).lower()


def _hits(text: str, words: list[str]) -> int:
    return sum(1 for word in words if word in text)


def _owner_for(text: str) -> str:
    low = text.lower()
    if "audit" in low or "control" in low:
        return "IT controls owner"
    if "security" in low or "access" in low:
        return "CISO office"
    if "budget" in low or "spend" in low:
        return "Finance owner"
    if "vendor" in low:
        return "Vendor manager"
    return "CIO delegate"


def _gap_for(domain: str, gaps: list[str]) -> str:
    for gap in gaps:
        if domain.replace("_", " ") in gap.lower() or any(word in gap.lower() for word in domain.split("_")):
            return gap
    return gaps[0] if gaps else "No explicit evidence gap found; validate control evidence."


def _with_packet(artifact: str, payload: Dict[str, Any], packet: Mapping[str, Any], recommendation: str) -> Dict[str, Any]:
    return {
        "artifact": artifact,
        artifact.lower().replace(" ", "_").replace("-", "_"): payload,
        "facts": packet["facts"],
        "assumptions": packet["assumptions"],
        "hypotheses": packet["hypotheses"],
        "missing_evidence": packet["missing_evidence"],
        "confidence": packet["confidence"],
        "recommended_action": {"recommendation": recommendation, "owner": "CIO office", "timebox": "Before assignment or approval"},
        "guardrails": GUARDRAILS,
    }


def _result(artifact: str, payload: Dict[str, Any], facts: list[str]) -> Dict[str, Any]:
    return {
        "artifact": artifact,
        artifact.lower().replace(" ", "_").replace("-", "_"): payload,
        "facts": facts,
        "assumptions": [],
        "hypotheses": ["Ledger output is local decision support and may be incomplete if memory is incomplete."],
        "missing_evidence": [],
        "confidence": "Medium",
        "recommended_action": {"recommendation": "Review ledger and traceability outputs before relying on them for governance evidence.", "owner": "CIO office", "timebox": "Next governance review"},
        "guardrails": GUARDRAILS,
    }
