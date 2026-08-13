"""High-differentiation local USP modules for The Autonomous CIO."""

from __future__ import annotations

from contextlib import contextmanager
from datetime import date, datetime, timedelta
import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, Mapping

try:
    from decision_intelligence_engine import build_autopilot_review, build_decision_packet
    from memory_store import init_memory_db, memory_aging
except ImportError:
    from .decision_intelligence_engine import build_autopilot_review, build_decision_packet
    from .memory_store import init_memory_db, memory_aging


GUARDRAILS = [
    "Uses only user-provided local context and optional local SQLite memory.",
    "Does not claim live system access.",
    "Does not persist memory automatically.",
    "Does not execute external actions.",
    "Does not train or update an external model.",
    "High-risk domain outputs are decision support, not final specialist determinations.",
]


def build_enterprise_operating_twin(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    review = build_autopilot_review(input_context)
    memory = _memory_snapshot(db_path)
    payload = {
        "systems": _signals(input_context, ["erp", "crm", "cloud", "identity", "network", "platform", "data", "manufacturing"]),
        "owners": sorted({_owner_for(item) for item in packet.get("missing_evidence", []) + packet.get("draft_next_steps", {}).get("next_24h", [])}),
        "vendors": _signals(input_context, ["vendor", "supplier", "partner", "contract", "milestone"]),
        "controls": _signals(input_context, ["audit", "control", "privacy", "security", "change", "evidence"]),
        "risk_chains": packet.get("risk_chain", []),
        "decision_backlog": review.get("executive_decision_backlog", {}),
        "memory_counts": memory["counts"],
        "operating_model_completeness": _score(35 + len(packet.get("facts", [])) * 6 + len(packet.get("risk_chain", [])) * 8 + sum(1 for v in memory["counts"].values() if v) * 7),
    }
    return _with_packet("Enterprise Operating Twin", payload, packet, "Use the twin as the local CIO operating model before adding more automation.")


def build_autonomy_contract_engine(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    review = build_autopilot_review(input_context)
    text = _text(input_context)
    domains = {
        "human_only": ["legal", "regulatory", "privacy", "security", "board approval", "risk acceptance"],
        "approval_required": ["budget", "vendor", "go-live", "change", "architecture"],
        "draft_allowed": ["email", "brief", "summary", "task", "question"],
        "suggest_only": ["strategy", "roadmap", "operating model", "portfolio"],
    }
    clauses = []
    for level, words in domains.items():
        hits = _signals(input_context, words)
        if hits:
            clauses.append({"autonomy_level": level, "trigger_terms": hits, "approval_gate": level in {"human_only", "approval_required"}, "external_execution_allowed": False})
    if not clauses:
        clauses.append({"autonomy_level": "draft_allowed", "trigger_terms": ["default local analysis"], "approval_gate": True, "external_execution_allowed": False})
    payload = {
        "contract_status": "Restricted autonomy",
        "clauses": clauses,
        "autonomy_gate": review.get("autonomy_gate", {}),
        "risk_budget": review.get("autonomy_risk_budget", {}),
        "detected_high_risk_terms": _signals(input_context, ["security", "privacy", "audit", "financial", "regulatory", "customer"]),
        "context_signal_count": len(text.split()),
    }
    return _with_packet("Autonomy Contract Engine", payload, packet, "Approve the autonomy contract before converting drafts into assigned work.")


def build_decision_chain_of_custody(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    nodes = []
    for idx, fact in enumerate(packet.get("facts", []), start=1):
        nodes.append({"custody_id": f"FACT-{idx:03d}", "type": "fact", "claim": fact, "source": "provided_context", "version": 1})
    for idx, assumption in enumerate(packet.get("assumptions", []), start=1):
        nodes.append({"custody_id": f"ASM-{idx:03d}", "type": "assumption", "claim": assumption, "source": "engine_classification", "version": 1})
    for idx, gap in enumerate(packet.get("missing_evidence", []), start=1):
        nodes.append({"custody_id": f"GAP-{idx:03d}", "type": "missing_evidence", "claim": gap, "source": "engine_gap_analysis", "version": 1})
    payload = {
        "chain": nodes,
        "chain_count": len(nodes),
        "packet_fingerprint": _fingerprint(packet),
        "review_required": True,
        "audit_posture": "Traceable with missing evidence" if packet.get("missing_evidence") else "Traceable",
    }
    return _with_packet("Decision Chain of Custody", payload, packet, "Attach the custody chain to board or audit-facing decision packets.")


def allocate_executive_attention(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    review = build_autopilot_review(input_context)
    memory = _memory_snapshot(db_path)
    categories = {
        "board_risk": _score(packet.get("scorecard", {}).get("board_risk", {}).get("value", 0)),
        "value_leakage": _score(packet.get("scorecard", {}).get("value_leakage", {}).get("value", 0)),
        "decision_debt": _score(len(review.get("decision_debt_ledger", [])) * 18),
        "vendor_pressure": _score(len(_signals(input_context, ["vendor", "supplier", "contract", "milestone"])) * 25),
        "control_debt": _score(len(review.get("control_debt_burndown", {}).get("control_debt_items", [])) * 20 + memory["aging_pressure"]),
    }
    allocation = sorted(({"topic": key, "attention_score": value, "recommended_minutes": max(15, round(value / 2))} for key, value in categories.items()), key=lambda item: item["attention_score"], reverse=True)
    payload = {"allocation": allocation, "top_focus": allocation[0]["topic"], "total_recommended_minutes": sum(item["recommended_minutes"] for item in allocation)}
    return _with_packet("Executive Attention Allocator", payload, packet, "Spend CIO attention on the highest pressure item before broad status review.")


def build_kill_criteria_sentinel(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    review = build_autopilot_review(input_context)
    text = _text(input_context)
    criteria = [
        {"trigger": "testing_not_started_near_go_live", "active": "testing has not started" in text or ("go-live" in text and "testing" in text), "recommended_response": "Pause or re-scope go-live until test evidence exists."},
        {"trigger": "budget_reserve_consumed", "active": _hits(text, ["reserve", "over forecast", "budget pressure"]) >= 2, "recommended_response": "Stop scope expansion until funding decision is explicit."},
        {"trigger": "control_evidence_incomplete", "active": _hits(text, ["audit", "control", "incomplete", "missing evidence"]) >= 3, "recommended_response": "Block approval until control evidence is ready or risk is accepted."},
        {"trigger": "vendor_recovery_unproven", "active": _hits(text, ["vendor", "slipped", "delayed", "no evidence"]) >= 2, "recommended_response": "Require vendor recovery proof before additional commitment."},
    ]
    active = [item for item in criteria if item["active"]]
    payload = {
        "criteria": criteria,
        "active_kill_criteria": active,
        "kill_pressure": "High" if len(active) >= 2 else "Medium" if active else "Low",
        "transformation_kill_criteria": review.get("transformation_kill_criteria", {}),
    }
    return _with_packet("Kill-Criteria Sentinel", payload, packet, "Make stop, pause and re-scope thresholds explicit before the next steering decision.")


def build_benefit_realization_memory(db_path: str) -> Dict[str, Any]:
    init_memory_db(db_path)
    with _connect(db_path) as conn:
        decisions = _rows(conn, "select * from decisions order by id desc limit 50")
        outcomes = _rows(conn, "select * from outcomes order by id desc limit 50")
        reviews = _rows(conn, "select id,title,payload,created_on from reviews order by id desc limit 25")
    linked = []
    for decision in decisions:
        matching = [outcome for outcome in outcomes if _overlap(decision.get("decision", ""), outcome.get("decision", ""))]
        linked.append({"decision": decision.get("decision", ""), "owner": decision.get("owner", ""), "outcome_count": len(matching), "value_result": matching[0].get("value_result", "Missing outcome") if matching else "Missing outcome", "benefit_status": "Measured" if matching else "Unproven"})
    payload = {"db_path": db_path, "benefits": linked, "decision_count": len(decisions), "outcome_count": len(outcomes), "review_count": len(reviews), "unproven_benefit_count": sum(1 for item in linked if item["benefit_status"] == "Unproven")}
    return _result("Benefit Realization Memory", payload, [f"Compared {len(decisions)} decision(s) with {len(outcomes)} recorded outcome(s)."], "Record outcomes for decisions with unproven benefits.")


def detect_strategic_drift_early_warning(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    text = _text(input_context)
    drift_items = []
    checks = [
        ("strategy_vs_budget", ["strategy", "priority", "growth"], ["budget", "reserve", "cut", "over forecast"]),
        ("security_vs_speed", ["security", "control", "risk reduction"], ["accelerate", "go-live", "deadline"]),
        ("architecture_vs_delivery", ["architecture", "standard", "platform"], ["exception", "temporary", "workaround"]),
        ("vendor_vs_operating_model", ["vendor", "supplier"], ["internal owner", "ownership unclear", "no owner"]),
    ]
    for name, strategic, operational in checks:
        if _hits(text, strategic) and _hits(text, operational):
            drift_items.append({"drift": name, "severity": "High", "strategy_signal": strategic[0], "operating_signal": operational[0]})
    memory = _memory_snapshot(db_path)
    payload = {"drift_items": drift_items, "drift_count": len(drift_items), "memory_aging_pressure": memory["aging_pressure"], "warning_level": "High" if len(drift_items) >= 2 or memory["aging_pressure"] >= 50 else "Medium" if drift_items else "Low"}
    return _with_packet("Strategic Drift Early Warning", payload, packet, "Resolve strategy/operating drift before committing additional scope or spend.")


def backtest_vendor_promises(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    text = _text(input_context)
    promises = _sentences(input_context, ["vendor", "supplier", "milestone", "commit", "contract"])
    weak = _sentences(input_context, ["slipped", "delayed", "missed", "unknown", "no evidence", "unproven"])
    memory = _memory_snapshot(db_path)
    score = _score(80 - len(weak) * 14 - len(packet.get("missing_evidence", [])) * 4 + min(10, memory["counts"].get("outcomes", 0) * 3))
    payload = {
        "vendor_promises": promises[:10],
        "contrary_signals": weak[:10],
        "promise_reliability_score": score,
        "negotiation_posture": "Use as leverage" if score < 55 else "Challenge selectively" if score < 75 else "Evidence-backed",
        "memory_outcome_count": memory["counts"].get("outcomes", 0),
        "vendor_signal_terms": _signals(input_context, ["vendor", "supplier", "contract", "milestone"]),
        "context_signal_count": len(text.split()),
    }
    return _with_packet("Vendor Promise Backtester", payload, packet, "Use the backtest as negotiation material, not as a final vendor determination.")


def measure_decision_latency_cost(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    text = _text(input_context)
    delay_signals = _hits(text, ["delayed", "waiting", "defer", "not approved", "blocked", "pending"])
    board_risk = packet.get("scorecard", {}).get("board_risk", {}).get("value", 0)
    value_leakage = packet.get("scorecard", {}).get("value_leakage", {}).get("value", 0)
    daily_pressure = _score(delay_signals * 8 + board_risk * 0.25 + value_leakage * 0.25)
    payload = {
        "delay_signal_count": delay_signals,
        "daily_pressure_score": daily_pressure,
        "seven_day_compounded_pressure": _score(daily_pressure + 15),
        "thirty_day_compounded_pressure": _score(daily_pressure + 35),
        "cost_domains": _cost_domains(input_context),
        "recommended_decision_sla": "24h" if daily_pressure >= 70 else "7d" if daily_pressure >= 40 else "30d",
    }
    return _with_packet("Decision Latency Cost Meter", payload, packet, "Set an explicit decision SLA when delay pressure is material.")


def forecast_evidence_decay(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    today = date.today()
    evidence_items = []
    for idx, fact in enumerate(packet.get("facts", [])[:8], start=1):
        freshness = _freshness_days(fact)
        days_to_decay = max(0, 45 - freshness)
        evidence_items.append({"evidence_id": f"EVD-{idx:03d}", "claim": fact, "freshness_days": freshness, "expires_on": (today + timedelta(days=days_to_decay)).isoformat(), "decay_risk": "High" if days_to_decay <= 7 else "Medium" if days_to_decay <= 21 else "Low"})
    for idx, gap in enumerate(packet.get("missing_evidence", [])[:5], start=len(evidence_items) + 1):
        evidence_items.append({"evidence_id": f"EVD-{idx:03d}", "claim": gap, "freshness_days": None, "expires_on": None, "decay_risk": "Missing"})
    payload = {"evidence_items": evidence_items, "high_decay_count": sum(1 for item in evidence_items if item["decay_risk"] in {"High", "Missing"}), "next_refresh_due": (today + timedelta(days=7)).isoformat()}
    return _with_packet("Evidence Decay Forecast", payload, packet, "Refresh high-decay or missing evidence before board, audit or approval review.")


def simulate_synthetic_executive_committee(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    personas = [
        ("CEO", "What changes if we delay this decision by one month?", "enterprise outcome"),
        ("CFO", "Where is value leakage or unapproved spend hidden?", "financial exposure"),
        ("CISO", "What risk is being accepted and by whom?", "security exposure"),
        ("Audit Chair", "Which evidence would fail audit sampling?", "control evidence"),
        ("COO", "What breaks operationally if the dependency slips?", "operating continuity"),
        ("Board Director", "What would make this recommendation wrong?", "decision reversibility"),
    ]
    memory = _memory_snapshot(db_path)
    challenges = []
    for persona, question, pressure in personas:
        challenges.append({"persona": persona, "challenge_question": question, "pressure_domain": pressure, "follow_up": _follow_up_for(persona, packet), "answer_readiness": _score(packet.get("scorecard", {}).get("evidence_confidence", {}).get("value", 50) - len(packet.get("missing_evidence", [])) * 4 + memory["counts"].get("board_questions", 0) * 3)})
    payload = {"committee": challenges, "committee_size": len(challenges), "lowest_answer_readiness": min(item["answer_readiness"] for item in challenges), "memory_board_question_count": memory["counts"].get("board_questions", 0)}
    return _with_packet("Synthetic Executive Committee", payload, packet, "Use unanswered committee challenges to harden the board packet.")


def build_control_debt_ledger(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    text = _text(input_context)
    items = []
    for domain, words in {
        "security": ["security", "access", "privileged"],
        "audit": ["audit", "control", "evidence"],
        "privacy": ["privacy", "pii", "personal data"],
        "change_control": ["change", "release", "rollback", "testing"],
        "vendor_risk": ["vendor", "contract", "supplier"],
    }.items():
        if _hits(text, words):
            items.append({"control_domain": domain, "debt_item": _gap_for(domain, packet.get("missing_evidence", [])), "severity": "High" if domain in {"security", "audit"} else "Medium", "retirement_condition": "Evidence accepted by accountable owner"})
    payload = {"control_debt_items": items, "control_debt_count": len(items), "burndown_required": bool(items), "highest_severity": "High" if any(item["severity"] == "High" for item in items) else "Medium" if items else "Low"}
    return _with_packet("Control Debt Ledger", payload, packet, "Retire high-severity control debt before final approval or explicitly accept residual risk.")


def build_operating_rhythm_autopilot_v2(db_path: str) -> Dict[str, Any]:
    init_memory_db(db_path)
    aging = memory_aging(db_path)["memory_aging_review"]
    with _connect(db_path) as conn:
        decisions = _rows(conn, "select * from decisions order by id desc limit 20")
        reviews = _rows(conn, "select id,title,request_type,created_on from reviews order by id desc limit 20")
        outcomes = _rows(conn, "select * from outcomes order by id desc limit 20")
    cadences = [
        {"cadence": "weekly", "artifact": "CIO operating brief", "focus": "overdue actions, stale evidence, blocked decisions"},
        {"cadence": "monthly", "artifact": "board readiness review", "focus": "decision debt, value leakage, vendor pressure"},
        {"cadence": "quarterly", "artifact": "risk and control reset", "focus": "control debt, assumptions, outcome backtest"},
        {"cadence": "annual", "artifact": "strategy operating model reset", "focus": "strategic drift, architecture runway, portfolio options"},
    ]
    payload = {
        "db_path": db_path,
        "cadences": cadences,
        "decision_count": len(decisions),
        "review_count": len(reviews),
        "outcome_count": len(outcomes),
        "aging": aging,
        "next_operating_actions": [
            "Run weekly brief from local memory.",
            "Close overdue action owners.",
            "Backtest decisions with recorded outcomes.",
        ],
    }
    return _result("Operating Rhythm Autopilot", payload, [f"Built operating rhythm from {len(decisions)} decision(s), {len(reviews)} review(s) and {len(outcomes)} outcome(s)."], "Use the cadence pack as the recurring CIO operating rhythm.")


def build_enterprise_contradiction_memory(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    text = _text(input_context)
    contradictions = []
    rules = [
        ("on_track_vs_testing_gap", ["on track", "green", "under control"], ["testing has not started", "incomplete", "missing"]),
        ("budget_neutral_vs_spend_pressure", ["budget neutral", "within budget"], ["reserve", "over forecast", "spend pressure"]),
        ("low_risk_vs_control_gap", ["low risk", "no impact"], ["audit", "control", "security", "missing evidence"]),
        ("owner_accountable_vs_owner_gap", ["accountable", "owned"], ["no owner", "owner unclear", "unassigned"]),
    ]
    for name, narrative, facts in rules:
        if _hits(text, narrative) and _hits(text, facts):
            contradictions.append({"contradiction": name, "narrative_signal": narrative[0], "conflicting_signal": facts[0], "severity": "High"})
    memory = _memory_snapshot(db_path)
    payload = {"contradictions": contradictions, "contradiction_count": len(contradictions), "memory_collision_count": memory["counts"].get("decision_collisions", 0), "recurrence_risk": "High" if len(contradictions) + memory["counts"].get("decision_collisions", 0) >= 3 else "Medium" if contradictions else "Low"}
    return _with_packet("Enterprise Contradiction Memory", payload, packet, "Make recurring contradictions visible by owner, vendor and decision topic.")


def map_cio_replacement_surface(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    review = build_autopilot_review(input_context)
    surfaces = [
        {"work": "evidence classification", "automation_level": "prepared_by_ai", "human_control": "review evidence and source quality"},
        {"work": "board challenge simulation", "automation_level": "prepared_by_ai", "human_control": "approve final board narrative"},
        {"work": "decision packet assembly", "automation_level": "draft_allowed", "human_control": "own recommendation and residual risk"},
        {"work": "delegation drafting", "automation_level": "draft_allowed", "human_control": "assign only after approval"},
        {"work": "risk acceptance", "automation_level": "human_only", "human_control": "accountable executive approval"},
        {"work": "external execution", "automation_level": "blocked", "human_control": "requires explicit connector and user authorization"},
    ]
    prepared = sum(1 for item in surfaces if item["automation_level"] in {"prepared_by_ai", "draft_allowed"})
    payload = {
        "surfaces": surfaces,
        "estimated_cio_work_prepared_percent": round(prepared / len(surfaces) * 100),
        "human_only_count": sum(1 for item in surfaces if item["automation_level"] == "human_only"),
        "blocked_execution_count": sum(1 for item in surfaces if item["automation_level"] == "blocked"),
        "existing_cio_work_autonomy_map": review.get("cio_work_autonomy_map", {}),
        "replacement_boundary": "The plugin prepares and governs CIO work; accountable decisions and external actions remain human-controlled.",
    }
    return _with_packet("CIO Replacement Surface Map", payload, packet, "Use the map to separate replaceable CIO preparation work from human-only accountability.")


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


def _memory_snapshot(db_path: str | None) -> Dict[str, Any]:
    if not db_path:
        return {"counts": {}, "aging_pressure": 0}
    init_memory_db(db_path)
    counts: Dict[str, int] = {}
    with _connect(db_path) as conn:
        for table in ("decisions", "assumptions", "evidence", "risk_chains", "actions", "reviews", "outcomes", "board_questions", "decision_collisions"):
            counts[table] = int(conn.execute(f"select count(*) as c from {table}").fetchone()["c"])
    aging = memory_aging(db_path)["memory_aging_review"]
    pressure = _score(len(aging.get("overdue_actions", [])) * 12 + len(aging.get("stale_assumptions", [])) * 10 + len(aging.get("stale_evidence", [])) * 8)
    return {"counts": counts, "aging_pressure": pressure}


def _text(input_context: Mapping[str, Any]) -> str:
    return json.dumps(input_context, ensure_ascii=False).lower()


def _hits(text: str, words: list[str]) -> int:
    return sum(1 for word in words if word in text)


def _signals(input_context: Mapping[str, Any], words: list[str]) -> list[str]:
    text = _text(input_context)
    return [word for word in words if word in text]


def _sentences(input_context: Mapping[str, Any], words: list[str]) -> list[str]:
    raw = []
    for value in input_context.values():
        if isinstance(value, list):
            raw.extend(str(item) for item in value)
        elif isinstance(value, str):
            raw.append(value)
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
    if "architecture" in low or "platform" in low:
        return "Enterprise architecture"
    return "CIO delegate"


def _gap_for(domain: str, gaps: list[str]) -> str:
    for gap in gaps:
        low = gap.lower()
        if domain.replace("_", " ") in low or any(word in low for word in domain.split("_")):
            return gap
    return gaps[0] if gaps else "Missing accepted evidence, owner and review date."


def _overlap(left: Any, right: Any) -> bool:
    left_terms = {term for term in str(left).lower().split() if len(term) > 4}
    right_terms = {term for term in str(right).lower().split() if len(term) > 4}
    return bool(left_terms & right_terms)


def _fingerprint(payload: Mapping[str, Any]) -> str:
    text = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    checksum = sum((idx + 1) * ord(char) for idx, char in enumerate(text)) % 10_000_000
    return f"local-{checksum:07d}"


def _freshness_days(text: str) -> int:
    for token in str(text).replace(",", " ").split():
        try:
            parsed = datetime.fromisoformat(token[:10]).date()
            return max(0, (date.today() - parsed).days)
        except ValueError:
            continue
    return 30


def _cost_domains(input_context: Mapping[str, Any]) -> list[str]:
    domains = []
    text = _text(input_context)
    for domain, words in {
        "finance": ["budget", "spend", "forecast", "reserve"],
        "security": ["security", "access", "privileged"],
        "delivery": ["delivery", "go-live", "testing", "milestone"],
        "audit": ["audit", "control", "evidence"],
        "customer": ["customer", "billing", "outage"],
    }.items():
        if _hits(text, words):
            domains.append(domain)
    return domains


def _follow_up_for(persona: str, packet: Mapping[str, Any]) -> str:
    if persona == "CFO":
        return "Show the financial exposure, benefit baseline and stop criteria."
    if persona == "CISO":
        return "Name the accepting owner, control gap and compensating control."
    if persona == "Audit Chair":
        return "Separate tested evidence from assumptions and draft controls."
    if persona == "COO":
        return "Show the dependency chain and rollback option."
    if persona == "Board Director":
        return "State the strongest counterargument and what evidence would change the decision."
    gaps = packet.get("missing_evidence", [])
    return f"Close missing evidence first: {gaps[0]}" if gaps else "State the decision boundary and owner."


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


def _result(artifact: str, payload: Dict[str, Any], facts: list[str], recommendation: str) -> Dict[str, Any]:
    return {
        "artifact": artifact,
        artifact.lower().replace(" ", "_").replace("-", "_"): payload,
        "facts": facts,
        "assumptions": [],
        "hypotheses": ["Output depends on explicit local SQLite memory and may be incomplete when memory is sparse."],
        "missing_evidence": [],
        "confidence": "Medium",
        "recommended_action": {"recommendation": recommendation, "owner": "CIO office", "timebox": "Next operating review"},
        "guardrails": GUARDRAILS,
    }
