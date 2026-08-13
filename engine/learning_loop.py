"""Explicit local learning loop for The Autonomous CIO."""

from __future__ import annotations

from collections import Counter, defaultdict
from contextlib import contextmanager
from datetime import date
import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, Mapping

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
    "Learning updates are explicit local memory records only.",
    "High-risk domain outputs are decision support, not final specialist determinations.",
]


def record_feedback(feedback: Mapping[str, Any], db_path: str) -> Dict[str, Any]:
    init_memory_db(db_path)
    with _connect(db_path) as conn:
        conn.execute(
            "insert into feedback(packet_id, decision, rating, accepted, notes, payload, created_on) values(?,?,?,?,?,?,?)",
            (
                str(feedback.get("packet_id", "")),
                str(feedback.get("decision", "")),
                _int(feedback.get("rating"), 0),
                1 if feedback.get("accepted", False) else 0,
                str(feedback.get("notes", "")),
                json.dumps(dict(feedback), ensure_ascii=False),
                date.today().isoformat(),
            ),
        )
        conn.execute("insert into audit_events(event_type, payload, created_on) values(?,?,?)", ("feedback_recorded", json.dumps(dict(feedback), ensure_ascii=False), date.today().isoformat()))
    return _result("Decision Feedback Recorded", {"db_path": db_path, "packet_id": feedback.get("packet_id", ""), "rating": _int(feedback.get("rating"), 0)}, [f"Recorded feedback for packet {feedback.get('packet_id', '')}."])


def record_outcome(outcome: Mapping[str, Any], db_path: str) -> Dict[str, Any]:
    init_memory_db(db_path)
    with _connect(db_path) as conn:
        conn.execute(
            "insert into outcomes(packet_id, decision, actual_outcome, score_accuracy, realized_risks, value_result, payload, reviewed_on) values(?,?,?,?,?,?,?,?)",
            (
                str(outcome.get("packet_id", "")),
                str(outcome.get("decision", "")),
                str(outcome.get("actual_outcome", "")),
                _int(outcome.get("score_accuracy"), 0),
                json.dumps(outcome.get("realized_risks", []), ensure_ascii=False),
                str(outcome.get("value_result", "")),
                json.dumps(dict(outcome), ensure_ascii=False),
                str(outcome.get("reviewed_on", date.today().isoformat())),
            ),
        )
        conn.execute("insert into audit_events(event_type, payload, created_on) values(?,?,?)", ("outcome_recorded", json.dumps(dict(outcome), ensure_ascii=False), date.today().isoformat()))
    return _result("Decision Outcome Recorded", {"db_path": db_path, "packet_id": outcome.get("packet_id", ""), "score_accuracy": _int(outcome.get("score_accuracy"), 0)}, [f"Recorded outcome for packet {outcome.get('packet_id', '')}."])


def calibrate_scores(db_path: str) -> Dict[str, Any]:
    init_memory_db(db_path)
    with _connect(db_path) as conn:
        outcomes = [dict(row) for row in conn.execute("select * from outcomes").fetchall()]
        feedback = [dict(row) for row in conn.execute("select * from feedback").fetchall()]
        avg_accuracy = round(sum(row["score_accuracy"] for row in outcomes) / len(outcomes), 1) if outcomes else 0
        avg_rating = round(sum(row["rating"] for row in feedback) / len(feedback), 1) if feedback else 0
        adjustment = 0
        reason = "No calibration needed yet."
        if outcomes and avg_accuracy < 60:
            adjustment = -8
            reason = "Historical outcomes indicate scores were too optimistic."
        elif outcomes and avg_accuracy > 85 and avg_rating >= 4:
            adjustment = 4
            reason = "Historical outcomes and feedback support slightly higher confidence."
        conn.execute(
            "insert into score_calibrations(score_name, adjustment, reason, sample_size, created_on) values(?,?,?,?,?)",
            ("decision_readiness", adjustment, reason, len(outcomes), date.today().isoformat()),
        )
    return _result("Score Calibration", {"db_path": db_path, "sample_size": len(outcomes), "average_score_accuracy": avg_accuracy, "average_feedback_rating": avg_rating, "adjustments": [{"score_name": "decision_readiness", "adjustment": adjustment, "reason": reason}]}, [f"Calibrated scores from {len(outcomes)} outcome record(s)."])


