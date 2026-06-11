"""Deterministic local analysis helpers for The Autonomous CIO.

The engine is intentionally conservative. It works only on provided JSON context,
uses no network, writes no memory automatically, and returns decision-support
signals rather than final legal, security, financial or regulatory determinations.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import csv
import json
import re
import zipfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence
from xml.sax.saxutils import escape


GUARDRAILS = [
    "Uses only user-provided or demo JSON context.",
    "Does not claim live system access.",
    "Does not persist memory automatically.",
    "Does not execute external actions.",
    "High-risk domain outputs are decision support, not final specialist determinations.",
]

HIGH_RISK_TERMS = {
    "audit",
    "security",
    "compliance",
    "regulator",
    "privacy",
    "legal",
    "financial",
    "customer",
    "breach",
    "access",
}

VALUE_TERMS = {
    "spend",
    "budget",
    "forecast",
    "reserve",
    "cost",
    "license",
    "vendor",
    "adoption",
    "benefit",
    "value",
    "cycle time",
}

RISK_TERMS = {
    "red",
    "late",
    "delayed",
    "missing",
    "incomplete",
    "unknown",
    "unclear",
    "overdue",
    "slipped",
    "gap",
    "risk",
    "outage",
    "no eta",
    "blocked",
    "over forecast",
}

ASSUMPTION_TERMS = {"expects", "assume", "target", "wants", "claims", "should", "likely"}

SECRET_PATTERNS = [
    ("api_key", re.compile(r"(?i)(api[_-]?key|token|secret)\s*[:=]\s*[A-Za-z0-9_\-]{12,}")),
    ("email", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("phone", re.compile(r"\b(?:\+?\d[\d\s().-]{7,}\d)\b")),
]

DOMAIN_KEYWORDS = {
    "project": {"erp", "crm", "rollout", "project", "program", "workstream", "transformation"},
    "system": {"integration", "platform", "system", "environment", "application", "llm", "model"},
    "owner": {"owner", "sponsor", "cio", "ciso", "pmo", "audit", "finance", "sales", "support"},
    "vendor": {"vendor", "supplier", "contract", "outsourcing", "workshop"},
    "control": {"audit", "control", "access", "privacy", "compliance", "retention", "sign-off"},
    "finance": {"budget", "spend", "forecast", "reserve", "cost", "funding", "benefit"},
}

PERSONA_LENSES = {
    "CEO": ["strategic impact", "decision timing", "customer impact", "execution credibility"],
    "CFO": ["forecast", "funding", "reserve", "value leakage", "cost of waiting"],
    "CISO": ["access", "control", "security impact", "residual risk"],
    "Audit": ["evidence", "sign-off", "traceability", "control completeness"],
    "Regulator": ["obligations", "privacy", "compliance exposure", "customer harm"],
    "Customer": ["service impact", "communication", "trust", "recovery timeline"],
}


@dataclass(frozen=True)
class Score:
    value: int
    reasons: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {"value": self.value, "reasons": self.reasons}


def build_decision_packet(input_context: Mapping[str, Any]) -> Dict[str, Any]:
    """Build the signature Executive Decision Packet."""
    ctx = _normalize_context(input_context)
    evidence = _classify_evidence(ctx)
    scorecard = _scorecard(ctx, evidence)
    risk_chain = _risk_chain(ctx, evidence)
    risk_graph = _risk_graph(risk_chain, evidence)
    evidence_graph = _evidence_graph(evidence)
    assurance = _executive_decision_assurance(ctx, evidence, scorecard, risk_chain, evidence_graph)
    request_type = _request_type(ctx)
    selected_chain = _selected_chain(request_type)

    packet = {
        "artifact": "Executive Decision Packet",
        "generated_on": date.today().isoformat(),
        "request_type": request_type,
        "selected_skill_chain": selected_chain,
        "why_this_chain": _why_chain(request_type),
        "decision_needed": _decision_needed(ctx, request_type),
        "situation": _situation(ctx),
        "facts": evidence["facts"],
        "assumptions": evidence["assumptions"],
        "hypotheses": evidence["hypotheses"],
        "missing_evidence": evidence["missing_evidence"],
        "confidence": _confidence(scorecard["evidence_confidence"]["value"]),
        "weak_signals": _weak_signals(ctx),
        "contradictions": _contradictions(ctx),
        "decision_debt": _decision_debt(ctx),
        "semantic_model": _semantic_model(ctx, evidence),
        "llm_extraction_layer": _llm_extraction_layer(ctx, evidence),
        "entity_resolution": _entity_resolution(ctx),
        "risk_chain": risk_chain,
        "risk_graph": risk_graph,
        "causal_decision_graph": _causal_decision_graph(risk_chain),
        "evidence_graph": evidence_graph,
        "graph_metrics": _graph_metrics(risk_chain, evidence_graph, risk_graph),
        "scorecard": scorecard,
        "options": _options(ctx, request_type),
        "scenario_simulation": _scenario_simulation(ctx, request_type, scorecard),
        "counterfactual_simulation": _counterfactual_simulation(ctx, scorecard),
        "board_challenge_questions": _board_questions(ctx, request_type),
        "board_personas": _board_personas(ctx, request_type),
        "board_question_coverage": _board_question_coverage(ctx, request_type),
        "narrative_risk_detector": _narrative_risks(ctx),
        "decision_anti_patterns": _decision_anti_patterns(ctx, evidence),
        "red_team_blue_team": _red_team_blue_team(ctx, request_type, evidence),
        "executive_attention_budget": _executive_attention_budget(ctx, evidence, scorecard),
        "decision_latency_tracker": _decision_latency_tracker(ctx),
        "value_at_risk_estimate": _value_at_risk(ctx, scorecard),
        "governance_control_map": _governance_control_map(ctx),
        "meeting_to_decision_diff": _meeting_to_decision_diff(ctx),
        "decision_packet_quality_grade": _quality_grade(scorecard, evidence, ctx),
        "decision_twin": _decision_twin(ctx, request_type, evidence, scorecard),
        "executive_decision_assurance": assurance,
        "recommended_action": _recommended_action(ctx, request_type, scorecard),
        "draft_next_steps": _next_steps(request_type),
        "audit_trail": _audit_trail(ctx, evidence, scorecard, risk_chain),
        "operating_rhythm": _operating_rhythm(ctx, request_type, scorecard),
        "decision_quality_benchmark": _decision_quality_benchmark(ctx, evidence, scorecard),
        "trend_delta": _trend_delta(ctx, scorecard),
        "guardrails": GUARDRAILS,
    }
    return packet


def extract_semantic_model(input_context: Mapping[str, Any]) -> Dict[str, Any]:
    ctx = _normalize_context(input_context)
    evidence = _classify_evidence(ctx)
    scorecard = _scorecard(ctx, evidence)
    return {
        "artifact": "Semantic Decision Model",
        "semantic_model": _semantic_model(ctx, evidence),
        "facts": evidence["facts"],
        "assumptions": evidence["assumptions"],
        "hypotheses": evidence["hypotheses"],
        "missing_evidence": evidence["missing_evidence"],
        "confidence": _confidence(scorecard["evidence_confidence"]["value"]),
        "recommended_action": _recommended_action(ctx, _request_type(ctx), scorecard),
        "guardrails": GUARDRAILS,
    }


def simulate_scenarios(input_context: Mapping[str, Any]) -> Dict[str, Any]:
    ctx = _normalize_context(input_context)
    evidence = _classify_evidence(ctx)
    scorecard = _scorecard(ctx, evidence)
    return {
        "artifact": "Decision Scenario Simulation",
        "scenario_simulation": _scenario_simulation(ctx, _request_type(ctx), scorecard),
        "facts": evidence["facts"],
        "assumptions": evidence["assumptions"],
        "hypotheses": evidence["hypotheses"],
        "missing_evidence": evidence["missing_evidence"],
        "confidence": _confidence(scorecard["evidence_confidence"]["value"]),
        "recommended_action": _recommended_action(ctx, _request_type(ctx), scorecard),
        "guardrails": GUARDRAILS,
    }


def build_audit_trail(input_context: Mapping[str, Any]) -> Dict[str, Any]:
    ctx = _normalize_context(input_context)
    evidence = _classify_evidence(ctx)
    scorecard = _scorecard(ctx, evidence)
    risk_chain = _risk_chain(ctx, evidence)
    return {
        "artifact": "Decision Audit Trail",
        "audit_trail": _audit_trail(ctx, evidence, scorecard, risk_chain),
        "facts": evidence["facts"],
        "assumptions": evidence["assumptions"],
        "hypotheses": evidence["hypotheses"],
        "missing_evidence": evidence["missing_evidence"],
        "confidence": _confidence(scorecard["evidence_confidence"]["value"]),
        "recommended_action": _recommended_action(ctx, _request_type(ctx), scorecard),
        "guardrails": GUARDRAILS,
    }


def generate_dashboard_data(input_context: Mapping[str, Any]) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    scores = {key: value["value"] for key, value in packet["scorecard"].items()}
    return {
        "artifact": "Visual Command Center Data",
        "title": packet["decision_needed"],
        "request_type": packet["request_type"],
        "scores": scores,
        "heatmap": [
            {"label": item["label"][:64], "confidence": item["confidence"], "value": _confidence_value(item["confidence"])}
            for item in packet["evidence_graph"]["nodes"][:8]
        ],
        "risk_chain": [item["signal"] for item in packet["risk_chain"][:6]],
        "decision_debt": packet["decision_debt"],
        "board_questions": packet["board_challenge_questions"],
        "recommended_action": packet["recommended_action"]["recommendation"],
        "graph_metrics": packet["graph_metrics"],
        "scenario_simulation": packet["scenario_simulation"],
        "audit_trail": packet["audit_trail"],
        "operating_rhythm": packet["operating_rhythm"],
        "decision_quality_benchmark": packet["decision_quality_benchmark"],
        "trend_delta": packet["trend_delta"],
        "risk_graph": packet["risk_graph"],
        "decision_packet_quality_grade": packet["decision_packet_quality_grade"],
        "executive_attention_budget": packet["executive_attention_budget"],
        "value_at_risk_estimate": packet["value_at_risk_estimate"],
        "decision_anti_patterns": packet["decision_anti_patterns"],
        "board_question_coverage": packet["board_question_coverage"],
        "facts": packet["facts"],
        "assumptions": packet["assumptions"],
        "hypotheses": packet["hypotheses"],
        "missing_evidence": packet["missing_evidence"],
        "confidence": packet["confidence"],
        "guardrails": GUARDRAILS,
    }


def build_decision_packet_from_file(path: str) -> Dict[str, Any]:
    imported = import_context_file(path)
    packet = build_decision_packet(imported["input_context"])
    packet["source_file"] = imported["source_file"]
    packet["import_artifact"] = imported["artifact"]
    return packet


def build_autopilot_review_from_file(path: str, memory_path: str | None = None) -> Dict[str, Any]:
    target = Path(path)
    if target.is_dir():
        imported = ingest_source_directory(path)
        input_context = {
            "title": f"Autopilot review from {target.name}",
            "context": [signal.get("summary", "") for signal in imported.get("normalized_signals", [])],
            "domains": sorted({str(signal.get("domain", "unknown")) for signal in imported.get("normalized_signals", [])}),
            "decision_request": "Decide what leadership must act on, escalate, delegate or monitor from this source directory.",
        }
        source_artifact = imported["artifact"]
        source_ref = str(target)
    else:
        imported = import_context_file(path)
        input_context = imported["input_context"]
        source_artifact = imported["artifact"]
        source_ref = imported["source_file"]
    memory = load_memory_store(memory_path) if memory_path else None
    review = build_autopilot_review(input_context, memory)
    review["source_ref"] = source_ref
    review["source_artifact"] = source_artifact
    return review


def generate_dashboard_data_from_file(path: str) -> Dict[str, Any]:
    imported = import_context_file(path)
    dashboard = generate_dashboard_data(imported["input_context"])
    dashboard["source_file"] = imported["source_file"]
    dashboard["import_artifact"] = imported["artifact"]
    return dashboard


def refresh_dashboard_data(input_path: str, output_path: str) -> Dict[str, Any]:
    dashboard = generate_dashboard_data_from_file(input_path)
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(dashboard, indent=2, ensure_ascii=False), encoding="utf-8")
    return {
        "artifact": "Dashboard Data Refresh",
        "input_file": str(Path(input_path)),
        "output_file": str(target),
        "title": dashboard["title"],
        "request_type": dashboard["request_type"],
        "scores": dashboard["scores"],
        "facts": dashboard["facts"],
        "assumptions": dashboard["assumptions"],
        "hypotheses": dashboard["hypotheses"],
        "missing_evidence": dashboard["missing_evidence"],
        "confidence": dashboard["confidence"],
        "recommended_action": dashboard["recommended_action"],
        "guardrails": GUARDRAILS,
    }


def build_decision_assurance(input_context: Mapping[str, Any]) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    return {
        "artifact": "Executive Decision Assurance",
        "llm_extraction_layer": packet["llm_extraction_layer"],
        "entity_resolution": packet["entity_resolution"],
        "causal_decision_graph": packet["causal_decision_graph"],
        "counterfactual_simulation": packet["counterfactual_simulation"],
        "decision_twin": packet["decision_twin"],
        "board_question_coverage": packet["board_question_coverage"],
        "narrative_risk_detector": packet["narrative_risk_detector"],
        "decision_anti_patterns": packet["decision_anti_patterns"],
        "red_team_blue_team": packet["red_team_blue_team"],
        "executive_attention_budget": packet["executive_attention_budget"],
        "decision_latency_tracker": packet["decision_latency_tracker"],
        "value_at_risk_estimate": packet["value_at_risk_estimate"],
        "governance_control_map": packet["governance_control_map"],
        "meeting_to_decision_diff": packet["meeting_to_decision_diff"],
        "decision_packet_quality_grade": packet["decision_packet_quality_grade"],
        "executive_decision_assurance": packet["executive_decision_assurance"],
        "facts": packet["facts"],
        "assumptions": packet["assumptions"],
        "hypotheses": packet["hypotheses"],
        "missing_evidence": packet["missing_evidence"],
        "confidence": packet["confidence"],
        "recommended_action": packet["recommended_action"],
        "guardrails": GUARDRAILS,
    }


def build_autopilot_review(input_context: Mapping[str, Any], memory_context: Mapping[str, Any] | None = None) -> Dict[str, Any]:
    privacy = scan_privacy(input_context)
    safe_context = dict(input_context)
    if privacy["findings"]:
        safe_context["context"] = privacy["redacted_context"]
        safe_context.setdefault("title", str(input_context.get("title", "Autonomous CIO review")))
        safe_context.setdefault("decision_request", str(input_context.get("decision_request", "")))
        safe_context.setdefault("audience", str(input_context.get("audience", "Executive leadership")))

    packet = build_decision_packet(safe_context)
    assurance = build_decision_assurance(safe_context)
    action_review = action_governance(safe_context)
    rhythm = generate_operating_rhythm(safe_context)
    memory = compare_with_memory(safe_context, memory_context or {})
    attention_budget = _autonomous_attention_allocation(packet)
    replacement_surface = _cio_replacement_surface(packet, action_review["action_governance"])
    autonomy_gate = _autonomy_gate(action_review["action_governance"])
    action_ledger = _action_ledger(action_review["action_governance"])
    disruptive_layer = _disruptive_usp_layer(packet, action_review["action_governance"], memory)
    decision_defense = _executive_decision_defense(packet, memory, action_review["action_governance"])

    return {
        "artifact": "Autonomous CIO Autopilot Review",
        "generated_on": date.today().isoformat(),
        "operating_model": "Governed Autonomous CIO Operating System",
        "autopilot_loop": "Signals -> Truth -> Decision -> Action Draft -> Memory -> Operating Rhythm",
        "decision_packet": packet,
        "decision_readiness": packet["scorecard"]["decision_readiness"],
        "enterprise_status": _enterprise_status(packet),
        "evidence_graph": packet["evidence_graph"],
        "risk_chain": packet["risk_chain"],
        "attention_budget": attention_budget,
        "board_questions": packet["board_challenge_questions"],
        "decision_twin": packet["decision_twin"],
        "action_ledger": action_ledger,
        "autonomy_gate": autonomy_gate,
        "memory_update": memory["suggested_memory_updates"],
        "memory_diff": memory,
        "privacy_scan": privacy,
        "assurance": assurance,
        "executive_decision_defense": decision_defense,
        "decision_liability_shield": decision_defense["decision_liability_shield"],
        "executive_blind_spot_radar": decision_defense["executive_blind_spot_radar"],
        "commitment_integrity_score": decision_defense["commitment_integrity_score"],
        "board_narrative_stress_test": decision_defense["board_narrative_stress_test"],
        "autonomous_decision_memory_diff": decision_defense["autonomous_decision_memory_diff"],
        "value_realization_firewall": decision_defense["value_realization_firewall"],
        "risk_to_cash_translator": decision_defense["risk_to_cash_translator"],
        "decision_sla_monitor": decision_defense["decision_sla_monitor"],
        "control_evidence_readiness": decision_defense["control_evidence_readiness"],
        "executive_attention_allocator": decision_defense["executive_attention_allocator"],
        "scenario_kill_switch": decision_defense["scenario_kill_switch"],
        "cio_operating_system_loop": decision_defense["cio_operating_system_loop"],
        "operating_rhythm": rhythm["operating_rhythm"],
        "cio_replacement_surface": replacement_surface,
        "cio_work_autonomy_map": disruptive_layer["cio_work_autonomy_map"],
        "board_objection_simulator": disruptive_layer["board_objection_simulator"],
        "decision_debt_ledger": disruptive_layer["decision_debt_ledger"],
        "truth_gap_detector": disruptive_layer["truth_gap_detector"],
        "executive_time_saved_estimate": disruptive_layer["executive_time_saved_estimate"],
        "cio_shadow_agenda": disruptive_layer["cio_shadow_agenda"],
        "autonomous_steering_pack_factory": disruptive_layer["autonomous_steering_pack_factory"],
        "risk_chain_forecast": disruptive_layer["risk_chain_forecast"],
        "strategic_drift_detector": disruptive_layer["strategic_drift_detector"],
        "human_control_contract": disruptive_layer["human_control_contract"],
        "decision_sla_enforcer": disruptive_layer["decision_sla_enforcer"],
        "vendor_exit_simulator": disruptive_layer["vendor_exit_simulator"],
        "regulatory_shock_simulator": disruptive_layer["regulatory_shock_simulator"],
        "cyber_business_impact_translator": disruptive_layer["cyber_business_impact_translator"],
        "talent_criticality_radar": disruptive_layer["talent_criticality_radar"],
        "capital_allocation_copilot": disruptive_layer["capital_allocation_copilot"],
        "post_decision_learning_loop": disruptive_layer["post_decision_learning_loop"],
        "cio_os_maturity_index": disruptive_layer["cio_os_maturity_index"],
        "stakeholder_alignment_matrix": disruptive_layer["stakeholder_alignment_matrix"],
        "exception_waiver_factory": disruptive_layer["exception_waiver_factory"],
        "policy_as_code_readiness": disruptive_layer["policy_as_code_readiness"],
        "benefits_realization_sentinel": disruptive_layer["benefits_realization_sentinel"],
        "operating_rhythm_autopilot": disruptive_layer["operating_rhythm_autopilot"],
        "autonomous_escalation_drafts": disruptive_layer["autonomous_escalation_drafts"],
        "executive_decision_backlog": disruptive_layer["executive_decision_backlog"],
        "enterprise_control_tower": disruptive_layer["enterprise_control_tower"],
        "ma_carveout_readiness": disruptive_layer["ma_carveout_readiness"],
        "data_trust_radar": disruptive_layer["data_trust_radar"],
        "architecture_runway_guardian": disruptive_layer["architecture_runway_guardian"],
        "executive_narrative_generator": disruptive_layer["executive_narrative_generator"],
        "autonomous_due_diligence_questions": disruptive_layer["autonomous_due_diligence_questions"],
        "resilience_continuity_planner": disruptive_layer["resilience_continuity_planner"],
        "customer_trust_impact_radar": disruptive_layer["customer_trust_impact_radar"],
        "ai_portfolio_governance": disruptive_layer["ai_portfolio_governance"],
        "cost_of_delay_calculator": disruptive_layer["cost_of_delay_calculator"],
        "executive_commitment_tracker": disruptive_layer["executive_commitment_tracker"],
        "decision_rights_mapper": disruptive_layer["decision_rights_mapper"],
        "okr_strategy_fit_checker": disruptive_layer["okr_strategy_fit_checker"],
        "risk_acceptance_docket": disruptive_layer["risk_acceptance_docket"],
        "service_health_sentinel": disruptive_layer["service_health_sentinel"],
        "knowledge_continuity_planner": disruptive_layer["knowledge_continuity_planner"],
        "dependency_breakpoint_analyzer": disruptive_layer["dependency_breakpoint_analyzer"],
        "transformation_kill_criteria": disruptive_layer["transformation_kill_criteria"],
        "vendor_negotiation_brief": disruptive_layer["vendor_negotiation_brief"],
        "compliance_evidence_pack": disruptive_layer["compliance_evidence_pack"],
        "board_decision_simulator": disruptive_layer["board_decision_simulator"],
        "operating_risk_heatmap": disruptive_layer["operating_risk_heatmap"],
        "autonomous_roadmap_reprioritizer": disruptive_layer["autonomous_roadmap_reprioritizer"],
        "audit_finding_predictor": disruptive_layer["audit_finding_predictor"],
        "platform_rationalization_advisor": disruptive_layer["platform_rationalization_advisor"],
        "data_sovereignty_radar": disruptive_layer["data_sovereignty_radar"],
        "operating_model_debt_ledger": disruptive_layer["operating_model_debt_ledger"],
        "strategic_option_portfolio": disruptive_layer["strategic_option_portfolio"],
        "executive_decision_war_room": disruptive_layer["executive_decision_war_room"],
        "evidence_chain_of_custody": disruptive_layer["evidence_chain_of_custody"],
        "decision_rollback_planner": disruptive_layer["decision_rollback_planner"],
        "autonomy_risk_budget": disruptive_layer["autonomy_risk_budget"],
        "approval_boundary_mapper": disruptive_layer["approval_boundary_mapper"],
        "evidence_expiry_monitor": disruptive_layer["evidence_expiry_monitor"],
        "residual_risk_contract": disruptive_layer["residual_risk_contract"],
        "autonomy_stress_test": disruptive_layer["autonomy_stress_test"],
        "decision_consequence_ledger": disruptive_layer["decision_consequence_ledger"],
        "enterprise_friction_map": disruptive_layer["enterprise_friction_map"],
        "strategic_optionality_engine": disruptive_layer["strategic_optionality_engine"],
        "control_debt_burndown": disruptive_layer["control_debt_burndown"],
        "executive_dissent_synthesizer": disruptive_layer["executive_dissent_synthesizer"],
        "decision_backtest_simulator": disruptive_layer["decision_backtest_simulator"],
        "governance_drift_detector": disruptive_layer["governance_drift_detector"],
        "budget_shock_absorber": disruptive_layer["budget_shock_absorber"],
        "vendor_leverage_index": disruptive_layer["vendor_leverage_index"],
        "executive_narrative_diff": disruptive_layer["executive_narrative_diff"],
        "value_at_risk_estimate": packet["value_at_risk_estimate"],
        "narrative_risk_detector": packet["narrative_risk_detector"],
        "facts": packet["facts"],
        "assumptions": packet["assumptions"],
        "hypotheses": packet["hypotheses"],
        "missing_evidence": packet["missing_evidence"],
        "confidence": packet["confidence"],
        "recommended_action": packet["recommended_action"],
        "guardrails": GUARDRAILS,
    }


def build_executive_decision_defense(
    input_context: Mapping[str, Any], memory_context: Mapping[str, Any] | None = None
) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    memory = compare_with_memory(input_context, memory_context or {})
    action_review = action_governance(input_context)
    defense = _executive_decision_defense(packet, memory, action_review["action_governance"])
    return {
        "artifact": "Executive Decision Defense",
        **defense,
        "facts": packet["facts"],
        "assumptions": packet["assumptions"],
        "hypotheses": packet["hypotheses"],
        "missing_evidence": packet["missing_evidence"],
        "confidence": packet["confidence"],
        "recommended_action": packet["recommended_action"],
        "guardrails": GUARDRAILS,
    }


def analyze_risk_graph(input_context: Mapping[str, Any]) -> Dict[str, Any]:
    ctx = _normalize_context(input_context)
    evidence = _classify_evidence(ctx)
    scorecard = _scorecard(ctx, evidence)
    risk_chain = _risk_chain(ctx, evidence)
    risk_graph = _risk_graph(risk_chain, evidence)
    evidence_graph = _evidence_graph(evidence)
    return {
        "artifact": "Risk Graph Analysis",
        "risk_graph": risk_graph,
        "graph_metrics": _graph_metrics(risk_chain, evidence_graph, risk_graph),
        "facts": evidence["facts"],
        "assumptions": evidence["assumptions"],
        "hypotheses": evidence["hypotheses"],
        "missing_evidence": evidence["missing_evidence"],
        "confidence": _confidence(scorecard["evidence_confidence"]["value"]),
        "recommended_action": _recommended_action(ctx, _request_type(ctx), scorecard),
        "guardrails": GUARDRAILS,
    }


def compare_packet_trend(input_context: Mapping[str, Any]) -> Dict[str, Any]:
    ctx = _normalize_context(input_context)
    evidence = _classify_evidence(ctx)
    scorecard = _scorecard(ctx, evidence)
    return {
        "artifact": "Decision Packet Trend Delta",
        "trend_delta": _trend_delta(ctx, scorecard),
        "facts": evidence["facts"],
        "assumptions": evidence["assumptions"],
        "hypotheses": evidence["hypotheses"],
        "missing_evidence": evidence["missing_evidence"],
        "confidence": _confidence(scorecard["evidence_confidence"]["value"]),
        "recommended_action": _recommended_action(ctx, _request_type(ctx), scorecard),
        "guardrails": GUARDRAILS,
    }


def export_review_artifact(input_context: Mapping[str, Any], export_format: str = "markdown") -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    if export_format not in {"markdown", "json"}:
        raise ValueError("export format must be markdown or json")
    content: Any
    if export_format == "json":
        content = packet
    else:
        content = _packet_markdown(packet)
    return {
        "artifact": "Review Artifact Export",
        "format": export_format,
        "content": content,
        "facts": packet["facts"],
        "assumptions": packet["assumptions"],
        "hypotheses": packet["hypotheses"],
        "missing_evidence": packet["missing_evidence"],
        "confidence": packet["confidence"],
        "recommended_action": packet["recommended_action"],
        "guardrails": GUARDRAILS,
    }


def export_autopilot_review_artifact(
    input_context: Mapping[str, Any], memory_context: Mapping[str, Any] | None = None, export_format: str = "markdown"
) -> Dict[str, Any]:
    review = build_autopilot_review(input_context, memory_context)
    if export_format not in {"markdown", "json"}:
        raise ValueError("export format must be markdown or json")
    content: Any = review if export_format == "json" else _autopilot_review_markdown(review)
    return {
        "artifact": "Autopilot Review Export",
        "format": export_format,
        "content": content,
        "facts": review["facts"],
        "assumptions": review["assumptions"],
        "hypotheses": review["hypotheses"],
        "missing_evidence": review["missing_evidence"],
        "confidence": review["confidence"],
        "recommended_action": review["recommended_action"],
        "guardrails": GUARDRAILS,
    }


def generate_operating_rhythm(input_context: Mapping[str, Any]) -> Dict[str, Any]:
    ctx = _normalize_context(input_context)
    evidence = _classify_evidence(ctx)
    scorecard = _scorecard(ctx, evidence)
    request_type = _request_type(ctx)
    return {
        "artifact": "Autonomous CIO Operating Rhythm",
        "operating_rhythm": _operating_rhythm(ctx, request_type, scorecard),
        "facts": evidence["facts"],
        "assumptions": evidence["assumptions"],
        "hypotheses": evidence["hypotheses"],
        "missing_evidence": evidence["missing_evidence"],
        "confidence": _confidence(scorecard["evidence_confidence"]["value"]),
        "recommended_action": _recommended_action(ctx, request_type, scorecard),
        "guardrails": GUARDRAILS,
    }


def benchmark_decision_quality(input_context: Mapping[str, Any]) -> Dict[str, Any]:
    ctx = _normalize_context(input_context)
    evidence = _classify_evidence(ctx)
    scorecard = _scorecard(ctx, evidence)
    return {
        "artifact": "Decision Quality Benchmark",
        "decision_quality_benchmark": _decision_quality_benchmark(ctx, evidence, scorecard),
        "facts": evidence["facts"],
        "assumptions": evidence["assumptions"],
        "hypotheses": evidence["hypotheses"],
        "missing_evidence": evidence["missing_evidence"],
        "confidence": _confidence(scorecard["evidence_confidence"]["value"]),
        "recommended_action": _recommended_action(ctx, _request_type(ctx), scorecard),
        "guardrails": GUARDRAILS,
    }


def ingest_connector_signals(signal_context: Mapping[str, Any]) -> Dict[str, Any]:
    signals = signal_context.get("signals", [])
    if not isinstance(signals, Sequence) or isinstance(signals, (str, bytes, bytearray)):
        raise ValueError("connector signal context must include a signals array")
    normalized = []
    context_lines = []
    for idx, signal in enumerate(signals, start=1):
        if not isinstance(signal, Mapping):
            continue
        summary = str(signal.get("summary", "")).strip()
        if not summary:
            continue
        normalized.append(
            {
                "signal_id": str(signal.get("signal_id", f"SIG-{idx:03d}")),
                "source_type": str(signal.get("source_type", "manual")),
                "observed_at": str(signal.get("observed_at", "")),
                "summary": summary,
                "domain": str(signal.get("domain", "unknown")),
                "entity_refs": list(signal.get("entity_refs", [])),
                "owner_ref": str(signal.get("owner_ref", "")),
                "evidence_ref": str(signal.get("evidence_ref", "")),
                "confidence": str(signal.get("confidence", "Medium")),
                "actionability": str(signal.get("actionability", "monitor")),
            }
        )
        context_lines.append(summary)
    packet_input = {
        "title": "Connector Signal Decision Packet",
        "audience": "Executive leadership",
        "domains": sorted({item["domain"] for item in normalized}),
        "decision_request": "Decide which connector-derived signals require executive action.",
        "signals": context_lines,
    }
    packet = build_decision_packet(packet_input)
    return {
        "artifact": "Connector Signal Ingestion",
        "normalized_signals": normalized,
        "source_summary": _source_summary(normalized),
        "decision_packet": packet,
        "facts": packet["facts"],
        "assumptions": packet["assumptions"],
        "hypotheses": packet["hypotheses"],
        "missing_evidence": packet["missing_evidence"],
        "confidence": packet["confidence"],
        "recommended_action": packet["recommended_action"],
        "guardrails": GUARDRAILS,
    }


def ingest_source_directory(path: str) -> Dict[str, Any]:
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"source directory not found: {path}")
    if not source.is_dir():
        raise ValueError(f"source path must be a directory: {path}")
    supported = {".json", ".csv", ".txt", ".md"}
    signals = []
    for idx, file_path in enumerate(sorted(p for p in source.rglob("*") if p.is_file() and p.suffix.lower() in supported), start=1):
        imported = import_context_file(str(file_path))
        context = imported["input_context"].get("context", [])
        if isinstance(context, Sequence) and not isinstance(context, (str, bytes, bytearray)):
            summary = " ".join(str(item) for item in context)
        else:
            summary = str(context)
        if not summary.strip():
            continue
        signals.append(
            {
                "signal_id": f"LOCAL-{idx:03d}",
                "source_type": file_path.suffix.lower().lstrip("."),
                "observed_at": date.today().isoformat(),
                "summary": summary[:1200],
                "domain": _guess_domain(summary),
                "entity_refs": _entity_refs(summary),
                "owner_ref": "",
                "evidence_ref": str(file_path),
                "confidence": "Medium",
                "actionability": "review",
            }
        )
    ingestion = ingest_connector_signals({"signals": signals})
    ingestion["source_directory"] = str(source)
    ingestion["files_ingested"] = len(signals)
    return ingestion


def import_context_file(path: str) -> Dict[str, Any]:
    target = Path(path)
    if not target.exists():
        raise FileNotFoundError(f"input file not found: {path}")
    suffix = target.suffix.lower()
    if suffix == ".json":
        data = json.loads(target.read_text(encoding="utf-8"))
        if isinstance(data, Mapping):
            return {"artifact": "Imported Context", "input_context": dict(data), "source_file": str(target)}
        if isinstance(data, list):
            return {"artifact": "Imported Context", "input_context": {"context": [json.dumps(x) for x in data]}, "source_file": str(target)}
        raise ValueError("JSON input must be an object or array")
    if suffix == ".csv":
        with target.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        context = ["; ".join(f"{key}: {value}" for key, value in row.items() if value) for row in rows]
        return {"artifact": "Imported Context", "input_context": {"title": target.stem, "context": context}, "source_file": str(target)}
    if suffix in {".txt", ".md"}:
        lines = _lines(target.read_text(encoding="utf-8"))
        return {"artifact": "Imported Context", "input_context": {"title": target.stem, "context": lines}, "source_file": str(target)}
    raise ValueError("supported imports: .json, .csv, .txt, .md")


def scan_privacy(input_context: Mapping[str, Any]) -> Dict[str, Any]:
    ctx = _normalize_context(input_context)
    findings = []
    redacted_items = []
    for item in ctx["items"]:
        redacted = item
        for kind, pattern in SECRET_PATTERNS:
            for match in pattern.findall(item):
                matched_text = match if isinstance(match, str) else match[0]
                findings.append({"type": kind, "match": matched_text[:6] + "...", "risk": "High" if kind == "api_key" else "Medium"})
            redacted = pattern.sub(f"[REDACTED_{kind.upper()}]", redacted)
        redacted_items.append(redacted)
    evidence = _classify_evidence(ctx)
    scorecard = _scorecard(ctx, evidence)
    return {
        "artifact": "Privacy and Secret Scan",
        "findings": findings,
        "redacted_context": redacted_items,
        "data_classification": "Sensitive" if findings else "Unclassified provided context",
        "facts": evidence["facts"],
        "assumptions": evidence["assumptions"],
        "hypotheses": evidence["hypotheses"],
        "missing_evidence": evidence["missing_evidence"],
        "confidence": _confidence(scorecard["evidence_confidence"]["value"]),
        "recommended_action": _recommended_action(ctx, _request_type(ctx), scorecard),
        "guardrails": GUARDRAILS,
    }


def action_governance(input_context: Mapping[str, Any]) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    actions = []
    for idx, action in enumerate(packet["draft_next_steps"]["next_24h"] + packet["draft_next_steps"]["next_7d"], start=1):
        risk_level = _action_risk(action, packet["scorecard"])
        autonomy_level = _autonomy_level(action, risk_level, packet["request_type"])
        cannot_reasons = _cannot_automate_reasons(action, risk_level, packet["request_type"], autonomy_level)
        actions.append(
            {
                "action_id": f"ACT-GOV-{idx:03d}",
                "draft_action": action,
                "risk_level": risk_level,
                "required_approver_role": _required_approver(risk_level, packet["request_type"]),
                "required_approval": _required_approver(risk_level, packet["request_type"]),
                "reversibility": _action_reversibility(action, risk_level),
                "autonomy_level": autonomy_level,
                "automation_allowed": autonomy_level == "L3 Ready for Governed Execution",
                "cannot_automate_reasons": cannot_reasons,
                "audit_event": "drafted_only_not_executed",
            }
        )
    return {
        "artifact": "Action Governance Review",
        "action_governance": actions,
        "facts": packet["facts"],
        "assumptions": packet["assumptions"],
        "hypotheses": packet["hypotheses"],
        "missing_evidence": packet["missing_evidence"],
        "confidence": packet["confidence"],
        "recommended_action": packet["recommended_action"],
        "guardrails": GUARDRAILS,
    }


def connector_profile_catalog() -> Dict[str, Any]:
    profiles = [
        {
            "profile": "outlook_calendar",
            "signal_types": ["board_date", "steering_committee", "decision_deadline", "recurring_operating_review"],
            "required_fields": ["subject", "date", "attendees", "agenda"],
            "decision_use": "Find upcoming decision pressure, missing prep and owner availability.",
            "safe_mode": "optional_connector_or_user_export_no_automatic_access",
        },
        {
            "profile": "outlook_email",
            "signal_types": ["executive_thread", "approval_request", "escalation", "decision_evidence", "owner_commitment"],
            "required_fields": ["subject", "from", "to", "date", "body_excerpt"],
            "decision_use": "Convert email threads into decisions, evidence gaps, commitments, risks and action drafts.",
            "safe_mode": "optional_connector_or_user_export_no_automatic_access",
        },
        {
            "profile": "teams_messages",
            "signal_types": ["escalation_texture", "blocker_discussion", "owner_language", "weak_signal"],
            "required_fields": ["channel_or_chat", "timestamp", "message_excerpt", "participants"],
            "decision_use": "Detect contradiction, unresolved ownership and informal escalation signals.",
            "safe_mode": "optional_connector_or_user_export_no_automatic_access",
        },
        {
            "profile": "slack_messages",
            "signal_types": ["blocker_discussion", "incident_signal", "decision_fragment", "owner_language", "sentiment_shift"],
            "required_fields": ["channel", "timestamp", "user", "text"],
            "decision_use": "Transform Slack exports into weak signals, decision fragments, action candidates and escalation context.",
            "safe_mode": "user_export_or_future_connector_no_automatic_access",
        },
        {
            "profile": "gmail_workspace",
            "signal_types": ["executive_thread", "approval_request", "vendor_message", "risk_signal", "evidence_attachment"],
            "required_fields": ["subject", "sender", "recipients", "date", "snippet"],
            "decision_use": "Convert Gmail or Google Workspace mail exports into decision, evidence and action signals.",
            "safe_mode": "user_export_or_future_connector_no_automatic_access",
        },
        {
            "profile": "sharepoint_documents",
            "signal_types": ["board_pack", "policy", "audit_evidence", "roadmap", "architecture_note"],
            "required_fields": ["file_name", "modified_at", "owner", "excerpt"],
            "decision_use": "Classify facts, assumptions, evidence quality and missing artifacts.",
            "safe_mode": "profile_only_no_document_access",
        },
        {
            "profile": "github_delivery",
            "signal_types": ["release_risk", "dependency_change", "open_defect", "security_finding", "delivery_velocity"],
            "required_fields": ["repository", "issue_or_pr", "status", "owner", "summary"],
            "decision_use": "Translate delivery and technical signals into executive readiness risk.",
            "safe_mode": "profile_only_no_repo_access",
        },
        {
            "profile": "jira_delivery",
            "signal_types": ["initiative_status", "epic_risk", "blocked_story", "release_scope", "delivery_dependency"],
            "required_fields": ["issue_key", "issue_type", "status", "assignee", "summary"],
            "decision_use": "Translate Jira delivery exports into portfolio, dependency and decision-readiness signals.",
            "safe_mode": "user_export_or_future_connector_no_automatic_access",
        },
        {
            "profile": "azure_devops_delivery",
            "signal_types": ["work_item", "release_risk", "dependency", "defect", "sprint_pressure"],
            "required_fields": ["work_item_id", "work_item_type", "state", "assigned_to", "title"],
            "decision_use": "Convert Azure DevOps exports into delivery risk, owner and roadmap signals.",
            "safe_mode": "user_export_or_future_connector_no_automatic_access",
        },
        {
            "profile": "topdesk_service",
            "signal_types": ["incident", "change", "problem", "sla_breach", "service_health"],
            "required_fields": ["ticket_id", "service", "priority", "status", "summary"],
            "decision_use": "Connect service health, change risk and operational exposure to decisions.",
            "safe_mode": "profile_only_no_ticket_access",
        },
        {
            "profile": "servicenow_service",
            "signal_types": ["incident", "change", "problem", "cmdb_ci", "sla_breach"],
            "required_fields": ["number", "category", "priority", "state", "short_description"],
            "decision_use": "Convert ServiceNow exports into service health, change risk and operational exposure signals.",
            "safe_mode": "user_export_or_future_connector_no_automatic_access",
        },
        {
            "profile": "cmdb_assets",
            "signal_types": ["critical_asset", "application_owner", "dependency", "lifecycle_risk", "business_service"],
            "required_fields": ["asset_id", "asset_name", "owner", "criticality", "lifecycle_status"],
            "decision_use": "Map assets, applications and ownership into dependency and modernization decisions.",
            "safe_mode": "user_export_or_future_connector_no_automatic_access",
        },
        {
            "profile": "cloud_cost",
            "signal_types": ["budget_variance", "forecast_risk", "service_cost", "tag_gap", "optimization_candidate"],
            "required_fields": ["provider", "service", "cost", "forecast", "owner"],
            "decision_use": "Translate cloud cost exports into budget shock, value leakage and accountability signals.",
            "safe_mode": "user_export_or_future_connector_no_automatic_access",
        },
        {
            "profile": "security_findings",
            "signal_types": ["vulnerability", "control_gap", "identity_risk", "security_incident", "compliance_exposure"],
            "required_fields": ["finding_id", "severity", "asset", "owner", "summary"],
            "decision_use": "Convert security findings into business impact, risk acceptance and control-debt signals.",
            "safe_mode": "user_export_or_future_connector_no_automatic_access",
        },
        {
            "profile": "observability_monitoring",
            "signal_types": ["availability", "latency", "error_rate", "slo_breach", "capacity_pressure"],
            "required_fields": ["service", "metric", "status", "owner", "summary"],
            "decision_use": "Convert monitoring exports into service health, customer trust and resilience signals.",
            "safe_mode": "user_export_or_future_connector_no_automatic_access",
        },
        {
            "profile": "erp_sap",
            "signal_types": ["process_risk", "cutover_status", "finance_control", "master_data_issue", "business_dependency"],
            "required_fields": ["module", "process", "status", "owner", "summary"],
            "decision_use": "Map ERP/SAP process and cutover exports into business readiness and control decisions.",
            "safe_mode": "user_export_or_future_connector_no_automatic_access",
        },
        {
            "profile": "confluence_knowledge",
            "signal_types": ["decision_record", "runbook", "architecture_note", "risk_note", "knowledge_gap"],
            "required_fields": ["page_title", "space", "owner", "updated_at", "excerpt"],
            "decision_use": "Turn Confluence exports into decision memory, evidence and knowledge-continuity signals.",
            "safe_mode": "user_export_or_future_connector_no_automatic_access",
        },
        {
            "profile": "google_drive_documents",
            "signal_types": ["board_pack", "policy", "audit_evidence", "roadmap", "spreadsheet_signal"],
            "required_fields": ["file_name", "owner", "modified_at", "excerpt"],
            "decision_use": "Convert Google Drive document exports into evidence, policy, roadmap and KPI signals.",
            "safe_mode": "user_export_or_future_connector_no_automatic_access",
        },
        {
            "profile": "industrial_file_drop",
            "signal_types": ["erp_cutover", "mes_interface", "qms_evidence", "ot_dependency", "vendor_support"],
            "required_fields": ["source_file", "system", "risk_status", "owner", "evidence_ref"],
            "decision_use": "Ingest ERP/MES/QMS/OT exports as production-continuity decision signals.",
            "safe_mode": "local_files_only",
        },
    ]
    return {
        "artifact": "Connector Profile Catalog",
        "profiles": profiles,
        "facts": [],
        "assumptions": [],
        "hypotheses": ["Profiles define expected signal contracts; they do not connect to live systems."],
        "missing_evidence": ["Actual connector credentials, permissions and tenant-specific schemas are not included."],
        "confidence": "High",
        "recommended_action": {
            "recommendation": "Use these profiles to map available exports or future connectors into connector-neutral signals.",
            "owner": "CIO office",
            "timebox": "Before first live connector implementation",
        },
        "guardrails": GUARDRAILS,
    }


def detect_connector_profile(path: str) -> Dict[str, Any]:
    records = _read_export_records(path)
    joined_keys = " ".join(sorted({key.lower() for row in records for key in row.keys()}))
    joined_values = " ".join(" ".join(str(value).lower() for value in row.values()) for row in records[:10])
    fingerprint = f"{joined_keys} {joined_values}"
    profile_scores = {
        "outlook_calendar": _count_terms(fingerprint, {"subject", "attendees", "agenda", "organizer", "start", "meeting"}),
        "outlook_email": _count_terms(fingerprint, {"subject", "from", "to", "cc", "email", "body", "importance", "conversation"}),
        "teams_messages": _count_terms(fingerprint, {"channel", "chat", "message", "participants", "reply", "thread"}),
        "slack_messages": _count_terms(fingerprint, {"channel", "user", "text", "ts", "thread_ts", "reaction", "slack"}),
        "gmail_workspace": _count_terms(fingerprint, {"gmail", "sender", "recipients", "snippet", "label", "threadid", "messageid"}),
        "sharepoint_documents": _count_terms(fingerprint, {"file", "modified", "document", "library", "owner", "path"}),
        "github_delivery": _count_terms(fingerprint, {"repository", "issue", "pull", "pr", "commit", "branch"}),
        "jira_delivery": _count_terms(fingerprint, {"jira", "issue_key", "epic", "story", "sprint", "assignee", "resolution"}),
        "azure_devops_delivery": _count_terms(fingerprint, {"work_item", "work item", "ado", "azure devops", "assigned_to", "iteration", "area path"}),
        "topdesk_service": _count_terms(fingerprint, {"ticket", "incident", "change", "problem", "priority", "sla"}),
        "servicenow_service": _count_terms(fingerprint, {"servicenow", "sys_id", "number", "short_description", "cmdb_ci", "assignment_group"}),
        "cmdb_assets": _count_terms(fingerprint, {"cmdb", "asset_id", "asset", "criticality", "lifecycle", "business_service", "configuration item"}),
        "cloud_cost": _count_terms(fingerprint, {"cloud", "provider", "service", "cost", "forecast", "budget", "tag", "subscription"}),
        "security_findings": _count_terms(fingerprint, {"finding", "severity", "cve", "vulnerability", "identity", "control", "remediation"}),
        "observability_monitoring": _count_terms(fingerprint, {"slo", "latency", "error_rate", "availability", "metric", "alert", "monitor"}),
        "erp_sap": _count_terms(fingerprint, {"sap", "erp", "module", "process", "cutover", "master data", "finance control"}),
        "confluence_knowledge": _count_terms(fingerprint, {"confluence", "space", "page_title", "runbook", "decision record", "updated_at"}),
        "google_drive_documents": _count_terms(fingerprint, {"google drive", "drive", "sheet", "doc", "slides", "file_name", "modified_at"}),
        "industrial_file_drop": _count_terms(fingerprint, {"erp", "mes", "qms", "plm", "ot", "shopfloor", "production", "validated"}),
    }
    profile, score = max(profile_scores.items(), key=lambda item: item[1])
    confidence = "High" if score >= 3 else "Medium" if score >= 1 else "Low"
    return {
        "artifact": "Connector Export Profile Detection",
        "source_file": str(Path(path)),
        "detected_profile": profile if score else "manual",
        "confidence": confidence,
        "profile_scores": profile_scores,
        "record_count": len(records),
        "facts": [f"Detected {len(records)} record(s) in local export file."],
        "assumptions": [],
        "hypotheses": ["Profile detection uses local field and value fingerprints only."],
        "missing_evidence": [] if score else ["No strong connector-specific field fingerprint found."],
        "recommended_action": {
            "recommendation": "Use the detected profile for adapt-connector-export, or choose a profile manually if confidence is Low.",
            "owner": "CIO office",
            "timebox": "Before decision packet generation",
        },
        "guardrails": GUARDRAILS,
    }


def adapt_connector_export(path: str, profile: str = "auto") -> Dict[str, Any]:
    selected_profile = detect_connector_profile(path)["detected_profile"] if profile == "auto" else profile
    records = _read_export_records(path)
    signals = []
    for idx, row in enumerate(records, start=1):
        summary = _profile_summary(selected_profile, row)
        if not summary.strip():
            continue
        signals.append(
            {
                "signal_id": f"{selected_profile.upper().replace('-', '_')}-{idx:03d}",
                "source_type": selected_profile,
                "observed_at": _first_value(row, ["observed_at", "date", "timestamp", "modified_at", "created", "start"]),
                "summary": summary,
                "domain": _profile_domain(selected_profile, summary),
                "entity_refs": _profile_entities(row, summary),
                "owner_ref": _first_value(row, ["owner", "assignee", "organizer", "responsible", "participants", "attendees"]),
                "evidence_ref": f"{path}#row-{idx}",
                "confidence": "Medium",
                "actionability": "review",
            }
        )
    ingestion = ingest_connector_signals({"signals": signals})
    return {
        "artifact": "Connector Export Adapter",
        "source_file": str(Path(path)),
        "profile": selected_profile,
        "records_read": len(records),
        "signals_created": len(signals),
        "normalized_signals": signals,
        "decision_packet": ingestion["decision_packet"],
        "facts": ingestion["facts"],
        "assumptions": ingestion["assumptions"],
        "hypotheses": ingestion["hypotheses"],
        "missing_evidence": ingestion["missing_evidence"],
        "confidence": ingestion["confidence"],
        "recommended_action": ingestion["recommended_action"],
        "guardrails": GUARDRAILS,
    }


def build_llm_extraction_contract(input_context: Mapping[str, Any]) -> Dict[str, Any]:
    ctx = _normalize_context(input_context)
    evidence = _classify_evidence(ctx)
    scorecard = _scorecard(ctx, evidence)
    contract = {
        "input_fields": [
            "title",
            "audience",
            "decision_request",
            "context",
            "signals",
            "constraints",
            "known_decisions",
            "risk_tolerance",
        ],
        "required_output_fields": [
            "facts",
            "assumptions",
            "hypotheses",
            "missing_evidence",
            "contradictions",
            "weak_signals",
            "entities",
            "decisions",
            "risks",
            "actions",
        ],
        "classification_rules": [
            "Facts require explicit evidence in the provided context.",
            "Assumptions use language such as target, expects, assumes, likely or should.",
            "Hypotheses are plausible interpretations that still require validation.",
            "Missing evidence is the specific proof needed before approval or escalation.",
            "Contradictions compare claims across status, budget, risk, owner and deadline signals.",
        ],
        "sample_extraction": {
            "facts": evidence["facts"][:5],
            "assumptions": evidence["assumptions"][:5],
            "hypotheses": evidence["hypotheses"][:5],
            "missing_evidence": evidence["missing_evidence"][:5],
            "weak_signals": _weak_signals(ctx)[:5],
            "contradictions": _contradictions(ctx)[:5],
            "entities": _semantic_model(ctx, evidence)["entities"][:5],
        },
    }
    return {
        "artifact": "LLM Extraction Contract",
        "contract": contract,
        "facts": evidence["facts"],
        "assumptions": evidence["assumptions"],
        "hypotheses": evidence["hypotheses"],
        "missing_evidence": evidence["missing_evidence"],
        "confidence": _confidence(scorecard["evidence_confidence"]["value"]),
        "recommended_action": _recommended_action(ctx, _request_type(ctx), scorecard),
        "guardrails": GUARDRAILS,
    }


def run_skill_orchestrator(input_context: Mapping[str, Any], memory_context: Mapping[str, Any] | None = None) -> Dict[str, Any]:
    ctx = _normalize_context(input_context)
    packet = build_decision_packet(input_context)
    review = build_autopilot_review(input_context, memory_context)
    governance = action_governance(input_context)
    contract = build_llm_extraction_contract(input_context)
    industrial = _is_industrial_context(ctx)
    chain = list(packet["selected_skill_chain"])
    if industrial:
        chain = [
            "industrial-cio-operating-system",
            "it-ot-production-risk-command",
            "qms-audit-evidence-readiness",
        ] + chain
    chain.extend(["autonomous-action-framework", "autonomous-executive-memory"])
    if "board-challenger" not in chain and packet["request_type"] in {"Board Prep", "Crisis Command"}:
        chain.insert(-2, "board-challenger")
    orchestration = {
        "detected_request_type": packet["request_type"],
        "detected_domains": _detected_domains(ctx),
        "selected_skill_chain": _unique(chain),
        "why": _orchestrator_why(packet["request_type"], industrial),
        "integrated_outputs": [
            "Executive Decision Packet",
            "Autonomous CIO Autopilot Review",
            "Action Governance Review",
            "Memory Update Proposal",
            "LLM Extraction Contract",
        ],
        "next_engine_commands": [
            "build-decision-packet",
            "autopilot-review",
            "action-governance",
            "save-memory",
            "export-package",
        ],
    }
    memory_proposal = propose_memory_updates(input_context, memory_context or {})
    return {
        "artifact": "Autonomous CIO Skill Orchestration",
        "orchestration": orchestration,
        "decision_packet": packet,
        "autopilot_review": review,
        "action_governance": governance["action_governance"],
        "memory_update_proposal": memory_proposal["memory_update_proposal"],
        "llm_extraction_contract": contract["contract"],
        "facts": packet["facts"],
        "assumptions": packet["assumptions"],
        "hypotheses": packet["hypotheses"],
        "missing_evidence": packet["missing_evidence"],
        "confidence": packet["confidence"],
        "recommended_action": packet["recommended_action"],
        "guardrails": GUARDRAILS,
    }


def propose_memory_updates(input_context: Mapping[str, Any], memory_context: Mapping[str, Any] | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    memory = memory_context or {}
    comparison = compare_with_memory(input_context, memory) if memory else None
    proposal = {
        "decision_memory": [
            {
                "decision": packet["decision_needed"],
                "owner": packet["recommended_action"]["owner"],
                "status": "Draft",
                "confidence": packet["confidence"],
            }
        ],
        "assumption_register": [
            {"assumption": item, "status": "Open", "validation_needed": _missing_for(item)}
            for item in packet["assumptions"]
        ],
        "evidence_graph": packet["evidence_graph"]["nodes"][:12],
        "risk_chain_map": packet["risk_chain"][:8],
        "action_ledger": [
            {"action": item, "status": "Draft", "approval_required": True}
            for item in packet["draft_next_steps"]["next_24h"]
        ],
        "memory_conflicts": (comparison or {}).get("conflicting_claims", []),
        "stale_assumptions": (comparison or {}).get("stale_assumptions", []),
        "overdue_actions": (comparison or {}).get("overdue_actions", []),
    }
    return {
        "artifact": "Executive Memory Update Proposal",
        "memory_update_proposal": proposal,
        "facts": packet["facts"],
        "assumptions": packet["assumptions"],
        "hypotheses": packet["hypotheses"],
        "missing_evidence": packet["missing_evidence"],
        "confidence": packet["confidence"],
        "recommended_action": packet["recommended_action"],
        "guardrails": GUARDRAILS,
    }


def inspect_memory_store(path: str) -> Dict[str, Any]:
    store = load_memory_store(path)
    stale = []
    overdue = []
    for item in store.get("assumption_register", []):
        if str(item.get("status", "")).lower() in {"open", "stale", ""}:
            stale.append(item)
    for item in store.get("action_ledger", []):
        if str(item.get("status", "")).lower() in {"draft", "open", "overdue", ""}:
            overdue.append(item)
    decision_count = len(store.get("decision_memory", []))
    packet_count = len(store.get("decision_packets", []))
    confidence = "Medium" if packet_count else "Low"
    return {
        "artifact": "Executive Memory Store Inspection",
        "memory_path": path,
        "store_counts": {key: len(value) for key, value in store.items() if isinstance(value, list)},
        "stale_assumptions": stale[:12],
        "open_or_overdue_actions": overdue[:12],
        "decision_count": decision_count,
        "facts": [f"Memory store contains {packet_count} saved decision packet(s)."],
        "assumptions": [],
        "hypotheses": ["Open assumptions and draft actions may require owner review."],
        "missing_evidence": [] if packet_count else ["No saved decision packets found in memory store."],
        "confidence": confidence,
        "recommended_action": {
            "recommendation": "Review stale assumptions and draft actions before the next operating review.",
            "owner": "CIO office",
            "timebox": "Next review cycle",
        },
        "guardrails": GUARDRAILS,
    }


def export_decision_package(input_context: Mapping[str, Any], output_dir: str) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    review = build_autopilot_review(input_context)
    governance = action_governance(input_context)
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    files: Dict[str, str] = {}
    files["executive_decision_packet.json"] = json.dumps(packet, indent=2, ensure_ascii=False)
    files["autonomous_cio_operating_review.json"] = json.dumps(review, indent=2, ensure_ascii=False)
    files["board_pack.md"] = _board_pack_markdown(packet, review)
    files["audit_evidence_pack.md"] = _audit_pack_markdown(packet)
    files["steering_committee_deck_outline.md"] = _deck_outline_markdown(packet, review)
    files["action_ledger.csv"] = _action_ledger_csv(governance["action_governance"])
    files["decision_log.json"] = json.dumps(propose_memory_updates(input_context)["memory_update_proposal"], indent=2, ensure_ascii=False)
    written = []
    for file_name, content in files.items():
        file_path = target / file_name
        file_path.write_text(content, encoding="utf-8")
        written.append(str(file_path))
    return {
        "artifact": "Decision Export Package",
        "output_dir": str(target),
        "files": written,
        "facts": packet["facts"],
        "assumptions": packet["assumptions"],
        "hypotheses": packet["hypotheses"],
        "missing_evidence": packet["missing_evidence"],
        "confidence": packet["confidence"],
        "recommended_action": packet["recommended_action"],
        "guardrails": GUARDRAILS,
    }


def export_office_package(input_context: Mapping[str, Any], output_dir: str) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    review = build_autopilot_review(input_context)
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    docx_path = target / "board_decision_pack.docx"
    pptx_path = target / "steering_committee_deck.pptx"
    _write_docx(
        docx_path,
        [
            "Board Decision Pack",
            f"Decision needed: {packet['decision_needed']}",
            f"Request type: {packet['request_type']}",
            f"Confidence: {packet['confidence']}",
            f"Recommended action: {packet['recommended_action']['recommendation']}",
            "Facts:",
            *[f"- {item}" for item in packet["facts"][:10]],
            "Missing evidence:",
            *[f"- {item}" for item in packet["missing_evidence"][:10]],
            "Guardrails:",
            *[f"- {item}" for item in packet["guardrails"]],
        ],
    )
    _write_pptx(
        pptx_path,
        [
            ("Decision Required", [packet["decision_needed"], f"Confidence: {packet['confidence']}"]),
            ("Readiness Scores", [f"{key}: {value['value']}" for key, value in packet["scorecard"].items()]),
            ("Risk Chain", [f"{item.get('signal')} -> {item.get('business_impact')}" for item in packet["risk_chain"][:5]]),
            ("Recommended Action", [packet["recommended_action"]["recommendation"]]),
            ("Action Ledger", [str(item.get("draft_action", "")) for item in review.get("action_ledger", [])[:6]]),
        ],
    )
    return {
        "artifact": "Office Export Package",
        "output_dir": str(target),
        "files": [str(docx_path), str(pptx_path)],
        "facts": packet["facts"],
        "assumptions": packet["assumptions"],
        "hypotheses": packet["hypotheses"],
        "missing_evidence": packet["missing_evidence"],
        "confidence": packet["confidence"],
        "recommended_action": packet["recommended_action"],
        "guardrails": GUARDRAILS,
    }


def initialize_memory_store() -> Dict[str, Any]:
    return {
        "version": "1.0",
        "created_on": date.today().isoformat(),
        "decision_packets": [],
        "decision_memory": [],
        "assumption_register": [],
        "evidence_graph": [],
        "risk_chain_map": [],
        "action_ledger": [],
        "audit_events": [],
    }


def load_memory_store(path: str) -> Dict[str, Any]:
    target = Path(path)
    if not target.exists():
        return initialize_memory_store()
    data = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(data, Mapping):
        raise ValueError("memory store must be a JSON object")
    store = initialize_memory_store()
    store.update(data)
    return store


def save_packet_to_memory(input_context: Mapping[str, Any], memory_path: str) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    store = load_memory_store(memory_path)
    packet_id = f"PKT-{date.today().isoformat()}-{len(store['decision_packets']) + 1:03d}"
    store["decision_packets"].append({"packet_id": packet_id, "saved_on": date.today().isoformat(), "packet": packet})
    store["decision_memory"].append(
        {
            "decision_id": packet_id.replace("PKT", "DEC"),
            "decision": packet["decision_needed"],
            "owner": packet["recommended_action"]["owner"],
            "status": "Draft",
            "confidence": packet["confidence"],
        }
    )
    for assumption in packet["assumptions"]:
        store["assumption_register"].append({"assumption_id": f"ASM-{len(store['assumption_register']) + 1:03d}", "assumption": assumption, "status": "Open"})
    for action in packet["draft_next_steps"]["next_24h"]:
        store["action_ledger"].append({"action_id": f"ACT-{len(store['action_ledger']) + 1:03d}", "action": action, "status": "Draft"})
    store["audit_events"].append({"event": "packet_saved", "packet_id": packet_id, "date": date.today().isoformat()})
    target = Path(memory_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(store, indent=2, ensure_ascii=False), encoding="utf-8")
    return {
        "artifact": "Memory Store Update",
        "memory_path": str(target),
        "packet_id": packet_id,
        "store_counts": {key: len(value) for key, value in store.items() if isinstance(value, list)},
        "facts": packet["facts"],
        "assumptions": packet["assumptions"],
        "hypotheses": packet["hypotheses"],
        "missing_evidence": packet["missing_evidence"],
        "confidence": packet["confidence"],
        "recommended_action": packet["recommended_action"],
        "guardrails": GUARDRAILS,
    }


def evaluate_golden_examples(examples_dir: str | None = None) -> Dict[str, Any]:
    base = Path(examples_dir) if examples_dir else Path(__file__).resolve().parent / "examples"
    cases = [
        ("board_prep.json", "Board Prep", "decision_readiness", 35, 80),
        ("crisis.json", "Crisis Command", "board_risk", 50, 100),
        ("ai_governance.json", "AI Approval", "evidence_confidence", 35, 90),
        ("transformation_value.json", "Transformation Value", "value_leakage", 40, 100),
    ]
    results = []
    for file_name, expected_type, score_name, low, high in cases:
        data = json.loads((base / file_name).read_text(encoding="utf-8"))
        packet = build_decision_packet(data)
        score = packet["scorecard"][score_name]["value"]
        passed = packet["request_type"] == expected_type and low <= score <= high
        results.append(
            {
                "case": file_name,
                "passed": passed,
                "request_type": packet["request_type"],
                "expected_request_type": expected_type,
                "score_name": score_name,
                "score": score,
                "expected_range": [low, high],
            }
        )
    return {
        "artifact": "Golden Evaluation Report",
        "passed": all(item["passed"] for item in results),
        "results": results,
        "facts": [],
        "assumptions": [],
        "hypotheses": ["Evaluation uses deterministic local golden examples."],
        "missing_evidence": [],
        "confidence": "High",
        "recommended_action": {"recommendation": "Review failed cases and recalibrate scoring rules if needed.", "owner": "Plugin maintainer", "first_action": "Inspect evaluation results."},
        "guardrails": GUARDRAILS,
    }


def score_decision_readiness(input_context: Mapping[str, Any]) -> Dict[str, Any]:
    """Return only the scorecard and evidence summary."""
    ctx = _normalize_context(input_context)
    evidence = _classify_evidence(ctx)
    return {
        "artifact": "Decision Intelligence Scorecard",
        "scorecard": _scorecard(ctx, evidence),
        "facts": evidence["facts"],
        "assumptions": evidence["assumptions"],
        "hypotheses": evidence["hypotheses"],
        "missing_evidence": evidence["missing_evidence"],
        "confidence": _confidence(_scorecard(ctx, evidence)["evidence_confidence"]["value"]),
        "recommended_action": _recommended_action(ctx, _request_type(ctx), _scorecard(ctx, evidence)),
        "guardrails": GUARDRAILS,
    }


def map_risk_chain(input_context: Mapping[str, Any]) -> Dict[str, Any]:
    ctx = _normalize_context(input_context)
    evidence = _classify_evidence(ctx)
    scorecard = _scorecard(ctx, evidence)
    return {
        "artifact": "Risk Chain Map",
        "risk_chain": _risk_chain(ctx, evidence),
        "scorecard": {"board_risk": scorecard["board_risk"]},
        "facts": evidence["facts"],
        "assumptions": evidence["assumptions"],
        "hypotheses": evidence["hypotheses"],
        "missing_evidence": evidence["missing_evidence"],
        "confidence": _confidence(scorecard["evidence_confidence"]["value"]),
        "recommended_action": _recommended_action(ctx, _request_type(ctx), scorecard),
        "guardrails": GUARDRAILS,
    }


def extract_evidence_graph(input_context: Mapping[str, Any]) -> Dict[str, Any]:
    ctx = _normalize_context(input_context)
    evidence = _classify_evidence(ctx)
    scorecard = _scorecard(ctx, evidence)
    return {
        "artifact": "Evidence Graph",
        "evidence_graph": _evidence_graph(evidence),
        "semantic_model": _semantic_model(ctx, evidence),
        "facts": evidence["facts"],
        "assumptions": evidence["assumptions"],
        "hypotheses": evidence["hypotheses"],
        "missing_evidence": evidence["missing_evidence"],
        "confidence": _confidence(scorecard["evidence_confidence"]["value"]),
        "recommended_action": _recommended_action(ctx, _request_type(ctx), scorecard),
        "guardrails": GUARDRAILS,
    }


def compare_with_memory(
    input_context: Mapping[str, Any], memory_context: Mapping[str, Any] | None = None
) -> Dict[str, Any]:
    ctx = _normalize_context(input_context)
    memory = memory_context or {}
    evidence = _classify_evidence(ctx)
    repeated_debt = _memory_matches(_decision_debt(ctx), memory.get("decision_memory", []))
    stale_assumptions = _memory_matches(evidence["assumptions"], memory.get("assumption_register", []))
    overdue_actions = [
        item
        for item in memory.get("action_ledger", [])
        if str(item.get("status", "")).lower() not in {"done", "closed", "complete"}
        and str(item.get("due_date", "9999-12-31")) < date.today().isoformat()
    ]
    conflicting_claims = _memory_matches(_contradictions(ctx), memory.get("evidence_graph", []))
    scorecard = _scorecard(ctx, evidence)
    return {
        "artifact": "Memory Comparison",
        "stale_assumptions": stale_assumptions,
        "repeated_decision_debt": repeated_debt,
        "conflicting_claims": conflicting_claims,
        "overdue_actions": overdue_actions,
        "suggested_memory_updates": {
            "decision_memory": _decision_debt(ctx)[:3],
            "assumption_register": evidence["assumptions"][:5],
            "risk_chain_map": _risk_chain(ctx, evidence)[:3],
        },
        "decision_timeline": _decision_timeline(memory),
        "facts": evidence["facts"],
        "assumptions": evidence["assumptions"],
        "hypotheses": evidence["hypotheses"],
        "missing_evidence": evidence["missing_evidence"],
        "confidence": _confidence(scorecard["evidence_confidence"]["value"]),
        "recommended_action": _recommended_action(ctx, _request_type(ctx), scorecard),
        "guardrails": GUARDRAILS,
    }


def _normalize_context(input_context: Mapping[str, Any]) -> Dict[str, Any]:
    if not isinstance(input_context, Mapping):
        raise ValueError("input context must be a JSON object")
    items: List[str] = []
    for key in ("meeting_notes", "risk_register", "budget_update", "context", "signals"):
        value = input_context.get(key)
        if isinstance(value, str):
            items.extend(_lines(value))
        elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
            items.extend(str(x).strip() for x in value if str(x).strip())
    return {
        "title": str(input_context.get("title", "Untitled decision context")),
        "decision_request": str(input_context.get("decision_request", "")).strip(),
        "audience": str(input_context.get("audience", "Executive leadership")).strip(),
        "domains": [str(x).lower() for x in input_context.get("domains", [])],
        "items": items,
        "raw": dict(input_context),
    }


def _lines(text: str) -> List[str]:
    return [line.strip(" -\t") for line in text.splitlines() if line.strip(" -\t")]


def _classify_evidence(ctx: Mapping[str, Any]) -> Dict[str, List[str]]:
    facts: List[str] = []
    assumptions: List[str] = []
    hypotheses: List[str] = []
    missing: List[str] = []
    for item in ctx["items"]:
        low = item.lower()
        if "no " in low or "missing" in low or "incomplete" in low or "unknown" in low or "unclear" in low:
            facts.append(item)
            missing.append(_missing_for(item))
        elif any(term in low for term in ASSUMPTION_TERMS):
            assumptions.append(item)
        elif any(term in low for term in RISK_TERMS):
            facts.append(item)
        else:
            facts.append(item)
    if ctx["decision_request"]:
        hypotheses.append(f"Decision request may require trade-off: {ctx['decision_request']}")
    if not missing:
        missing.append("Source evidence, owner confirmation and decision deadline.")
    return {
        "facts": _unique(facts)[:12],
        "assumptions": _unique(assumptions)[:8],
        "hypotheses": _unique(hypotheses)[:8],
        "missing_evidence": _unique(missing)[:10],
    }


def _missing_for(item: str) -> str:
    low = item.lower()
    if "test" in low:
        return "Test plan, readiness date, defect trend and exit criteria."
    if "security" in low or "access" in low:
        return "Security impact assessment, owner sign-off and control evidence."
    if "budget" in low or "spend" in low or "forecast" in low or "reserve" in low:
        return "Updated forecast, recovery plan and funding decision options."
    if "root cause" in low or "eta" in low:
        return "Root-cause hypothesis, recovery ETA and customer impact list."
    if "data owner" in low or "baseline" in low:
        return "Data owner approval, data classification, evaluation plan and baseline metrics."
    return f"Validation evidence for: {item}"


def _scorecard(ctx: Mapping[str, Any], evidence: Mapping[str, List[str]]) -> Dict[str, Any]:
    items_text = " ".join(ctx["items"]).lower()
    risk_hits = _count_terms(items_text, RISK_TERMS)
    high_risk_hits = _count_terms(items_text, HIGH_RISK_TERMS)
    value_hits = _count_terms(items_text, VALUE_TERMS)
    missing_count = len(evidence["missing_evidence"])
    facts_count = len(evidence["facts"])
    assumptions_count = len(evidence["assumptions"])
    contradictions = len(_contradictions(ctx))
    debt = len(_decision_debt(ctx))

    evidence_conf = _bounded(70 + facts_count * 3 - missing_count * 5 - assumptions_count * 4 - contradictions * 8)
    decision_readiness = _bounded(
        65 + facts_count * 2 - missing_count * 6 - debt * 6 - contradictions * 7 - high_risk_hits * 2
    )
    board_risk = _bounded(25 + risk_hits * 8 + high_risk_hits * 7 + contradictions * 10 + missing_count * 3)
    value_leakage = _bounded(15 + value_hits * 9 + _count_terms(items_text, {"no adoption", "no baseline"}) * 15)
    autonomy = _bounded(75 - high_risk_hits * 8 - board_risk // 5 + (10 if decision_readiness > 70 else 0))

    return {
        "decision_readiness": Score(decision_readiness, _score_reasons(decision_readiness, "decision readiness")).to_dict(),
        "board_risk": Score(board_risk, _score_reasons(board_risk, "board risk")).to_dict(),
        "evidence_confidence": Score(evidence_conf, _score_reasons(evidence_conf, "evidence confidence")).to_dict(),
        "value_leakage": Score(value_leakage, _score_reasons(value_leakage, "value leakage")).to_dict(),
        "autonomy_readiness": Score(autonomy, _score_reasons(autonomy, "autonomy readiness")).to_dict(),
    }


def _score_reasons(value: int, label: str) -> List[str]:
    if label == "board risk":
        return ["Higher when high-impact, audit, security, customer or financial signals combine with missing evidence."]
    if label == "value leakage":
        return ["Higher when spend, budget, adoption or outcome gaps appear in the provided context."]
    if label == "autonomy readiness":
        return ["Lower when human approval, high-risk domains or low reversibility are present."]
    if value >= 70:
        return [f"{label.title()} is relatively strong based on provided context."]
    if value >= 40:
        return [f"{label.title()} is partial and needs targeted evidence before approval."]
    return [f"{label.title()} is weak because evidence gaps or unresolved decisions dominate."]


def _risk_chain(ctx: Mapping[str, Any], evidence: Mapping[str, List[str]]) -> List[Dict[str, str]]:
    chains = []
    facts = evidence["facts"] or ctx["items"]
    for item in facts[:5]:
        low = item.lower()
        dependency = "owner decision and evidence validation"
        impact = "executive decision risk"
        if "test" in low or "vendor" in low:
            dependency = "delivery readiness and vendor recovery"
            impact = "go-live, quality and board confidence risk"
        elif "security" in low or "access" in low:
            dependency = "security control owner sign-off"
            impact = "control, audit and risk acceptance exposure"
        elif "budget" in low or "spend" in low or "reserve" in low:
            dependency = "funding, forecast and benefit case"
            impact = "CFO challenge and value leakage risk"
        elif "outage" in low or "eta" in low or "customer" in low:
            dependency = "incident command, root cause and communication owner"
            impact = "customer impact and crisis escalation risk"
        chains.append(
            {
                "signal": item,
                "dependency": dependency,
                "amplifier": "missing evidence or constrained ownership",
                "business_impact": impact,
                "decision_pressure": "decide, defer, escalate or approve with conditions",
            }
        )
    return chains


def _evidence_graph(evidence: Mapping[str, List[str]]) -> Dict[str, Any]:
    nodes = []
    edges = []
    for idx, fact in enumerate(evidence["facts"], start=1):
        nodes.append({"id": f"F{idx}", "type": "fact", "label": fact, "confidence": "High"})
    for idx, assumption in enumerate(evidence["assumptions"], start=1):
        nodes.append({"id": f"A{idx}", "type": "assumption", "label": assumption, "confidence": "Low"})
        if evidence["facts"]:
            edges.append({"from": "F1", "to": f"A{idx}", "relationship": "weakens_or_requires_validation"})
    for idx, missing in enumerate(evidence["missing_evidence"], start=1):
        nodes.append({"id": f"M{idx}", "type": "missing_evidence", "label": missing, "confidence": "Unknown"})
    return {"nodes": nodes, "edges": edges}


def _semantic_model(ctx: Mapping[str, Any], evidence: Mapping[str, List[str]]) -> Dict[str, Any]:
    entities: List[Dict[str, str]] = []
    claims: List[Dict[str, str]] = []
    dependencies: List[Dict[str, str]] = []
    decisions: List[Dict[str, str]] = []
    for item in ctx["items"]:
        low = item.lower()
        for entity_type, keywords in DOMAIN_KEYWORDS.items():
            if any(keyword in low for keyword in keywords):
                entities.append({"type": entity_type, "label": _entity_label(item), "source": item})
        claim_type = "fact" if item in evidence["facts"] else "assumption" if item in evidence["assumptions"] else "claim"
        claims.append({"claim": item, "type": claim_type, "source": "provided_context"})
        if "depend" in low or "support" in low or "blocked" in low or "same two" in low:
            dependencies.append({"dependency": item, "criticality": "High" if any(t in low for t in RISK_TERMS) else "Medium"})
        if "decide" in low or "approve" in low or "not approved" in low or "owner" in low:
            decisions.append({"decision_signal": item, "status": "open_or_unresolved"})
    if ctx["decision_request"]:
        decisions.append({"decision_signal": ctx["decision_request"], "status": "explicit_request"})
    return {
        "entities": _dedupe_dicts(entities, "label")[:16],
        "claims": claims[:16],
        "dependencies": dependencies[:10],
        "decisions": decisions[:10],
    }


def _entity_label(item: str) -> str:
    words = [word.strip(".,:;()") for word in item.split()]
    candidates = [word for word in words if word[:1].isupper() or word.isupper() or any(char.isdigit() for char in word)]
    return " ".join(candidates[:4]) if candidates else item[:48]


def _guess_domain(text: str) -> str:
    low = text.lower()
    scores = {
        domain: sum(1 for keyword in keywords if keyword in low)
        for domain, keywords in DOMAIN_KEYWORDS.items()
    }
    best_domain, best_score = max(scores.items(), key=lambda item: item[1])
    return best_domain if best_score else "unknown"


def _detected_domains(ctx: Mapping[str, Any]) -> List[str]:
    text = " ".join(ctx["items"]).lower()
    domains = []
    domain_terms = {
        "industrial_it_ot": {"mes", "qms", "plm", "shopfloor", "production", "ot", "validated", "erp cutover"},
        "security": {"security", "access", "privileged", "ciso", "zero trust"},
        "finance": {"budget", "forecast", "reserve", "funding", "spend"},
        "vendor": {"vendor", "supplier", "contract", "license"},
        "audit_compliance": {"audit", "compliance", "control", "evidence", "regulator", "validation"},
        "delivery": {"project", "rollout", "milestone", "test", "go-live", "backlog"},
        "customer": {"customer", "order", "service", "sla", "trust"},
    }
    for domain, terms in domain_terms.items():
        if any(term in text for term in terms):
            domains.append(domain)
    return domains or ["general_enterprise"]


def _is_industrial_context(ctx: Mapping[str, Any]) -> bool:
    return "industrial_it_ot" in _detected_domains(ctx)


def _orchestrator_why(request_type: str, industrial: bool) -> str:
    base = {
        "Board Prep": "Board prep requires challenge questions, evidence quality and decision protection.",
        "Crisis Command": "Crisis context requires fact separation, risk propagation and governed action drafts.",
        "AI Approval": "AI approval requires value, control, ownership, risk and evidence readiness.",
        "Transformation Value": "Transformation review requires value leakage, decision debt and option clarity.",
    }.get(request_type, "Broad CIO context requires signal ranking, truth classification, risk chains and action governance.")
    if industrial:
        return base + " Industrial context adds IT/OT, production continuity and QMS audit evidence gates."
    return base


def _read_export_records(path: str) -> List[Dict[str, str]]:
    target = Path(path)
    if not target.exists():
        raise FileNotFoundError(f"connector export not found: {path}")
    suffix = target.suffix.lower()
    if suffix == ".csv":
        with target.open("r", encoding="utf-8-sig", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]
    if suffix == ".json":
        data = json.loads(target.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return [_flatten_record(item) for item in data if isinstance(item, Mapping)]
        if isinstance(data, Mapping):
            for key in ("records", "items", "signals", "events", "tickets", "messages", "documents"):
                value = data.get(key)
                if isinstance(value, list):
                    return [_flatten_record(item) for item in value if isinstance(item, Mapping)]
            return [_flatten_record(data)]
        raise ValueError("connector JSON export must be an object or array")
    if suffix in {".txt", ".md"}:
        return [{"summary": line} for line in _lines(target.read_text(encoding="utf-8"))]
    raise ValueError("supported connector exports: .csv, .json, .txt, .md")


def _flatten_record(record: Mapping[str, Any], prefix: str = "") -> Dict[str, str]:
    flat: Dict[str, str] = {}
    for key, value in record.items():
        name = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(value, Mapping):
            flat.update(_flatten_record(value, name))
        elif isinstance(value, list):
            flat[name] = "; ".join(json.dumps(item, ensure_ascii=False) if isinstance(item, Mapping) else str(item) for item in value)
        else:
            flat[name] = "" if value is None else str(value)
    return flat


def _first_value(row: Mapping[str, str], names: Sequence[str]) -> str:
    lowered = {key.lower(): value for key, value in row.items()}
    for name in names:
        if name.lower() in lowered and str(lowered[name.lower()]).strip():
            return str(lowered[name.lower()]).strip()
    for key, value in row.items():
        low = key.lower()
        if any(name.lower() in low for name in names) and str(value).strip():
            return str(value).strip()
    return ""


def _profile_summary(profile: str, row: Mapping[str, str]) -> str:
    if profile == "outlook_calendar":
        return _join_nonempty(
            [
                "Calendar meeting",
                _first_value(row, ["subject", "title"]),
                _first_value(row, ["agenda", "body", "description"]),
                _first_value(row, ["attendees", "participants"]),
            ]
        )
    if profile == "teams_messages":
        return _join_nonempty(
            [
                "Teams message",
                _first_value(row, ["channel", "chat", "team"]),
                _first_value(row, ["message", "summary", "body", "text"]),
                _first_value(row, ["participants", "sender", "from"]),
            ]
        )
    if profile == "outlook_email":
        return _join_nonempty(
            [
                "Outlook email",
                _first_value(row, ["subject", "conversation", "title"]),
                _first_value(row, ["body", "body_excerpt", "snippet", "summary", "message"]),
                _first_value(row, ["from", "sender"]),
                _first_value(row, ["to", "recipients", "cc"]),
            ]
        )
    if profile == "slack_messages":
        return _join_nonempty(
            [
                "Slack message",
                _first_value(row, ["channel", "channel_name"]),
                _first_value(row, ["text", "message", "summary"]),
                _first_value(row, ["user", "username", "sender"]),
                _first_value(row, ["thread_ts", "ts", "timestamp"]),
            ]
        )
    if profile == "gmail_workspace":
        return _join_nonempty(
            [
                "Gmail workspace email",
                _first_value(row, ["subject", "title"]),
                _first_value(row, ["snippet", "body", "message", "summary"]),
                _first_value(row, ["sender", "from"]),
                _first_value(row, ["recipients", "to", "cc"]),
            ]
        )
    if profile == "sharepoint_documents":
        return _join_nonempty(
            [
                "SharePoint document",
                _first_value(row, ["file_name", "name", "title", "path"]),
                _first_value(row, ["excerpt", "summary", "description"]),
                _first_value(row, ["owner", "modified_by"]),
            ]
        )
    if profile == "github_delivery":
        return _join_nonempty(
            [
                "GitHub delivery signal",
                _first_value(row, ["repository", "repo"]),
                _first_value(row, ["issue", "pull_request", "pr", "title"]),
                _first_value(row, ["status", "state", "summary"]),
            ]
        )
    if profile in {"jira_delivery", "azure_devops_delivery"}:
        return _join_nonempty(
            [
                "Delivery work item",
                _first_value(row, ["issue_key", "work_item_id", "id", "key"]),
                _first_value(row, ["issue_type", "work_item_type", "type"]),
                _first_value(row, ["status", "state", "resolution"]),
                _first_value(row, ["summary", "title", "description"]),
                _first_value(row, ["assignee", "assigned_to", "owner"]),
            ]
        )
    if profile == "topdesk_service":
        return _join_nonempty(
            [
                "TOPdesk service signal",
                _first_value(row, ["ticket_id", "number", "id"]),
                _first_value(row, ["service", "category"]),
                _first_value(row, ["priority", "status"]),
                _first_value(row, ["summary", "request", "briefDescription"]),
            ]
        )
    if profile == "servicenow_service":
        return _join_nonempty(
            [
                "ServiceNow service signal",
                _first_value(row, ["number", "sys_id", "id"]),
                _first_value(row, ["category", "assignment_group", "cmdb_ci"]),
                _first_value(row, ["priority", "state", "status"]),
                _first_value(row, ["short_description", "description", "summary"]),
            ]
        )
    if profile == "cmdb_assets":
        return _join_nonempty(
            [
                "CMDB asset signal",
                _first_value(row, ["asset_id", "ci_id", "id"]),
                _first_value(row, ["asset_name", "ci_name", "application", "service"]),
                _first_value(row, ["criticality", "lifecycle_status", "status"]),
                _first_value(row, ["owner", "business_owner", "technical_owner"]),
            ]
        )
    if profile == "cloud_cost":
        return _join_nonempty(
            [
                "Cloud cost signal",
                _first_value(row, ["provider", "account", "subscription"]),
                _first_value(row, ["service", "resource_group", "project"]),
                _first_value(row, ["cost", "actual", "spend"]),
                _first_value(row, ["forecast", "budget", "variance"]),
                _first_value(row, ["owner", "tag_owner", "cost_center"]),
            ]
        )
    if profile == "security_findings":
        return _join_nonempty(
            [
                "Security finding",
                _first_value(row, ["finding_id", "id", "cve"]),
                _first_value(row, ["severity", "risk", "priority"]),
                _first_value(row, ["asset", "system", "application"]),
                _first_value(row, ["summary", "description", "remediation"]),
                _first_value(row, ["owner", "assignee"]),
            ]
        )
    if profile == "observability_monitoring":
        return _join_nonempty(
            [
                "Observability signal",
                _first_value(row, ["service", "application", "system"]),
                _first_value(row, ["metric", "slo", "alert"]),
                _first_value(row, ["status", "severity", "state"]),
                _first_value(row, ["summary", "description"]),
                _first_value(row, ["owner", "team"]),
            ]
        )
    if profile == "erp_sap":
        return _join_nonempty(
            [
                "ERP/SAP signal",
                _first_value(row, ["module", "system"]),
                _first_value(row, ["process", "business_process"]),
                _first_value(row, ["status", "risk_status"]),
                _first_value(row, ["summary", "issue", "description"]),
                _first_value(row, ["owner", "process_owner"]),
            ]
        )
    if profile in {"confluence_knowledge", "google_drive_documents"}:
        return _join_nonempty(
            [
                "Knowledge document signal",
                _first_value(row, ["page_title", "file_name", "name", "title"]),
                _first_value(row, ["space", "folder", "drive", "library"]),
                _first_value(row, ["excerpt", "summary", "description"]),
                _first_value(row, ["owner", "modified_by"]),
            ]
        )
    if profile == "industrial_file_drop":
        return _join_nonempty(
            [
                "Industrial operating signal",
                _first_value(row, ["system", "application", "asset"]),
                _first_value(row, ["risk_status", "status", "severity"]),
                _first_value(row, ["summary", "risk", "issue", "description"]),
                _first_value(row, ["evidence_ref", "evidence", "owner"]),
            ]
        )
    return _join_nonempty([str(value) for value in row.values()])


def _profile_domain(profile: str, summary: str) -> str:
    if profile in {"topdesk_service", "outlook_calendar", "outlook_email", "teams_messages", "slack_messages", "gmail_workspace"}:
        return _guess_domain(summary)
    if profile == "github_delivery":
        return "delivery"
    if profile in {"jira_delivery", "azure_devops_delivery"}:
        return "delivery"
    if profile == "sharepoint_documents":
        return "control" if any(term in summary.lower() for term in ("audit", "policy", "control", "evidence")) else "unknown"
    if profile in {"confluence_knowledge", "google_drive_documents"}:
        return "control" if any(term in summary.lower() for term in ("audit", "policy", "control", "evidence")) else "unknown"
    if profile in {"servicenow_service", "observability_monitoring"}:
        return "operations"
    if profile == "cmdb_assets":
        return "architecture"
    if profile == "cloud_cost":
        return "finance"
    if profile == "security_findings":
        return "security"
    if profile == "erp_sap":
        return "business_operations"
    if profile == "industrial_file_drop":
        return "industrial_it_ot"
    return _guess_domain(summary)


def _profile_entities(row: Mapping[str, str], summary: str) -> List[str]:
    candidates = [
        _first_value(row, ["system", "application", "service", "repository", "file_name", "page_title", "ticket_id", "number", "issue_key", "work_item_id", "subject", "asset", "asset_name", "channel", "sender", "from"]),
        _entity_label(summary),
    ]
    return [item for item in _unique(candidates) if item][:8]


def _join_nonempty(items: Sequence[str]) -> str:
    return " | ".join(str(item).strip() for item in items if str(item).strip())


def _entity_refs(text: str) -> List[str]:
    refs = []
    for sentence in _lines(text):
        label = _entity_label(sentence)
        if label and label not in refs:
            refs.append(label)
    return refs[:8]


def _risk_graph(risk_chain: Sequence[Mapping[str, Any]], evidence: Mapping[str, List[str]]) -> Dict[str, Any]:
    nodes: Dict[str, Dict[str, Any]] = {}
    edges: List[Dict[str, Any]] = []
    for idx, path in enumerate(risk_chain, start=1):
        signal_id = f"S{idx}"
        dependency_id = f"D{idx}"
        impact_id = f"I{idx}"
        nodes[signal_id] = {"id": signal_id, "type": "signal", "label": path.get("signal", ""), "weight": 2}
        nodes[dependency_id] = {
            "id": dependency_id,
            "type": "dependency",
            "label": path.get("dependency", ""),
            "weight": 3,
        }
        nodes[impact_id] = {
            "id": impact_id,
            "type": "business_impact",
            "label": path.get("business_impact", ""),
            "weight": 3,
        }
        edges.append({"from": signal_id, "to": dependency_id, "type": "depends_on", "weight": 2})
        edges.append({"from": dependency_id, "to": impact_id, "type": "creates_risk_for", "weight": 3})
    for idx, missing in enumerate(evidence["missing_evidence"], start=1):
        missing_id = f"M{idx}"
        nodes[missing_id] = {"id": missing_id, "type": "missing_evidence", "label": missing, "weight": 2}
        if risk_chain:
            edges.append({"from": missing_id, "to": "D1", "type": "weakens_confidence", "weight": 2})
    centrality = _centrality(nodes, edges)
    propagation_paths = _propagation_paths(nodes, edges)
    return {
        "nodes": list(nodes.values()),
        "edges": edges,
        "centrality": centrality,
        "propagation_paths": propagation_paths,
    }


def _centrality(nodes: Mapping[str, Mapping[str, Any]], edges: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    counts = {node_id: 0 for node_id in nodes}
    for edge in edges:
        counts[str(edge["from"])] = counts.get(str(edge["from"]), 0) + int(edge.get("weight", 1))
        counts[str(edge["to"])] = counts.get(str(edge["to"]), 0) + int(edge.get("weight", 1))
    ranked = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return [
        {
            "node_id": node_id,
            "label": str(nodes[node_id].get("label", ""))[:96],
            "type": nodes[node_id].get("type", ""),
            "score": score,
        }
        for node_id, score in ranked[:8]
    ]


def _propagation_paths(nodes: Mapping[str, Mapping[str, Any]], edges: Sequence[Mapping[str, Any]]) -> List[List[str]]:
    adjacency: Dict[str, List[str]] = {}
    for edge in edges:
        adjacency.setdefault(str(edge["from"]), []).append(str(edge["to"]))
    paths: List[List[str]] = []
    for start in [node_id for node_id, node in nodes.items() if node.get("type") in {"signal", "missing_evidence"}]:
        stack = [(start, [start])]
        while stack:
            current, path = stack.pop()
            next_nodes = adjacency.get(current, [])
            if not next_nodes:
                paths.append([str(nodes[node].get("label", node)) for node in path])
            for nxt in next_nodes:
                if nxt not in path and len(path) < 5:
                    stack.append((nxt, path + [nxt]))
    return paths[:8]


def _graph_metrics(
    risk_chain: Sequence[Mapping[str, Any]], evidence_graph: Mapping[str, Any], risk_graph: Mapping[str, Any] | None = None
) -> Dict[str, Any]:
    dependency_counts: Dict[str, int] = {}
    domains = set()
    for path in risk_chain:
        dep = str(path.get("dependency", "unknown"))
        dependency_counts[dep] = dependency_counts.get(dep, 0) + 1
        impact = str(path.get("business_impact", "")).lower()
        for domain in ("project", "architecture", "security", "compliance", "finance", "operations", "customer", "vendor"):
            if domain in impact:
                domains.add(domain)
    central = sorted(dependency_counts.items(), key=lambda item: item[1], reverse=True)
    nodes = evidence_graph.get("nodes", [])
    edges = evidence_graph.get("edges", [])
    risk_nodes = risk_graph.get("nodes", []) if risk_graph else []
    risk_edges = risk_graph.get("edges", []) if risk_graph else []
    centrality = risk_graph.get("centrality", []) if risk_graph else []
    return {
        "node_count": len(nodes) + len(risk_nodes),
        "edge_count": len(edges) + len(risk_edges),
        "critical_dependency": centrality[0]["label"] if centrality else central[0][0] if central else "unknown",
        "blast_radius_domains": sorted(domains) if domains else ["executive decision"],
        "systemic_risk_level": "High" if len(domains) >= 3 or len(risk_chain) >= 5 else "Medium",
        "centrality_top": centrality[:3],
    }


def _scenario_simulation(ctx: Mapping[str, Any], request_type: str, scorecard: Mapping[str, Any]) -> List[Dict[str, Any]]:
    readiness = int(scorecard["decision_readiness"]["value"])
    board_risk = int(scorecard["board_risk"]["value"])
    value_leakage = int(scorecard["value_leakage"]["value"])
    return [
        {
            "scenario": "Approve now",
            "risk_delta": "+High" if board_risk >= 60 else "+Medium",
            "value_delta": "+Short-term momentum",
            "cost_of_waiting": "Low",
            "reversibility": "Low",
            "confidence_sensitivity": "Very sensitive to missing evidence",
            "decision_readiness_after": _bounded(readiness - 10),
        },
        {
            "scenario": "Defer",
            "risk_delta": "-Medium",
            "value_delta": "-Timeline momentum, +control confidence",
            "cost_of_waiting": "Medium to High" if value_leakage >= 50 else "Medium",
            "reversibility": "Medium",
            "confidence_sensitivity": "Improves if evidence gaps close",
            "decision_readiness_after": _bounded(readiness + 12),
        },
        {
            "scenario": "Approve with conditions",
            "risk_delta": "-Medium if gates are enforced",
            "value_delta": "+Momentum with control gates",
            "cost_of_waiting": "Medium",
            "reversibility": "Medium",
            "confidence_sensitivity": "Depends on named owners and gate date",
            "decision_readiness_after": _bounded(readiness + 8),
        },
    ]


def _board_personas(ctx: Mapping[str, Any], request_type: str) -> List[Dict[str, Any]]:
    text = " ".join(ctx["items"]).lower()
    personas = []
    for persona, lenses in PERSONA_LENSES.items():
        matched = [lens for lens in lenses if any(part in text for part in lens.split())]
        if not matched and persona in {"CEO", "CFO", "CISO", "Audit"}:
            matched = lenses[:2]
        if matched:
            personas.append(
                {
                    "persona": persona,
                    "lens": matched,
                    "question": _persona_question(persona, matched),
                    "weak_answer_risk": "High" if persona in {"CFO", "CISO", "Audit"} else "Medium",
                }
            )
    return personas


def _persona_question(persona: str, lenses: Sequence[str]) -> str:
    topic = ", ".join(lenses[:2])
    return f"{persona}: What evidence supports the decision on {topic}?"


def _audit_trail(
    ctx: Mapping[str, Any],
    evidence: Mapping[str, List[str]],
    scorecard: Mapping[str, Any],
    risk_chain: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    drivers = {
        "facts_count": len(evidence["facts"]),
        "assumptions_count": len(evidence["assumptions"]),
        "missing_evidence_count": len(evidence["missing_evidence"]),
        "risk_chain_paths": len(risk_chain),
        "domains": ctx["domains"],
    }
    return {
        "source_scope": "provided JSON context only",
        "score_drivers": drivers,
        "score_explanations": {key: value["reasons"] for key, value in scorecard.items()},
        "recommendation_drivers": [
            "decision readiness score",
            "board risk score",
            "missing evidence",
            "risk chain path count",
        ],
        "changed_since_last_packet": _change_summary(ctx),
        "export_note": "This audit trail is safe to copy into review materials; it contains no secrets or live connector claims.",
    }


def _operating_rhythm(ctx: Mapping[str, Any], request_type: str, scorecard: Mapping[str, Any]) -> Dict[str, Any]:
    board_risk = int(scorecard["board_risk"]["value"])
    readiness = int(scorecard["decision_readiness"]["value"])
    daily_focus = "evidence closure and executive signal scan" if board_risk >= 60 else "monitor decision readiness"
    weekly_focus = "decision debt review and owner accountability" if readiness < 70 else "decision outcome review"
    if request_type == "Crisis Command":
        cadence = "1h / 4h / 24h / 7d crisis rhythm"
    elif request_type == "AI Approval":
        cadence = "AI approval gate review"
    elif request_type == "Board Prep":
        cadence = "board-prep countdown"
    else:
        cadence = "daily / weekly / monthly CIO operating rhythm"
    return {
        "cadence": cadence,
        "daily_signal_scan": daily_focus,
        "weekly_decision_debt_review": weekly_focus,
        "monthly_operating_review": "trend score changes, value leakage, overdue actions and stale assumptions",
        "board_prep_countdown": ["T-14 evidence map", "T-7 decision gates", "T-2 board pressure simulation", "T+1 decision memory update"],
        "crisis_war_room": ["1h facts and unknowns", "4h containment options", "24h stakeholder update", "7d lessons and controls"],
        "ai_approval_gate": ["value hypothesis", "data owner", "control evidence", "evaluation baseline", "human review"],
    }


def _decision_quality_benchmark(
    ctx: Mapping[str, Any], evidence: Mapping[str, List[str]], scorecard: Mapping[str, Any]
) -> Dict[str, Any]:
    total_claims = max(1, len(ctx["items"]))
    missing_rate = round(len(evidence["missing_evidence"]) / total_claims, 2)
    assumption_rate = round(len(evidence["assumptions"]) / total_claims, 2)
    question_coverage = len(_board_personas(ctx, _request_type(ctx)))
    return {
        "raw_input_quality": _bounded(50 + len(evidence["facts"]) * 4 - len(evidence["missing_evidence"]) * 8),
        "missing_evidence_rate": missing_rate,
        "assumption_rate": assumption_rate,
        "board_question_coverage": question_coverage,
        "decision_readiness": scorecard["decision_readiness"]["value"],
        "before_after": {
            "before": "raw fragmented context with implicit claims and unclear decision gates",
            "after": "structured decision packet with evidence classes, risk chain, scenarios, personas and action drafts",
        },
        "benchmark_note": "Directional local benchmark; compare across repeated packets for trend, not final performance measurement.",
    }


def _change_summary(ctx: Mapping[str, Any]) -> str:
    raw = ctx.get("raw", {})
    prior = raw.get("prior_packet")
    if not isinstance(prior, Mapping):
        return "Not evaluated unless prior packet or memory context is provided."
    previous_decision = str(prior.get("decision_needed", ""))
    current_decision = str(ctx.get("decision_request", ""))
    if previous_decision and current_decision and previous_decision != current_decision:
        return "Decision request changed since prior packet."
    return "No material decision-request change detected from provided prior packet."


def _trend_delta(ctx: Mapping[str, Any], scorecard: Mapping[str, Any]) -> Dict[str, Any]:
    prior = ctx.get("raw", {}).get("prior_packet")
    current_scores = {key: value["value"] for key, value in scorecard.items()}
    if not isinstance(prior, Mapping):
        return {
            "available": False,
            "summary": "No prior packet provided.",
            "score_delta": {},
            "new_risks": [],
            "resolved_risks": [],
        }
    prior_scores = prior.get("scorecard", {})
    normalized_prior = {
        key: int(value.get("value", value)) for key, value in prior_scores.items() if isinstance(value, (Mapping, int))
    }
    score_delta = {key: current_scores[key] - normalized_prior.get(key, current_scores[key]) for key in current_scores}
    current_risks = set(_weak_signals(ctx))
    prior_risks = set(str(item) for item in prior.get("weak_signals", []))
    return {
        "available": True,
        "summary": "Score and risk deltas were computed from provided prior packet.",
        "score_delta": score_delta,
        "new_risks": sorted(current_risks - prior_risks),
        "resolved_risks": sorted(prior_risks - current_risks),
    }


def _source_summary(signals: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    by_source: Dict[str, int] = {}
    by_domain: Dict[str, int] = {}
    for signal in signals:
        source = str(signal.get("source_type", "unknown"))
        domain = str(signal.get("domain", "unknown"))
        by_source[source] = by_source.get(source, 0) + 1
        by_domain[domain] = by_domain.get(domain, 0) + 1
    return {"signal_count": len(signals), "by_source": by_source, "by_domain": by_domain}


def _llm_extraction_layer(ctx: Mapping[str, Any], evidence: Mapping[str, List[str]]) -> Dict[str, Any]:
    provided = ctx.get("raw", {}).get("llm_extraction")
    if isinstance(provided, Mapping):
        return {
            "mode": "provided_llm_output",
            "used": True,
            "extraction": dict(provided),
            "fallback_available": True,
            "confidence": "User-provided",
        }
    return {
        "mode": "heuristic_fallback",
        "used": False,
        "extraction": {
            "facts": evidence["facts"],
            "assumptions": evidence["assumptions"],
            "hypotheses": evidence["hypotheses"],
            "missing_evidence": evidence["missing_evidence"],
        },
        "fallback_available": True,
        "confidence": "Medium",
        "note": "Standalone engine mode uses local heuristics. In Codex plugin usage, the host LLM can populate llm_extraction and the engine will use that structured layer.",
    }


def _entity_resolution(ctx: Mapping[str, Any]) -> Dict[str, Any]:
    aliases: Dict[str, List[str]] = {}
    for item in ctx["items"]:
        low = item.lower()
        if "erp" in low:
            aliases.setdefault("ERP Modernization", []).append(item)
        if "iam" in low or "privileged access" in low:
            aliases.setdefault("Identity and Access Remediation", []).append(item)
        if "cloud" in low:
            aliases.setdefault("Cloud Migration", []).append(item)
        if "vendor" in low:
            aliases.setdefault("Vendor Delivery", []).append(item)
        if "audit" in low or "change-control" in low:
            aliases.setdefault("Audit Evidence", []).append(item)
    return {
        "resolved_entities": [
            {"canonical": canonical, "aliases_or_mentions": _unique(mentions), "mention_count": len(mentions)}
            for canonical, mentions in aliases.items()
        ],
        "merge_policy": "case-insensitive keyword and acronym matching; no external entity store",
    }


def _causal_decision_graph(risk_chain: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    paths = []
    for item in risk_chain:
        paths.append(
            {
                "cause": item.get("signal", ""),
                "mechanism": item.get("dependency", ""),
                "intermediate_effect": item.get("amplifier", ""),
                "outcome": item.get("business_impact", ""),
                "decision_pressure": item.get("decision_pressure", ""),
            }
        )
    return {"causal_paths": paths, "counterfactual_ready": True}


def _counterfactual_simulation(ctx: Mapping[str, Any], scorecard: Mapping[str, Any]) -> List[Dict[str, Any]]:
    readiness = int(scorecard["decision_readiness"]["value"])
    board_risk = int(scorecard["board_risk"]["value"])
    return [
        {
            "intervention": "Add two critical experts or architects",
            "expected_effect": "Reduces dependency bottleneck and improves delivery confidence",
            "decision_readiness_delta": 8,
            "board_risk_delta": -6,
            "new_readiness": _bounded(readiness + 8),
            "new_board_risk": _bounded(board_risk - 6),
        },
        {
            "intervention": "Defer go-live or approval gate",
            "expected_effect": "Increases evidence quality but may increase cost of waiting",
            "decision_readiness_delta": 12,
            "board_risk_delta": -10,
            "new_readiness": _bounded(readiness + 12),
            "new_board_risk": _bounded(board_risk - 10),
        },
        {
            "intervention": "Reduce vendor scope and force recovery plan",
            "expected_effect": "Narrows delivery risk and creates clearer accountability",
            "decision_readiness_delta": 6,
            "board_risk_delta": -5,
            "new_readiness": _bounded(readiness + 6),
            "new_board_risk": _bounded(board_risk - 5),
        },
    ]


def _decision_twin(
    ctx: Mapping[str, Any], request_type: str, evidence: Mapping[str, List[str]], scorecard: Mapping[str, Any]
) -> Dict[str, Any]:
    return {
        "decision": _decision_needed(ctx, request_type),
        "owner": "Executive sponsor with relevant domain owners",
        "current_health": _quality_grade(scorecard, evidence, ctx)["grade"],
        "assumptions": evidence["assumptions"],
        "evidence": evidence["facts"],
        "options": [item["option"] for item in _options(ctx, request_type)],
        "consequences": [item["business_impact"] for item in _risk_chain(ctx, evidence)[:5]],
        "next_review_date": "Set by user; recommended within 7 days for material decisions.",
    }


def _board_question_coverage(ctx: Mapping[str, Any], request_type: str) -> Dict[str, Any]:
    personas = _board_personas(ctx, request_type)
    covered = {item["persona"] for item in personas}
    required = ["CEO", "CFO", "CISO", "Audit", "Regulator", "Customer"]
    missing = [persona for persona in required if persona not in covered]
    score = _bounded(round(len(covered) / len(required) * 100))
    return {
        "score": score,
        "covered_personas": sorted(covered),
        "missing_personas": missing,
        "weak_answer_risk": "High" if score < 70 else "Medium" if score < 90 else "Low",
    }


def _narrative_risks(ctx: Mapping[str, Any]) -> List[Dict[str, str]]:
    risky_phrases = {
        "broadly on track": "Could mask contradictory delivery evidence.",
        "no expected impact": "Requires evidence for schedule, customer, audit and control impact.",
        "manageable risk": "Requires owner, mitigation, trigger and residual risk statement.",
        "temporary workaround": "Requires expiry date and control acceptance.",
        "under control": "Requires evidence and decision-owner sign-off.",
    }
    findings = []
    text = " ".join(ctx["items"]).lower()
    for phrase, challenge in risky_phrases.items():
        if phrase in text:
            findings.append({"phrase": phrase, "challenge": challenge, "question": f"What evidence supports '{phrase}'?"})
    return findings


def _decision_anti_patterns(ctx: Mapping[str, Any], evidence: Mapping[str, List[str]]) -> List[Dict[str, str]]:
    text = " ".join(ctx["items"]).lower()
    patterns = []
    if "approve" in text and evidence["missing_evidence"]:
        patterns.append({"pattern": "approval without evidence", "risk": "Decision may be approved before required facts are available."})
    if "target" in text or "go-live" in text:
        patterns.append({"pattern": "date-driven delivery", "risk": "Timeline may dominate quality, control or value evidence."})
    if "no additional" in text or "unfunded" in text:
        patterns.append({"pattern": "unfunded dependency", "risk": "Dependency is required but not resourced."})
    if "owner" in text and ("no " in text or "unclear" in text):
        patterns.append({"pattern": "ownerless risk", "risk": "Accountability is unclear or missing."})
    if "activity" in text and ("no adoption" in text or "no metrics" in text):
        patterns.append({"pattern": "activity without outcome", "risk": "Work may continue without measurable value."})
    if "gap" in text or "incomplete" in text:
        patterns.append({"pattern": "control gap normalization", "risk": "Known control issues may become accepted background risk."})
    return patterns


def _red_team_blue_team(ctx: Mapping[str, Any], request_type: str, evidence: Mapping[str, List[str]]) -> Dict[str, Any]:
    red = [
        "The proposal depends on missing evidence or optimistic assumptions.",
        "The decision may transfer unresolved risk to the board or steering committee.",
        "Owners and evidence gates may be too weak for approval.",
    ]
    blue = [
        "Convert approval into conditional approval with explicit evidence gates.",
        "Name owners and review dates for each missing evidence item.",
        "Document residual risk and escalation criteria before approval.",
    ]
    if request_type == "AI Approval":
        red.append("The value claim may be unvalidated and data ownership may be unresolved.")
        blue.append("Require data-owner sign-off, baseline metrics and human review before pilot approval.")
    return {"red_team": red, "blue_team": blue}


def _executive_attention_budget(
    ctx: Mapping[str, Any], evidence: Mapping[str, List[str]], scorecard: Mapping[str, Any]
) -> Dict[str, Any]:
    items = _weak_signals(ctx) + _decision_debt(ctx) + evidence["missing_evidence"]
    unique = _unique(items)
    return {
        "top_5": unique[:5],
        "delegate": unique[5:10],
        "monitor": [item for item in ctx["items"] if item not in unique][:10],
        "attention_note": "Top items are selected by risk keywords, decision debt and missing evidence.",
    }


def _decision_latency_tracker(ctx: Mapping[str, Any]) -> Dict[str, Any]:
    raw = ctx.get("raw", {})
    opened = raw.get("decision_opened_on") or raw.get("opened_on")
    today = date.today().isoformat()
    days_open = None
    if isinstance(opened, str) and re.match(r"\d{4}-\d{2}-\d{2}", opened):
        try:
            days_open = (date.fromisoformat(today) - date.fromisoformat(opened[:10])).days
        except ValueError:
            days_open = None
    return {
        "opened_on": opened or "not provided",
        "as_of": today,
        "days_open": days_open,
        "latency_risk": "High" if days_open is not None and days_open > 30 else "Medium" if days_open is not None and days_open > 7 else "Unknown" if days_open is None else "Low",
        "drift_note": "Risk and cost drift should be reviewed for decisions open longer than one review cycle.",
    }


def _value_at_risk(ctx: Mapping[str, Any], scorecard: Mapping[str, Any]) -> Dict[str, Any]:
    text = " ".join(ctx["items"]).lower()
    exposures = []
    if "spend" in text or "budget" in text or "reserve" in text:
        exposures.append("financial exposure")
    if "audit" in text or "control" in text:
        exposures.append("audit/control exposure")
    if "customer" in text or "outage" in text:
        exposures.append("customer impact exposure")
    if "security" in text or "access" in text:
        exposures.append("security residual risk")
    risk = int(scorecard["board_risk"]["value"])
    band = "High" if risk >= 70 else "Medium" if risk >= 45 else "Low"
    return {
        "value_at_risk_band": band,
        "exposures": exposures or ["execution credibility"],
        "semiquantitative_note": "Directional estimate only; attach finance, customer or audit data for numeric exposure.",
    }


def _governance_control_map(ctx: Mapping[str, Any]) -> List[Dict[str, str]]:
    text = " ".join(ctx["items"]).lower()
    controls = []
    if "data" in text or "llm" in text or "ai" in text:
        controls.append({"control": "Data owner approval", "required_for": "AI/data use case", "status": "Required"})
    if "security" in text or "access" in text:
        controls.append({"control": "CISO sign-off", "required_for": "security/control risk", "status": "Required"})
    if "audit" in text or "change-control" in text:
        controls.append({"control": "Audit evidence checklist", "required_for": "control readiness", "status": "Required"})
    if "budget" in text or "spend" in text or "reserve" in text:
        controls.append({"control": "CFO funding gate", "required_for": "financial exposure", "status": "Required"})
    if "architecture" in text or "integration" in text:
        controls.append({"control": "Architecture waiver or review", "required_for": "technology dependency", "status": "Required"})
    return controls


def _meeting_to_decision_diff(ctx: Mapping[str, Any]) -> Dict[str, Any]:
    meeting = ctx.get("raw", {}).get("meeting_notes", [])
    final = ctx.get("raw", {}).get("final_decision", "")
    if not final:
        return {"available": False, "ignored_risks": [], "missing_actions": [], "narrative_drops": []}
    meeting_lines = meeting if isinstance(meeting, Sequence) and not isinstance(meeting, str) else _lines(str(meeting))
    final_text = str(final).lower()
    ignored = [line for line in meeting_lines if any(term in line.lower() for term in RISK_TERMS) and line.lower() not in final_text]
    actions = [line for line in meeting_lines if "action" in line.lower() or "owner" in line.lower()]
    missing_actions = [line for line in actions if line.lower() not in final_text]
    return {
        "available": True,
        "ignored_risks": ignored[:8],
        "missing_actions": missing_actions[:8],
        "narrative_drops": ignored[:5],
    }


def _quality_grade(scorecard: Mapping[str, Any], evidence: Mapping[str, List[str]], ctx: Mapping[str, Any]) -> Dict[str, Any]:
    readiness = int(scorecard["decision_readiness"]["value"])
    confidence = int(scorecard["evidence_confidence"]["value"])
    board_risk = int(scorecard["board_risk"]["value"])
    penalty = len(evidence["missing_evidence"]) * 3 + len(_decision_anti_patterns(ctx, evidence)) * 5
    score = _bounded((readiness + confidence + (100 - board_risk)) // 3 - penalty)
    if score >= 85:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 55:
        grade = "C"
    elif score >= 40:
        grade = "D"
    else:
        grade = "F"
    return {
        "grade": grade,
        "score": score,
        "board_ready": score >= 70,
        "audit_ready": confidence >= 70 and not evidence["missing_evidence"],
        "action_ready": readiness >= 70,
        "improvement_actions": evidence["missing_evidence"][:5] or ["Maintain evidence trail and owner sign-off."],
    }


def _executive_decision_assurance(
    ctx: Mapping[str, Any],
    evidence: Mapping[str, List[str]],
    scorecard: Mapping[str, Any],
    risk_chain: Sequence[Mapping[str, Any]],
    evidence_graph: Mapping[str, Any],
) -> Dict[str, Any]:
    quality = _quality_grade(scorecard, evidence, ctx)
    return {
        "assurance_level": "Strong" if quality["grade"] in {"A", "B"} else "Developing" if quality["grade"] == "C" else "Weak",
        "quality_grade": quality,
        "anti_pattern_count": len(_decision_anti_patterns(ctx, evidence)),
        "narrative_risk_count": len(_narrative_risks(ctx)),
        "control_count": len(_governance_control_map(ctx)),
        "risk_path_count": len(risk_chain),
        "evidence_node_count": len(evidence_graph.get("nodes", [])),
    }


def _action_risk(action: str, scorecard: Mapping[str, Any]) -> str:
    board_risk = int(scorecard["board_risk"]["value"])
    autonomy = int(scorecard["autonomy_readiness"]["value"])
    if board_risk >= 70 or autonomy < 45:
        return "High"
    if board_risk >= 45 or autonomy < 70:
        return "Medium"
    return "Low"


def _autonomy_level(action: str, risk_level: str, request_type: str) -> str:
    text = f"{action} {request_type}".lower()
    if any(term in text for term in {"legal", "regulator", "privacy", "breach", "security", "audit", "financial", "hr"}):
        return "L4 Human-Only"
    if risk_level == "High":
        return "L4 Human-Only"
    if risk_level == "Medium":
        return "L2 Draft"
    if "confirm" in text or "request" in text or "draft" in text:
        return "L3 Ready for Governed Execution"
    return "L1 Advise"


def _action_reversibility(action: str, risk_level: str) -> str:
    text = action.lower()
    if risk_level == "High" or "approve" in text or "execute" in text:
        return "Low"
    if "draft" in text or "request" in text or "confirm" in text:
        return "High"
    return "Medium"


def _cannot_automate_reasons(action: str, risk_level: str, request_type: str, autonomy_level: str) -> List[str]:
    reasons = []
    text = f"{action} {request_type}".lower()
    if autonomy_level == "L4 Human-Only":
        reasons.append("human accountable decision required")
    if any(term in text for term in {"security", "audit", "compliance", "privacy", "legal", "financial", "breach"}):
        reasons.append("regulated or high-risk domain")
    if risk_level != "Low":
        reasons.append("approval gate required before external execution")
    if not reasons and autonomy_level != "L3 Ready for Governed Execution":
        reasons.append("advisory action only in current connector-neutral version")
    return reasons


def _autonomy_gate(actions: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    levels: Dict[str, int] = {}
    for action in actions:
        level = str(action.get("autonomy_level", "L1 Advise"))
        levels[level] = levels.get(level, 0) + 1
    highest = "L4 Human-Only" if levels.get("L4 Human-Only") else "L3 Ready for Governed Execution" if levels.get("L3 Ready for Governed Execution") else "L2 Draft"
    return {
        "highest_required_level": highest,
        "level_counts": levels,
        "external_execution_allowed": False,
        "policy": "Draft and prepare only. External execution requires future connector tools plus explicit user approval.",
    }


def _action_ledger(actions: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    return [
        {
            "action_id": action.get("action_id"),
            "draft_action": action.get("draft_action"),
            "status": "drafted_not_executed",
            "autonomy_level": action.get("autonomy_level"),
            "required_approval": action.get("required_approval"),
            "risk_level": action.get("risk_level"),
            "reversibility": action.get("reversibility"),
        }
        for action in actions
    ]


def _autonomous_attention_allocation(packet: Mapping[str, Any]) -> Dict[str, List[str]]:
    budget = packet.get("executive_attention_budget", {})
    top = list(budget.get("top_5", []))
    delegate = list(budget.get("delegate", []))
    monitor = list(budget.get("monitor", []))
    decisions = list(packet.get("decision_debt", []))[:5]
    escalations = [item for item in top if any(term in str(item).lower() for term in {"red", "missing", "incomplete", "security", "audit", "outage"})]
    return {
        "act_now": escalations[:3],
        "escalate": escalations[3:] + decisions[:2],
        "decide": decisions[2:5],
        "delegate": delegate[:5],
        "monitor": monitor[:8],
        "ignore": ["Low-impact updates without decision, risk or evidence implications."],
    }


def _enterprise_status(packet: Mapping[str, Any]) -> Dict[str, Any]:
    scores = packet.get("scorecard", {})
    board_risk = int(scores.get("board_risk", {}).get("value", 0))
    readiness = int(scores.get("decision_readiness", {}).get("value", 0))
    confidence = int(scores.get("evidence_confidence", {}).get("value", 0))
    status = "Red" if board_risk >= 70 or readiness < 45 else "Amber" if board_risk >= 45 or confidence < 65 else "Green"
    return {
        "overall": status,
        "decision_readiness": readiness,
        "board_risk": board_risk,
        "evidence_confidence": confidence,
        "reason": "Status is derived from decision readiness, board risk and evidence confidence.",
    }


def _cio_replacement_surface(packet: Mapping[str, Any], actions: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    return {
        "automated_or_deterministic": [
            "score decision readiness",
            "build evidence graph",
            "map risk chain",
            "generate operating rhythm",
            "scan privacy indicators",
        ],
        "drafted_by_plugin": [
            "executive briefing",
            "board challenge questions",
            "action ledger",
            "decision memory update",
            "approval and escalation drafts",
        ],
        "decision_supported": [
            "approve, defer or conditionally approve",
            "risk acceptance",
            "budget or capacity trade-off",
            "AI governance approval",
        ],
        "human_only": [
            "final accountability",
            "regulated approval",
            "external execution",
            "irreversible financial, legal, HR or security decisions",
        ],
        "autonomy_distribution": _autonomy_gate(actions)["level_counts"],
        "replacement_note": "The plugin replaces preparation, triage and drafting work; human leaders retain final accountability.",
        "request_type": packet.get("request_type"),
    }


def _disruptive_usp_layer(
    packet: Mapping[str, Any],
    actions: Sequence[Mapping[str, Any]],
    memory: Mapping[str, Any],
) -> Dict[str, Any]:
    debt = _decision_debt_ledger(packet, memory)
    truth_gaps = _truth_gap_detector(packet)
    return {
        "cio_work_autonomy_map": _cio_work_autonomy_map(packet, actions),
        "board_objection_simulator": _board_objection_simulator(packet),
        "decision_debt_ledger": debt,
        "truth_gap_detector": truth_gaps,
        "executive_time_saved_estimate": _executive_time_saved_estimate(packet, actions),
        "cio_shadow_agenda": _cio_shadow_agenda(packet, debt, truth_gaps),
        "autonomous_steering_pack_factory": _autonomous_steering_pack_factory(packet),
        "risk_chain_forecast": _risk_chain_forecast(packet),
        "strategic_drift_detector": _strategic_drift_detector(packet),
        "human_control_contract": _human_control_contract(actions),
        "decision_sla_enforcer": _decision_sla_enforcer(packet, debt),
        "vendor_exit_simulator": _vendor_exit_simulator(packet),
        "regulatory_shock_simulator": _regulatory_shock_simulator(packet),
        "cyber_business_impact_translator": _cyber_business_impact_translator(packet),
        "talent_criticality_radar": _talent_criticality_radar(packet),
        "capital_allocation_copilot": _capital_allocation_copilot(packet),
        "post_decision_learning_loop": _post_decision_learning_loop(packet, memory),
        "cio_os_maturity_index": _cio_os_maturity_index(packet, actions, truth_gaps, debt),
        "stakeholder_alignment_matrix": _stakeholder_alignment_matrix(packet),
        "exception_waiver_factory": _exception_waiver_factory(packet, actions),
        "policy_as_code_readiness": _policy_as_code_readiness(packet),
        "benefits_realization_sentinel": _benefits_realization_sentinel(packet),
        "operating_rhythm_autopilot": _operating_rhythm_autopilot(packet, debt, truth_gaps),
        "autonomous_escalation_drafts": _autonomous_escalation_drafts(packet, actions),
        "executive_decision_backlog": _executive_decision_backlog(packet, debt),
        "enterprise_control_tower": _enterprise_control_tower(packet, truth_gaps, debt),
        "ma_carveout_readiness": _ma_carveout_readiness(packet),
        "data_trust_radar": _data_trust_radar(packet),
        "architecture_runway_guardian": _architecture_runway_guardian(packet),
        "executive_narrative_generator": _executive_narrative_generator(packet),
        "autonomous_due_diligence_questions": _autonomous_due_diligence_questions(packet),
        "resilience_continuity_planner": _resilience_continuity_planner(packet),
        "customer_trust_impact_radar": _customer_trust_impact_radar(packet),
        "ai_portfolio_governance": _ai_portfolio_governance(packet),
        "cost_of_delay_calculator": _cost_of_delay_calculator(packet),
        "executive_commitment_tracker": _executive_commitment_tracker(packet, memory),
        "decision_rights_mapper": _decision_rights_mapper(packet),
        "okr_strategy_fit_checker": _okr_strategy_fit_checker(packet),
        "risk_acceptance_docket": _risk_acceptance_docket(packet),
        "service_health_sentinel": _service_health_sentinel(packet),
        "knowledge_continuity_planner": _knowledge_continuity_planner(packet),
        "dependency_breakpoint_analyzer": _dependency_breakpoint_analyzer(packet),
        "transformation_kill_criteria": _transformation_kill_criteria(packet),
        "vendor_negotiation_brief": _vendor_negotiation_brief(packet),
        "compliance_evidence_pack": _compliance_evidence_pack(packet),
        "board_decision_simulator": _board_decision_simulator(packet),
        "operating_risk_heatmap": _operating_risk_heatmap(packet),
        "autonomous_roadmap_reprioritizer": _autonomous_roadmap_reprioritizer(packet),
        "audit_finding_predictor": _audit_finding_predictor(packet),
        "platform_rationalization_advisor": _platform_rationalization_advisor(packet),
        "data_sovereignty_radar": _data_sovereignty_radar(packet),
        "operating_model_debt_ledger": _operating_model_debt_ledger(packet),
        "strategic_option_portfolio": _strategic_option_portfolio(packet),
        "executive_decision_war_room": _executive_decision_war_room(packet),
        "evidence_chain_of_custody": _evidence_chain_of_custody(packet),
        "decision_rollback_planner": _decision_rollback_planner(packet),
        "autonomy_risk_budget": _autonomy_risk_budget(packet, actions),
        "approval_boundary_mapper": _approval_boundary_mapper(packet, actions),
        "evidence_expiry_monitor": _evidence_expiry_monitor(packet),
        "residual_risk_contract": _residual_risk_contract(packet),
        "autonomy_stress_test": _autonomy_stress_test(packet, actions),
        "decision_consequence_ledger": _decision_consequence_ledger(packet),
        "enterprise_friction_map": _enterprise_friction_map(packet),
        "strategic_optionality_engine": _strategic_optionality_engine(packet),
        "control_debt_burndown": _control_debt_burndown(packet),
        "executive_dissent_synthesizer": _executive_dissent_synthesizer(packet),
        "decision_backtest_simulator": _decision_backtest_simulator(packet, memory),
        "governance_drift_detector": _governance_drift_detector(packet, memory),
        "budget_shock_absorber": _budget_shock_absorber(packet),
        "vendor_leverage_index": _vendor_leverage_index(packet),
        "executive_narrative_diff": _executive_narrative_diff(packet, memory),
    }


def _executive_decision_defense(
    packet: Mapping[str, Any],
    memory: Mapping[str, Any],
    actions: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    liability = _decision_liability_shield(packet, actions)
    blind_spots = _executive_blind_spot_radar(packet)
    commitment = _commitment_integrity_score(packet)
    narrative = _board_narrative_stress_test(packet)
    memory_diff = _autonomous_decision_memory_diff(packet, memory)
    firewall = _value_realization_firewall(packet)
    risk_cash = _risk_to_cash_translator(packet)
    sla = _decision_sla_monitor(packet, memory)
    controls = _control_evidence_readiness(packet)
    attention = _executive_attention_allocator(packet)
    kill_switch = _scenario_kill_switch(packet)
    cio_loop = _cio_operating_system_loop(packet, memory, attention)
    defense_score = _bounded(
        (100 - liability["liability_score"])
        + commitment["score"]
        + controls["readiness_score"]
        + (100 - len(blind_spots["blind_spots"]) * 8)
    ) // 4
    return {
        "defense_score": defense_score,
        "defense_posture": "Board-ready" if defense_score >= 75 else "Defensible with gates" if defense_score >= 55 else "Exposed",
        "decision_liability_shield": liability,
        "executive_blind_spot_radar": blind_spots,
        "commitment_integrity_score": commitment,
        "board_narrative_stress_test": narrative,
        "autonomous_decision_memory_diff": memory_diff,
        "value_realization_firewall": firewall,
        "risk_to_cash_translator": risk_cash,
        "decision_sla_monitor": sla,
        "control_evidence_readiness": controls,
        "executive_attention_allocator": attention,
        "scenario_kill_switch": kill_switch,
        "cio_operating_system_loop": cio_loop,
    }


def _decision_liability_shield(packet: Mapping[str, Any], actions: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    exposures = []
    if packet.get("missing_evidence"):
        exposures.append("approval with missing evidence")
    if packet.get("decision_debt"):
        exposures.append("open or ownerless decision debt")
    if packet.get("governance_control_map"):
        exposures.append("controls or sign-offs required before defensible approval")
    if any(action.get("autonomy_level") == "L4 Human-Only" for action in actions):
        exposures.append("human-only accountability boundary")
    if packet.get("scorecard", {}).get("board_risk", {}).get("value", 0) >= 70:
        exposures.append("material board-risk exposure")
    liability_score = _bounded(20 + len(exposures) * 14 + len(packet.get("missing_evidence", [])) * 4)
    return {
        "liability_score": liability_score,
        "posture": "High exposure" if liability_score >= 70 else "Managed exposure" if liability_score >= 45 else "Low exposure",
        "exposures": exposures,
        "defense_actions": [
            "Name accountable owner and decision forum.",
            "Attach evidence gates and expiry dates to any conditional approval.",
            "Document residual risk, dissent and escalation threshold.",
        ],
    }


def _executive_blind_spot_radar(packet: Mapping[str, Any]) -> Dict[str, Any]:
    blind_spots = []
    if packet.get("narrative_risk_detector"):
        blind_spots.append({"blind_spot": "positive narrative without evidence", "source": "narrative risk detector"})
    if packet.get("contradictions"):
        blind_spots.append({"blind_spot": "contradictory status signals", "source": "contradiction detection"})
    if packet.get("value_at_risk_estimate", {}).get("exposures"):
        blind_spots.append({"blind_spot": "business exposure hidden behind technical status", "source": "value-at-risk estimate"})
    if packet.get("scorecard", {}).get("value_leakage", {}).get("value", 0) >= 60:
        blind_spots.append({"blind_spot": "activity may be disconnected from realized value", "source": "value leakage score"})
    if not blind_spots:
        blind_spots.append({"blind_spot": "no major blind spot detected from provided context", "source": "provided evidence"})
    return {
        "blind_spot_count": len(blind_spots),
        "blind_spots": blind_spots,
        "next_probe": "Ask for the strongest disconfirming evidence before approving the narrative.",
    }


def _commitment_integrity_score(packet: Mapping[str, Any]) -> Dict[str, Any]:
    text = " ".join(packet.get("facts", []) + packet.get("assumptions", []) + [packet.get("decision_needed", "")]).lower()
    factors = {
        "date_defined": any(term in text for term in {"date", "target", "go-live", "deadline", "30 september"}),
        "scope_defined": any(term in text for term in {"scope", "workstream", "project", "program", "erp", "crm", "ai"}),
        "budget_defined": any(term in text for term in {"budget", "spend", "reserve", "forecast", "funding"}),
        "capacity_defined": any(term in text for term in {"capacity", "architect", "owner", "team", "resource"}),
        "control_defined": any(term in text for term in {"audit", "control", "security", "sign-off", "evidence"}),
        "recovery_defined": any(term in text for term in {"recovery", "mitigation", "fallback", "defer", "conditions"}),
    }
    score = _bounded(sum(1 for value in factors.values() if value) * 16 - len(packet.get("missing_evidence", [])) * 5)
    return {
        "score": score,
        "grade": "Strong" if score >= 75 else "Partial" if score >= 50 else "Weak",
        "factors": factors,
        "integrity_gap": [key for key, value in factors.items() if not value],
    }


def _board_narrative_stress_test(packet: Mapping[str, Any]) -> Dict[str, Any]:
    narrative = packet.get("situation", "")
    objections = _board_objection_simulator(packet)
    failures = []
    if packet.get("missing_evidence"):
        failures.append("narrative lacks evidence for one or more approval-critical claims")
    if packet.get("scorecard", {}).get("board_risk", {}).get("value", 0) >= 60:
        failures.append("board risk remains material")
    if packet.get("decision_anti_patterns"):
        failures.append("decision anti-patterns weaken the story")
    return {
        "tested_narrative": narrative,
        "stress_result": "Fails without caveats" if len(failures) >= 2 else "Passes with evidence gates" if failures else "Passes",
        "failure_modes": failures,
        "hardest_questions": objections[:5],
        "rewrite_rule": "Replace confidence claims with evidence-backed status, residual risk and explicit decision ask.",
    }


def _autonomous_decision_memory_diff(packet: Mapping[str, Any], memory: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "repeated_decision_debt": memory.get("repeated_decision_debt", []),
        "stale_assumptions": memory.get("stale_assumptions", []),
        "overdue_actions": memory.get("overdue_actions", []),
        "conflicting_claims": memory.get("conflicting_claims", []),
        "suggested_updates": memory.get("suggested_memory_updates", {}),
        "memory_action": "Update decision memory only after user confirms the decision outcome.",
    }


def _value_realization_firewall(packet: Mapping[str, Any]) -> Dict[str, Any]:
    leakage = int(packet.get("scorecard", {}).get("value_leakage", {}).get("value", 0))
    blocks = []
    text = " ".join(packet.get("facts", []) + packet.get("assumptions", [])).lower()
    if leakage >= 60:
        blocks.append("benefit gate required before additional spend or scope expansion")
    if "no adoption" in text or "no metrics" in text or "no baseline" in text:
        blocks.append("adoption and baseline evidence required")
    if "owner" in text and "no owner" in text:
        blocks.append("benefit owner required")
    return {
        "firewall_status": "Block expansion" if blocks else "Proceed with value checks",
        "value_leakage_score": leakage,
        "required_gates": blocks or ["Confirm baseline, owner, adoption metric and stop/continue date."],
    }


def _risk_to_cash_translator(packet: Mapping[str, Any]) -> Dict[str, Any]:
    exposures = packet.get("value_at_risk_estimate", {}).get("exposures", [])
    translations = []
    for exposure in exposures:
        if "financial" in exposure:
            impact = "forecast variance, reserve consumption, funding pressure"
        elif "audit" in exposure or "control" in exposure:
            impact = "audit remediation cost, delayed approval, control exception effort"
        elif "customer" in exposure:
            impact = "retention risk, service credits, revenue trust impact"
        elif "security" in exposure:
            impact = "incident response cost, risk acceptance, remediation funding"
        else:
            impact = "execution delay and management attention cost"
        translations.append({"risk_exposure": exposure, "business_impact": impact})
    return {
        "translations": translations or [{"risk_exposure": "execution credibility", "business_impact": "delayed value realization"}],
        "precision": "directional",
        "note": "Attach finance or customer data for quantified cash exposure.",
    }


def _decision_sla_monitor(packet: Mapping[str, Any], memory: Mapping[str, Any]) -> Dict[str, Any]:
    latency = packet.get("decision_latency_tracker", {})
    debt_count = len(packet.get("decision_debt", [])) + len(memory.get("repeated_decision_debt", []))
    board_risk = int(packet.get("scorecard", {}).get("board_risk", {}).get("value", 0))
    sla = "24h" if board_risk >= 70 else "7d" if board_risk >= 45 or debt_count else "30d"
    return {
        "recommended_sla": sla,
        "latency_risk": latency.get("latency_risk", "Unknown"),
        "days_open": latency.get("days_open"),
        "debt_count": debt_count,
        "breach_action": "Escalate to decision owner if SLA is missed; do not let implicit approval occur.",
    }


def _control_evidence_readiness(packet: Mapping[str, Any]) -> Dict[str, Any]:
    controls = packet.get("governance_control_map", [])
    missing = packet.get("missing_evidence", [])
    readiness = _bounded(100 - len(controls) * 8 - len(missing) * 10)
    return {
        "readiness_score": readiness,
        "readiness": "Ready" if readiness >= 75 else "Partial" if readiness >= 50 else "Not ready",
        "required_controls": controls,
        "missing_evidence": missing,
        "minimum_evidence_pack": ["decision owner", "risk acceptance", "control sign-off", "evidence source", "review date"],
    }


def _executive_attention_allocator(packet: Mapping[str, Any]) -> Dict[str, Any]:
    return _autonomous_attention_allocation(packet)


def _scenario_kill_switch(packet: Mapping[str, Any]) -> Dict[str, Any]:
    criteria = [
        "Stop or defer if evidence gates remain unmet at review date.",
        "Stop expansion if value baseline, adoption and benefit owner are missing.",
        "Escalate if board risk stays High after mitigation.",
        "Require human approval for any external execution or risk acceptance.",
    ]
    if packet.get("scorecard", {}).get("value_leakage", {}).get("value", 0) >= 60:
        criteria.append("Pause low-evidence spend until value realization proof exists.")
    return {
        "kill_switch_required": True,
        "criteria": criteria,
        "owner": packet.get("recommended_action", {}).get("owner", "Executive sponsor"),
        "review_cadence": "weekly until risk is below material threshold",
    }


def _cio_operating_system_loop(
    packet: Mapping[str, Any], memory: Mapping[str, Any], attention: Mapping[str, Any]
) -> Dict[str, Any]:
    return {
        "loop": ["Signals", "Truth", "Risk Chain", "Decision", "Action Draft", "Memory", "Operating Rhythm"],
        "current_cycle": {
            "signals": len(packet.get("facts", [])) + len(packet.get("assumptions", [])),
            "truth_gaps": len(packet.get("missing_evidence", [])),
            "risk_paths": len(packet.get("risk_chain", [])),
            "decisions": len(packet.get("decision_debt", [])) + 1,
            "actions": len(packet.get("draft_next_steps", {}).get("next_24h", [])),
            "memory_updates": len(memory.get("suggested_memory_updates", {}).get("decision_memory", [])),
        },
        "next_operating_cadence": "daily for crisis/high board risk, weekly for portfolio decisions, monthly for stable operating review",
        "attention_contract": attention,
    }


def _cio_work_autonomy_map(packet: Mapping[str, Any], actions: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    high_risk = sum(1 for action in actions if action.get("autonomy_level") == "L4 Human-Only")
    readiness = int(packet.get("scorecard", {}).get("decision_readiness", {}).get("value", 0))
    board_risk = int(packet.get("scorecard", {}).get("board_risk", {}).get("value", 0))
    prep_percent = 90 if readiness >= 70 and board_risk < 45 else 70 if readiness >= 45 else 50
    return {
        "estimated_cio_work_prepared_percent": prep_percent,
        "task_decomposition": [
            {"task": "signal triage", "mode": "Automated", "prepared_percent": 90},
            {"task": "truth and evidence classification", "mode": "Automated", "prepared_percent": 85},
            {"task": "board briefing preparation", "mode": "Drafted", "prepared_percent": 80},
            {"task": "decision option framing", "mode": "Decision-Supported", "prepared_percent": 70},
            {"task": "risk acceptance", "mode": "Human-Only", "prepared_percent": 40 if high_risk else 60},
            {"task": "external execution", "mode": "Human-Only", "prepared_percent": 0},
        ],
        "human_accountability_boundary": "Final accountability, regulated approvals and external execution remain human-owned.",
    }


def _board_objection_simulator(packet: Mapping[str, Any]) -> List[Dict[str, str]]:
    objections = []
    persona_questions = packet.get("board_personas", [])
    if isinstance(persona_questions, Mapping):
        iterable = [
            {"persona": persona, "question": questions[0] if questions else f"What would {persona} challenge?"}
            for persona, questions in persona_questions.items()
        ]
    else:
        iterable = list(persona_questions)
    for persona_item in iterable:
        persona = str(persona_item.get("persona", "Board")) if isinstance(persona_item, Mapping) else "Board"
        question = str(persona_item.get("question", f"What would {persona} challenge?")) if isinstance(persona_item, Mapping) else str(persona_item)
        objections.append(
            {
                "persona": persona,
                "likely_objection": question,
                "weak_answer_risk": "High" if packet.get("missing_evidence") else "Medium",
                "evidence_needed": "; ".join(packet.get("missing_evidence", [])[:2]) or "Confirm owner sign-off and decision rationale.",
            }
        )
    return objections[:8]


def _decision_debt_ledger(packet: Mapping[str, Any], memory: Mapping[str, Any]) -> List[Dict[str, str]]:
    ledger = []
    for index, item in enumerate(packet.get("decision_debt", [])[:8], start=1):
        ledger.append(
            {
                "debt_id": f"DD-{index:03d}",
                "decision_debt": str(item),
                "age": "unknown",
                "owner": "Executive sponsor or named domain owner required",
                "risk_if_unresolved": "Decision latency may convert uncertainty into delivery, audit, value or trust exposure.",
                "next_clearance_action": "Name owner, decision date, evidence gate and escalation threshold.",
            }
        )
    for index, item in enumerate(memory.get("overdue_actions", [])[:3], start=len(ledger) + 1):
        ledger.append(
            {
                "debt_id": f"DD-{index:03d}",
                "decision_debt": str(item),
                "age": "from memory",
                "owner": "Prior action owner",
                "risk_if_unresolved": "Prior commitment remains open and may undermine executive credibility.",
                "next_clearance_action": "Confirm whether the old commitment is closed, superseded or escalated.",
            }
        )
    return ledger


def _truth_gap_detector(packet: Mapping[str, Any]) -> Dict[str, Any]:
    missing = list(packet.get("missing_evidence", []))
    assumptions = list(packet.get("assumptions", []))
    contradictions = list(packet.get("contradictions", []))
    narrative_risks = list(packet.get("narrative_risk_detector", []))
    return {
        "truth_gap_count": len(missing) + len(assumptions) + len(contradictions) + len(narrative_risks),
        "status": "Red" if missing and assumptions else "Amber" if missing or assumptions else "Green",
        "gaps": [
            {"type": "missing_evidence", "item": str(item), "closure_action": "Attach source evidence or owner sign-off."}
            for item in missing[:5]
        ]
        + [
            {"type": "assumption", "item": str(item), "closure_action": "Convert into fact, accepted assumption or explicit risk."}
            for item in assumptions[:5]
        ],
        "narrative_warning": "Status narratives should not be accepted without evidence gates." if missing or narrative_risks else "No major narrative gap detected.",
    }


def _executive_time_saved_estimate(packet: Mapping[str, Any], actions: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    sections = 8 + len(packet.get("risk_chain", [])) + len(actions)
    hours = min(18, max(3, sections))
    return {
        "estimated_hours_prepared": hours,
        "prepared_work": [
            "signal triage",
            "evidence classification",
            "risk chain mapping",
            "board Q&A preparation",
            "action ledger drafting",
            "decision memory update",
        ],
        "not_included": "Human review, political alignment, specialist sign-off and external execution time.",
    }


def _cio_shadow_agenda(
    packet: Mapping[str, Any],
    debt: Sequence[Mapping[str, Any]],
    truth_gaps: Mapping[str, Any],
) -> List[Dict[str, str]]:
    agenda = []
    for index, item in enumerate(packet.get("executive_attention_budget", {}).get("top_5", [])[:5], start=1):
        agenda.append(
            {
                "rank": str(index),
                "topic": str(item),
                "why_it_matters": "High executive attention signal from risk, evidence, decision debt or value exposure.",
                "recommended_posture": "Act Now" if index <= 2 else "Escalate" if index <= 4 else "Monitor",
            }
        )
    if debt:
        agenda.append(
            {
                "rank": str(len(agenda) + 1),
                "topic": "decision debt clearance",
                "why_it_matters": f"{len(debt)} unresolved decision-debt item(s) may block leadership credibility.",
                "recommended_posture": "Decide",
            }
        )
    if truth_gaps.get("truth_gap_count", 0):
        agenda.append(
            {
                "rank": str(len(agenda) + 1),
                "topic": "truth gap closure",
                "why_it_matters": "Missing evidence and assumptions can create false confidence.",
                "recommended_posture": "Delegate",
            }
        )
    return agenda


def _autonomous_steering_pack_factory(packet: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "pack_sections": [
            "1. Executive narrative",
            "2. Decision request",
            "3. Evidence and assumptions",
            "4. Risk chain and value-at-risk",
            "5. Options and trade-offs",
            "6. Board objections and weak answers",
            "7. Recommended safeguards",
            "8. Action ledger and owners",
        ],
        "decision_requests": [packet.get("decision_needed", "")],
        "slides_ready_outline": [
            "Situation and decision needed",
            "Readiness score and truth gaps",
            "Risk chain forecast",
            "Options, recommendation and approval gates",
        ],
        "factory_status": "draft_ready_no_external_execution",
    }


def _risk_chain_forecast(packet: Mapping[str, Any]) -> List[Dict[str, str]]:
    forecast = []
    for index, path in enumerate(packet.get("risk_chain", [])[:6], start=1):
        forecast.append(
            {
                "forecast_id": f"RF-{index:03d}",
                "current_signal": str(path.get("signal", "")),
                "likely_next_escalation": str(path.get("business_impact", "executive decision risk")),
                "trigger": "No owner, no evidence gate or no decision within the next review cycle.",
                "preventive_action": "Assign owner, confirm mitigation evidence and define escalation threshold.",
            }
        )
    return forecast


def _strategic_drift_detector(packet: Mapping[str, Any]) -> Dict[str, Any]:
    signals = [str(item) for item in packet.get("facts", []) + packet.get("assumptions", [])]
    drift_terms = {"legacy", "duplicate", "unclear value", "adoption", "over forecast", "unfunded", "misaligned", "target"}
    drift_signals = [signal for signal in signals if any(term in signal.lower() for term in drift_terms)]
    return {
        "drift_status": "Red" if len(drift_signals) >= 4 else "Amber" if drift_signals else "Green",
        "drift_signals": drift_signals[:8],
        "kill_switch_question": "Should this initiative continue unchanged if value, architecture fit, controls and adoption cannot be evidenced?",
        "recommended_gate": "Require value evidence, architecture/security sign-off and explicit stop/change/continue decision.",
    }


def _human_control_contract(actions: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    return {
        "execution_policy": "draft_only_until_explicit_tool_and_user_approval_exist",
        "approval_required_for": [
            "external communications",
            "task creation in enterprise systems",
            "financial commitments",
            "security, privacy, legal, HR and compliance decisions",
            "irreversible changes",
        ],
        "action_controls": [
            {
                "action_id": action.get("action_id"),
                "autonomy_level": action.get("autonomy_level"),
                "required_approval": action.get("required_approval"),
                "cannot_automate_reasons": action.get("cannot_automate_reasons", []),
            }
            for action in actions
        ],
        "human_control_statement": "The plugin may prepare and structure work; accountable humans approve, execute and own regulated outcomes.",
    }


def _decision_sla_enforcer(packet: Mapping[str, Any], debt: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    board_risk = int(packet.get("scorecard", {}).get("board_risk", {}).get("value", 0))
    missing_count = len(packet.get("missing_evidence", []))
    if board_risk >= 70 or missing_count >= 3:
        sla = "24h"
        breach_risk = "High"
    elif board_risk >= 45 or debt:
        sla = "7d"
        breach_risk = "Medium"
    else:
        sla = "30d"
        breach_risk = "Low"
    return {
        "recommended_decision_sla": sla,
        "breach_risk": breach_risk,
        "sla_drivers": [
            f"board_risk={board_risk}",
            f"missing_evidence={missing_count}",
            f"decision_debt_items={len(debt)}",
        ],
        "required_checkpoint": "Owner, evidence gate, decision date and escalation threshold must be named.",
        "missed_sla_consequence": "Unresolved decision pressure may convert into delivery, audit, cost or trust exposure.",
    }


def _vendor_exit_simulator(packet: Mapping[str, Any]) -> Dict[str, Any]:
    signals = _signals_containing(packet, {"vendor", "supplier", "contract", "license", "lock-in", "outsourcing"})
    return {
        "exit_pressure": "High" if len(signals) >= 3 else "Medium" if signals else "Low",
        "vendor_signals": signals[:8],
        "exit_options": [
            "renegotiate recovery plan and commercial remedies",
            "reduce vendor scope to critical path",
            "prepare alternative supplier or internal fallback",
            "freeze new commitments until evidence gates pass",
        ],
        "exit_readiness_gaps": [
            "current contract rights not provided",
            "transition cost and operational fallback not evidenced",
            "data, IP, security and continuity obligations not confirmed",
        ],
        "decision_note": "Exit simulation is directional unless contract, cost and continuity evidence is attached.",
    }


def _regulatory_shock_simulator(packet: Mapping[str, Any]) -> Dict[str, Any]:
    signals = _signals_containing(packet, {"audit", "regulator", "compliance", "privacy", "control", "evidence", "customer"})
    shock_level = "High" if len(signals) >= 4 else "Medium" if signals else "Low"
    return {
        "shock_level": shock_level,
        "trigger_scenarios": [
            "audit requests evidence within 48 hours",
            "regulator asks for owner, control and decision traceability",
            "customer impact creates executive disclosure pressure",
        ],
        "exposed_signals": signals[:8],
        "minimum_response_pack": [
            "facts and timeline",
            "control owner and sign-off status",
            "decision log and residual risk",
            "customer impact and communications position",
        ],
    }


def _cyber_business_impact_translator(packet: Mapping[str, Any]) -> Dict[str, Any]:
    signals = _signals_containing(packet, {"security", "access", "iam", "breach", "privileged", "zero trust", "vulnerability", "control"})
    impacts = []
    if signals:
        impacts = [
            "control and audit exposure",
            "service continuity or customer trust risk",
            "delivery dependency if remediation blocks go-live",
            "executive risk acceptance required before approval",
        ]
    return {
        "cyber_signal_count": len(signals),
        "business_impacts": impacts,
        "executive_translation": "Security signals should be framed as decision, trust, continuity and control exposure, not only technical findings." if signals else "No strong cyber signal detected in provided context.",
        "required_business_decision": "Accept, remediate, defer with safeguards or escalate to accountable risk owner." if signals else "Monitor only.",
        "source_signals": signals[:8],
    }


def _talent_criticality_radar(packet: Mapping[str, Any]) -> Dict[str, Any]:
    signals = _signals_containing(packet, {"architect", "capacity", "resource", "team", "owner", "skills", "knowledge", "overload"})
    criticality = "High" if len(signals) >= 3 else "Medium" if signals else "Low"
    return {
        "criticality": criticality,
        "talent_signals": signals[:8],
        "key_person_risks": [
            signal for signal in signals if any(term in signal.lower() for term in {"architect", "owner", "capacity", "resource"})
        ][:5],
        "mitigations": [
            "name backup owners for critical roles",
            "reduce parallel demand on scarce experts",
            "fund temporary capacity or descope lower-value work",
            "capture decision rationale and operational knowledge",
        ],
    }


def _capital_allocation_copilot(packet: Mapping[str, Any]) -> Dict[str, Any]:
    signals = _signals_containing(packet, {"budget", "spend", "forecast", "reserve", "cost", "funding", "benefit", "value"})
    value_band = packet.get("value_at_risk_estimate", {}).get("value_at_risk_band", "Unknown")
    return {
        "capital_pressure": "High" if value_band == "High" or len(signals) >= 3 else "Medium" if signals else "Low",
        "financial_signals": signals[:8],
        "allocation_options": [
            {"option": "protect critical controls and customer-impact work", "trade_off": "may delay lower-value transformation scope"},
            {"option": "pause spend without decision readiness", "trade_off": "may create delivery delay but reduces value leakage"},
            {"option": "fund bottleneck capacity", "trade_off": "near-term cost increase to protect strategic delivery"},
        ],
        "cfo_question": "Which spend is protecting value, which is buying time, and which is masking decision debt?",
    }


def _post_decision_learning_loop(packet: Mapping[str, Any], memory: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "learning_items": [
            "Which assumptions became facts?",
            "Which risks materialized or disappeared?",
            "Which owner actions closed evidence gaps?",
            "Which board objections were not anticipated?",
        ],
        "memory_comparison_available": bool(memory),
        "suggested_review_cadence": "T+7 for urgent decisions, T+30 for operating decisions, T+90 for strategic investments.",
        "update_targets": [
            "decision twin",
            "assumption register",
            "risk chain",
            "action ledger",
            "executive memory",
        ],
        "success_metric": "Future similar decisions require fewer missing-evidence items and lower decision latency.",
    }


def _cio_os_maturity_index(
    packet: Mapping[str, Any],
    actions: Sequence[Mapping[str, Any]],
    truth_gaps: Mapping[str, Any],
    debt: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    readiness = int(packet.get("scorecard", {}).get("decision_readiness", {}).get("value", 0))
    confidence = int(packet.get("scorecard", {}).get("evidence_confidence", {}).get("value", 0))
    penalty = min(40, truth_gaps.get("truth_gap_count", 0) * 4 + len(debt) * 3)
    score = max(0, min(100, round((readiness + confidence) / 2) - penalty))
    level = "L3 Operating System" if score >= 75 else "L2 Governed Copilot" if score >= 55 else "L1 Decision Toolkit" if score >= 35 else "L0 Ad Hoc"
    return {
        "score": score,
        "maturity_level": level,
        "drivers": [
            f"decision_readiness={readiness}",
            f"evidence_confidence={confidence}",
            f"truth_gaps={truth_gaps.get('truth_gap_count', 0)}",
            f"decision_debt_items={len(debt)}",
            f"action_count={len(actions)}",
        ],
        "next_maturity_moves": [
            "close recurring evidence gaps",
            "make decision SLA mandatory",
            "maintain executive memory after each review",
            "standardize human-control contracts for action drafts",
        ],
    }


def _stakeholder_alignment_matrix(packet: Mapping[str, Any]) -> Dict[str, Any]:
    personas = packet.get("board_personas", [])
    rows = []
    for persona_item in personas:
        if not isinstance(persona_item, Mapping):
            continue
        persona = str(persona_item.get("persona", "Stakeholder"))
        rows.append(
            {
                "stakeholder": persona,
                "likely_concern": str(persona_item.get("question", "Decision evidence and risk exposure")),
                "alignment_risk": str(persona_item.get("weak_answer_risk", "Medium")),
                "message_needed": f"Explain decision impact and evidence from the {persona} perspective.",
                "required_evidence": "; ".join(packet.get("missing_evidence", [])[:2]) or "Owner sign-off and decision rationale.",
            }
        )
    if not rows:
        rows.append(
            {
                "stakeholder": "Executive sponsor",
                "likely_concern": "Decision ownership and evidence quality",
                "alignment_risk": "Medium",
                "message_needed": "Confirm why this decision matters now.",
                "required_evidence": "Decision owner, options and risk acceptance.",
            }
        )
    return {
        "alignment_status": "Red" if any(row["alignment_risk"] == "High" for row in rows) else "Amber",
        "matrix": rows[:8],
        "first_alignment_action": "Pre-align high-risk stakeholders with evidence gaps and proposed safeguards before the meeting.",
    }


def _exception_waiver_factory(packet: Mapping[str, Any], actions: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    candidates = _signals_containing(packet, {"waiver", "exception", "defer", "accept", "missing", "incomplete", "control", "risk"})
    return {
        "waiver_needed": bool(candidates or any(action.get("risk_level") == "High" for action in actions)),
        "candidate_exceptions": candidates[:8],
        "waiver_template": {
            "decision": str(packet.get("decision_needed", "")),
            "exception_scope": "Define control, delivery, security, budget or architecture exception.",
            "expiry": "Set explicit review date; do not leave open-ended.",
            "residual_risk_owner": "Executive sponsor or accountable domain owner",
            "compensating_controls": [
                "evidence gate",
                "owner sign-off",
                "time-boxed review",
                "escalation threshold",
            ],
        },
        "approval_note": "Waivers are drafts only and require accountable human approval.",
    }


def _policy_as_code_readiness(packet: Mapping[str, Any]) -> Dict[str, Any]:
    control_signals = _signals_containing(packet, {"control", "policy", "audit", "access", "privacy", "security", "compliance"})
    readiness = "High" if len(control_signals) >= 4 and not packet.get("missing_evidence") else "Medium" if control_signals else "Low"
    return {
        "readiness": readiness,
        "codifiable_controls": [
            "owner sign-off required before approval",
            "evidence gate required for control exceptions",
            "high-risk actions require human approval",
            "missing evidence blocks board-ready status",
        ],
        "source_signals": control_signals[:8],
        "missing_for_policy_as_code": [
            "formal control taxonomy",
            "system of record for evidence",
            "approval workflow owner",
            "exception expiry policy",
        ],
    }


def _benefits_realization_sentinel(packet: Mapping[str, Any]) -> Dict[str, Any]:
    signals = _signals_containing(packet, {"benefit", "value", "adoption", "forecast", "spend", "budget", "cost", "reserve"})
    risk = "High" if len(signals) >= 4 else "Medium" if signals else "Low"
    return {
        "benefits_risk": risk,
        "value_signals": signals[:8],
        "watch_items": [
            "spend continues without adoption evidence",
            "forecast pressure masks benefit shortfall",
            "delivery activity is not linked to measurable business outcome",
            "benefit owner is not named",
        ],
        "next_value_gate": "Require benefit owner, metric, baseline, target and next measurement date.",
    }


def _operating_rhythm_autopilot(
    packet: Mapping[str, Any],
    debt: Sequence[Mapping[str, Any]],
    truth_gaps: Mapping[str, Any],
) -> Dict[str, Any]:
    status = _enterprise_status(packet)["overall"]
    if status == "Red":
        cadence = "daily until evidence and decision debt are closed"
    elif status == "Amber":
        cadence = "twice weekly until next steering checkpoint"
    else:
        cadence = "weekly monitor"
    return {
        "recommended_cadence": cadence,
        "next_rituals": [
            "15-minute evidence closure standup",
            "decision debt clearance review",
            "owner sign-off checkpoint",
            "executive briefing refresh",
        ],
        "auto_prepared_inputs": [
            "top risks",
            "missing evidence",
            "decision SLA",
            "action ledger",
            "stakeholder objections",
        ],
        "rhythm_triggers": {
            "truth_gap_count": truth_gaps.get("truth_gap_count", 0),
            "decision_debt_count": len(debt),
            "enterprise_status": status,
        },
    }


def _autonomous_escalation_drafts(packet: Mapping[str, Any], actions: Sequence[Mapping[str, Any]]) -> List[Dict[str, str]]:
    drafts = []
    for index, item in enumerate(packet.get("executive_attention_budget", {}).get("top_5", [])[:5], start=1):
        drafts.append(
            {
                "draft_id": f"ESC-{index:03d}",
                "subject": f"Escalation draft: {str(item)[:80]}",
                "audience": "Executive sponsor and accountable domain owner",
                "message": f"Please confirm owner, evidence, decision path and escalation threshold for: {item}",
                "approval_required": "User approval required before sending or creating tasks.",
                "status": "drafted_not_executed",
            }
        )
    if not drafts:
        drafts.append(
            {
                "draft_id": "ESC-001",
                "subject": "Escalation draft: decision readiness checkpoint",
                "audience": "Executive sponsor",
                "message": "Please confirm whether this item should be monitored, delegated, decided or escalated.",
                "approval_required": "User approval required before sending or creating tasks.",
                "status": "drafted_not_executed",
            }
        )
    return drafts


def _executive_decision_backlog(packet: Mapping[str, Any], debt: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    backlog = []
    for index, item in enumerate(packet.get("decision_debt", [])[:6], start=1):
        backlog.append(
            {
                "backlog_id": f"EDB-{index:03d}",
                "decision": str(item),
                "priority": "P1" if index <= 2 else "P2",
                "required_input": "owner, evidence, options and risk acceptance",
                "routing": "executive sponsor" if index <= 2 else "domain owner",
            }
        )
    if not backlog:
        backlog.append(
            {
                "backlog_id": "EDB-001",
                "decision": str(packet.get("decision_needed", "Confirm whether leadership decision is needed.")),
                "priority": "P2",
                "required_input": "decision owner and evidence gate",
                "routing": "executive sponsor",
            }
        )
    return {
        "backlog_count": len(backlog),
        "items": backlog,
        "clearance_rule": "P1 decisions require a named owner and next checkpoint before the next leadership review.",
        "source_decision_debt_count": len(debt),
    }


def _enterprise_control_tower(
    packet: Mapping[str, Any],
    truth_gaps: Mapping[str, Any],
    debt: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    status = _enterprise_status(packet)
    return {
        "overall_status": status["overall"],
        "control_panels": [
            {"panel": "decision readiness", "status": _status_from_score(status["decision_readiness"], inverse=False)},
            {"panel": "board risk", "status": _status_from_score(status["board_risk"], inverse=True)},
            {"panel": "evidence confidence", "status": _status_from_score(status["evidence_confidence"], inverse=False)},
            {"panel": "truth gaps", "status": "Red" if truth_gaps.get("truth_gap_count", 0) >= 5 else "Amber" if truth_gaps.get("truth_gap_count", 0) else "Green"},
            {"panel": "decision debt", "status": "Red" if len(debt) >= 5 else "Amber" if debt else "Green"},
        ],
        "operator_instruction": "Run the next operating review from red panels first, then amber panels, then monitor green panels.",
    }


def _ma_carveout_readiness(packet: Mapping[str, Any]) -> Dict[str, Any]:
    signals = _signals_containing(packet, {"separation", "integration", "vendor", "contract", "data", "system", "customer", "finance", "access"})
    readiness = "Low" if len(signals) >= 4 and packet.get("missing_evidence") else "Medium" if signals else "Not indicated"
    return {
        "readiness": readiness,
        "relevant_signals": signals[:8],
        "readiness_domains": [
            "systems and data separation",
            "vendor and contract dependencies",
            "identity and access readiness",
            "finance and customer continuity",
            "control evidence and audit trail",
        ],
        "first_due_diligence_questions": [
            "Which systems, contracts and data flows are inseparable?",
            "Which access/control gaps would block separation or integration?",
            "Which customers, services or financial processes are operationally exposed?",
        ],
    }


def _data_trust_radar(packet: Mapping[str, Any]) -> Dict[str, Any]:
    signals = _signals_containing(packet, {"data", "evidence", "quality", "lineage", "owner", "privacy", "report", "metric"})
    missing = [item for item in packet.get("missing_evidence", []) if any(term in str(item).lower() for term in {"data", "evidence", "owner", "metric"})]
    trust = "Low" if len(missing) >= 2 else "Medium" if signals or missing else "Unknown"
    return {
        "trust_level": trust,
        "trust_signals": signals[:8],
        "missing_trust_evidence": missing[:5],
        "required_controls": [
            "data owner",
            "metric definition",
            "lineage or source reference",
            "freshness timestamp",
            "privacy classification",
        ],
    }


def _architecture_runway_guardian(packet: Mapping[str, Any]) -> Dict[str, Any]:
    signals = _signals_containing(packet, {"architecture", "architect", "technical debt", "legacy", "integration", "platform", "environment", "runway"})
    runway_risk = "High" if len(signals) >= 3 else "Medium" if signals else "Low"
    return {
        "runway_risk": runway_risk,
        "architecture_signals": signals[:8],
        "guardrails": [
            "protect scarce architecture capacity",
            "do not approve go-live without integration readiness evidence",
            "time-box waivers and technical debt acceptance",
            "connect architecture exceptions to business risk",
        ],
        "next_architecture_gate": "Confirm capacity, integration readiness, exception owner and debt expiry before approval.",
    }


def _executive_narrative_generator(packet: Mapping[str, Any]) -> Dict[str, Any]:
    status = _enterprise_status(packet)["overall"]
    recommendation = packet.get("recommended_action", {}).get("recommendation", "")
    decision = packet.get("decision_needed", "")
    return {
        "board_narrative": f"{status} status: {decision} Recommendation: {recommendation}",
        "ceo_line": "The decision issue is not activity; it is whether the enterprise has enough evidence, ownership and risk control to proceed.",
        "cfo_line": "Funding should follow value protection, evidence quality and bottleneck removal, not unresolved decision debt.",
        "ciso_audit_line": "Control and evidence gaps should be treated as approval conditions, not background noise.",
        "customer_line": "Customer trust risk must be translated into clear ownership, communication posture and recovery evidence.",
    }


def _autonomous_due_diligence_questions(packet: Mapping[str, Any]) -> Dict[str, Any]:
    questions = []
    for persona in packet.get("board_personas", []):
        if isinstance(persona, Mapping):
            questions.append(
                {
                    "domain": str(persona.get("persona", "Executive")),
                    "question": str(persona.get("question", "What evidence supports this decision?")),
                    "why_it_matters": "Prevents weak answers before executive review.",
                    "evidence_needed": "; ".join(packet.get("missing_evidence", [])[:2]) or "Owner sign-off and source evidence.",
                }
            )
    for item in packet.get("risk_chain", [])[:4]:
        questions.append(
            {
                "domain": "Risk chain",
                "question": f"What breaks next if {item.get('dependency')} is not resolved?",
                "why_it_matters": str(item.get("business_impact", "business impact")),
                "evidence_needed": "Mitigation owner, due date and residual-risk decision.",
            }
        )
    return {
        "question_count": len(questions),
        "questions": questions[:12],
        "usage": "Use these before board, vendor, transformation, audit or crisis reviews.",
    }


def _resilience_continuity_planner(packet: Mapping[str, Any]) -> Dict[str, Any]:
    signals = _signals_containing(packet, {"outage", "continuity", "recovery", "customer", "incident", "environment", "integration", "billing"})
    level = "High" if len(signals) >= 3 else "Medium" if signals else "Low"
    return {
        "resilience_pressure": level,
        "continuity_signals": signals[:8],
        "minimum_plan": [
            "critical service and customer impact owner",
            "manual workaround or fallback path",
            "communication trigger and audience",
            "recovery checkpoint cadence",
            "post-incident control update",
        ],
        "first_24h_actions": [
            "confirm known facts and unknowns",
            "name incident or continuity commander",
            "separate containment from root-cause work",
            "prepare customer and board holding statements",
        ],
    }


def _customer_trust_impact_radar(packet: Mapping[str, Any]) -> Dict[str, Any]:
    signals = _signals_containing(packet, {"customer", "billing", "service", "outage", "trust", "communication", "sla", "recovery"})
    trust_risk = "High" if len(signals) >= 3 else "Medium" if signals else "Low"
    return {
        "trust_risk": trust_risk,
        "customer_signals": signals[:8],
        "trust_dimensions": [
            "service continuity",
            "billing or commercial accuracy",
            "communication credibility",
            "recovery transparency",
            "control and privacy assurance",
        ],
        "recommended_position": "Prepare a factual customer-impact position with owner, timeline and next update trigger." if signals else "Monitor for customer-impact signals.",
    }


def _ai_portfolio_governance(packet: Mapping[str, Any]) -> Dict[str, Any]:
    signals = _signals_containing(packet, {"ai", "model", "llm", "automation", "data", "privacy", "use case", "governance"})
    governance_level = "High" if len(signals) >= 3 else "Medium" if signals else "Not indicated"
    return {
        "governance_level": governance_level,
        "ai_signals": signals[:8],
        "portfolio_controls": [
            "business owner",
            "data owner",
            "model risk tier",
            "evaluation baseline",
            "human review control",
            "rollback or disable path",
        ],
        "approval_gate": "AI use cases should not move from pilot to production without owner, data, evaluation and control evidence.",
    }


def _cost_of_delay_calculator(packet: Mapping[str, Any]) -> Dict[str, Any]:
    value_band = packet.get("value_at_risk_estimate", {}).get("value_at_risk_band", "Unknown")
    board_risk = int(packet.get("scorecard", {}).get("board_risk", {}).get("value", 0))
    debt_count = len(packet.get("decision_debt", []))
    qualitative_cost = "High" if value_band == "High" or board_risk >= 70 or debt_count >= 5 else "Medium" if board_risk >= 45 or debt_count else "Low"
    return {
        "qualitative_cost_of_delay": qualitative_cost,
        "drivers": [
            f"value_at_risk={value_band}",
            f"board_risk={board_risk}",
            f"decision_debt_items={debt_count}",
        ],
        "delay_impacts": [
            "higher delivery recovery cost",
            "lost management attention",
            "audit or control exposure window remains open",
            "customer trust risk may increase",
        ],
        "next_decision_gate": "Decide now, explicitly defer with owner and date, or stop consuming scarce capacity.",
    }


def _executive_commitment_tracker(packet: Mapping[str, Any], memory: Mapping[str, Any]) -> Dict[str, Any]:
    commitments = []
    next_steps = packet.get("draft_next_steps", [])
    if isinstance(next_steps, Mapping):
        step_items: List[str] = []
        for value in next_steps.values():
            if isinstance(value, list):
                step_items.extend(str(item) for item in value)
            elif value:
                step_items.append(str(value))
    elif isinstance(next_steps, list):
        step_items = [str(item) for item in next_steps]
    else:
        step_items = [str(next_steps)] if next_steps else []
    for index, action in enumerate(step_items[:6], start=1):
        commitments.append(
            {
                "commitment_id": f"COM-{index:03d}",
                "commitment": str(action),
                "owner": "to be assigned",
                "status": "draft",
                "next_check": "next operating review",
            }
        )
    for index, item in enumerate(memory.get("overdue_actions", [])[:3], start=len(commitments) + 1):
        commitments.append(
            {
                "commitment_id": f"COM-{index:03d}",
                "commitment": str(item),
                "owner": "from prior memory",
                "status": "overdue_or_unconfirmed",
                "next_check": "immediate confirmation",
            }
        )
    return {
        "commitment_count": len(commitments),
        "commitments": commitments,
        "tracker_note": "Commitments are draft tracking items until persisted by user or future memory tooling.",
    }


def _decision_rights_mapper(packet: Mapping[str, Any]) -> Dict[str, Any]:
    request_type = str(packet.get("request_type", "Executive Decision"))
    high_risk = bool(packet.get("missing_evidence")) or int(packet.get("scorecard", {}).get("board_risk", {}).get("value", 0)) >= 70
    rights = [
        {"decision_area": "business priority", "decision_right": "executive sponsor", "approval_mode": "approve or defer"},
        {"decision_area": "security/control risk", "decision_right": "CISO or control owner", "approval_mode": "sign off or risk acceptance"},
        {"decision_area": "financial exposure", "decision_right": "CFO or budget owner", "approval_mode": "fund, pause or reallocate"},
        {"decision_area": "architecture exception", "decision_right": "enterprise architect", "approval_mode": "approve with guardrails"},
    ]
    return {
        "request_type": request_type,
        "rights_clarity": "Low" if high_risk else "Medium",
        "decision_rights": rights,
        "missing_rights": ["named accountable decision owner"] if high_risk else [],
        "next_action": "Name accountable owner, contributors, consulted parties and final approver before approval.",
    }


def _okr_strategy_fit_checker(packet: Mapping[str, Any]) -> Dict[str, Any]:
    signals = _signals_containing(packet, {"strategy", "okr", "objective", "key result", "value", "benefit", "target", "adoption", "customer"})
    drift = packet.get("strategic_drift_detector", {})
    fit = "Weak" if len(signals) == 0 or packet.get("scorecard", {}).get("value_leakage", {}).get("value", 0) >= 70 else "Partial" if len(signals) < 3 else "Strong"
    return {
        "fit": fit,
        "strategy_signals": signals[:8],
        "fit_questions": [
            "Which objective does this decision advance?",
            "Which measurable key result changes?",
            "What work should stop if this remains lower priority?",
            "Which benefit owner confirms the value path?",
        ],
        "recommended_gate": "Require objective, key result, benefit owner and stop/change/continue decision for weak-fit work.",
        "drift_reference": drift if isinstance(drift, Mapping) else {},
    }


def _risk_acceptance_docket(packet: Mapping[str, Any]) -> Dict[str, Any]:
    risks = packet.get("risk_chain", [])[:6]
    docket = []
    for index, risk in enumerate(risks, start=1):
        docket.append(
            {
                "risk_id": f"RA-{index:03d}",
                "risk": str(risk.get("signal", "")),
                "business_impact": str(risk.get("business_impact", "")),
                "acceptance_owner": "accountable executive or domain risk owner",
                "expiry": "time-box required",
                "required_evidence": "mitigation, residual risk, compensating controls and review date",
            }
        )
    return {
        "docket_required": bool(docket),
        "items": docket,
        "acceptance_rule": "Material risks require named owner, expiry, compensating controls and explicit residual-risk decision.",
    }


def _service_health_sentinel(packet: Mapping[str, Any]) -> Dict[str, Any]:
    signals = _signals_containing(packet, {"service", "incident", "ticket", "sla", "outage", "billing", "recovery", "operations"})
    status = "Red" if any("outage" in signal.lower() or "billing" in signal.lower() for signal in signals) else "Amber" if signals else "Green"
    return {
        "service_health": status,
        "service_signals": signals[:8],
        "health_dimensions": [
            "availability",
            "performance",
            "customer impact",
            "incident trend",
            "recovery confidence",
            "support load",
        ],
        "next_health_check": "Confirm customer impact, SLA exposure, incident owner and recovery checkpoint.",
    }


def _knowledge_continuity_planner(packet: Mapping[str, Any]) -> Dict[str, Any]:
    signals = _signals_containing(packet, {"knowledge", "architect", "owner", "team", "capacity", "expert", "documentation", "handover"})
    risk = "High" if len(signals) >= 3 else "Medium" if signals else "Low"
    return {
        "knowledge_risk": risk,
        "knowledge_signals": signals[:8],
        "continuity_actions": [
            "name backup owner for critical decision areas",
            "capture decision rationale and architecture exceptions",
            "document recovery and operational knowledge",
            "reduce dependency on single experts before approval",
        ],
        "next_action": "Create a knowledge handover checklist for any high-risk owner or expert dependency.",
    }


def _dependency_breakpoint_analyzer(packet: Mapping[str, Any]) -> Dict[str, Any]:
    dependencies = packet.get("semantic_model", {}).get("dependencies", [])
    paths = packet.get("risk_chain", [])
    breakpoints = []
    for index, dep in enumerate(dependencies[:6], start=1):
        breakpoints.append(
            {
                "breakpoint_id": f"BP-{index:03d}",
                "dependency": str(dep.get("dependency", dep)),
                "criticality": str(dep.get("criticality", "Medium")) if isinstance(dep, Mapping) else "Medium",
                "failure_mode": "owner, evidence, integration, capacity or control gap",
                "stabilizer": "name owner, fallback, evidence gate and escalation trigger",
            }
        )
    if not breakpoints:
        for index, path in enumerate(paths[:4], start=1):
            breakpoints.append(
                {
                    "breakpoint_id": f"BP-{index:03d}",
                    "dependency": str(path.get("dependency", "")),
                    "criticality": "High",
                    "failure_mode": str(path.get("amplifier", "unresolved dependency")),
                    "stabilizer": "confirm mitigation and fallback before approval",
                }
            )
    return {
        "breakpoint_count": len(breakpoints),
        "breakpoints": breakpoints,
        "analysis_note": "Breakpoints are inferred from provided dependencies and risk-chain paths.",
    }


def _transformation_kill_criteria(packet: Mapping[str, Any]) -> Dict[str, Any]:
    value = int(packet.get("scorecard", {}).get("value_leakage", {}).get("value", 0))
    readiness = int(packet.get("scorecard", {}).get("decision_readiness", {}).get("value", 0))
    criteria = [
        "no named benefit owner",
        "no measurable value baseline or target",
        "critical evidence remains missing after next checkpoint",
        "architecture or control risk increases without accepted waiver",
        "scarce capacity remains unfunded or overloaded",
    ]
    return {
        "kill_pressure": "High" if value >= 70 or readiness < 45 else "Medium" if value >= 45 else "Low",
        "criteria": criteria,
        "stop_change_continue_gate": "Stop if evidence and value ownership remain unresolved; change scope if controls or architecture can be stabilized; continue only with owner-backed value gate.",
        "recommended_review": "Run stop/change/continue review at the next steering checkpoint.",
    }


def _vendor_negotiation_brief(packet: Mapping[str, Any]) -> Dict[str, Any]:
    signals = _signals_containing(packet, {"vendor", "supplier", "contract", "milestone", "recovery", "license", "cost"})
    return {
        "negotiation_pressure": "High" if len(signals) >= 2 else "Medium" if signals else "Low",
        "vendor_signals": signals[:8],
        "asks": [
            "approved recovery plan with named accountable owner",
            "commercial remedy or service credit for missed commitment",
            "scope reduction or priority reset around critical path",
            "evidence delivery dates and escalation rights",
        ],
        "fallback_position": "Prepare alternate sourcing, scope reduction or internal fallback if recovery evidence is not accepted.",
        "human_review": "Commercial and legal review required before negotiation or contract action.",
    }


def _compliance_evidence_pack(packet: Mapping[str, Any]) -> Dict[str, Any]:
    signals = _signals_containing(packet, {"audit", "compliance", "control", "evidence", "privacy", "regulator", "access"})
    return {
        "pack_required": bool(signals or packet.get("missing_evidence")),
        "evidence_signals": signals[:8],
        "pack_sections": [
            "control objective",
            "owner and approver",
            "source evidence",
            "decision log",
            "residual risk",
            "exception expiry",
            "follow-up action",
        ],
        "missing_evidence": list(packet.get("missing_evidence", []))[:8],
        "readiness_note": "Evidence pack is draft-ready only; audit owner must validate completeness.",
    }


def _board_decision_simulator(packet: Mapping[str, Any]) -> Dict[str, Any]:
    options = [option.get("option", option) for option in packet.get("options", [])[:4]]
    if not options:
        options = ["approve", "defer", "approve with conditions", "escalate"]
    simulated = []
    for option in options:
        option_text = str(option)
        simulated.append(
            {
                "option": option_text,
                "likely_board_reaction": "challenge" if packet.get("missing_evidence") else "support with conditions",
                "main_objection": "missing evidence, owner accountability or residual risk" if packet.get("missing_evidence") else "confirm value and safeguards",
                "condition_for_support": "name owner, evidence gate, residual risk and next checkpoint",
            }
        )
    return {
        "simulation": simulated,
        "recommended_board_motion": "Approve with explicit conditions or defer until evidence gate passes.",
        "weakest_point": list(packet.get("missing_evidence", ["owner accountability"]))[0],
    }


def _operating_risk_heatmap(packet: Mapping[str, Any]) -> Dict[str, Any]:
    domains = {
        "delivery": _signals_containing(packet, {"late", "milestone", "go-live", "blocked", "dependency"}),
        "finance": _signals_containing(packet, {"budget", "spend", "forecast", "reserve", "cost"}),
        "security_control": _signals_containing(packet, {"security", "access", "control", "audit", "privacy"}),
        "customer": _signals_containing(packet, {"customer", "billing", "service", "outage"}),
        "capacity": _signals_containing(packet, {"capacity", "architect", "team", "resource", "owner"}),
    }
    cells = []
    for domain, signals in domains.items():
        cells.append(
            {
                "domain": domain,
                "status": "Red" if len(signals) >= 3 else "Amber" if signals else "Green",
                "signal_count": len(signals),
                "top_signal": signals[0] if signals else "",
            }
        )
    return {
        "heatmap": cells,
        "red_domains": [cell["domain"] for cell in cells if cell["status"] == "Red"],
        "operator_note": "Use red domains as the first agenda items for the next operating review.",
    }


def _autonomous_roadmap_reprioritizer(packet: Mapping[str, Any]) -> Dict[str, Any]:
    attention = packet.get("executive_attention_budget", {})
    act_now = list(attention.get("top_5", []))[:5]
    return {
        "reprioritization_required": bool(act_now or packet.get("decision_debt")),
        "promote": act_now[:3],
        "pause_or_defer": [
            "low-evidence work without decision owner",
            "initiatives with weak strategy fit",
            "work consuming scarce architecture or security capacity without value gate",
        ],
        "protect": [
            "customer-impact mitigation",
            "audit/control evidence closure",
            "critical dependency stabilization",
        ],
        "roadmap_rule": "Prioritize risk closure and value protection before new discretionary scope.",
    }


def _audit_finding_predictor(packet: Mapping[str, Any]) -> Dict[str, Any]:
    signals = _signals_containing(packet, {"audit", "control", "evidence", "access", "privacy", "compliance", "missing", "incomplete"})
    predicted = []
    if signals or packet.get("missing_evidence"):
        predicted = [
            {"finding": "insufficient evidence traceability", "likelihood": "High", "prevention": "attach source evidence and owner sign-off"},
            {"finding": "unclear control ownership", "likelihood": "Medium", "prevention": "name accountable control owner"},
            {"finding": "exception without expiry", "likelihood": "Medium", "prevention": "time-box waiver and residual-risk review"},
        ]
    return {
        "finding_risk": "High" if len(signals) >= 3 or packet.get("missing_evidence") else "Low",
        "signals": signals[:8],
        "predicted_findings": predicted,
        "prevention_window": "before next audit, steering or approval gate",
    }


def _platform_rationalization_advisor(packet: Mapping[str, Any]) -> Dict[str, Any]:
    signals = _signals_containing(packet, {"platform", "application", "system", "legacy", "duplicate", "integration", "license", "vendor"})
    return {
        "rationalization_pressure": "High" if len(signals) >= 4 else "Medium" if signals else "Low",
        "platform_signals": signals[:8],
        "candidate_actions": [
            "consolidate duplicate capability",
            "retire low-value or low-adoption platform",
            "renegotiate license or vendor scope",
            "stabilize integration before new roadmap scope",
        ],
        "decision_gate": "Do not fund expansion until ownership, usage, integration and value evidence are clear.",
    }


def _data_sovereignty_radar(packet: Mapping[str, Any]) -> Dict[str, Any]:
    signals = _signals_containing(packet, {"data", "privacy", "regulator", "customer", "country", "region", "retention", "cross-border", "sovereignty"})
    return {
        "sovereignty_risk": "High" if any("privacy" in signal.lower() or "regulator" in signal.lower() for signal in signals) else "Medium" if signals else "Low",
        "sovereignty_signals": signals[:8],
        "required_checks": [
            "data owner",
            "processing location",
            "retention rule",
            "cross-border transfer basis",
            "customer or regulator obligation",
        ],
        "approval_gate": "Do not approve data movement or AI processing without owner, location, purpose and control evidence.",
    }


def _operating_model_debt_ledger(packet: Mapping[str, Any]) -> Dict[str, Any]:
    signals = _signals_containing(packet, {"owner", "handoff", "governance", "role", "team", "capacity", "decision", "accountability"})
    items = []
    for index, signal in enumerate(signals[:6], start=1):
        items.append(
            {
                "debt_id": f"OMD-{index:03d}",
                "signal": signal,
                "debt_type": "unclear ownership or overloaded governance",
                "impact": "slower decisions, weak accountability or recurring escalation",
                "clearance_action": "name owner, decision right, cadence and escalation path",
            }
        )
    return {
        "debt_count": len(items),
        "items": items,
        "ledger_note": "Operating-model debt is inferred from owner, role, governance and capacity signals.",
    }


def _strategic_option_portfolio(packet: Mapping[str, Any]) -> Dict[str, Any]:
    base_options = [str(option.get("option", option)) for option in packet.get("options", [])[:4]]
    if not base_options:
        base_options = ["approve with conditions", "defer", "descope", "escalate"]
    portfolio = []
    for index, option in enumerate(base_options, start=1):
        portfolio.append(
            {
                "option_id": f"OPT-{index:03d}",
                "option": option,
                "value_posture": "protect value" if "approve" in option.lower() else "reduce exposure",
                "risk_posture": "requires safeguards" if packet.get("missing_evidence") else "standard review",
                "next_evidence": "; ".join(packet.get("missing_evidence", [])[:1]) or "owner sign-off",
            }
        )
    return {
        "portfolio": portfolio,
        "recommended_option_pattern": "choose the lowest-regret option that preserves value while closing evidence gaps",
        "decision_note": "Options are decision frames, not approvals.",
    }


def _executive_decision_war_room(packet: Mapping[str, Any]) -> Dict[str, Any]:
    status = _enterprise_status(packet)["overall"]
    return {
        "war_room_required": status == "Red" or bool(packet.get("missing_evidence")),
        "roles": [
            "decision owner",
            "risk/control owner",
            "finance/value owner",
            "architecture/security owner",
            "communications owner",
        ],
        "first_60_minutes": [
            "confirm facts, assumptions and unknowns",
            "name decision owner and approval path",
            "identify blockers and evidence gaps",
            "draft board/customer/internal position",
            "set next checkpoint and escalation threshold",
        ],
        "exit_criteria": "decision owner named, evidence gate set, risk accepted or mitigated, next checkpoint scheduled",
    }


def _evidence_chain_of_custody(packet: Mapping[str, Any]) -> Dict[str, Any]:
    evidence_nodes = packet.get("evidence_graph", {}).get("nodes", [])
    custody_items = []
    for index, node in enumerate(evidence_nodes[:8], start=1):
        custody_items.append(
            {
                "custody_id": f"ECOC-{index:03d}",
                "claim": str(node.get("label", "")) if isinstance(node, Mapping) else str(node),
                "evidence_type": str(node.get("type", "unknown")) if isinstance(node, Mapping) else "unknown",
                "source_owner": "not provided",
                "verification_status": "needs owner validation",
                "next_control": "attach source reference, owner and timestamp before board or audit use",
            }
        )
    return {
        "custody_required": bool(custody_items or packet.get("missing_evidence")),
        "custody_items": custody_items,
        "missing_chain_links": list(packet.get("missing_evidence", []))[:8],
        "control_note": "Evidence is not board/audit ready until owner, source and timestamp are attached.",
    }


def _decision_rollback_planner(packet: Mapping[str, Any]) -> Dict[str, Any]:
    options = [str(option.get("option", option)) for option in packet.get("options", [])[:4]]
    if not options:
        options = ["approve with conditions", "defer", "descope", "escalate"]
    rollback_triggers = [
        "evidence gate missed",
        "customer impact exceeds tolerance",
        "control owner refuses sign-off",
        "cost or capacity breach crosses escalation threshold",
    ]
    return {
        "rollback_needed": any("approve" in option.lower() for option in options) or bool(packet.get("missing_evidence")),
        "decision_options": options,
        "rollback_triggers": rollback_triggers,
        "rollback_actions": [
            "pause approval path",
            "revert to prior operating state if available",
            "activate fallback owner and communication plan",
            "update decision memory with reason and lessons",
        ],
        "reversibility_note": "Rollback feasibility must be confirmed by accountable owners before approval.",
    }


def _autonomy_risk_budget(packet: Mapping[str, Any], actions: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    high = sum(1 for action in actions if action.get("risk_level") == "High")
    medium = sum(1 for action in actions if action.get("risk_level") == "Medium")
    l4 = sum(1 for action in actions if action.get("autonomy_level") == "L4 Human-Only")
    total = max(1, len(actions))
    used = min(100, high * 25 + medium * 12 + l4 * 15 + len(packet.get("missing_evidence", [])) * 8)
    return {
        "budget_used_percent": used,
        "remaining_percent": max(0, 100 - used),
        "risk_drivers": [
            f"high_risk_actions={high}",
            f"medium_risk_actions={medium}",
            f"human_only_actions={l4}",
            f"missing_evidence={len(packet.get('missing_evidence', []))}",
            f"total_actions={total}",
        ],
        "autonomy_posture": "Constrained" if used >= 70 else "Guarded" if used >= 40 else "Available",
        "budget_rule": "Do not increase autonomy while missing evidence, high-risk actions or L4 human-only controls dominate the review.",
    }


def _approval_boundary_mapper(packet: Mapping[str, Any], actions: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    boundaries = []
    for action in actions[:8]:
        boundaries.append(
            {
                "action_id": str(action.get("action_id", "")),
                "action": str(action.get("draft_action", "")),
                "autonomy_level": str(action.get("autonomy_level", "L1 Advise")),
                "required_approval": str(action.get("required_approval", "accountable owner")),
                "boundary": "human approval required" if action.get("autonomy_level") in {"L3 Ready for Governed Execution", "L4 Human-Only"} else "draft or advise only",
                "control": "record approver, evidence gate and residual-risk owner before execution",
            }
        )
    if not boundaries:
        boundaries.append(
            {
                "action_id": "BOUNDARY-001",
                "action": "confirm decision and approval path",
                "autonomy_level": "L1 Advise",
                "required_approval": _required_approver("Medium", str(packet.get("request_type", ""))),
                "boundary": "draft or advise only",
                "control": "name accountable owner before further automation",
            }
        )
    return {
        "boundary_count": len(boundaries),
        "approval_boundaries": boundaries,
        "human_only_domains": ["legal", "HR", "regulated financial reporting", "security exception acceptance", "external execution"],
        "boundary_rule": "The plugin may prepare and route decisions, but accountable humans approve controlled, regulated or irreversible actions.",
    }


def _evidence_expiry_monitor(packet: Mapping[str, Any]) -> Dict[str, Any]:
    evidence_nodes = packet.get("evidence_graph", {}).get("nodes", [])
    watched_items = []
    for index, node in enumerate(evidence_nodes[:6], start=1):
        label = str(node.get("label", node)) if isinstance(node, Mapping) else str(node)
        watched_items.append(
            {
                "evidence_id": f"EXP-{index:03d}",
                "evidence": label,
                "expiry_risk": "High" if any(term in label.lower() for term in ("forecast", "status", "date", "test", "budget")) else "Medium",
                "refresh_trigger": "before board, audit, approval gate or material context change",
                "owner_needed": "yes",
            }
        )
    for index, item in enumerate(packet.get("missing_evidence", [])[:4], start=len(watched_items) + 1):
        watched_items.append(
            {
                "evidence_id": f"EXP-{index:03d}",
                "evidence": str(item),
                "expiry_risk": "High",
                "refresh_trigger": "must be supplied before decision-ready status",
                "owner_needed": "yes",
            }
        )
    return {
        "expiry_monitor_required": bool(watched_items),
        "watched_items": watched_items,
        "refresh_cadence": "24h for Red items, 7d for Amber items, before every board/audit use",
        "staleness_rule": "Treat status, forecast, risk, control and customer-impact evidence as stale unless owner and timestamp are explicit.",
    }


def _residual_risk_contract(packet: Mapping[str, Any]) -> Dict[str, Any]:
    risk_items = []
    for index, path in enumerate(packet.get("risk_chain", [])[:5], start=1):
        risk_items.append(
            {
                "risk_id": f"RRC-{index:03d}",
                "residual_risk": str(path.get("business_impact", path)),
                "acceptance_owner": "not provided",
                "conditions": ["evidence gate passed", "owner sign-off recorded", "rollback trigger defined"],
                "review_trigger": "material change, missed control, customer impact or budget/capacity breach",
            }
        )
    if not risk_items and packet.get("missing_evidence"):
        risk_items.append(
            {
                "risk_id": "RRC-001",
                "residual_risk": "approval under missing evidence",
                "acceptance_owner": "not provided",
                "conditions": ["missing evidence closed or explicitly accepted", "expiry date set"],
                "review_trigger": "evidence remains unresolved at next checkpoint",
            }
        )
    return {
        "contract_required": bool(risk_items or packet.get("scorecard", {}).get("board_risk", {}).get("value", 0) >= 45),
        "residual_risks": risk_items,
        "minimum_contract_terms": [
            "risk owner",
            "accepted residual risk",
            "evidence basis",
            "expiry or review date",
            "rollback trigger",
            "communication obligation",
        ],
        "contract_note": "Residual risk acceptance is prepared as a draft contract; accountable leaders must approve it.",
    }


def _autonomy_stress_test(packet: Mapping[str, Any], actions: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    stressors = [
        "evidence changes after approval",
        "owner refuses sign-off",
        "customer impact becomes material",
        "regulator or audit asks for proof",
        "budget or capacity threshold is breached",
    ]
    high_risk = sum(1 for action in actions if action.get("risk_level") == "High")
    l4 = sum(1 for action in actions if action.get("autonomy_level") == "L4 Human-Only")
    score = min(100, 25 + high_risk * 15 + l4 * 10 + len(packet.get("missing_evidence", [])) * 8)
    return {
        "stress_score": score,
        "stress_posture": "Fail-close" if score >= 70 else "Tight guardrails" if score >= 45 else "Standard guardrails",
        "stressors": stressors,
        "failure_modes": [
            "draft becomes interpreted as approval",
            "missing evidence is treated as accepted risk",
            "human-only control is bypassed by urgency",
        ],
        "required_safeguards": [
            "explicit approver",
            "evidence gate",
            "rollback trigger",
            "human-only domain check",
        ],
    }


def _decision_consequence_ledger(packet: Mapping[str, Any]) -> Dict[str, Any]:
    options = [str(option.get("option", option)) for option in packet.get("options", [])[:4]] or ["approve with conditions", "defer", "descope"]
    consequences = []
    for index, option in enumerate(options, start=1):
        consequences.append(
            {
                "consequence_id": f"DCL-{index:03d}",
                "option": option,
                "first_order_effect": "changes approval path, delivery focus or risk posture",
                "second_order_effect": "affects capacity, confidence, vendor leverage or control exposure",
                "watch_metric": "decision readiness, board risk, value leakage or evidence confidence",
                "reversal_signal": "evidence, control or value assumption fails",
            }
        )
    return {
        "consequence_count": len(consequences),
        "consequences": consequences,
        "ledger_rule": "Do not approve a strategic option without naming second-order effects and reversal signals.",
    }


def _enterprise_friction_map(packet: Mapping[str, Any]) -> Dict[str, Any]:
    friction_domains = {
        "decision": _signals_containing(packet, {"decision", "approval", "owner", "escalation"}),
        "evidence": _signals_containing(packet, {"evidence", "missing", "audit", "control"}),
        "capacity": _signals_containing(packet, {"capacity", "resource", "architect", "team"}),
        "vendor": _signals_containing(packet, {"vendor", "supplier", "contract", "milestone"}),
        "value": _signals_containing(packet, {"value", "benefit", "budget", "forecast", "cost"}),
    }
    cells = []
    for domain, signals in friction_domains.items():
        cells.append(
            {
                "domain": domain,
                "friction_level": "High" if len(signals) >= 3 else "Medium" if signals else "Low",
                "signals": signals[:3],
                "unblocker": "name owner, evidence, decision forum and deadline",
            }
        )
    return {
        "friction_hotspots": [cell for cell in cells if cell["friction_level"] != "Low"],
        "friction_map": cells,
        "friction_rule": "Resolve decision, evidence and capacity friction before adding new scope.",
    }


def _strategic_optionality_engine(packet: Mapping[str, Any]) -> Dict[str, Any]:
    options = [str(option.get("option", option)) for option in packet.get("options", [])[:4]] or ["approve with conditions", "defer", "pause", "split decision"]
    option_set = []
    for index, option in enumerate(options, start=1):
        option_set.append(
            {
                "option_id": f"SOE-{index:03d}",
                "option": option,
                "optionality_effect": "preserves future choices" if any(term in option.lower() for term in ("defer", "pause", "split")) else "commits capacity and risk",
                "real_option_value": "High" if any(term in option.lower() for term in ("defer", "pause", "split")) else "Medium",
                "decision_deadline": "before evidence expires or cost-of-delay becomes material",
            }
        )
    return {
        "optionality_preserved": any(item["real_option_value"] == "High" for item in option_set),
        "options": option_set,
        "recommended_pattern": "preserve reversible options until evidence, owner accountability and value gates are stronger",
    }


def _control_debt_burndown(packet: Mapping[str, Any]) -> Dict[str, Any]:
    signals = _signals_containing(packet, {"control", "audit", "evidence", "access", "privacy", "compliance", "waiver", "exception"})
    items = []
    for index, signal in enumerate((signals or list(packet.get("missing_evidence", [])))[:6], start=1):
        items.append(
            {
                "control_debt_id": f"CDB-{index:03d}",
                "signal": str(signal),
                "debt_type": "missing evidence, weak owner, expired exception or incomplete control proof",
                "burndown_action": "assign owner, collect proof, set expiry and confirm residual risk",
                "target_window": "24h" if index <= 2 else "7d",
            }
        )
    return {
        "control_debt_count": len(items),
        "burndown_items": items,
        "burndown_rule": "Control debt must decrease before autonomy or approval confidence increases.",
    }


def _executive_dissent_synthesizer(packet: Mapping[str, Any]) -> Dict[str, Any]:
    personas = ["CFO", "CISO", "COO", "Audit", "Enterprise Architect", "Customer"]
    dissent = []
    missing = list(packet.get("missing_evidence", []))
    for index, persona in enumerate(personas, start=1):
        dissent.append(
            {
                "dissent_id": f"EDS-{index:03d}",
                "persona": persona,
                "objection": f"What would make this decision unsafe or premature for {persona}?",
                "weak_answer_risk": missing[0] if missing else "owner accountability and measurable value",
                "strong_answer_requirement": "evidence, owner, trade-off, residual risk and next checkpoint",
            }
        )
    return {
        "dissent_count": len(dissent),
        "dissent_items": dissent,
        "synthesis_rule": "Treat dissent as a design input for stronger decisions, not as meeting resistance.",
    }


def _decision_backtest_simulator(packet: Mapping[str, Any], memory: Mapping[str, Any]) -> Dict[str, Any]:
    prior_packets = list(memory.get("decision_packets", [])) if isinstance(memory, Mapping) else []
    current_signals = set(str(item).lower() for item in packet.get("facts", []) + packet.get("assumptions", []))
    matches = []
    for index, prior in enumerate(prior_packets[:5], start=1):
        prior_text = " ".join(str(value) for value in prior.values()).lower() if isinstance(prior, Mapping) else str(prior).lower()
        overlap = sum(1 for signal in current_signals if signal[:24] and signal[:24] in prior_text)
        matches.append(
            {
                "backtest_id": f"DBT-{index:03d}",
                "prior_decision": str(prior.get("decision_needed", prior.get("packet_id", "prior decision"))) if isinstance(prior, Mapping) else "prior decision",
                "pattern_overlap": overlap,
                "lesson_to_check": "compare assumptions, missed evidence, owner clarity and follow-up actions",
            }
        )
    return {
        "backtest_available": bool(matches),
        "matches": matches,
        "synthetic_backtest": [
            "If the same evidence gap existed last time, require stronger owner sign-off.",
            "If prior action tracking failed, lower autonomy and tighten operating rhythm.",
            "If value realization was weak, require measurable benefits before approval.",
        ],
        "backtest_rule": "Use prior decision memory as challenge material; do not treat it as deterministic prediction.",
    }


def _governance_drift_detector(packet: Mapping[str, Any], memory: Mapping[str, Any]) -> Dict[str, Any]:
    signals = _signals_containing(packet, {"exception", "waiver", "bypass", "urgent", "temporary", "owner", "approval", "governance"})
    prior_actions = list(memory.get("open_actions", [])) if isinstance(memory, Mapping) else []
    drift_items = []
    for index, signal in enumerate(signals[:6], start=1):
        drift_items.append(
            {
                "drift_id": f"GDD-{index:03d}",
                "signal": signal,
                "drift_type": "process bypass, recurring exception or unclear accountability",
                "correction": "restore decision forum, owner, expiry and evidence requirement",
            }
        )
    return {
        "drift_detected": bool(drift_items or prior_actions),
        "drift_items": drift_items,
        "open_action_pressure": len(prior_actions),
        "drift_rule": "Recurring exceptions and ownerless approvals are treated as governance drift until explicitly closed.",
    }


def _budget_shock_absorber(packet: Mapping[str, Any]) -> Dict[str, Any]:
    finance_signals = _signals_containing(packet, {"budget", "cost", "spend", "forecast", "reserve", "saving", "run-rate"})
    shock_level = "High" if len(finance_signals) >= 3 else "Medium" if finance_signals else "Low"
    return {
        "shock_level": shock_level,
        "finance_signals": finance_signals[:8],
        "absorption_moves": [
            "freeze low-evidence discretionary scope",
            "protect customer, control and resilience work",
            "renegotiate vendor milestones or payment triggers",
            "split irreversible decisions into staged gates",
        ],
        "tradeoff_questions": [
            "What value is protected by spending now?",
            "What risk increases if spend is deferred?",
            "Which commitments become irreversible?",
        ],
        "shock_rule": "Budget shocks should reduce optionality last and reduce low-evidence scope first.",
    }


def _vendor_leverage_index(packet: Mapping[str, Any]) -> Dict[str, Any]:
    signals = _signals_containing(packet, {"vendor", "supplier", "contract", "license", "milestone", "recovery", "dependency"})
    leverage_score = max(0, min(100, 70 - len(signals) * 8 + len(packet.get("missing_evidence", [])) * -3))
    return {
        "leverage_score": leverage_score,
        "leverage_posture": "Weak" if leverage_score < 40 else "Negotiable" if leverage_score < 70 else "Strong",
        "vendor_signals": signals[:8],
        "leverage_moves": [
            "tie recovery plan to evidence dates",
            "request commercial remedy for missed commitments",
            "create fallback or scope-reduction option",
            "separate strategic dependency from current incident pressure",
        ],
        "leverage_rule": "Vendor leverage weakens when evidence, fallback and milestone accountability are unclear.",
    }


def _executive_narrative_diff(packet: Mapping[str, Any], memory: Mapping[str, Any]) -> Dict[str, Any]:
    current = str(packet.get("situation", packet.get("decision_needed", "")))
    prior_packets = list(memory.get("decision_packets", [])) if isinstance(memory, Mapping) else []
    prior_summary = ""
    if prior_packets and isinstance(prior_packets[0], Mapping):
        prior_summary = str(prior_packets[0].get("situation", prior_packets[0].get("decision_needed", "")))
    diffs = []
    if packet.get("narrative_risk_detector"):
        diffs.append("current narrative has unsupported confidence or political framing risk")
    if packet.get("contradictions"):
        diffs.append("current narrative conflicts with provided signals")
    if prior_summary and current and prior_summary[:80] != current[:80]:
        diffs.append("current narrative differs from prior memory and should be reconciled")
    return {
        "diff_detected": bool(diffs),
        "current_narrative": current[:280],
        "prior_narrative": prior_summary[:280],
        "diffs": diffs,
        "reconciliation_questions": [
            "What changed since the prior narrative?",
            "Which assumption is no longer valid?",
            "Which owner accepts the revised position?",
        ],
        "diff_rule": "Narrative changes should be reconciled before board, audit or customer communication.",
    }


def _status_from_score(value: int, inverse: bool = False) -> str:
    if inverse:
        return "Red" if value >= 70 else "Amber" if value >= 45 else "Green"
    return "Green" if value >= 70 else "Amber" if value >= 45 else "Red"


def _signals_containing(packet: Mapping[str, Any], terms: set[str]) -> List[str]:
    signals = [str(item) for item in packet.get("facts", []) + packet.get("assumptions", []) + packet.get("missing_evidence", [])]
    return [signal for signal in signals if any(term in signal.lower() for term in terms)]


def _required_approver(risk_level: str, request_type: str) -> str:
    if risk_level == "High":
        if request_type == "AI Approval":
            return "AI governance board and data owner"
        if request_type == "Crisis Command":
            return "Crisis commander and executive sponsor"
        return "Executive sponsor"
    if risk_level == "Medium":
        return "Domain owner"
    return "Action owner"


def _autopilot_review_markdown(review: Mapping[str, Any]) -> str:
    lines = [
        "# Autonomous CIO Operating Review",
        "",
        f"**Generated On:** {review.get('generated_on', '')}",
        f"**Enterprise Status:** {review.get('enterprise_status', {}).get('overall', '')}",
        f"**Confidence:** {review.get('confidence', '')}",
        "",
        "## Executive Summary",
        str(review.get("decision_packet", {}).get("situation", "")),
        "",
        "## Decision Readiness",
        f"- Score: {review.get('decision_readiness', {}).get('value')}",
        f"- Reasons: {'; '.join(review.get('decision_readiness', {}).get('reasons', []))}",
        "",
        "## Attention Budget",
    ]
    for bucket in ("act_now", "escalate", "decide", "delegate", "monitor"):
        lines.append(f"### {bucket.replace('_', ' ').title()}")
        for item in review.get("attention_budget", {}).get(bucket, []):
            lines.append(f"- {item}")
    lines.extend(["", "## Risk Chain"])
    for path in review.get("risk_chain", []):
        lines.append(f"- {path.get('signal')} -> {path.get('dependency')} -> {path.get('business_impact')}")
    lines.extend(["", "## Board Questions"])
    for question in review.get("board_questions", []):
        lines.append(f"- {question}")
    lines.extend(["", "## Action Ledger"])
    for action in review.get("action_ledger", []):
        lines.append(
            f"- {action.get('action_id')}: {action.get('draft_action')} "
            f"[{action.get('autonomy_level')}, approval: {action.get('required_approval')}]"
        )
    lines.extend(["", "## CIO Shadow Agenda"])
    for item in review.get("cio_shadow_agenda", []):
        lines.append(f"- {item.get('rank')}. {item.get('topic')} [{item.get('recommended_posture')}]")
    lines.extend(["", "## Risk Chain Forecast"])
    for item in review.get("risk_chain_forecast", []):
        lines.append(f"- {item.get('current_signal')} -> {item.get('likely_next_escalation')}")
    lines.extend(["", "## Human Control Contract"])
    lines.append(str(review.get("human_control_contract", {}).get("human_control_statement", "")))
    lines.extend(["", "## Decision SLA"])
    sla = review.get("decision_sla_enforcer", {})
    lines.append(f"- SLA: {sla.get('recommended_decision_sla')} [{sla.get('breach_risk')}]")
    lines.extend(["", "## CIO OS Maturity"])
    maturity = review.get("cio_os_maturity_index", {})
    lines.append(f"- Score: {maturity.get('score')} ({maturity.get('maturity_level')})")
    lines.extend(["", "## Stakeholder Alignment"])
    alignment = review.get("stakeholder_alignment_matrix", {})
    lines.append(f"- Status: {alignment.get('alignment_status')}")
    lines.extend(["", "## Operating Rhythm Autopilot"])
    rhythm = review.get("operating_rhythm_autopilot", {})
    lines.append(f"- Cadence: {rhythm.get('recommended_cadence')}")
    lines.extend(["", "## Escalation Drafts"])
    for draft in review.get("autonomous_escalation_drafts", [])[:5]:
        lines.append(f"- {draft.get('draft_id')}: {draft.get('subject')}")
    lines.extend(["", "## Enterprise Control Tower"])
    tower = review.get("enterprise_control_tower", {})
    lines.append(f"- Overall: {tower.get('overall_status')}")
    lines.extend(["", "## Executive Narrative"])
    narrative = review.get("executive_narrative_generator", {})
    lines.append(f"- {narrative.get('board_narrative')}")
    lines.extend(["", "## Due Diligence Questions"])
    ddq = review.get("autonomous_due_diligence_questions", {})
    lines.append(f"- Count: {ddq.get('question_count')}")
    lines.extend(["", "## Resilience Continuity"])
    resilience = review.get("resilience_continuity_planner", {})
    lines.append(f"- Pressure: {resilience.get('resilience_pressure')}")
    lines.extend(["", "## Cost of Delay"])
    delay = review.get("cost_of_delay_calculator", {})
    lines.append(f"- Qualitative cost: {delay.get('qualitative_cost_of_delay')}")
    lines.extend(["", "## Decision Rights"])
    rights = review.get("decision_rights_mapper", {})
    lines.append(f"- Rights clarity: {rights.get('rights_clarity')}")
    lines.extend(["", "## Dependency Breakpoints"])
    breakpoints = review.get("dependency_breakpoint_analyzer", {})
    lines.append(f"- Count: {breakpoints.get('breakpoint_count')}")
    lines.extend(["", "## Transformation Kill Criteria"])
    kill = review.get("transformation_kill_criteria", {})
    lines.append(f"- Pressure: {kill.get('kill_pressure')}")
    lines.extend(["", "## Roadmap Reprioritizer"])
    roadmap = review.get("autonomous_roadmap_reprioritizer", {})
    lines.append(f"- Required: {roadmap.get('reprioritization_required')}")
    lines.extend(["", "## Audit Finding Predictor"])
    audit = review.get("audit_finding_predictor", {})
    lines.append(f"- Risk: {audit.get('finding_risk')}")
    lines.extend(["", "## Decision War Room"])
    war_room = review.get("executive_decision_war_room", {})
    lines.append(f"- Required: {war_room.get('war_room_required')}")
    lines.extend(["", "## Evidence Chain of Custody"])
    custody = review.get("evidence_chain_of_custody", {})
    lines.append(f"- Required: {custody.get('custody_required')}")
    lines.extend(["", "## Autonomy Risk Budget"])
    budget = review.get("autonomy_risk_budget", {})
    lines.append(f"- Used: {budget.get('budget_used_percent')}% [{budget.get('autonomy_posture')}]")
    lines.extend(["", "## Approval Boundary Mapper"])
    boundary = review.get("approval_boundary_mapper", {})
    lines.append(f"- Boundaries: {boundary.get('boundary_count')}")
    lines.extend(["", "## Evidence Expiry Monitor"])
    expiry = review.get("evidence_expiry_monitor", {})
    lines.append(f"- Required: {expiry.get('expiry_monitor_required')}")
    lines.extend(["", "## Residual Risk Contract"])
    residual = review.get("residual_risk_contract", {})
    lines.append(f"- Required: {residual.get('contract_required')}")
    lines.extend(["", "## Autonomy Stress Test"])
    stress = review.get("autonomy_stress_test", {})
    lines.append(f"- Score: {stress.get('stress_score')} [{stress.get('stress_posture')}]")
    lines.extend(["", "## Decision Consequence Ledger"])
    consequence = review.get("decision_consequence_ledger", {})
    lines.append(f"- Consequences: {consequence.get('consequence_count')}")
    lines.extend(["", "## Enterprise Friction Map"])
    friction = review.get("enterprise_friction_map", {})
    lines.append(f"- Hotspots: {len(friction.get('friction_hotspots', []))}")
    lines.extend(["", "## Strategic Optionality Engine"])
    optionality = review.get("strategic_optionality_engine", {})
    lines.append(f"- Optionality preserved: {optionality.get('optionality_preserved')}")
    lines.extend(["", "## Control Debt Burndown"])
    control_debt = review.get("control_debt_burndown", {})
    lines.append(f"- Items: {control_debt.get('control_debt_count')}")
    lines.extend(["", "## Executive Dissent Synthesizer"])
    dissent = review.get("executive_dissent_synthesizer", {})
    lines.append(f"- Dissent items: {dissent.get('dissent_count')}")
    lines.extend(["", "## Decision Backtest Simulator"])
    backtest = review.get("decision_backtest_simulator", {})
    lines.append(f"- Available: {backtest.get('backtest_available')}")
    lines.extend(["", "## Governance Drift Detector"])
    drift = review.get("governance_drift_detector", {})
    lines.append(f"- Drift detected: {drift.get('drift_detected')}")
    lines.extend(["", "## Budget Shock Absorber"])
    shock = review.get("budget_shock_absorber", {})
    lines.append(f"- Shock level: {shock.get('shock_level')}")
    lines.extend(["", "## Vendor Leverage Index"])
    vendor = review.get("vendor_leverage_index", {})
    lines.append(f"- Leverage: {vendor.get('leverage_score')} [{vendor.get('leverage_posture')}]")
    lines.extend(["", "## Executive Narrative Diff"])
    diff = review.get("executive_narrative_diff", {})
    lines.append(f"- Diff detected: {diff.get('diff_detected')}")
    lines.extend(["", "## Missing Evidence"])
    for item in review.get("missing_evidence", []):
        lines.append(f"- {item}")
    lines.extend(["", "## Guardrails"])
    for item in review.get("guardrails", []):
        lines.append(f"- {item}")
    return "\n".join(lines)


def _board_pack_markdown(packet: Mapping[str, Any], review: Mapping[str, Any]) -> str:
    lines = [
        "# Board Decision Pack",
        "",
        f"Decision needed: {packet.get('decision_needed', '')}",
        f"Request type: {packet.get('request_type', '')}",
        f"Confidence: {packet.get('confidence', '')}",
        "",
        "## Recommended Action",
        str(packet.get("recommended_action", {}).get("recommendation", "")),
        "",
        "## Facts",
    ]
    lines.extend(f"- {item}" for item in packet.get("facts", [])[:10])
    lines.extend(["", "## Assumptions"])
    lines.extend(f"- {item}" for item in packet.get("assumptions", [])[:8])
    lines.extend(["", "## Risk Chain"])
    for item in packet.get("risk_chain", [])[:8]:
        lines.append(f"- {item.get('signal')} -> {item.get('dependency')} -> {item.get('business_impact')}")
    lines.extend(["", "## Board Challenge Questions"])
    lines.extend(f"- {item}" for item in packet.get("board_challenge_questions", [])[:10])
    lines.extend(["", "## Enterprise Status"])
    status = review.get("enterprise_status", {})
    if isinstance(status, Mapping):
        lines.append(f"- Overall: {status.get('overall', '')}")
        lines.append(f"- Rationale: {status.get('rationale', '')}")
    lines.extend(["", "## Missing Evidence"])
    lines.extend(f"- {item}" for item in packet.get("missing_evidence", [])[:10])
    return "\n".join(lines)


def _audit_pack_markdown(packet: Mapping[str, Any]) -> str:
    lines = [
        "# Audit Evidence Pack",
        "",
        "This pack is decision support and does not replace specialist audit, legal, security or regulatory review.",
        "",
        "## Evidence Nodes",
    ]
    for node in packet.get("evidence_graph", {}).get("nodes", [])[:20]:
        lines.append(f"- {node.get('id')}: {node.get('type')} | {node.get('confidence')} | {node.get('label')}")
    lines.extend(["", "## Control Map"])
    control_map = packet.get("governance_control_map", [])
    for item in control_map[:12] if isinstance(control_map, list) else []:
        lines.append(f"- {item.get('control_area')}: {item.get('readiness')} | {item.get('evidence_needed')}")
    lines.extend(["", "## Missing Evidence"])
    lines.extend(f"- {item}" for item in packet.get("missing_evidence", [])[:12])
    lines.extend(["", "## Guardrails"])
    lines.extend(f"- {item}" for item in packet.get("guardrails", []))
    return "\n".join(lines)


def _deck_outline_markdown(packet: Mapping[str, Any], review: Mapping[str, Any]) -> str:
    scores = packet.get("scorecard", {})
    lines = [
        "# Steering Committee Deck Outline",
        "",
        "## Slide 1 - Decision Required",
        str(packet.get("decision_needed", "")),
        "",
        "## Slide 2 - Readiness Scores",
    ]
    for key, score in scores.items():
        value = score.get("value") if isinstance(score, Mapping) else score
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Slide 3 - Facts vs Assumptions"])
    lines.append(f"- Facts: {len(packet.get('facts', []))}")
    lines.append(f"- Assumptions: {len(packet.get('assumptions', []))}")
    lines.append(f"- Missing evidence: {len(packet.get('missing_evidence', []))}")
    lines.extend(["", "## Slide 4 - Risk Chain"])
    for item in packet.get("risk_chain", [])[:5]:
        lines.append(f"- {item.get('signal')} -> {item.get('business_impact')}")
    lines.extend(["", "## Slide 5 - Recommended Action"])
    lines.append(str(packet.get("recommended_action", {}).get("recommendation", "")))
    lines.extend(["", "## Slide 6 - Action Ledger"])
    for item in review.get("action_ledger", [])[:8]:
        lines.append(f"- {item.get('action_id')}: {item.get('draft_action')}")
    return "\n".join(lines)


def _action_ledger_csv(actions: Sequence[Mapping[str, Any]]) -> str:
    headers = ["action_id", "draft_action", "risk_level", "required_approver_role", "autonomy_level", "automation_allowed", "audit_event"]
    rows = [",".join(headers)]
    for action in actions:
        values = []
        for header in headers:
            raw = str(action.get(header, "")).replace('"', '""')
            values.append(f'"{raw}"')
        rows.append(",".join(values))
    return "\n".join(rows) + "\n"


def _write_docx(path: Path, paragraphs: Sequence[str]) -> None:
    document = "".join(
        f"<w:p><w:r><w:t>{escape(str(paragraph))}</w:t></w:r></w:p>"
        for paragraph in paragraphs
    )
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "[Content_Types].xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>""",
        )
        archive.writestr(
            "_rels/.rels",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>""",
        )
        archive.writestr(
            "word/document.xml",
            f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>{document}<w:sectPr/></w:body>
</w:document>""",
        )


