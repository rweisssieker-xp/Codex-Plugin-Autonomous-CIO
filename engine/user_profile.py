"""Local user/company profile support."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Mapping

GUARDRAILS = [
    "Uses only user-provided local context.",
    "Does not claim live system access.",
    "Does not persist memory automatically.",
    "Does not execute external actions.",
    "High-risk domain outputs are decision support, not final specialist determinations.",
]

DEFAULT_PROFILE = {
    "risk_tolerance": "medium",
    "board_style": "concise_challenge_ready",
    "standard_systems": ["ERP", "MES", "QMS", "ITSM", "GitHub"],
    "roles": {"cio": "CIO", "ciso": "CISO", "finance": "CFO", "audit": "Audit"},
    "kpis": ["decision_readiness", "board_risk", "evidence_confidence", "value_leakage"],
    "output_language": "de",
}


def init_profile(path: str) -> Dict[str, Any]:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(DEFAULT_PROFILE, indent=2, ensure_ascii=False), encoding="utf-8")
    return _result("User Company Profile Initialized", {"profile_path": str(target), "profile": DEFAULT_PROFILE}, [f"Initialized local profile at {target}."])


def apply_profile(input_context: Mapping[str, Any], profile_path: str) -> Dict[str, Any]:
    target = Path(profile_path)
    profile = json.loads(target.read_text(encoding="utf-8"))
    enriched = dict(input_context)
    enriched["user_company_profile"] = profile
    enriched.setdefault("constraints", [])
    if isinstance(enriched["constraints"], list):
        enriched["constraints"].append(f"Risk tolerance: {profile.get('risk_tolerance')}")
        enriched["constraints"].append(f"Board style: {profile.get('board_style')}")
    return _result("User Company Profile Applied", {"profile_path": str(target), "input_context": enriched}, [f"Applied local profile from {target}."])


def _result(artifact: str, payload: Dict[str, Any], facts: list[str]) -> Dict[str, Any]:
    return {
        "artifact": artifact,
        artifact.lower().replace(" ", "_"): payload,
        "facts": facts,
        "assumptions": [],
        "hypotheses": ["Profile contains local preferences, not credentials or secrets."],
        "missing_evidence": [],
        "confidence": "High",
        "recommended_action": {"recommendation": "Use profile as context enrichment before building decision packets.", "owner": "CIO office", "timebox": "Before recurring reviews"},
        "guardrails": GUARDRAILS,
    }
