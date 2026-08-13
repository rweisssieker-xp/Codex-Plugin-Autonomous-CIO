"""SQLite executive memory store for The Autonomous CIO."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from contextlib import contextmanager
import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, Mapping


GUARDRAILS = [
    "Uses only user-provided local context.",
    "Does not claim live system access.",
    "Does not persist memory automatically.",
    "Does not execute external actions.",
    "High-risk domain outputs are decision support, not final specialist determinations.",
]

SCHEMA_VERSION = "1.3"


def init_memory_db(db_path: str) -> Dict[str, Any]:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with _connect(path) as conn:
        _create_schema(conn)
    return _result(
        "SQLite Executive Memory Initialized",
        {"db_path": str(path), "memory_schema_version": SCHEMA_VERSION},
        facts=[f"Initialized memory DB at {path}."],
    )


def migrate_memory_json(memory_path: str, db_path: str) -> Dict[str, Any]:
    init_memory_db(db_path)
    source = Path(memory_path)
    data = json.loads(source.read_text(encoding="utf-8"))
    counts = {"decisions": 0, "assumptions": 0, "actions": 0}
    with _connect(Path(db_path)) as conn:
        for item in data.get("decision_memory", []):
            conn.execute(
                "insert into decisions(decision, owner, status, confidence, source_ref, created_on) values(?,?,?,?,?,?)",
                (
                    str(item.get("decision", "")),
                    str(item.get("owner", "")),
                    str(item.get("status", "Imported")),
                    str(item.get("confidence", "")),
                    str(source),
                    date.today().isoformat(),
                ),
            )
            counts["decisions"] += 1
        for item in data.get("assumption_register", []):
            assumption = item.get("assumption", item) if isinstance(item, Mapping) else item
            conn.execute(
                "insert into assumptions(assumption, status, validation_needed, source_ref, created_on, review_on) values(?,?,?,?,?,?)",
                (str(assumption), "Open", "", str(source), date.today().isoformat(), _future_days(30)),
            )
            counts["assumptions"] += 1
        for item in data.get("action_ledger", []):
            action = item.get("action", item) if isinstance(item, Mapping) else item
            conn.execute(
                "insert into actions(action, owner, status, source_ref, created_on, due_on) values(?,?,?,?,?,?)",
                (str(action), str(item.get("owner", "")) if isinstance(item, Mapping) else "", "Draft", str(source), date.today().isoformat(), _future_days(7)),
            )
            counts["actions"] += 1
        conn.execute("insert into audit_events(event_type, payload, created_on) values(?,?,?)", ("memory_json_migrated", json.dumps(counts), date.today().isoformat()))
    return _result("Memory JSON Migration", {"db_path": db_path, "source_file": str(source), "counts": counts}, facts=[f"Migrated {sum(counts.values())} memory item(s)."])


def save_review_to_db(input_context: Mapping[str, Any], db_path: str) -> Dict[str, Any]:
    try:
        from decision_intelligence_engine import build_autopilot_review
    except ImportError:
        from .decision_intelligence_engine import build_autopilot_review

    init_memory_db(db_path)
    review = build_autopilot_review(input_context)
    packet = review.get("decision_packet", {})
    review_id = ""
    with _connect(Path(db_path)) as conn:
        cur = conn.execute(
            "insert into reviews(title, request_type, payload, created_on) values(?,?,?,?)",
            (str(packet.get("decision_needed", "Autonomous CIO Review"))[:240], str(packet.get("request_type", "")), json.dumps(review, ensure_ascii=False), date.today().isoformat()),
        )
        review_id = str(cur.lastrowid)
        conn.execute(
            "insert into decisions(decision, owner, status, confidence, source_ref, created_on) values(?,?,?,?,?,?)",
            (
                str(packet.get("decision_needed", "")),
                str(packet.get("recommended_action", {}).get("owner", "")),
                "Draft",
                str(packet.get("confidence", "")),
                f"review:{review_id}",
                date.today().isoformat(),
            ),
        )
        for assumption in packet.get("assumptions", []):
            conn.execute(
                "insert into assumptions(assumption, status, validation_needed, source_ref, created_on, review_on) values(?,?,?,?,?,?)",
                (str(assumption), "Open", "", f"review:{review_id}", date.today().isoformat(), _future_days(30)),
            )
        for node in packet.get("evidence_graph", {}).get("nodes", []):
            conn.execute(
                "insert into evidence(claim, source_type, source_ref, quality, created_on, expires_on) values(?,?,?,?,?,?)",
                (str(node.get("label", "")), str(node.get("type", "")), f"review:{review_id}", str(node.get("confidence", "")), date.today().isoformat(), _future_days(45)),
            )
        for chain in packet.get("risk_chain", []):
            conn.execute(
                "insert into risk_chains(signal, dependency, business_impact, source_ref, created_on) values(?,?,?,?,?)",
                (str(chain.get("signal", "")), str(chain.get("dependency", "")), str(chain.get("business_impact", "")), f"review:{review_id}", date.today().isoformat()),
            )
        for action in review.get("action_ledger", []):
            conn.execute(
                "insert into actions(action, owner, status, source_ref, created_on, due_on) values(?,?,?,?,?,?)",
                (str(action.get("draft_action", "")), str(action.get("required_approval", "")), "Draft", f"review:{review_id}", date.today().isoformat(), _future_days(7)),
            )
    return _result("Review Saved To SQLite Memory", {"db_path": db_path, "review_id": review_id}, facts=[f"Saved review {review_id} to local memory DB."])


def query_memory_db(db_path: str, query: str = "", limit: int = 20) -> Dict[str, Any]:
    init_memory_db(db_path)
    like = f"%{query}%"
    results: Dict[str, Any] = {}
    with _connect(Path(db_path)) as conn:
        for table, column in (("decisions", "decision"), ("assumptions", "assumption"), ("actions", "action"), ("evidence", "claim")):
            rows = conn.execute(f"select * from {table} where ? = '' or {column} like ? order by id desc limit ?", (query, like, limit)).fetchall()
            results[table] = [dict(row) for row in rows]
    return _result("SQLite Memory Query", {"db_path": db_path, "query": query, "results": results}, facts=[f"Queried memory DB for '{query}'." if query else "Queried memory DB."])


def memory_aging(db_path: str) -> Dict[str, Any]:
    init_memory_db(db_path)
    today = date.today().isoformat()
    with _connect(Path(db_path)) as conn:
        stale_assumptions = [dict(row) for row in conn.execute("select * from assumptions where status != 'Closed' and review_on <= ?", (today,)).fetchall()]
        stale_evidence = [dict(row) for row in conn.execute("select * from evidence where expires_on <= ?", (today,)).fetchall()]
        overdue_actions = [dict(row) for row in conn.execute("select * from actions where status not in ('Closed','Done') and due_on <= ?", (today,)).fetchall()]
    payload = {"stale_assumptions": stale_assumptions, "stale_evidence": stale_evidence, "overdue_actions": overdue_actions}
    return _result("Memory Aging Review", payload, facts=[f"Found {len(stale_assumptions)} stale assumption(s), {len(stale_evidence)} stale evidence item(s), and {len(overdue_actions)} overdue action(s)."])


def sla_monitor(db_path: str) -> Dict[str, Any]:
    aging = memory_aging(db_path)
    p = aging["memory_aging_review"]
    risk = "High" if p["overdue_actions"] or p["stale_assumptions"] else "Low"
    return _result(
        "Decision SLA Monitor",
        {"db_path": db_path, "breach_risk": risk, **p},
        facts=[f"Decision SLA breach risk is {risk}."],
        recommendation="Review overdue actions and stale assumptions before the next CIO operating review.",
    )


def sla_digest(db_path: str) -> Dict[str, Any]:
    monitor = sla_monitor(db_path)
    p = monitor["decision_sla_monitor"]
    digest = [
        f"Breach risk: {p['breach_risk']}",
        f"Overdue actions: {len(p['overdue_actions'])}",
        f"Stale assumptions: {len(p['stale_assumptions'])}",
        f"Stale evidence: {len(p['stale_evidence'])}",
    ]
    return _result("Decision SLA Digest", {"db_path": db_path, "digest": digest}, facts=digest)


@contextmanager
def _connect(path: Path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def _create_schema(conn: sqlite3.Connection) -> None:
    conn.execute("create table if not exists meta(key text primary key, value text)")
    conn.execute("insert or replace into meta(key,value) values('memory_schema_version', ?)", (SCHEMA_VERSION,))
    conn.execute("create table if not exists decisions(id integer primary key, decision text, owner text, status text, confidence text, source_ref text, created_on text)")
    conn.execute("create table if not exists assumptions(id integer primary key, assumption text, status text, validation_needed text, source_ref text, created_on text, review_on text)")
    conn.execute("create table if not exists evidence(id integer primary key, claim text, source_type text, source_ref text, quality text, created_on text, expires_on text)")
    conn.execute("create table if not exists risk_chains(id integer primary key, signal text, dependency text, business_impact text, source_ref text, created_on text)")
    conn.execute("create table if not exists actions(id integer primary key, action text, owner text, status text, source_ref text, created_on text, due_on text)")
    conn.execute("create table if not exists owners(id integer primary key, owner text, role text, notes text)")
    conn.execute("create table if not exists reviews(id integer primary key, title text, request_type text, payload text, created_on text)")
    conn.execute("create table if not exists source_refs(id integer primary key, source_ref text, source_type text, path text, created_on text)")
    conn.execute("create table if not exists audit_events(id integer primary key, event_type text, payload text, created_on text)")
    conn.execute("create table if not exists feedback(id integer primary key, packet_id text, decision text, rating integer, accepted integer, notes text, payload text, created_on text)")
    conn.execute("create table if not exists outcomes(id integer primary key, packet_id text, decision text, actual_outcome text, score_accuracy integer, realized_risks text, value_result text, payload text, reviewed_on text)")
    conn.execute("create table if not exists score_calibrations(id integer primary key, score_name text, adjustment integer, reason text, sample_size integer, created_on text)")
    conn.execute("create table if not exists learned_patterns(id integer primary key, pattern text, pattern_type text, frequency integer, confidence text, evidence_refs text, created_on text)")
    conn.execute("create table if not exists source_reputation(id integer primary key, source_ref text, trust_score integer, signal_count integer, contradiction_count integer, last_seen text)")
    conn.execute("create table if not exists skill_chain_feedback(id integer primary key, request_type text, skill_chain text, rating integer, accepted integer, notes text, created_on text)")
    conn.execute("create table if not exists board_questions(id integer primary key, persona text, question text, topic text, pressure_level text, source_ref text, created_on text)")
    conn.execute("create table if not exists decision_dna_snapshots(id integer primary key, profile text, payload text, created_on text)")
    conn.execute("create table if not exists risk_appetite_snapshots(id integer primary key, profile text, payload text, created_on text)")
    conn.execute("create table if not exists accountability_edges(id integer primary key, source text, target text, role text, evidence text, created_on text)")
    conn.execute("create table if not exists decision_collisions(id integer primary key, collision text, severity text, payload text, created_on text)")
    conn.execute("create table if not exists strategic_contradictions(id integer primary key, contradiction text, severity text, payload text, created_on text)")
    conn.execute("create table if not exists vendor_truth_records(id integer primary key, vendor_signal text, truth_score integer, payload text, created_on text)")
    conn.execute("create table if not exists control_decision_links(id integer primary key, decision_ref text, control_domain text, evidence_gap text, payload text, created_on text)")
    conn.execute("create table if not exists delegation_drafts(id integer primary key, owner text, task text, evidence_needed text, due_on text, payload text, created_on text)")
    conn.execute("create table if not exists weekly_operating_snapshots(id integer primary key, title text, payload text, created_on text)")
    conn.execute("create table if not exists pending_memory_updates(id integer primary key, area text, payload text, status text, reviewer text default '', created_on text, reviewed_on text)")


def _future_days(days: int) -> str:
    return (date.today() + timedelta(days=days)).isoformat()


def _result(artifact: str, payload: Dict[str, Any], facts: list[str] | None = None, recommendation: str = "Use this output as local decision-support memory only.") -> Dict[str, Any]:
    key = artifact.lower().replace(" ", "_")
    return {
        "artifact": artifact,
        key: payload,
        "facts": facts or [],
        "assumptions": [],
        "hypotheses": ["SQLite memory is local and only changes when an explicit memory command is run."],
        "missing_evidence": [],
        "confidence": "High",
        "recommended_action": {"recommendation": recommendation, "owner": "CIO office", "timebox": "Next review cycle"},
        "guardrails": GUARDRAILS,
    }
