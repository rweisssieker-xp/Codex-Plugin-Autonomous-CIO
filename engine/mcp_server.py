"""Optional MCP adapter for the local Decision Intelligence Engine.

This file is intentionally optional. If the MCP Python package is unavailable,
the module can still be imported and used through the plain Python functions.
"""

from __future__ import annotations

from typing import Any, Dict

try:
    from decision_intelligence_engine import (
        analyze_risk_graph,
        action_governance,
        adapt_connector_export,
        build_autopilot_review,
        build_autopilot_review_from_file,
        build_decision_assurance,
        build_audit_trail,
        build_decision_packet,
        build_decision_packet_from_file,
        build_executive_decision_defense,
        build_llm_extraction_contract,
        benchmark_decision_quality,
        connector_profile_catalog,
        detect_connector_profile,
        compare_packet_trend,
        compare_with_memory,
        export_decision_package,
        export_office_package,
        export_review_artifact,
        export_autopilot_review_artifact,
        evaluate_golden_examples,
        extract_evidence_graph,
        extract_semantic_model,
        generate_dashboard_data,
        generate_dashboard_data_from_file,
        generate_operating_rhythm,
        ingest_connector_signals,
        ingest_source_directory,
        inspect_memory_store,
        refresh_dashboard_data,
        propose_memory_updates,
        run_skill_orchestrator,
        scan_privacy,
        map_risk_chain,
        score_decision_readiness,
        simulate_scenarios,
    )
except ImportError:  # pragma: no cover - package import path
    from .decision_intelligence_engine import (
        analyze_risk_graph,
        action_governance,
        adapt_connector_export,
        build_autopilot_review,
        build_autopilot_review_from_file,
        build_decision_assurance,
        build_audit_trail,
        build_decision_packet,
        build_decision_packet_from_file,
        build_executive_decision_defense,
        build_llm_extraction_contract,
        benchmark_decision_quality,
        connector_profile_catalog,
        detect_connector_profile,
        compare_packet_trend,
        compare_with_memory,
        export_decision_package,
        export_office_package,
        export_review_artifact,
        export_autopilot_review_artifact,
        evaluate_golden_examples,
        extract_evidence_graph,
        extract_semantic_model,
        generate_dashboard_data,
        generate_dashboard_data_from_file,
        generate_operating_rhythm,
        ingest_connector_signals,
        ingest_source_directory,
        inspect_memory_store,
        refresh_dashboard_data,
        propose_memory_updates,
        run_skill_orchestrator,
        scan_privacy,
        map_risk_chain,
        score_decision_readiness,
        simulate_scenarios,
    )


def build_decision_packet_tool(input_context: Dict[str, Any]) -> Dict[str, Any]:
    return build_decision_packet(input_context)


def build_autopilot_review_tool(input_context: Dict[str, Any]) -> Dict[str, Any]:
    return build_autopilot_review(input_context)


def build_autopilot_review_from_file_tool(path: str, memory_path: str | None = None) -> Dict[str, Any]:
    return build_autopilot_review_from_file(path, memory_path)


def build_decision_packet_from_file_tool(path: str) -> Dict[str, Any]:
    return build_decision_packet_from_file(path)


def build_executive_decision_defense_tool(input_context: Dict[str, Any]) -> Dict[str, Any]:
    return build_executive_decision_defense(input_context)


def connector_profile_catalog_tool() -> Dict[str, Any]:
    return connector_profile_catalog()


def build_llm_extraction_contract_tool(input_context: Dict[str, Any]) -> Dict[str, Any]:
    return build_llm_extraction_contract(input_context)


def run_skill_orchestrator_tool(input_context: Dict[str, Any]) -> Dict[str, Any]:
    return run_skill_orchestrator(input_context)


def propose_memory_updates_tool(input_context: Dict[str, Any], memory_context: Dict[str, Any] | None = None) -> Dict[str, Any]:
    return propose_memory_updates(input_context, memory_context)


def inspect_memory_store_tool(path: str) -> Dict[str, Any]:
    return inspect_memory_store(path)


