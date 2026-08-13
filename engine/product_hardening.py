"""Product-hardening utilities for the local Autonomous CIO runtime."""

from __future__ import annotations

from contextlib import contextmanager
from datetime import date
import json
import shutil
import sqlite3
import zipfile
from pathlib import Path
from typing import Any, Dict, Mapping

try:
    from decision_intelligence_engine import build_decision_packet, build_llm_extraction_contract, propose_memory_updates
    from eval_runner import run_evals
    from memory_store import init_memory_db
except ImportError:
    from .decision_intelligence_engine import build_decision_packet, build_llm_extraction_contract, propose_memory_updates
    from .eval_runner import run_evals
    from .memory_store import init_memory_db


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "engine" / "schemas"

GUARDRAILS = [
    "Uses only user-provided local context and optional local SQLite memory.",
    "Does not claim live system access.",
    "Does not persist memory automatically.",
    "Does not execute external actions.",
    "Does not train or update an external model.",
    "High-risk domain outputs are decision support, not final specialist determinations.",
]


def build_llm_extraction_pipeline(input_context: Mapping[str, Any]) -> Dict[str, Any]:
    """Accept host-LLM structured extraction or produce a local fallback packet."""
    contract = build_llm_extraction_contract(input_context)
    llm_extraction = input_context.get("llm_extraction")
    if not isinstance(llm_extraction, Mapping):
        llm_extraction = _fallback_extraction(input_context)
        mode = "heuristic_fallback"
    else:
        mode = "host_llm_structured_input"
    enriched = dict(input_context)
    enriched["llm_extraction"] = dict(llm_extraction)
    packet = build_decision_packet(enriched)
    extraction_check = _validate_extraction(dict(llm_extraction), contract["contract"]["required_output_fields"])
    packet_check = validate_output_schema(packet, "executive-decision-packet.schema.json")
    return {
        "artifact": "LLM Extraction Pipeline",
        "llm_extraction_pipeline": {
            "mode": mode,
            "contract": contract["contract"],
            "extraction": llm_extraction,
            "extraction_check": extraction_check,
            "packet_schema_check": packet_check["schema_validation"],
            "decision_packet": packet,
        },
        "facts": packet["facts"],
        "assumptions": packet["assumptions"],
        "hypotheses": packet["hypotheses"],
        "missing_evidence": packet["missing_evidence"],
        "confidence": packet["confidence"],
        "recommended_action": packet["recommended_action"],
        "guardrails": GUARDRAILS,
    }


def validate_output_schema(output: Mapping[str, Any], schema_name: str) -> Dict[str, Any]:
    schema_path = SCHEMA_DIR / schema_name
    if not schema_path.exists():
        raise FileNotFoundError(f"schema not found: {schema_name}")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = _validate_node(output, schema, "$")
    payload = {"schema": schema_name, "valid": not errors, "errors": errors}
    return _result("Schema Validation", {"schema_validation": payload}, [f"Validated output against {schema_name}."])


def validate_schema_file(output_path: str, schema_name: str) -> Dict[str, Any]:
    data = json.loads(Path(output_path).read_text(encoding="utf-8"))
    if not isinstance(data, Mapping):
        raise ValueError("output JSON root must be an object")
    return validate_output_schema(data, schema_name)


def queue_memory_updates(input_context: Mapping[str, Any], db_path: str) -> Dict[str, Any]:
    init_memory_db(db_path)
    proposal = propose_memory_updates(input_context, {})
    updates = []
    payload = proposal.get("memory_update_proposal", {})
    for area in ("decision_memory", "assumption_register", "evidence_graph", "risk_chain_map", "action_ledger"):
        value = payload.get(area, [])
        items = value if isinstance(value, list) else [value]
        for item in items:
            if item:
                updates.append({"area": area, "payload": item})
    with _connect(db_path) as conn:
        for item in updates:
            conn.execute(
                "insert into pending_memory_updates(area,payload,status,created_on,reviewed_on) values(?,?,?,?,?)",
                (item["area"], json.dumps(item["payload"], ensure_ascii=False), "Pending", date.today().isoformat(), ""),
            )
    return _result(
        "Memory Update Queue",
        {"memory_update_queue": {"db_path": db_path, "queued_count": len(updates), "status": "Pending", "updates": updates}},
        [f"Queued {len(updates)} pending memory update(s)."],
        "Review queued updates and approve only evidence-backed memory changes.",
    )


def list_memory_update_queue(db_path: str, status: str = "Pending") -> Dict[str, Any]:
    init_memory_db(db_path)
    with _connect(db_path) as conn:
        rows = _rows(conn, "select * from pending_memory_updates where ? = '' or status = ? order by id desc", (status, status))
    return _result("Memory Update Queue Review", {"memory_update_queue_review": {"db_path": db_path, "status": status, "updates": rows}}, [f"Loaded {len(rows)} queued memory update(s)."])