def _write_pptx(path: Path, slides: Sequence[tuple[str, Sequence[str]]]) -> None:
    slide_overrides = "\n".join(
        f'  <Override PartName="/ppt/slides/slide{idx}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for idx in range(1, len(slides) + 1)
    )
    slide_ids = "\n".join(
        f'    <p:sldId id="{255 + idx}" r:id="rId{idx}"/>'
        for idx in range(1, len(slides) + 1)
    )
    presentation_rels = "\n".join(
        f'  <Relationship Id="rId{idx}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{idx}.xml"/>'
        for idx in range(1, len(slides) + 1)
    )
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "[Content_Types].xml",
            f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
{slide_overrides}
</Types>""",
        )
        archive.writestr(
            "_rels/.rels",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>""",
        )
        archive.writestr(
            "ppt/_rels/presentation.xml.rels",
            f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
{presentation_rels}
</Relationships>""",
        )
        archive.writestr(
            "ppt/presentation.xml",
            f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <p:sldIdLst>
{slide_ids}
  </p:sldIdLst>
  <p:sldSz cx="12192000" cy="6858000" type="screen16x9"/>
</p:presentation>""",
        )
        for idx, (title, bullets) in enumerate(slides, start=1):
            archive.writestr(f"ppt/slides/slide{idx}.xml", _slide_xml(title, bullets))


