"""Local source bundle and connector discovery helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

GUARDRAILS = [
    "Uses only user-provided local context.",
    "Does not claim live system access.",
    "Does not persist memory automatically.",
    "Does not execute external actions.",
    "High-risk domain outputs are decision support, not final specialist determinations.",
]

SUPPORTED = {".json", ".csv", ".txt", ".md"}


def discover_sources(path: str = "engine/examples") -> Dict[str, Any]:
    root = Path(path)
    files = sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED) if root.exists() else []
    sources = [{"path": str(p), "extension": p.suffix.lower(), "profile_hint": _profile_hint(p.name)} for p in files]
    return _result("Source Discovery", {"root": str(root), "sources": sources}, [f"Discovered {len(sources)} local source file(s)."])


def pull_signals(path: str, profile: str = "auto") -> Dict[str, Any]:
    try:
        from decision_intelligence_engine import adapt_connector_export
    except ImportError:
        from .decision_intelligence_engine import adapt_connector_export

    return adapt_connector_export(path, profile)


def ingest_source_bundle(input_dir: str, db_path: str | None = None, profile: str = "auto") -> Dict[str, Any]:
    try:
        from decision_intelligence_engine import adapt_connector_export, build_decision_packet
        from memory_store import save_review_to_db
    except ImportError:
        from .decision_intelligence_engine import adapt_connector_export, build_decision_packet
        from .memory_store import save_review_to_db

    root = Path(input_dir)
    if not root.exists() or not root.is_dir():
        raise FileNotFoundError(f"source bundle directory not found: {input_dir}")
    signals = []
    provenance = []
    for file_path in sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED):
        try:
            adapted = adapt_connector_export(str(file_path), profile)
            signals.extend(adapted.get("normalized_signals", []))
            provenance.append({"source_file": str(file_path), "profile": adapted.get("profile"), "signals_created": adapted.get("signals_created", 0)})
        except Exception as exc:
            provenance.append({"source_file": str(file_path), "error": str(exc)})
    context = {"title": root.name, "signals": [signal["summary"] for signal in signals], "decision_request": "Build an integrated decision packet from the local source bundle."}
    packet = build_decision_packet(context)
    saved = None
    if db_path:
        saved = save_review_to_db(context, db_path)
    return {
        "artifact": "Source Bundle Ingestion",
        "source_bundle": {"input_dir": str(root), "signals_created": len(signals), "source_provenance": provenance, "memory_save": saved},
        "decision_packet": packet,
        "facts": packet["facts"],
        "assumptions": packet["assumptions"],
        "hypotheses": packet["hypotheses"],
        "missing_evidence": packet["missing_evidence"],
        "confidence": packet["confidence"],
        "recommended_action": packet["recommended_action"],
        "guardrails": GUARDRAILS,
    }


def connector_readiness_report(path: str = "engine/examples") -> Dict[str, Any]:
    root = Path(path)
    local_sources = discover_sources(path)["source_discovery"]["sources"]
    profiles = sorted({source["profile_hint"] for source in local_sources if source["profile_hint"] != "auto"})
    live_profiles = [
        "outlook_email",
        "outlook_calendar",
        "teams_messages",
        "sharepoint_documents",
        "github_delivery",
        "jira_delivery",
        "azure_devops_delivery",
        "topdesk_service",
    ]
    readiness = []
    for profile in live_profiles:
        hint = profile.split("_")[0]
        readiness.append(
            {
                "profile": profile,
                "local_export_adapter_ready": hint in profiles or any(hint in source["path"].lower() for source in local_sources),
                "live_connector_ready": False,
                "required_for_live": "Enable the matching Codex/App connector and provide explicit user authorization in the host environment.",
                "external_execution_allowed": False,
            }
        )
    payload = {
        "root": str(root),
        "local_source_count": len(local_sources),
        "detected_local_profiles": profiles,
        "connector_readiness": readiness,
        "live_access_claim": False,
        "safe_default": "Use local exports and source bundles unless a host connector is explicitly available and authorized.",
    }
    return {
        "artifact": "Connector Readiness Report",
        "connector_readiness_report": payload,
        "facts": [f"Inspected {len(local_sources)} local source file(s)."],
        "assumptions": ["Live connector availability cannot be inferred from local files."],
        "hypotheses": ["Export-first adapters are sufficient for marketplace review and local pilots."],
        "missing_evidence": ["Authorized live connector context is not supplied."],
        "confidence": "High",
        "recommended_action": {
            "recommendation": "Pilot live connector profiles only after the matching Codex connector is authorized by the user.",
            "owner": "CIO office",
            "timebox": "Before live enterprise rollout",
        },
        "guardrails": GUARDRAILS,
    }


def _profile_hint(name: str) -> str:
    low = name.lower()
    for key in ("topdesk", "servicenow", "jira", "azure", "github", "slack", "gmail", "outlook", "sharepoint", "sap", "erp", "cmdb", "security", "cloud", "observability"):
        if key in low:
            return key
    return "auto"


def _result(artifact: str, payload: Dict[str, Any], facts: list[str]) -> Dict[str, Any]:
    return {
        "artifact": artifact,
        artifact.lower().replace(" ", "_"): payload,
        "facts": facts,
        "assumptions": [],
        "hypotheses": ["Discovery inspects local files only."],
        "missing_evidence": [],
        "confidence": "High",
        "recommended_action": {"recommendation": "Use pull-signals or ingest-source-bundle on selected local sources.", "owner": "CIO office", "timebox": "Before analysis"},
        "guardrails": GUARDRAILS,
    }