def export_decision_package_tool(input_context: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
    return export_decision_package(input_context, output_dir)


def export_office_package_tool(input_context: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
    return export_office_package(input_context, output_dir)


def detect_connector_profile_tool(path: str) -> Dict[str, Any]:
    return detect_connector_profile(path)


def adapt_connector_export_tool(path: str, profile: str = "auto") -> Dict[str, Any]:
    return adapt_connector_export(path, profile)


def score_decision_readiness_tool(input_context: Dict[str, Any]) -> Dict[str, Any]:
    return score_decision_readiness(input_context)


def map_risk_chain_tool(input_context: Dict[str, Any]) -> Dict[str, Any]:
    return map_risk_chain(input_context)


def extract_evidence_graph_tool(input_context: Dict[str, Any]) -> Dict[str, Any]:
    return extract_evidence_graph(input_context)


def compare_with_memory_tool(input_context: Dict[str, Any], memory_context: Dict[str, Any]) -> Dict[str, Any]:
    return compare_with_memory(input_context, memory_context)


def extract_semantic_model_tool(input_context: Dict[str, Any]) -> Dict[str, Any]:
    return extract_semantic_model(input_context)


def simulate_scenarios_tool(input_context: Dict[str, Any]) -> Dict[str, Any]:
    return simulate_scenarios(input_context)


def build_audit_trail_tool(input_context: Dict[str, Any]) -> Dict[str, Any]:
    return build_audit_trail(input_context)


def generate_dashboard_data_tool(input_context: Dict[str, Any]) -> Dict[str, Any]:
    return generate_dashboard_data(input_context)


def generate_dashboard_data_from_file_tool(path: str) -> Dict[str, Any]:
    return generate_dashboard_data_from_file(path)


def refresh_dashboard_data_tool(input_path: str, output_path: str = "visual-command-center/demo-data.json") -> Dict[str, Any]:
    return refresh_dashboard_data(input_path, output_path)


def generate_operating_rhythm_tool(input_context: Dict[str, Any]) -> Dict[str, Any]:
    return generate_operating_rhythm(input_context)


def benchmark_decision_quality_tool(input_context: Dict[str, Any]) -> Dict[str, Any]:
    return benchmark_decision_quality(input_context)


def ingest_connector_signals_tool(signal_context: Dict[str, Any]) -> Dict[str, Any]:
    return ingest_connector_signals(signal_context)


def ingest_source_directory_tool(path: str) -> Dict[str, Any]:
    return ingest_source_directory(path)


def analyze_risk_graph_tool(input_context: Dict[str, Any]) -> Dict[str, Any]:
    return analyze_risk_graph(input_context)


def compare_packet_trend_tool(input_context: Dict[str, Any]) -> Dict[str, Any]:
    return compare_packet_trend(input_context)


def export_review_artifact_tool(input_context: Dict[str, Any], export_format: str = "markdown") -> Dict[str, Any]:
    return export_review_artifact(input_context, export_format)


def export_autopilot_review_artifact_tool(input_context: Dict[str, Any], export_format: str = "markdown") -> Dict[str, Any]:
    return export_autopilot_review_artifact(input_context, None, export_format)


def scan_privacy_tool(input_context: Dict[str, Any]) -> Dict[str, Any]:
    return scan_privacy(input_context)


def action_governance_tool(input_context: Dict[str, Any]) -> Dict[str, Any]:
    return action_governance(input_context)


def build_decision_assurance_tool(input_context: Dict[str, Any]) -> Dict[str, Any]:
    return build_decision_assurance(input_context)


def evaluate_golden_examples_tool() -> Dict[str, Any]:
    return evaluate_golden_examples()


def create_mcp_server() -> Any:
    try:
        from mcp.server.fastmcp import FastMCP
    except Exception as exc:  # pragma: no cover - optional dependency
        raise RuntimeError("MCP Python package is not installed; use engine/cli.py instead.") from exc

    server = FastMCP("the-autonomous-cio-decision-intelligence")
    server.tool(name="build_decision_packet")(build_decision_packet_tool)
    server.tool(name="build_autopilot_review")(build_autopilot_review_tool)
    server.tool(name="build_autopilot_review_from_file")(build_autopilot_review_from_file_tool)
    server.tool(name="build_decision_packet_from_file")(build_decision_packet_from_file_tool)
    server.tool(name="build_executive_decision_defense")(build_executive_decision_defense_tool)
    server.tool(name="connector_profile_catalog")(connector_profile_catalog_tool)
    server.tool(name="build_llm_extraction_contract")(build_llm_extraction_contract_tool)
    server.tool(name="run_skill_orchestrator")(run_skill_orchestrator_tool)
    server.tool(name="propose_memory_updates")(propose_memory_updates_tool)
    server.tool(name="inspect_memory_store")(inspect_memory_store_tool)
    server.tool(name="export_decision_package")(export_decision_package_tool)
    server.tool(name="export_office_package")(export_office_package_tool)
    server.tool(name="detect_connector_profile")(detect_connector_profile_tool)
    server.tool(name="adapt_connector_export")(adapt_connector_export_tool)
    server.tool(name="score_decision_readiness")(score_decision_readiness_tool)
    server.tool(name="map_risk_chain")(map_risk_chain_tool)
    server.tool(name="extract_evidence_graph")(extract_evidence_graph_tool)
    server.tool(name="compare_with_memory")(compare_with_memory_tool)
    server.tool(name="extract_semantic_model")(extract_semantic_model_tool)
    server.tool(name="simulate_scenarios")(simulate_scenarios_tool)
    server.tool(name="build_audit_trail")(build_audit_trail_tool)
    server.tool(name="generate_dashboard_data")(generate_dashboard_data_tool)
    server.tool(name="generate_dashboard_data_from_file")(generate_dashboard_data_from_file_tool)
    server.tool(name="refresh_dashboard_data")(refresh_dashboard_data_tool)
    server.tool(name="generate_operating_rhythm")(generate_operating_rhythm_tool)
    server.tool(name="benchmark_decision_quality")(benchmark_decision_quality_tool)
    server.tool(name="ingest_connector_signals")(ingest_connector_signals_tool)
    server.tool(name="ingest_source_directory")(ingest_source_directory_tool)
    server.tool(name="analyze_risk_graph")(analyze_risk_graph_tool)
    server.tool(name="compare_packet_trend")(compare_packet_trend_tool)
    server.tool(name="export_review_artifact")(export_review_artifact_tool)
    server.tool(name="export_autopilot_review_artifact")(export_autopilot_review_artifact_tool)
    server.tool(name="scan_privacy")(scan_privacy_tool)
    server.tool(name="action_governance")(action_governance_tool)
    server.tool(name="build_decision_assurance")(build_decision_assurance_tool)
    server.tool(name="evaluate_golden_examples")(evaluate_golden_examples_tool)
    return server


if __name__ == "__main__":  # pragma: no cover - optional runtime entry
    create_mcp_server().run()