def review_memory_update(db_path: str, update_id: int, decision: str, reviewer: str = "CIO office") -> Dict[str, Any]:
    if decision not in {"Approved", "Rejected"}:
        raise ValueError("decision must be Approved or Rejected")
    init_memory_db(db_path)
    with _connect(db_path) as conn:
        row = conn.execute("select * from pending_memory_updates where id = ?", (update_id,)).fetchone()
        if row is None:
            raise ValueError(f"pending memory update not found: {update_id}")
        conn.execute(
            "update pending_memory_updates set status = ?, reviewer = ?, reviewed_on = ? where id = ?",
            (decision, reviewer, date.today().isoformat(), update_id),
        )
    return _result("Memory Update Reviewed", {"memory_update_reviewed": {"db_path": db_path, "update_id": update_id, "decision": decision, "reviewer": reviewer}}, [f"Marked memory update {update_id} as {decision}."])


def skill_suite_map() -> Dict[str, Any]:
    suites = [
        {"suite": "Board Decision Suite", "frontdoor": "autonomous-cio-orchestrator", "skills": ["executive-decision-packet", "board-challenger", "executive-decision-defense"], "engine_commands": ["build-decision-packet", "synthetic-executive-committee", "decision-chain-custody"]},
        {"suite": "Crisis Command Suite", "frontdoor": "autonomous-cio-operating-review", "skills": ["crisis-command-mode", "risk-chain-intelligence", "autonomous-action-framework"], "engine_commands": ["autopilot-review", "map-risk-chain", "kill-criteria-sentinel"]},
        {"suite": "AI Governance Suite", "frontdoor": "autonomous-cio-orchestrator", "skills": ["ai-governance-intelligence", "governance-gap-predictor", "executive-decision-packet"], "engine_commands": ["llm-extraction-pipeline", "evaluate-policy", "control-debt-ledger"]},
        {"suite": "Transformation Value Suite", "frontdoor": "autonomous-cio-operating-review", "skills": ["transformation-value-tracker", "value-leakage-intelligence", "decision-debt-intelligence"], "engine_commands": ["benefit-realization-memory", "decision-latency-cost", "strategic-drift-warning"]},
        {"suite": "Vendor and Operating Model Suite", "frontdoor": "autonomous-cio-orchestrator", "skills": ["vendor-risk-intelligence", "operating-model-debt", "executive-accountability"], "engine_commands": ["vendor-promise-backtest", "enterprise-operating-twin", "accountability-graph"]},
        {"suite": "Autonomy and Memory Suite", "frontdoor": "autonomous-cio-operating-review", "skills": ["autonomous-executive-memory", "autonomous-action-framework", "human-control-contract"], "engine_commands": ["queue-memory-updates", "autonomy-contract", "cio-replacement-surface-map"]},
    ]
    return _result("Skill Suite Map", {"skill_suite_map": {"suite_count": len(suites), "suites": suites}}, [f"Mapped {len(suites)} product-frontdoor skill suite(s)."])


def run_hardening_evals(eval_dir: str = "engine/evals") -> Dict[str, Any]:
    report = run_evals(eval_dir)
    results = report["eval_report"]["results"]
    high_risk_cases = [item for item in results if item["request_type"] in {"Crisis Command", "AI Approval", "Board Prep"}]
    payload = {
        "base_eval_report": report["eval_report"],
        "hardening_checks": {
            "minimum_case_count": len(results) >= 50,
            "high_risk_case_count": len(high_risk_cases),
            "failed_count": report["eval_report"]["failed_count"],
            "guardrail_regression": report["eval_report"]["failed_count"] == 0,
        },
    }
    return _result("Hardening Eval Report", {"hardening_eval_report": payload}, [f"Ran hardening evals across {len(results)} case(s)."], "Treat any failed hardening check as release-blocking.")


