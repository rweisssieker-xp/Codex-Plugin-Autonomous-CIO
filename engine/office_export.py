"""High-level board pack export wrappers."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Mapping

GUARDRAILS = [
    "Uses only user-provided local context.",
    "Does not claim live system access.",
    "Does not persist memory automatically.",
    "Does not execute external actions.",
    "High-risk domain outputs are decision support, not final specialist determinations.",
]


def build_board_pack(input_context: Mapping[str, Any], output_dir: str, export_format: str = "both") -> Dict[str, Any]:
    try:
        from decision_intelligence_engine import export_decision_package, export_office_package, build_decision_packet
    except ImportError:
        from .decision_intelligence_engine import export_decision_package, export_office_package, build_decision_packet

    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    files = []
    if export_format in {"markdown", "json", "both"}:
        package = export_decision_package(input_context, str(target / "json_markdown"))
        files.extend(package.get("files", []))
    if export_format in {"docx", "pptx", "office", "both"}:
        office = export_office_package(input_context, str(target / "office"))
        if export_format == "docx":
            files.extend([path for path in office.get("files", []) if path.endswith(".docx")])
        elif export_format == "pptx":
            files.extend([path for path in office.get("files", []) if path.endswith(".pptx")])
        else:
            files.extend(office.get("files", []))
    packet = build_decision_packet(input_context)
    return {
        "artifact": "High Quality Board Pack",
        "output_dir": str(target),
        "format": export_format,
        "files": files,
        "facts": packet["facts"],
        "assumptions": packet["assumptions"],
        "hypotheses": packet["hypotheses"],
        "missing_evidence": packet["missing_evidence"],
        "confidence": packet["confidence"],
        "recommended_action": packet["recommended_action"],
        "guardrails": GUARDRAILS,
    }
