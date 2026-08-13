"""Enterprise operating intelligence for CIO decision support."""

from __future__ import annotations

from contextlib import contextmanager
from datetime import date
from html import escape
import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, Mapping

try:
    from decision_intelligence_engine import build_decision_packet
    from decision_behavior import build_board_memory, build_decision_dna, build_risk_appetite_twin
    from memory_store import init_memory_db, memory_aging
except ImportError:
    from .decision_intelligence_engine import build_decision_packet
    from .decision_behavior import build_board_memory, build_decision_dna, build_risk_appetite_twin
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


def build_executive_weekly_brief(db_path: str, output_dir: str | None = None, export_format: str = "markdown") -> Dict[str, Any]:
    autopilot = build_weekly_operating_autopilot(db_path)
    data = autopilot["cio_weekly_operating_autopilot"]
    behavior = {
        "decision_dna": build_decision_dna(db_path).get("decision_dna", {}),
        "risk_appetite": build_risk_appetite_twin(db_path).get("cio_risk_appetite_twin", {}),
        "board_memory": build_board_memory(db_path).get("board_memory", {}),
    }
    quality = _brief_quality(data, behavior)
    markdown = _weekly_markdown(data, behavior, quality)
    files: list[str] = []
    formats = [export_format]
    if export_format == "both":
        formats = ["markdown", "html"]
    target = Path(output_dir) if output_dir else None
    if target:
        target.mkdir(parents=True, exist_ok=True)
        if "markdown" in formats:
            md_path = target / "executive_weekly_brief.md"
            md_path.write_text(markdown, encoding="utf-8")
            files.append(str(md_path))
        if "html" in formats:
            html_path = target / "executive_weekly_brief.html"
            html_path.write_text(_weekly_html(markdown), encoding="utf-8")
            files.append(str(html_path))
    content = _weekly_html(markdown) if export_format == "html" else markdown
    payload = {
        "db_path": db_path,
        "format": export_format,
        "content": content,
        "files": files,
        "top_decision_count": len(data.get("top_decisions", [])),
        "overdue_action_count": len(data.get("overdue_actions", [])),
        "stale_assumption_count": len(data.get("stale_assumptions", [])),
        "board_risk_count": len(data.get("board_risks", [])),
        "vendor_pressure_count": len(data.get("vendor_pressure", [])),
        "evidence_gap_count": len(data.get("evidence_gaps", [])),
        "brief_quality": quality,
        "decision_dna": behavior["decision_dna"],
        "risk_appetite": behavior["risk_appetite"],
        "board_memory": behavior["board_memory"],
    }
    return {
        "artifact": "Executive Weekly Brief",
        "executive_weekly_brief": payload,
        "facts": autopilot["facts"],
        "assumptions": autopilot["assumptions"],
        "hypotheses": autopilot["hypotheses"],
        "missing_evidence": autopilot["missing_evidence"],
        "confidence": autopilot["confidence"],
        "recommended_action": {"recommendation": "Use this brief as the Monday CIO operating start point.", "owner": "CIO office", "timebox": "Weekly"},
        "guardrails": GUARDRAILS,
    }


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