def build_release_package(output_dir: str) -> Dict[str, Any]:
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    notes = _release_notes()
    notes_path = target / "RELEASE_NOTES.md"
    manifest_path = target / "release-manifest.json"
    zip_path = target / "the-autonomous-cio-local-release.zip"
    notes_path.write_text(notes, encoding="utf-8")
    manifest = {
        "artifact": "Autonomous CIO Local Release Package",
        "version": "0.1.0",
        "generated_on": date.today().isoformat(),
        "included_paths": ["README.md", "docs", "engine", "app", "scripts", ".codex-plugin"],
        "safety": GUARDRAILS,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for rel in manifest["included_paths"]:
            source = ROOT / rel
            if source.is_file():
                archive.write(source, source.relative_to(ROOT))
            elif source.is_dir():
                for path in source.rglob("*"):
                    if path.is_file() and ".local-" not in str(path):
                        archive.write(path, path.relative_to(ROOT))
        archive.write(notes_path, notes_path.name)
        archive.write(manifest_path, manifest_path.name)
    return _result("Release Package", {"release_package": {"output_dir": str(target), "notes": str(notes_path), "manifest": str(manifest_path), "zip": str(zip_path), "zip_size_bytes": zip_path.stat().st_size}}, [f"Built local release package at {zip_path}."])


@contextmanager
def _connect(db_path: str):
    conn = sqlite3.connect(Path(db_path))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def _rows(conn: sqlite3.Connection, query: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    return [dict(row) for row in conn.execute(query, params).fetchall()]


def _fallback_extraction(input_context: Mapping[str, Any]) -> Dict[str, Any]:
    packet = build_decision_packet(input_context)
    return {
        "facts": packet["facts"],
        "assumptions": packet["assumptions"],
        "hypotheses": packet["hypotheses"],
        "missing_evidence": packet["missing_evidence"],
        "contradictions": packet["contradictions"],
        "weak_signals": packet["weak_signals"],
        "entities": packet["semantic_model"]["entities"],
        "decisions": [packet["decision_needed"]],
        "risks": [item.get("business_impact", "") for item in packet["risk_chain"]],
        "actions": packet["draft_next_steps"]["next_24h"],
    }


def _validate_extraction(extraction: Mapping[str, Any], required_fields: list[str]) -> Dict[str, Any]:
    missing = [field for field in required_fields if field not in extraction]
    empty = [field for field in required_fields if field in extraction and not extraction.get(field)]
    return {"valid": not missing, "missing_fields": missing, "empty_fields": empty}


def _validate_node(data: Any, schema: Mapping[str, Any], path: str) -> list[str]:
    errors: list[str] = []
    if "const" in schema and data != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}")
    expected_type = schema.get("type")
    if expected_type and not _type_ok(data, expected_type):
        errors.append(f"{path}: expected type {expected_type}")
        return errors
    if isinstance(data, Mapping):
        for key in schema.get("required", []):
            if key not in data:
                errors.append(f"{path}.{key}: required key missing")
        properties = schema.get("properties", {})
        if isinstance(properties, Mapping):
            for key, child_schema in properties.items():
                if key in data and isinstance(child_schema, Mapping):
                    errors.extend(_validate_node(data[key], child_schema, f"{path}.{key}"))
    if isinstance(data, (int, float)):
        if "minimum" in schema and data < schema["minimum"]:
            errors.append(f"{path}: below minimum {schema['minimum']}")
        if "maximum" in schema and data > schema["maximum"]:
            errors.append(f"{path}: above maximum {schema['maximum']}")
    return errors


def _type_ok(data: Any, expected_type: str) -> bool:
    if expected_type == "object":
        return isinstance(data, Mapping)
    if expected_type == "array":
        return isinstance(data, list)
    if expected_type == "string":
        return isinstance(data, str)
    if expected_type == "integer":
        return isinstance(data, int) and not isinstance(data, bool)
    if expected_type == "boolean":
        return isinstance(data, bool)
    return True


def _release_notes() -> str:
    return """# The Autonomous CIO 0.1.0 Local Release

## Release Focus

- AI-native executive decision intelligence for CIO operating workflows.
- Local Decision Intelligence Engine with schema validation, LLM extraction pipeline, memory approval queue, skill suites and release packaging.
- Governed decision support only: no live access, no external execution and no automatic persistence.

## Proof Path

1. Seed demo memory from the local web app.
2. Build an Executive Decision Packet.
3. Queue memory updates for review.
4. Generate the Executive Weekly Brief.
5. Export board pack and release artifacts.

## Validation

Run:

```text
powershell -ExecutionPolicy Bypass -File scripts\\run-engine-smoke-tests.ps1
```
"""


def _result(artifact: str, payload: Dict[str, Any], facts: list[str], recommendation: str = "Use this output as local decision support only.") -> Dict[str, Any]:
    return {
        "artifact": artifact,
        **payload,
        "facts": facts,
        "assumptions": [],
        "hypotheses": ["Product-hardening outputs are local deterministic checks over provided context and files."],
        "missing_evidence": [],
        "confidence": "High",
        "recommended_action": {"recommendation": recommendation, "owner": "CIO office", "timebox": "Before release or operating cadence"},
        "guardrails": GUARDRAILS,
    }
