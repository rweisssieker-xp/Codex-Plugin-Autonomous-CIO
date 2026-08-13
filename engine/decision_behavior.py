"""Decision behavior intelligence for local CIO memory."""

from __future__ import annotations

from contextlib import contextmanager
from datetime import date
import json
import sqlite3
from pathlib import Path
from typing import Any, Dict

try:
    from memory_store import init_memory_db
except ImportError:
    from .memory_store import init_memory_db


GUARDRAILS = [
    "Uses only user-provided local context.",
    "Does not claim live system access.",
    "Does not persist memory automatically.",
    "Does not execute external actions.",
    "Does not train or update an external model.",
    "High-risk domain outputs are decision support, not final specialist determinations.",
]


def build_decision_dna(db_path: str) -> Dict[str, Any]:
    init_memory_db(db_path)
    with _connect(db_path) as conn:
        decisions = _rows(conn, "select * from decisions")
        feedback = _rows(conn, "select * from feedback")
        outcomes = _rows(conn, "select * from outcomes")
        questions = _rows(conn, "select * from board_questions")
        text = _joined(decisions, "decision") + " " + _joined(outcomes, "actual_outcome")
        traits = {
            "slow": _score(len([d for d in decisions if str(d.get("status", "")).lower() in {"draft", "open"}]) * 12),
            "optimistic": _score(_hits(text, ["on track", "under control", "no impact"]) * 25 + _low_accuracy(outcomes) * 10),
            "risk_averse": _score(_hits(text, ["defer", "stop", "rollback", "conditions"]) * 18),
            "vendor_dependent": _score(_hits(text, ["vendor", "supplier", "milestone"]) * 16),
            "evidence_driven": _score(len([f for f in feedback if int(f.get("accepted") or 0) == 1]) * 15 + _hits(text, ["evidence", "control", "audit"]) * 8),
            "board_reactive": _score(len(questions) * 12 + _hits(text, ["board", "steering"]) * 10),
        }
        dominant = max(traits, key=traits.get) if traits else "unknown"
        payload = {"traits": traits, "dominant_pattern": dominant, "sample": {"decisions": len(decisions), "feedback": len(feedback), "outcomes": len(outcomes), "board_questions": len(questions)}}
        conn.execute("insert into decision_dna_snapshots(profile, payload, created_on) values(?,?,?)", (dominant, json.dumps(payload, ensure_ascii=False), date.today().isoformat()))
    return _result("Decision DNA", {"db_path": db_path, **payload}, [f"Decision DNA dominant pattern is {dominant}."])


def build_risk_appetite_twin(db_path: str) -> Dict[str, Any]:
    init_memory_db(db_path)
    with _connect(db_path) as conn:
        feedback = _rows(conn, "select * from feedback")
        outcomes = _rows(conn, "select * from outcomes")
        decisions = _rows(conn, "select * from decisions")
        text = _joined(decisions, "decision") + " " + _joined(outcomes, "actual_outcome")
        accepted = sum(int(row.get("accepted") or 0) for row in feedback)
        avg_accuracy = round(sum(int(row.get("score_accuracy") or 0) for row in outcomes) / len(outcomes), 1) if outcomes else 0
        tolerance = _score(45 + accepted * 8 + _hits(text, ["approve", "fund"]) * 10 - _hits(text, ["defer", "stop", "rollback"]) * 12)
        profile = "balanced"
        if tolerance >= 70:
            profile = "growth_tolerant"
        elif tolerance <= 35:
            profile = "control_first"
        payload = {"risk_appetite_score": tolerance, "profile": profile, "average_outcome_accuracy": avg_accuracy, "accepted_feedback_count": accepted, "escalation_triggers": _triggers(text)}
        conn.execute("insert into risk_appetite_snapshots(profile, payload, created_on) values(?,?,?)", (profile, json.dumps(payload, ensure_ascii=False), date.today().isoformat()))
    return _result("CIO Risk Appetite Twin", {"db_path": db_path, **payload}, [f"Risk appetite profile is {profile}."])


def build_board_memory(db_path: str) -> Dict[str, Any]:
    init_memory_db(db_path)
    with _connect(db_path) as conn:
        questions = _rows(conn, "select * from board_questions order by id desc")
    personas: dict[str, int] = {}
    topics: dict[str, int] = {}
    pressure: dict[str, int] = {}
    for row in questions:
        personas[str(row.get("persona") or "Board")] = personas.get(str(row.get("persona") or "Board"), 0) + 1
        topics[str(row.get("topic") or "General")] = topics.get(str(row.get("topic") or "General"), 0) + 1
        pressure[str(row.get("pressure_level") or "Medium")] = pressure.get(str(row.get("pressure_level") or "Medium"), 0) + 1
    payload = {"db_path": db_path, "question_count": len(questions), "personas": personas, "topics": topics, "pressure_levels": pressure, "recent_questions": questions[:20]}
    return _result("Board Memory", payload, [f"Loaded {len(questions)} board question(s) from local memory."])


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


def _joined(rows: list[dict[str, Any]], field: str) -> str:
    return " ".join(str(row.get(field, "")) for row in rows).lower()


def _hits(text: str, words: list[str]) -> int:
    return sum(1 for word in words if word in text)


def _low_accuracy(outcomes: list[dict[str, Any]]) -> int:
    return len([row for row in outcomes if int(row.get("score_accuracy") or 0) < 60])


def _triggers(text: str) -> list[str]:
    triggers = []
    for name, words in {
        "audit_or_control_gap": ["audit", "control", "evidence"],
        "security_gap": ["security", "privileged", "access"],
        "vendor_dependency": ["vendor", "supplier", "milestone"],
        "budget_pressure": ["budget", "spend", "reserve"],
    }.items():
        if _hits(text, words):
            triggers.append(name)
    return triggers or ["insufficient_history"]


def _score(value: int) -> int:
    return max(0, min(100, int(value)))


def _result(artifact: str, payload: Dict[str, Any], facts: list[str]) -> Dict[str, Any]:
    return {
        "artifact": artifact,
        artifact.lower().replace(" ", "_").replace("-", "_"): payload,
        "facts": facts,
        "assumptions": [],
        "hypotheses": ["Behavior intelligence reflects explicit local memory records, not model training."],
        "missing_evidence": [],
        "confidence": "Medium",
        "recommended_action": {"recommendation": "Use this local pattern profile to challenge the next decision packet.", "owner": "CIO office", "timebox": "Next review"},
        "guardrails": GUARDRAILS,
    }