def _slide_xml(title: str, bullets: Sequence[str]) -> str:
    bullet_text = "\n".join(
        f'<a:p><a:r><a:t>{escape(str(item)[:220])}</a:t></a:r></a:p>'
        for item in bullets[:8]
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr/>
      <p:sp>
        <p:nvSpPr><p:cNvPr id="2" name="Title"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="457200" y="274320"/><a:ext cx="11277600" cy="914400"/></a:xfrm></p:spPr>
        <p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:r><a:t>{escape(str(title))}</a:t></a:r></a:p></p:txBody>
      </p:sp>
      <p:sp>
        <p:nvSpPr><p:cNvPr id="3" name="Body"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="685800" y="1371600"/><a:ext cx="10668000" cy="4572000"/></a:xfrm></p:spPr>
        <p:txBody><a:bodyPr/><a:lstStyle/>{bullet_text}</p:txBody>
      </p:sp>
    </p:spTree>
  </p:cSld>
</p:sld>"""


def _packet_markdown(packet: Mapping[str, Any]) -> str:
    lines = [
        "# Executive Decision Packet",
        "",
        f"**Request Type:** {packet.get('request_type', '')}",
        f"**Decision Needed:** {packet.get('decision_needed', '')}",
        f"**Confidence:** {packet.get('confidence', '')}",
        "",
        "## Recommended Action",
        str(packet.get("recommended_action", {}).get("recommendation", "")),
        "",
        "## Scorecard",
    ]
    for key, value in packet.get("scorecard", {}).items():
        lines.append(f"- {key}: {value.get('value')} ({'; '.join(value.get('reasons', []))})")
    lines.extend(["", "## Risk Chain"])
    for path in packet.get("risk_chain", []):
        lines.append(f"- {path.get('signal')} -> {path.get('dependency')} -> {path.get('business_impact')}")
    lines.extend(["", "## Missing Evidence"])
    for item in packet.get("missing_evidence", []):
        lines.append(f"- {item}")
    lines.extend(["", "## Guardrails"])
    for item in packet.get("guardrails", []):
        lines.append(f"- {item}")
    return "\n".join(lines)


def _decision_timeline(memory: Mapping[str, Any]) -> List[Dict[str, Any]]:
    decisions = []
    for item in memory.get("decision_memory", []):
        decisions.append(
            {
                "date": item.get("date") or item.get("review_date") or "unknown",
                "decision": item.get("decision", ""),
                "status": item.get("status", "unknown"),
                "owner": item.get("owner", "unknown"),
            }
        )
    return sorted(decisions, key=lambda item: item["date"])


def _request_type(ctx: Mapping[str, Any]) -> str:
    text = " ".join([ctx["title"], ctx["decision_request"], *ctx["items"]]).lower()
    if "outage" in text or "crisis" in text or "eta" in text:
        return "Crisis Command"
    if "ai " in text or "llm" in text or "model" in text:
        return "AI Approval"
    if "board" in text or "approve" in text or "approval" in text:
        return "Board Prep"
    if "transformation" in text or "adoption" in text or "value leakage" in text:
        return "Transformation Value"
    if "portfolio" in text or "project" in text:
        return "Portfolio Decision"
    return "General Executive Decision"


def _selected_chain(request_type: str) -> List[str]:
    base = ["enterprise-signal-ranking", "executive-truth-layer", "risk-chain-intelligence"]
    if request_type == "AI Approval":
        return ["ai-governance-intelligence", "assumption-mining-engine", "governance-gap-predictor", "executive-decision-packet"]
    if request_type == "Crisis Command":
        return ["crisis-command-mode", "risk-chain-intelligence", "management-attention-optimizer", "executive-decision-packet"]
    if request_type == "Transformation Value":
        return ["transformation-value-tracker", "value-leakage-intelligence", "decision-debt-intelligence", "executive-decision-packet"]
    return base + ["decision-scenario-intelligence", "executive-decision-packet"]


def _why_chain(request_type: str) -> str:
    return {
        "Crisis Command": "Crisis context needs fact separation, command roles, risk propagation and fast draft actions.",
        "AI Approval": "AI approval needs value, data risk, controls, owner readiness and missing evidence review.",
        "Transformation Value": "Transformation context needs value leakage, decision debt and benefit gate analysis.",
        "Board Prep": "Board context needs truth classification, risk chain, options and challenge questions.",
    }.get(request_type, "Mixed executive context needs signal ranking, truth classification, risk chain and options.")


def _decision_needed(ctx: Mapping[str, Any], request_type: str) -> str:
    if ctx["decision_request"]:
        return ctx["decision_request"]
    return {
        "Crisis Command": "Approve immediate crisis posture, communication approach and next operational decisions.",
        "AI Approval": "Approve, defer or conditionally approve the AI use case.",
        "Transformation Value": "Continue, pause or reset transformation work based on value evidence.",
        "Board Prep": "Approve the board narrative, revise it or escalate material risks.",
    }.get(request_type, "Decide whether to proceed, defer, escalate or approve with conditions.")


def _situation(ctx: Mapping[str, Any]) -> str:
    top = ctx["items"][:3]
    if not top:
        return "No detailed context was provided; decision packet confidence is low."
    return " ".join(top)


def _weak_signals(ctx: Mapping[str, Any]) -> List[str]:
    return [item for item in ctx["items"] if any(term in item.lower() for term in RISK_TERMS)][:8]


def _contradictions(ctx: Mapping[str, Any]) -> List[str]:
    text = " ".join(ctx["items"]).lower()
    contradictions = []
    if ("red" in text or "late" in text or "incomplete" in text) and ("under control" in text or "on track" in text):
        contradictions.append("Positive delivery narrative conflicts with red, late or incomplete evidence.")
    if "no baseline" in text and ("20%" in text or "improvement" in text):
        contradictions.append("Quantified value claim lacks a baseline.")
    return contradictions


def _decision_debt(ctx: Mapping[str, Any]) -> List[str]:
    debt = []
    for item in ctx["items"]:
        low = item.lower()
        if "not approved" in low or "owner" in low and "no " in low or "unclear" in low:
            debt.append(item)
    if ctx["decision_request"]:
        debt.append(f"Open decision: {ctx['decision_request']}")
    return _unique(debt)[:8]


def _options(ctx: Mapping[str, Any], request_type: str) -> List[Dict[str, str]]:
    return [
        {
            "option": "Proceed now",
            "benefit": "Maintains momentum.",
            "risk": "May accept unresolved evidence, risk or value gaps.",
            "dependency": "Executive risk acceptance.",
            "reversibility": "Low",
            "confidence": "Low",
        },
        {
            "option": "Defer",
            "benefit": "Protects quality, controls and decision confidence.",
            "risk": "May create delay cost, stakeholder pressure or missed timeline.",
            "dependency": "Revised plan and owner accountability.",
            "reversibility": "Medium",
            "confidence": "Medium",
        },
        {
            "option": "Approve with conditions",
            "benefit": "Keeps momentum while forcing evidence gates.",
            "risk": "Needs disciplined follow-up and clear stop criteria.",
            "dependency": "Named owners, evidence gates and review date.",
            "reversibility": "Medium",
            "confidence": "Medium",
        },
    ]


def _board_questions(ctx: Mapping[str, Any], request_type: str) -> List[str]:
    return [
        "CEO: What decision is needed now, and what happens if we wait?",
        "CFO: What are the cost, forecast and value implications?",
        "CISO: What security or control risk is being accepted?",
        "Audit / Risk: Which evidence is missing, and who owns it?",
        "Customer / Regulator: What external impact or obligation could be triggered?",
    ]


def _recommended_action(ctx: Mapping[str, Any], request_type: str, scorecard: Mapping[str, Any]) -> Dict[str, Any]:
    readiness = int(scorecard["decision_readiness"]["value"])
    board_risk = int(scorecard["board_risk"]["value"])
    if readiness < 45 or board_risk > 70:
        recommendation = "Defer or escalate until missing evidence and owner accountability are resolved."
    elif readiness < 70:
        recommendation = "Approve with explicit evidence gates, owners and review date."
    else:
        recommendation = "Proceed with documented safeguards and monitoring."
    return {
        "recommendation": recommendation,
        "owner": "Executive sponsor with relevant domain owners",
        "first_action": "Run a 24-hour evidence and owner confirmation review.",
        "confidence": _confidence(scorecard["evidence_confidence"]["value"]),
    }


def _next_steps(request_type: str) -> Dict[str, List[str]]:
    return {
        "next_24h": [
            "Confirm decision owner, affected domains and missing evidence.",
            "Request source evidence from accountable owners.",
            "Draft decision language with explicit assumptions and guardrails.",
        ],
        "next_7d": [
            "Run evidence gate review.",
            "Resolve or escalate decision debt.",
            "Update decision packet with owner sign-off and residual risk.",
        ],
        "next_30d": [
            "Review outcomes against expected value and risk reduction.",
            "Update decision memory, assumption register and action ledger if the user chooses to persist them.",
        ],
    }


def _memory_matches(items: Iterable[Any], memory_items: Iterable[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    matches = []
    item_text = " ".join(str(item).lower() for item in items)
    for memory in memory_items:
        text = " ".join(str(value).lower() for value in memory.values())
        shared = set(item_text.split()) & set(text.split())
        if len(shared) >= 2:
            matches.append(dict(memory))
    return matches[:8]


def _count_terms(text: str, terms: Iterable[str]) -> int:
    return sum(1 for term in terms if term in text)


def _bounded(value: int) -> int:
    return max(0, min(100, int(value)))


def _confidence(score: int) -> str:
    if score >= 70:
        return "High"
    if score >= 45:
        return "Medium"
    return "Low"


def _confidence_value(confidence: str) -> int:
    return {"High": 82, "Medium": 55, "Low": 30, "Unknown": 15}.get(confidence, 25)


def _dedupe_dicts(items: Iterable[Mapping[str, str]], key: str) -> List[Dict[str, str]]:
    seen = set()
    result = []
    for item in items:
        marker = str(item.get(key, "")).lower()
        if marker and marker not in seen:
            seen.add(marker)
            result.append(dict(item))
    return result


def _unique(items: Iterable[str]) -> List[str]:
    seen = set()
    result = []
    for item in items:
        normalized = item.strip()
        key = normalized.lower()
        if normalized and key not in seen:
            seen.add(key)
            result.append(normalized)
    return result