def learn_patterns(db_path: str) -> Dict[str, Any]:
    init_memory_db(db_path)
    with _connect(db_path) as conn:
        texts = []
        refs = []
        for table, col in (("assumptions", "assumption"), ("risk_chains", "signal"), ("actions", "action"), ("outcomes", "actual_outcome")):
            for row in conn.execute(f"select id, {col} as text from {table}").fetchall():
                texts.append(str(row["text"]))
                refs.append(f"{table}:{row['id']}")
        terms = _extract_terms(texts)
        patterns = []
        for term, freq in terms.most_common(12):
            if freq < 2:
                continue
            pattern_type = _pattern_type(term)
            confidence = "High" if freq >= 4 else "Medium"
            patterns.append({"pattern": term, "pattern_type": pattern_type, "frequency": freq, "confidence": confidence})
            conn.execute(
                "insert into learned_patterns(pattern, pattern_type, frequency, confidence, evidence_refs, created_on) values(?,?,?,?,?,?)",
                (term, pattern_type, freq, confidence, json.dumps(refs[:20]), date.today().isoformat()),
            )
    return _result("Learned Pattern Library", {"db_path": db_path, "patterns": patterns}, [f"Learned {len(patterns)} recurring local pattern(s)."])


def source_reputation(db_path: str) -> Dict[str, Any]:
    init_memory_db(db_path)
    with _connect(db_path) as conn:
        evidence = [dict(row) for row in conn.execute("select source_ref, quality, claim from evidence").fetchall()]
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for item in evidence:
            grouped[item.get("source_ref") or "unknown"].append(item)
        reputations = []
        for source_ref, items in grouped.items():
            contradictions = sum(1 for item in items if any(term in str(item.get("claim", "")).lower() for term in ("contradict", "unclear", "unsupported")))
            trust = max(0, min(100, 70 + len(items) * 2 - contradictions * 12))
            row = {"source_ref": source_ref, "trust_score": trust, "signal_count": len(items), "contradiction_count": contradictions}
            reputations.append(row)
            conn.execute(
                "insert into source_reputation(source_ref, trust_score, signal_count, contradiction_count, last_seen) values(?,?,?,?,?)",
                (source_ref, trust, len(items), contradictions, date.today().isoformat()),
            )
    return _result("Source Reputation", {"db_path": db_path, "sources": reputations}, [f"Scored reputation for {len(reputations)} local source reference(s)."])


def record_skill_chain_feedback(feedback: Mapping[str, Any], db_path: str) -> Dict[str, Any]:
    init_memory_db(db_path)
    chain = feedback.get("skill_chain", [])
    if not isinstance(chain, list):
        chain = [str(chain)]
    with _connect(db_path) as conn:
        conn.execute(
            "insert into skill_chain_feedback(request_type, skill_chain, rating, accepted, notes, created_on) values(?,?,?,?,?,?)",
            (
                str(feedback.get("request_type", "")),
                json.dumps(chain, ensure_ascii=False),
                _int(feedback.get("rating"), 0),
                1 if feedback.get("accepted", False) else 0,
                str(feedback.get("notes", "")),
                date.today().isoformat(),
            ),
        )
    return _result("Skill Chain Feedback Recorded", {"db_path": db_path, "request_type": feedback.get("request_type", ""), "skill_chain": chain, "rating": _int(feedback.get("rating"), 0)}, [f"Recorded skill-chain feedback for {feedback.get('request_type', '')}."])


