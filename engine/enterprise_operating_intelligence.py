"""Enterprise operating intelligence for CIO decision support."""

from __future__ import annotations

from contextlib import contextmanager
from datetime import date
import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, Mapping

try:
    from decision_intelligence_engine import build_decision_packet
    from memory_store import init_memory_db, memory_aging
except ImportError:
    from .decision_intelligence_engine import build_decision_packet
    from .memory_store import init_memory_db, memory_aging


GUARDRAILS = [
    "Uses only user-provided local context.",
    "Does not claim live system access.",
    "Does not persist memory automatically.",
    "Does not execute external actions.",
    "Does not train or update an external model.",
    "High-risk domain outputs are decision support, not final specialist determinations.",
]


def build_accountability_graph(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    edges = []
    for action in packet.get("draft_next_steps", {}).get("next_24h", []) + packet.get("draft_next_steps", {}).get("next_7d", []):
        owner = _owner_for(action)
        edges.append({"source": "CIO office", "target": owner, "role": "accountable_owner", "evidence": action})
    for item in packet.get("missing_evidence", [])[:8]:
        edges.append({"source": "Evidence gap", "target": _owner_for(item), "role": "contributor", "evidence": item})
    if db_path:
        init_memory_db(db_path)
        with _connect(db_path) as conn:
            for edge in edges:
                conn.execute("insert into accountability_edges(source,target,role,evidence,created_on) values(?,?,?,?,?)", (edge["source"], edge["target"], edge["role"], edge["evidence"], date.today().isoformat()))
    return _with_packet("Executive Accountability Graph", {"edges": edges, "node_count": len({e["source"] for e in edges} | {e["target"] for e in edges}), "edge_count": len(edges)}, packet, "Assign owners for accountability gaps before approval.")


def score_organizational_friction(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    text = _text(input_context)
    factors = {
        "missing_owner": _score(_hits(text, ["owner unclear", "no owner", "ownerless"]) * 25 + len(packet.get("missing_evidence", [])) * 4),
        "evidence_gap": _score(len(packet.get("missing_evidence", [])) * 10),
        "budget_pressure": _score(_hits(text, ["budget", "spend", "reserve", "forecast"]) * 18),
        "vendor_dependency": _score(_hits(text, ["vendor", "supplier", "milestone"]) * 18),
        "decision_latency": _score(_hits(text, ["delayed", "defer", "waiting", "not approved"]) * 16),
    }
    if db_path:
        aging = memory_aging(db_path)["memory_aging_review"]
        factors["memory_aging"] = _score(len(aging["overdue_actions"]) * 12 + len(aging["stale_assumptions"]) * 10)
    score = round(sum(factors.values()) / len(factors))
    return _with_packet("Organizational Friction Score", {"score": score, "factors": factors, "posture": "High" if score >= 65 else "Medium" if score >= 35 else "Low"}, packet, "Remove the top friction factor before adding more scope.")


def detect_decision_collisions(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    text = _text(input_context)
    collisions = []
    rules = [
        ("cost_reduction_vs_spend_growth", ["cost", "reduce"], ["spend", "over forecast", "budget"]),
        ("go_live_vs_testing_gap", ["go-live", "go live", "approve"], ["testing has not started", "test environment", "testing"]),
        ("control_commitment_vs_evidence_gap", ["audit", "control"], ["missing", "incomplete", "evidence gap"]),
        ("speed_vs_capacity_constraint", ["accelerate", "target", "deadline"], ["overloaded", "capacity", "same architects"]),
    ]
    for name, left, right in rules:
        if _hits(text, left) and _hits(text, right):
            collisions.append({"collision": name, "severity": "High", "evidence": f"Detected {left} and {right} in the same decision context."})
    if db_path:
        init_memory_db(db_path)
        with _connect(db_path) as conn:
            prior = [dict(row) for row in conn.execute("select * from decisions order by id desc limit 25").fetchall()]
            for row in prior:
                if "approve" in str(row.get("decision", "")).lower() and packet.get("missing_evidence"):
                    collisions.append({"collision": "prior_approval_vs_current_evidence_gap", "severity": "Medium", "evidence": str(row.get("decision", ""))})
            for item in collisions:
                conn.execute("insert into decision_collisions(collision,severity,payload,created_on) values(?,?,?,?)", (item["collision"], item["severity"], json.dumps(item, ensure_ascii=False), date.today().isoformat()))
    return _with_packet("Decision Collision Detector", {"collisions": collisions, "collision_count": len(collisions)}, packet, "Resolve high-severity collisions before presenting the decision.")


def detect_strategic_contradictions(input_context: Mapping[str, Any], db_path: str | None = None) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    text = _text(input_context)
    contradictions = []
    checks = [
        ("simplify_strategy_vs_point_solutions", ["simplify", "consolidate", "reduce complexity"], ["new solution", "point solution", "duplicate"]),
        ("resilience_strategy_vs_testing_delay", ["resilience", "continuity", "stable"], ["testing postponed", "no failover", "testing has not started"]),
        ("security_strategy_vs_access_gap", ["secure", "zero trust", "risk reduction"], ["privileged access", "access gap", "manual review"]),
        ("value_strategy_vs_no_metrics", ["value", "benefit", "productivity"], ["no baseline", "no adoption", "no metrics"]),
    ]
    for name, strategy_words, execution_words in checks:
        if _hits(text, strategy_words) and _hits(text, execution_words):
            contradictions.append({"contradiction": name, "severity": "High", "strategy_signal": strategy_words[0], "execution_signal": execution_words[0]})
    if db_path:
        init_memory_db(db_path)
        with _connect(db_path) as conn:
            for item in contradictions:
                conn.execute("insert into strategic_contradictions(contradiction,severity,payload,created_on) values(?,?,?,?)", (item["contradiction"], item["severity"], json.dumps(item, ensure_ascii=False), date.today().isoformat()))
    return _with_packet("Strategic Contradiction Radar", {"contradictions": contradictions, "contradiction_count": len(contradictions)}, packet, "Make the strategy/execution contradiction explicit in the next steering review.")


def build_weekly_operating_autopilot(db_path: str) -> Dict[str, Any]:
    init_memory_db(db_path)
    aging = memory_aging(db_path)["memory_aging_review"]
    with _connect(db_path) as conn:
        decisions = _rows(conn, "select * from decisions order by id desc limit 10")
        evidence = _rows(conn, "select * from evidence order by id desc limit 10")
        risks = _rows(conn, "select * from risk_chains order by id desc limit 10")
        vendor_pressure = [row for row in risks + decisions if _hits(str(row).lower(), ["vendor", "supplier", "milestone"])]
        payload = {
            "top_decisions": decisions,
            "stale_assumptions": aging["stale_assumptions"],
            "overdue_actions": aging["overdue_actions"],
            "board_risks": risks[:5],
            "vendor_pressure": vendor_pressure[:5],
            "evidence_gaps": evidence[:5],
        }
        conn.execute("insert into weekly_operating_snapshots(title,payload,created_on) values(?,?,?)", ("Weekly CIO Operating Autopilot", json.dumps(payload, ensure_ascii=False), date.today().isoformat()))
    return _result("CIO Weekly Operating Autopilot", {"db_path": db_path, **payload}, [f"Prepared weekly operating autopilot from {len(decisions)} decision(s)."])


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


def _hits(text: str, words: list[str]) -> int:
    return sum(1 for word in words if word in text)


def _score(value: int) -> int:
    return max(0, min(100, int(value)))


def _with_packet(artifact: str, payload: Dict[str, Any], packet: Mapping[str, Any], recommendation: str) -> Dict[str, Any]:
    return {
        "artifact": artifact,
        artifact.lower().replace(" ", "_").replace("-", "_"): payload,
        "facts": packet["facts"],
        "assumptions": packet["assumptions"],
        "hypotheses": packet["hypotheses"],
        "missing_evidence": packet["missing_evidence"],
        "confidence": packet["confidence"],
        "recommended_action": {"recommendation": recommendation, "owner": "CIO office", "timebox": "Next operating review"},
        "guardrails": GUARDRAILS,
    }


def _result(artifact: str, payload: Dict[str, Any], facts: list[str]) -> Dict[str, Any]:
    return {
        "artifact": artifact,
        artifact.lower().replace(" ", "_").replace("-", "_"): payload,
        "facts": facts,
        "assumptions": [],
        "hypotheses": ["Weekly operating output is based on explicit local SQLite memory only."],
        "missing_evidence": [],
        "confidence": "Medium",
        "recommended_action": {"recommendation": "Review the weekly operating pack before leadership cadence.", "owner": "CIO office", "timebox": "Weekly"},
        "guardrails": GUARDRAILS,
    }
