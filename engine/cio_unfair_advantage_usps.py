"""Explicit unfair-advantage CIO USP modules.

These modules make the most marketable CIO replacement and augmentation claims
available as local, testable decision-support outputs.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Mapping

try:
    from decision_intelligence_engine import build_decision_packet
    from executive_autonomy_innovation import (
        allocate_executive_attention,
        build_decision_chain_of_custody,
        detect_strategic_drift_early_warning,
        forecast_evidence_decay,
        map_cio_replacement_surface,
        measure_decision_latency_cost,
        simulate_synthetic_executive_committee,
    )
    from governed_execution_intelligence import detect_narrative_integrity
except ImportError:
    from .decision_intelligence_engine import build_decision_packet
    from .executive_autonomy_innovation import (
        allocate_executive_attention,
        build_decision_chain_of_custody,
        detect_strategic_drift_early_warning,
        forecast_evidence_decay,
        map_cio_replacement_surface,
        measure_decision_latency_cost,
        simulate_synthetic_executive_committee,
    )
    from .governed_execution_intelligence import detect_narrative_integrity


GUARDRAILS = [
    "Uses only user-provided local context and optional local SQLite memory.",
    "Does not claim live system access.",
    "Does not persist memory automatically.",
    "Does not execute external actions.",
    "Does not train or update an external model.",
    "High-risk domain outputs are decision support, not final specialist determinations.",
]


def detect_executive_blind_spots(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    text = _text(input_context)
    expected = {
        "decision_owner": ["owner", "accountable", "approver"],
        "financial_exposure": ["budget", "spend", "cost", "forecast", "reserve"],
        "security_exposure": ["security", "access", "privileged", "identity"],
        "audit_evidence": ["audit", "control", "evidence", "compliance"],
        "customer_impact": ["customer", "revenue", "billing", "sla"],
        "rollback_path": ["rollback", "fallback", "reversible", "contingency"],
        "vendor_dependency": ["vendor", "supplier", "contract", "milestone"],
    }
    blind_spots = []
    for domain, terms in expected.items():
        if not _hits(text, terms):
            blind_spots.append(
                {
                    "domain": domain,
                    "missing_signal": f"No explicit {domain.replace('_', ' ')} evidence found.",
                    "board_risk": "High" if domain in {"decision_owner", "financial_exposure", "audit_evidence"} else "Medium",
                    "question_to_ask": _blind_spot_question(domain),
                }
            )
    payload = {
        "blind_spots": blind_spots,
        "blind_spot_count": len(blind_spots),
        "blind_spot_pressure": "High" if len(blind_spots) >= 4 else "Medium" if blind_spots else "Low",
        "covered_domains": [domain for domain, terms in expected.items() if _hits(text, terms)],
    }
    return _with_packet("Executive Blind Spot Radar", payload, packet, "Close high-pressure blind spots before board or steering review.")


def calculate_decision_latency_cost_engine(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    base = measure_decision_latency_cost(input_context, db_path)
    packet = build_decision_packet(input_context)
    base_payload = base["decision_latency_cost_meter"]
    text = _text(input_context)
    payload = {
        **base_payload,
        "hidden_compounding_paths": [
            {"path": "defer -> vendor leverage -> scope pressure", "active": _hits(text, ["defer", "vendor", "scope"]) >= 2},
            {"path": "defer -> audit evidence decay -> approval delay", "active": _hits(text, ["audit", "evidence", "approval"]) >= 2},
            {"path": "defer -> duplicated work -> value leakage", "active": _hits(text, ["duplicate", "workstream", "value", "adoption"]) >= 1},
        ],
        "non_decision_cost_statement": "The cost signal is directional and does not estimate actual currency without supplied financial data.",
    }
    return _with_packet("Decision Latency Cost Engine", payload, packet, "Assign a decision SLA and name the cost of not deciding.")


def score_board_trust(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    narrative = detect_narrative_integrity(input_context)
    scorecard = packet.get("scorecard", {})
    evidence = scorecard.get("evidence_confidence", {}).get("value", 50)
    board_risk = scorecard.get("board_risk", {}).get("value", 50)
    narrative_score = narrative["narrative_integrity_detector"]["integrity_score"]
    trust_score = _score(evidence * 0.45 + narrative_score * 0.35 + (100 - board_risk) * 0.2 - len(packet.get("missing_evidence", [])) * 3)
    payload = {
        "board_trust_score": trust_score,
        "trust_posture": "Board-ready" if trust_score >= 75 else "Defensible with gates" if trust_score >= 55 else "Likely to trigger challenge",
        "trust_drivers": {
            "evidence_confidence": evidence,
            "narrative_integrity": narrative_score,
            "board_risk_inverse": 100 - board_risk,
            "missing_evidence_count": len(packet.get("missing_evidence", [])),
        },
        "trust_repair_actions": _trust_repair_actions(packet, narrative_score),
    }
    return _with_packet("Board Trust Score", payload, packet, "Raise board trust by closing evidence gaps and naming uncertainty directly.")


def map_cio_replacement_map(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    surface = map_cio_replacement_surface(input_context, db_path)
    packet = build_decision_packet(input_context)
    payload = {
        "replacement_map": surface["cio_replacement_surface_map"]["surfaces"],
        "prepared_work_percent": surface["cio_replacement_surface_map"]["estimated_cio_work_prepared_percent"],
        "replacement_zones": [
            {"zone": "replaceable_preparation", "work": ["evidence classification", "board challenge simulation", "decision packet assembly"]},
            {"zone": "assistive_governance", "work": ["approval gate mapping", "risk-chain analysis", "delegation drafting"]},
            {"zone": "human_only_accountability", "work": ["risk acceptance", "external execution", "final board commitment"]},
        ],
        "boundary_statement": surface["cio_replacement_surface_map"]["replacement_boundary"],
    }
    return _with_packet("CIO Replacement Map", payload, packet, "Use the map to maximize prepared CIO work while preserving accountable human control.")


def run_executive_narrative_firewall(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    narrative = detect_narrative_integrity(input_context)["narrative_integrity_detector"]
    text = _text(input_context)
    optimistic_claims = _sentences(input_context, ["on track", "green", "under control", "no impact", "broadly"])
    blocked = []
    for claim in optimistic_claims:
        if _hits(text, ["missing", "incomplete", "unknown", "slipped", "over forecast", "not started"]):
            blocked.append({"claim": claim, "reason": "Conflicting uncertainty or negative evidence exists in the same context."})
    payload = {
        "blocked_claims": blocked,
        "allowed_claims": [claim for claim in optimistic_claims if claim not in {item["claim"] for item in blocked}],
        "firewall_score": narrative["integrity_score"],
        "rewrite_required": bool(blocked) or narrative["integrity_score"] < 70,
        "minimum_safe_narrative": _minimum_safe_narrative(packet),
    }
    return _with_packet("Executive Narrative Firewall", payload, packet, "Rewrite blocked claims into evidence-backed board language.")


def analyze_vendor_leverage_intelligence(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    text = _text(input_context)
    drivers = []
    checks = {
        "knowledge_monopoly": ["vendor knows", "vendor owns", "supplier owns", "external expert"],
        "milestone_dependency": ["vendor", "milestone", "slipped", "delayed"],
        "commercial_pressure": ["contract", "renewal", "change request", "scope"],
        "weak_evidence": ["no evidence", "unknown", "unproven", "missing"],
        "internal_owner_gap": ["no owner", "owner unclear", "unassigned"],
    }
    for name, terms in checks.items():
        if _hits(text, terms):
            drivers.append({"driver": name, "severity": "High" if name in {"milestone_dependency", "weak_evidence"} else "Medium"})
    score = _score(len(drivers) * 18 + len(packet.get("missing_evidence", [])) * 4)
    payload = {
        "vendor_leverage_score": score,
        "leverage_posture": "Vendor has leverage" if score >= 60 else "Challengeable" if score >= 30 else "Low leverage detected",
        "drivers": drivers,
        "counter_moves": [
            "Require evidence-backed milestone recovery.",
            "Name internal accountable owner for vendor dependency.",
            "Separate commercial negotiation from delivery evidence.",
        ],
    }
    return _with_packet("Vendor Leverage Intelligence", payload, packet, "Use leverage drivers to rebalance vendor accountability before further commitment.")


def translate_risk_to_cash(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    text = _text(input_context)
    domains = []
    mapping = {
        "security": ("incident exposure, remediation cost, insurance or customer trust pressure", ["security", "privileged", "access"]),
        "audit": ("audit finding, delayed approval or additional control work", ["audit", "control", "evidence"]),
        "delivery": ("late rework, go-live delay or parallel-run cost", ["testing", "go-live", "milestone", "delayed"]),
        "vendor": ("change-request pressure, negotiation loss or dependency premium", ["vendor", "contract", "supplier"]),
        "operations": ("service disruption, productivity loss or escalation load", ["outage", "sla", "operations", "incident"]),
        "portfolio": ("stranded spend, duplicated work or adoption leakage", ["portfolio", "adoption", "workstream", "duplicate"]),
    }
    for domain, (cash_effect, terms) in mapping.items():
        if _hits(text, terms):
            domains.append({"risk_domain": domain, "cash_translation": cash_effect, "confidence": "Medium", "actual_currency_estimate": None})
    payload = {
        "cash_exposure_domains": domains,
        "cash_pressure_score": _score(len(domains) * 16 + packet.get("scorecard", {}).get("value_leakage", {}).get("value", 0) * 0.4),
        "financial_data_required": ["run-rate impact", "cost baseline", "vendor commercial exposure", "benefit baseline"],
    }
    return _with_packet("Risk-to-Cash Translator", payload, packet, "Add financial baselines before presenting any quantified cash claim.")


def detect_strategic_drift_early_warning_usp(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    base = detect_strategic_drift_early_warning(input_context, db_path)
    packet = build_decision_packet(input_context)
    payload = {
        **base["strategic_drift_early_warning"],
        "drift_response_options": ["reconfirm strategy", "re-scope portfolio", "pause conflicting work", "fund explicit exception"],
    }
    return _with_packet("Strategic Drift Early Warning", payload, packet, "Resolve strategy drift before approving more spend or scope.")


def detect_accountability_gaps(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    text = _text(input_context)
    gaps = []
    if not _hits(text, ["owner", "accountable", "approver"]):
        gaps.append({"gap": "No accountable owner named", "required_role": "accountable owner", "severity": "High"})
    if not _hits(text, ["due", "date", "sla", "deadline"]):
        gaps.append({"gap": "No review or due date named", "required_role": "CIO delegate", "severity": "Medium"})
    for item in packet.get("missing_evidence", [])[:5]:
        gaps.append({"gap": item, "required_role": _owner_for(item), "severity": "High" if "audit" in item.lower() or "security" in item.lower() else "Medium"})
    payload = {
        "accountability_gaps": gaps,
        "gap_count": len(gaps),
        "accountability_score": _score(100 - len(gaps) * 14),
        "owner_model": ["accountable owner", "approver", "contributor", "informed", "CIO escalation"],
    }
    return _with_packet("Accountability Gap Detector", payload, packet, "Assign named owners and review dates to each high-severity gap.")


def monitor_evidence_decay(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    decay = forecast_evidence_decay(input_context, db_path)
    packet = build_decision_packet(input_context)
    payload = {
        **decay["evidence_decay_forecast"],
        "monitoring_posture": "Refresh now" if decay["evidence_decay_forecast"]["high_decay_count"] else "Monitor weekly",
    }
    return _with_packet("Evidence Decay Monitor", payload, packet, "Refresh stale or missing evidence before relying on the packet.")


def build_autonomy_boundary_engine(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    text = _text(input_context)
    boundaries = [
        {"work": "classify evidence", "autonomy": "allowed", "approval_required": False, "external_execution_allowed": False},
        {"work": "draft board questions", "autonomy": "allowed", "approval_required": False, "external_execution_allowed": False},
        {"work": "draft delegation", "autonomy": "draft_only", "approval_required": True, "external_execution_allowed": False},
        {"work": "recommend risk acceptance", "autonomy": "decision_support_only", "approval_required": True, "external_execution_allowed": False},
        {"work": "approve budget or vendor commitment", "autonomy": "human_only", "approval_required": True, "external_execution_allowed": False},
        {"work": "execute external system action", "autonomy": "blocked_without_explicit_connector_authorization", "approval_required": True, "external_execution_allowed": False},
    ]
    high_risk_terms = _signals(text, ["security", "privacy", "audit", "regulatory", "financial", "vendor", "customer"])
    payload = {
        "boundaries": boundaries,
        "high_risk_terms": high_risk_terms,
        "autonomy_boundary_score": _score(packet.get("scorecard", {}).get("autonomy_readiness", {}).get("value", 50) - len(high_risk_terms) * 5),
        "human_control_required": True,
    }
    return _with_packet("Autonomy Boundary Engine", payload, packet, "Keep high-risk decisions inside explicit human-control boundaries.")


def allocate_executive_attention_usp(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    base = allocate_executive_attention(input_context, db_path)
    packet = build_decision_packet(input_context)
    payload = {
        **base["executive_attention_allocator"],
        "attention_rule": "Prioritize irreversible, high-risk, low-evidence and board-visible topics before status review.",
    }
    return _with_packet("Executive Attention Allocator", payload, packet, "Use the allocation as the weekly CIO attention agenda.")


def detect_portfolio_cannibalization(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    lines = _sentences(input_context, ["initiative", "project", "workstream", "program", "roadmap", "portfolio", "migration", "erp", "crm", "cloud"])
    scarce = {
        "budget": ["budget", "reserve", "funding", "spend"],
        "architecture_capacity": ["architect", "architecture", "platform"],
        "business_attention": ["adoption", "training", "business owner", "stakeholder"],
        "vendor_capacity": ["vendor", "supplier", "partner"],
        "change_window": ["change", "release", "go-live", "testing"],
    }
    collisions = []
    for resource, terms in scarce.items():
        related = [line for line in lines if _hits(line.lower(), terms)]
        if len(related) >= 2 or (_hits(_text(input_context), terms) and len(lines) >= 3):
            collisions.append({"resource": resource, "collision_signal_count": max(len(related), 1), "affected_work": related[:4], "severity": "High" if resource in {"budget", "architecture_capacity"} else "Medium"})
    payload = {
        "cannibalization_signals": collisions,
        "cannibalization_count": len(collisions),
        "portfolio_cannibalization_score": _score(len(collisions) * 22 + packet.get("scorecard", {}).get("value_leakage", {}).get("value", 0) * 0.35),
        "recommended_portfolio_move": "Re-rank or stop lower-value work" if collisions else "Monitor shared constraints",
    }
    return _with_packet("Portfolio Cannibalization Detector", payload, packet, "Re-rank initiatives that consume the same scarce budget, capacity or business attention.")


def build_decision_chain_of_custody_usp(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    base = build_decision_chain_of_custody(input_context, db_path)
    packet = build_decision_packet(input_context)
    payload = {
        **base["decision_chain_of_custody"],
        "custody_use_case": "Trace evidence, assumptions, missing evidence and recommendation before audit or board review.",
    }
    return _with_packet("Decision Chain of Custody", payload, packet, "Attach custody to any decision that may be challenged later.")


def run_synthetic_executive_committee_usp(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    base = simulate_synthetic_executive_committee(input_context, db_path)
    packet = build_decision_packet(input_context)
    payload = {
        **base["synthetic_executive_committee"],
        "simulation_posture": "Use as pre-board pressure test, not as a substitute for actual stakeholder approval.",
    }
    return _with_packet("Synthetic Executive Committee", payload, packet, "Resolve low-readiness persona challenges before the real meeting.")


def build_unfair_advantage_usp_suite(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    modules = {
        "executive_blind_spot_radar": detect_executive_blind_spots(input_context, db_path),
        "decision_latency_cost_engine": calculate_decision_latency_cost_engine(input_context, db_path),
        "board_trust_score": score_board_trust(input_context, db_path),
        "cio_replacement_map": map_cio_replacement_map(input_context, db_path),
        "executive_narrative_firewall": run_executive_narrative_firewall(input_context, db_path),
        "vendor_leverage_intelligence": analyze_vendor_leverage_intelligence(input_context, db_path),
        "risk_to_cash_translator": translate_risk_to_cash(input_context, db_path),
        "strategic_drift_early_warning": detect_strategic_drift_early_warning_usp(input_context, db_path),
        "accountability_gap_detector": detect_accountability_gaps(input_context, db_path),
        "evidence_decay_monitor": monitor_evidence_decay(input_context, db_path),
        "autonomy_boundary_engine": build_autonomy_boundary_engine(input_context, db_path),
        "executive_attention_allocator": allocate_executive_attention_usp(input_context, db_path),
        "portfolio_cannibalization_detector": detect_portfolio_cannibalization(input_context, db_path),
        "decision_chain_of_custody": build_decision_chain_of_custody_usp(input_context, db_path),
        "synthetic_executive_committee": run_synthetic_executive_committee_usp(input_context, db_path),
    }
    packet = build_decision_packet(input_context)
    payload = {
        "module_count": len(modules),
        "modules": {name: output.get(output["artifact"].lower().replace(" ", "_").replace("-", "_"), {}) for name, output in modules.items()},
        "top_usps": [
            "Detect what leadership is not seeing.",
            "Quantify the pressure created by non-decisions.",
            "Protect board trust with evidence-backed narratives.",
            "Translate technology risk into business consequence.",
            "Separate AI-preparable CIO work from human-only accountability.",
        ],
    }
    return _with_packet("Unfair Advantage CIO USP Suite", payload, packet, "Run this suite before high-stakes CIO reviews to expose hidden risk, ownership gaps and board pressure.")


def _text(input_context: Mapping[str, Any]) -> str:
    return json.dumps(input_context, ensure_ascii=False).lower()


def _hits(text: str, words: list[str]) -> int:
    return sum(1 for word in words if word in text)


def _signals(text: str, words: list[str]) -> list[str]:
    return [word for word in words if word in text]


def _sentences(input_context: Mapping[str, Any], words: list[str]) -> list[str]:
    raw = []
    for value in input_context.values():
        if isinstance(value, list):
            raw.extend(str(item) for item in value)
        elif isinstance(value, dict):
            raw.extend(str(item) for item in value.values())
        else:
            raw.append(str(value))
    return [item for item in raw if any(word in item.lower() for word in words)]


def _score(value: Any) -> int:
    try:
        number = int(round(float(value)))
    except (TypeError, ValueError):
        number = 0
    return max(0, min(100, number))


def _owner_for(text: str) -> str:
    low = text.lower()
    if "audit" in low or "control" in low:
        return "IT controls owner"
    if "security" in low or "access" in low:
        return "CISO office"
    if "budget" in low or "spend" in low:
        return "Finance owner"
    if "vendor" in low or "supplier" in low:
        return "Vendor manager"
    if "architecture" in low:
        return "Enterprise architecture"
    return "CIO delegate"


def _blind_spot_question(domain: str) -> str:
    questions = {
        "decision_owner": "Who owns the decision, the risk and the review date?",
        "financial_exposure": "What is the financial exposure if the decision is wrong or delayed?",
        "security_exposure": "What security risk is being accepted, reduced or deferred?",
        "audit_evidence": "Which evidence would satisfy audit or control review?",
        "customer_impact": "Which customer, revenue or trust impact is possible?",
        "rollback_path": "How reversible is the decision and what triggers rollback?",
        "vendor_dependency": "Where does vendor dependency change leverage or delivery risk?",
    }
    return questions.get(domain, "What is missing from the executive decision record?")


def _trust_repair_actions(packet: Mapping[str, Any], narrative_score: int) -> list[str]:
    actions = []
    if packet.get("missing_evidence"):
        actions.append("Close or explicitly disclose missing evidence.")
    if narrative_score < 70:
        actions.append("Replace optimistic phrasing with evidence-backed uncertainty.")
    if packet.get("scorecard", {}).get("board_risk", {}).get("value", 0) >= 60:
        actions.append("Add counterargument, rollback trigger and accountable owner.")
    return actions or ["Maintain evidence trail and board challenge questions."]


def _minimum_safe_narrative(packet: Mapping[str, Any]) -> str:
    decision = packet.get("decision_needed", "The decision requires executive review.")
    gaps = packet.get("missing_evidence", [])
    if gaps:
        return f"{decision} Current evidence is incomplete; the top gap is: {gaps[0]}"
    return f"{decision} Current evidence supports review, with assumptions and risk chain disclosed."


def _with_packet(artifact: str, payload: Dict[str, Any], packet: Mapping[str, Any], recommendation: str) -> Dict[str, Any]:
    return {
        "artifact": artifact,
        artifact.lower().replace(" ", "_").replace("-", "_"): payload,
        "facts": packet["facts"],
        "assumptions": packet["assumptions"],
        "hypotheses": packet["hypotheses"],
        "missing_evidence": packet["missing_evidence"],
        "confidence": packet["confidence"],
        "recommended_action": {"recommendation": recommendation, "owner": "CIO office", "timebox": "Next executive review"},
        "guardrails": GUARDRAILS,
    }