def board_question_memory(question_input: Mapping[str, Any], db_path: str) -> Dict[str, Any]:
    init_memory_db(db_path)
    questions = question_input.get("questions", [])
    if isinstance(questions, str):
        questions = [{"question": questions}]
    with _connect(db_path) as conn:
        for item in questions:
            conn.execute(
                "insert into board_questions(persona, question, topic, pressure_level, source_ref, created_on) values(?,?,?,?,?,?)",
                (
                    str(item.get("persona", question_input.get("persona", "Board"))),
                    str(item.get("question", "")),
                    str(item.get("topic", question_input.get("topic", ""))),
                    str(item.get("pressure_level", question_input.get("pressure_level", "Medium"))),
                    str(item.get("source_ref", question_input.get("source_ref", ""))),
                    date.today().isoformat(),
                ),
            )
        stored = [dict(row) for row in conn.execute("select * from board_questions order by id desc limit 25").fetchall()]
    return _result("Board Question Memory", {"db_path": db_path, "stored_count": len(questions), "recent_questions": stored}, [f"Stored {len(questions)} board question(s)."])


def recommendation_backtest(db_path: str) -> Dict[str, Any]:
    init_memory_db(db_path)
    with _connect(db_path) as conn:
        outcomes = [dict(row) for row in conn.execute("select * from outcomes").fetchall()]
        feedback = [dict(row) for row in conn.execute("select * from feedback").fetchall()]
    accepted = sum(row["accepted"] for row in feedback)
    low_accuracy = [row for row in outcomes if row["score_accuracy"] < 60]
    lessons = []
    if low_accuracy:
        lessons.append("Lower readiness or confidence when similar missing evidence appears again.")
    if feedback and accepted / len(feedback) < 0.6:
        lessons.append("Recommendations need stronger executive framing or clearer options.")
    if not lessons:
        lessons.append("No negative backtest signal yet; continue collecting outcomes.")
    return _result("Recommendation Backtest", {"db_path": db_path, "outcome_count": len(outcomes), "feedback_count": len(feedback), "accepted_feedback_count": accepted, "low_accuracy_count": len(low_accuracy), "lessons": lessons}, [f"Backtested {len(outcomes)} outcome(s) and {len(feedback)} feedback record(s)."])


def learning_digest(db_path: str) -> Dict[str, Any]:
    calibration = calibrate_scores(db_path)
    patterns = learn_patterns(db_path)
    reputation = source_reputation(db_path)
    backtest = recommendation_backtest(db_path)
    return _result(
        "Adaptive CIO Learning Digest",
        {
            "db_path": db_path,
            "score_calibration": calibration["score_calibration"],
            "patterns": patterns["learned_pattern_library"]["patterns"],
            "source_reputation": reputation["source_reputation"]["sources"],
            "recommendation_backtest": backtest["recommendation_backtest"],
        },
        [f"Built adaptive learning digest for {db_path}."],
    )


@contextmanager
def _connect(db_path: str):
    conn = sqlite3.connect(Path(db_path))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def _int(value: Any, default: int) -> int:
    try:
        return int(value)
    except Exception:
        return default


def _extract_terms(texts: list[str]) -> Counter:
    terms: Counter = Counter()
    stop = {"the", "and", "for", "with", "that", "this", "from", "owner", "review", "decision", "action", "risk"}
    for text in texts:
        clean = "".join(ch.lower() if ch.isalnum() else " " for ch in text)
        for word in clean.split():
            if len(word) >= 5 and word not in stop:
                terms[word] += 1
    return terms


def _pattern_type(term: str) -> str:
    if term in {"vendor", "supplier", "contract", "milestone"}:
        return "vendor_pattern"
    if term in {"budget", "spend", "reserve", "forecast"}:
        return "value_pattern"
    if term in {"audit", "control", "evidence", "privacy"}:
        return "governance_pattern"
    if term in {"testing", "environment", "architecture", "integration"}:
        return "delivery_pattern"
    return "recurring_signal"


def _result(artifact: str, payload: Dict[str, Any], facts: list[str]) -> Dict[str, Any]:
    key = artifact.lower().replace(" ", "_")
    return {
        "artifact": artifact,
        key: payload,
        "facts": facts,
        "assumptions": [],
        "hypotheses": ["Learning quality depends on the completeness and honesty of recorded feedback and outcomes."],
        "missing_evidence": [],
        "confidence": "Medium",
        "recommended_action": {"recommendation": "Use learning outputs to tune future decision packets, not as automatic truth.", "owner": "CIO office", "timebox": "Next review cycle"},
        "guardrails": GUARDRAILS,
    }