def _weekly_markdown(data: Mapping[str, Any], behavior: Mapping[str, Any], quality: Mapping[str, Any]) -> str:
    decision_dna = behavior.get("decision_dna", {})
    risk_appetite = behavior.get("risk_appetite", {})
    board_memory = behavior.get("board_memory", {})
    lines = [
        "# Executive Weekly Brief",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        "## Executive Snapshot",
        f"- Brief quality score: {quality.get('score')} ({quality.get('posture')})",
        f"- Decision DNA: {decision_dna.get('dominant_pattern', 'insufficient_history')}",
        f"- Risk appetite: {risk_appetite.get('profile', 'insufficient_history')}",
        f"- Board memory questions: {board_memory.get('question_count', 0)}",
        "",
        "## Monday CIO Focus",
        f"- Top decisions: {len(data.get('top_decisions', []))}",
        f"- Overdue actions: {len(data.get('overdue_actions', []))}",
        f"- Stale assumptions: {len(data.get('stale_assumptions', []))}",
        f"- Board risks: {len(data.get('board_risks', []))}",
        f"- Vendor pressure: {len(data.get('vendor_pressure', []))}",
        f"- Evidence gaps: {len(data.get('evidence_gaps', []))}",
        "",
        "## Top Decisions",
    ]
    lines.extend(_bullets(data.get("top_decisions", []), "decision"))
    lines.extend(["", "## Overdue Actions"])
    lines.extend(_bullets(data.get("overdue_actions", []), "action"))
    lines.extend(["", "## Stale Assumptions"])
    lines.extend(_bullets(data.get("stale_assumptions", []), "assumption"))
    lines.extend(["", "## Board Risks"])
    lines.extend(_bullets(data.get("board_risks", []), "business_impact"))
    lines.extend(["", "## Vendor Pressure"])
    lines.extend(_bullets(data.get("vendor_pressure", []), "business_impact"))
    lines.extend(["", "## Evidence Gaps"])
    lines.extend(_bullets(data.get("evidence_gaps", []), "claim"))
    lines.extend(
        [
            "",
        "## Next 24h",
        "- Close the highest-risk evidence gap.",
        "- Confirm owners for overdue actions.",
        "- Prepare board-risk wording with visible uncertainty.",
            "",
            "## Next 7d",
            "- Resolve stale assumptions or mark them as accepted risk.",
            "- Challenge vendor-dependent milestones with evidence.",
            "- Update the local memory with outcomes and feedback.",
            "",
            "## Next 30d",
            "- Backtest recommendations against outcomes.",
            "- Refresh Decision DNA and Risk Appetite Twin.",
            "- Retire recurring decision debt from the ledger.",
        ]
    )
    return "\n".join(lines)


def _brief_quality(data: Mapping[str, Any], behavior: Mapping[str, Any]) -> Dict[str, Any]:
    factors = {
        "decision_coverage": min(100, len(data.get("top_decisions", [])) * 20),
        "risk_visibility": min(100, len(data.get("board_risks", [])) * 20 + len(data.get("vendor_pressure", [])) * 10),
        "evidence_visibility": min(100, len(data.get("evidence_gaps", [])) * 20),
        "memory_freshness": max(0, 100 - len(data.get("stale_assumptions", [])) * 15 - len(data.get("overdue_actions", [])) * 12),
        "board_context": min(100, int(behavior.get("board_memory", {}).get("question_count", 0)) * 20),
    }
    score = round(sum(factors.values()) / len(factors))
    return {"score": score, "posture": "Board-ready" if score >= 75 else "Usable with gaps" if score >= 45 else "Needs memory", "factors": factors}


def _bullets(items: list[Mapping[str, Any]], field: str) -> list[str]:
    if not items:
        return ["- None recorded in local memory."]
    lines = []
    for item in items[:8]:
        value = str(item.get(field) or item.get("decision") or item.get("action") or item.get("claim") or item)
        owner = item.get("owner") or item.get("source_ref") or item.get("created_on") or ""
        suffix = f" ({owner})" if owner else ""
        lines.append(f"- {value}{suffix}")
    return lines


def _weekly_html(markdown: str) -> str:
    html_lines = []
    for line in markdown.splitlines():
        if line.startswith("# "):
            html_lines.append(f"<h1>{escape(line[2:])}</h1>")
        elif line.startswith("## "):
            html_lines.append(f"<h2>{escape(line[3:])}</h2>")
        elif line.startswith("- "):
            html_lines.append(f"<li>{escape(line[2:])}</li>")
        elif not line:
            html_lines.append("")
        else:
            html_lines.append(f"<p>{escape(line)}</p>")
    body = "\n".join(html_lines)
    return f"<!doctype html><html><head><meta charset=\"utf-8\"><title>Executive Weekly Brief</title><style>body{{font-family:Arial,sans-serif;margin:32px;line-height:1.45;color:#172026}}h1,h2{{color:#0f766e}}li{{margin:4px 0}}</style></head><body>{body}</body></html>"


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
