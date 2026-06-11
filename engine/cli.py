"""Command-line interface for the local Decision Intelligence Engine."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
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
        import_context_file,
        refresh_dashboard_data,
        propose_memory_updates,
        run_skill_orchestrator,
        save_packet_to_memory,
        scan_privacy,
        map_risk_chain,
        score_decision_readiness,
        simulate_scenarios,
    )
except ImportError:  # pragma: no cover - package execution path
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
        import_context_file,
        refresh_dashboard_data,
        propose_memory_updates,
        run_skill_orchestrator,
        save_packet_to_memory,
        scan_privacy,
        map_risk_chain,
        score_decision_readiness,
        simulate_scenarios,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="The Autonomous CIO Decision Intelligence Engine")
    sub = parser.add_subparsers(dest="command", required=True)

    for name in (
        "build-decision-packet",
        "score",
        "map-risk-chain",
        "extract-evidence-graph",
        "semantic-model",
        "simulate-scenarios",
        "audit-trail",
        "dashboard-data",
        "operating-rhythm",
        "benchmark",
        "ingest-signals",
        "risk-graph",
        "trend-delta",
        "privacy-scan",
        "action-governance",
        "assurance",
        "decision-defense",
        "llm-extraction-contract",
        "orchestrate",
        "propose-memory-updates",
    ):
        cmd = sub.add_parser(name)
        cmd.add_argument("--input", required=True, help="Path to input JSON context")

    sub.add_parser("connector-profiles")

    export = sub.add_parser("export-review")
    export.add_argument("--input", required=True, help="Path to input JSON context")
    export.add_argument("--format", default="markdown", choices=["markdown", "json"], help="Export format")

    export_package = sub.add_parser("export-package")
    export_package.add_argument("--input", required=True, help="Path to input JSON context")
    export_package.add_argument("--output-dir", required=True, help="Directory for generated export artifacts")

    office_package = sub.add_parser("export-office-package")
    office_package.add_argument("--input", required=True, help="Path to input JSON context")
    office_package.add_argument("--output-dir", required=True, help="Directory for generated DOCX/PPTX artifacts")

    detect_export = sub.add_parser("detect-connector-profile")
    detect_export.add_argument("--input", required=True, help="Path to local connector export file")

    adapt_export = sub.add_parser("adapt-connector-export")
    adapt_export.add_argument("--input", required=True, help="Path to local connector export file")
    adapt_export.add_argument("--profile", default="auto", help="Connector profile name or auto")

    import_cmd = sub.add_parser("import-context")
    import_cmd.add_argument("--input", required=True, help="Path to .json, .csv, .txt or .md input")

    autopilot = sub.add_parser("autopilot-review")
    autopilot.add_argument("--input", required=True, help="Path to .json, .csv, .txt, .md or source directory")
    autopilot.add_argument("--memory", default=None, help="Optional local memory store JSON")
    autopilot.add_argument("--output", default=None, help="Optional output file path")
    autopilot.add_argument("--format", default="json", choices=["json", "markdown"], help="Output format")
    autopilot.add_argument("--view", default="full", choices=["compact", "board", "full"], help="Markdown view for autopilot-review")

    file_packet = sub.add_parser("build-from-file")
    file_packet.add_argument("--input", required=True, help="Path to .json, .csv, .txt or .md input")

    file_dashboard = sub.add_parser("dashboard-from-file")
    file_dashboard.add_argument("--input", required=True, help="Path to .json, .csv, .txt or .md input")

    refresh_dashboard = sub.add_parser("refresh-dashboard")
    refresh_dashboard.add_argument("--input", required=True, help="Path to .json, .csv, .txt or .md input")
    refresh_dashboard.add_argument("--output", default="visual-command-center/demo-data.json", help="Path to dashboard JSON output")

    ingest_dir = sub.add_parser("ingest-directory")
    ingest_dir.add_argument("--input", required=True, help="Path to a local source directory")

    save_cmd = sub.add_parser("save-memory")
    save_cmd.add_argument("--input", required=True, help="Path to input JSON context")
    save_cmd.add_argument("--memory", required=True, help="Path to local memory store JSON")

    eval_cmd = sub.add_parser("evaluate")
    eval_cmd.add_argument("--examples-dir", default=None, help="Optional examples directory")

    compare = sub.add_parser("compare-memory")
    compare.add_argument("--input", required=True, help="Path to input JSON context")
    compare.add_argument("--memory", required=True, help="Path to memory JSON context")

    inspect_memory = sub.add_parser("inspect-memory")
    inspect_memory.add_argument("--memory", required=True, help="Path to local memory store JSON")

    args = parser.parse_args(argv)

    try:
        file_commands = {
            "import-context",
            "build-from-file",
            "dashboard-from-file",
            "refresh-dashboard",
            "ingest-directory",
            "autopilot-review",
            "detect-connector-profile",
            "adapt-connector-export",
        }
        no_input_commands = {"evaluate", "connector-profiles", "inspect-memory"}
        input_context = None if args.command in no_input_commands else _read_json(args.input) if args.command not in file_commands else None
        if args.command == "build-decision-packet":
            result = build_decision_packet(input_context)
        elif args.command == "score":
            result = score_decision_readiness(input_context)
        elif args.command == "map-risk-chain":
            result = map_risk_chain(input_context)
        elif args.command == "extract-evidence-graph":
            result = extract_evidence_graph(input_context)
        elif args.command == "semantic-model":
            result = extract_semantic_model(input_context)
        elif args.command == "simulate-scenarios":
            result = simulate_scenarios(input_context)
        elif args.command == "audit-trail":
            result = build_audit_trail(input_context)
        elif args.command == "dashboard-data":
            result = generate_dashboard_data(input_context)
        elif args.command == "operating-rhythm":
            result = generate_operating_rhythm(input_context)
        elif args.command == "benchmark":
            result = benchmark_decision_quality(input_context)
        elif args.command == "ingest-signals":
            result = ingest_connector_signals(input_context)
        elif args.command == "risk-graph":
            result = analyze_risk_graph(input_context)
        elif args.command == "trend-delta":
            result = compare_packet_trend(input_context)
        elif args.command == "export-review":
            result = export_review_artifact(input_context, args.format)
        elif args.command == "privacy-scan":
            result = scan_privacy(input_context)
        elif args.command == "action-governance":
            result = action_governance(input_context)
        elif args.command == "assurance":
            result = build_decision_assurance(input_context)
        elif args.command == "decision-defense":
            result = build_executive_decision_defense(input_context)
        elif args.command == "llm-extraction-contract":
            result = build_llm_extraction_contract(input_context)
        elif args.command == "orchestrate":
            result = run_skill_orchestrator(input_context)
        elif args.command == "propose-memory-updates":
            result = propose_memory_updates(input_context)
        elif args.command == "connector-profiles":
            result = connector_profile_catalog()
        elif args.command == "export-package":
            result = export_decision_package(input_context, args.output_dir)
        elif args.command == "export-office-package":
            result = export_office_package(input_context, args.output_dir)
        elif args.command == "detect-connector-profile":
            result = detect_connector_profile(args.input)
        elif args.command == "adapt-connector-export":
            result = adapt_connector_export(args.input, args.profile)
        elif args.command == "autopilot-review":
            review = build_autopilot_review_from_file(args.input, args.memory)
            if args.format == "json":
                result = review
            else:
                result = {
                    "artifact": "Autopilot Review Export",
                    "format": "markdown",
                    "view": args.view,
                    "content": _autopilot_markdown_from_review(review, args.view),
                    "facts": review["facts"],
                    "assumptions": review["assumptions"],
                    "hypotheses": review["hypotheses"],
                    "missing_evidence": review["missing_evidence"],
                    "confidence": review["confidence"],
                    "recommended_action": review["recommended_action"],
                    "guardrails": review["guardrails"],
                }
            if args.output:
                target = Path(args.output)
                target.parent.mkdir(parents=True, exist_ok=True)
                if args.format == "json":
                    target.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
                else:
                    target.write_text(str(result["content"]), encoding="utf-8")
                result["output_file"] = str(target)
        elif args.command == "save-memory":
            result = save_packet_to_memory(input_context, args.memory)
        elif args.command == "import-context":
            result = import_context_file(args.input)
        elif args.command == "build-from-file":
            result = build_decision_packet_from_file(args.input)
        elif args.command == "dashboard-from-file":
            result = generate_dashboard_data_from_file(args.input)
        elif args.command == "refresh-dashboard":
            result = refresh_dashboard_data(args.input, args.output)
        elif args.command == "ingest-directory":
            result = ingest_source_directory(args.input)
        elif args.command == "evaluate":
            result = evaluate_golden_examples(args.examples_dir)
        elif args.command == "compare-memory":
            result = compare_with_memory(input_context, _read_json(args.memory))
        elif args.command == "inspect-memory":
            result = inspect_memory_store(args.memory)
        else:
            parser.error(f"unknown command: {args.command}")
            return 2
    except Exception as exc:  # keep CLI errors readable
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def _read_json(path: str) -> Dict[str, Any]:
    target = Path(path)
    if not target.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")
    with target.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return data


def _autopilot_markdown_from_review(review: Dict[str, Any], view: str = "full") -> str:
    if view == "compact":
        return _autopilot_compact_markdown(review)
    if view == "board":
        return _autopilot_board_markdown(review)
    lines = [
        "# Autonomous CIO Operating Review",
        "",
        f"**Enterprise Status:** {review.get('enterprise_status', {}).get('overall', '')}",
        f"**Confidence:** {review.get('confidence', '')}",
        "",
        "## Recommended Action",
        str(review.get("recommended_action", {}).get("recommendation", "")),
        "",
        "## Decisions and Attention",
    ]
    for bucket in ("act_now", "escalate", "decide", "delegate", "monitor"):
        lines.append(f"### {bucket.replace('_', ' ').title()}")
        for item in review.get("attention_budget", {}).get(bucket, []):
            lines.append(f"- {item}")
    lines.extend(["", "## Action Ledger"])
    for action in review.get("action_ledger", []):
        lines.append(f"- {action.get('action_id')}: {action.get('draft_action')} [{action.get('autonomy_level')}]")
    lines.extend(["", "## CIO Shadow Agenda"])
    for item in review.get("cio_shadow_agenda", []):
        lines.append(f"- {item.get('rank')}. {item.get('topic')} [{item.get('recommended_posture')}]")
    lines.extend(["", "## Board Objections"])
    for item in review.get("board_objection_simulator", []):
        lines.append(f"- {item.get('persona')}: {item.get('likely_objection')}")
    lines.extend(["", "## Risk Chain Forecast"])
    for item in review.get("risk_chain_forecast", []):
        lines.append(f"- {item.get('current_signal')} -> {item.get('likely_next_escalation')}")
    lines.extend(["", "## Human Control Contract"])
    lines.append(str(review.get("human_control_contract", {}).get("human_control_statement", "")))
    lines.extend(["", "## Decision SLA"])
    sla = review.get("decision_sla_enforcer", {})
    lines.append(f"- SLA: {sla.get('recommended_decision_sla')} [{sla.get('breach_risk')}]")
    lines.extend(["", "## CIO OS Maturity"])
    maturity = review.get("cio_os_maturity_index", {})
    lines.append(f"- Score: {maturity.get('score')} ({maturity.get('maturity_level')})")
    lines.extend(["", "## Stakeholder Alignment"])
    alignment = review.get("stakeholder_alignment_matrix", {})
    lines.append(f"- Status: {alignment.get('alignment_status')}")
    lines.extend(["", "## Operating Rhythm Autopilot"])
    rhythm = review.get("operating_rhythm_autopilot", {})
    lines.append(f"- Cadence: {rhythm.get('recommended_cadence')}")
    lines.extend(["", "## Escalation Drafts"])
    for draft in review.get("autonomous_escalation_drafts", [])[:5]:
        lines.append(f"- {draft.get('draft_id')}: {draft.get('subject')}")
    lines.extend(["", "## Enterprise Control Tower"])
    tower = review.get("enterprise_control_tower", {})
    lines.append(f"- Overall: {tower.get('overall_status')}")
    lines.extend(["", "## Executive Narrative"])
    narrative = review.get("executive_narrative_generator", {})
    lines.append(f"- {narrative.get('board_narrative')}")
    lines.extend(["", "## Due Diligence Questions"])
    ddq = review.get("autonomous_due_diligence_questions", {})
    lines.append(f"- Count: {ddq.get('question_count')}")
    lines.extend(["", "## Resilience Continuity"])
    resilience = review.get("resilience_continuity_planner", {})
    lines.append(f"- Pressure: {resilience.get('resilience_pressure')}")
    lines.extend(["", "## Cost of Delay"])
    delay = review.get("cost_of_delay_calculator", {})
    lines.append(f"- Qualitative cost: {delay.get('qualitative_cost_of_delay')}")
    lines.extend(["", "## Decision Rights"])
    rights = review.get("decision_rights_mapper", {})
    lines.append(f"- Rights clarity: {rights.get('rights_clarity')}")
    lines.extend(["", "## Dependency Breakpoints"])
    breakpoints = review.get("dependency_breakpoint_analyzer", {})
    lines.append(f"- Count: {breakpoints.get('breakpoint_count')}")
    lines.extend(["", "## Transformation Kill Criteria"])
    kill = review.get("transformation_kill_criteria", {})
    lines.append(f"- Pressure: {kill.get('kill_pressure')}")
    lines.extend(["", "## Roadmap Reprioritizer"])
    roadmap = review.get("autonomous_roadmap_reprioritizer", {})
    lines.append(f"- Required: {roadmap.get('reprioritization_required')}")
    lines.extend(["", "## Audit Finding Predictor"])
    audit = review.get("audit_finding_predictor", {})
    lines.append(f"- Risk: {audit.get('finding_risk')}")
    lines.extend(["", "## Decision War Room"])
    war_room = review.get("executive_decision_war_room", {})
    lines.append(f"- Required: {war_room.get('war_room_required')}")
    lines.extend(["", "## Evidence Chain of Custody"])
    custody = review.get("evidence_chain_of_custody", {})
    lines.append(f"- Required: {custody.get('custody_required')}")
    lines.extend(["", "## Autonomy Risk Budget"])
    budget = review.get("autonomy_risk_budget", {})
    lines.append(f"- Used: {budget.get('budget_used_percent')}% [{budget.get('autonomy_posture')}]")
    lines.extend(["", "## Approval Boundary Mapper"])
    boundary = review.get("approval_boundary_mapper", {})
    lines.append(f"- Boundaries: {boundary.get('boundary_count')}")
    lines.extend(["", "## Evidence Expiry Monitor"])
    expiry = review.get("evidence_expiry_monitor", {})
    lines.append(f"- Required: {expiry.get('expiry_monitor_required')}")
    lines.extend(["", "## Residual Risk Contract"])
    residual = review.get("residual_risk_contract", {})
    lines.append(f"- Required: {residual.get('contract_required')}")
    lines.extend(["", "## Autonomy Stress Test"])
    stress = review.get("autonomy_stress_test", {})
    lines.append(f"- Score: {stress.get('stress_score')} [{stress.get('stress_posture')}]")
    lines.extend(["", "## Decision Consequence Ledger"])
    consequence = review.get("decision_consequence_ledger", {})
    lines.append(f"- Consequences: {consequence.get('consequence_count')}")
    lines.extend(["", "## Enterprise Friction Map"])
    friction = review.get("enterprise_friction_map", {})
    lines.append(f"- Hotspots: {len(friction.get('friction_hotspots', []))}")
    lines.extend(["", "## Strategic Optionality Engine"])
    optionality = review.get("strategic_optionality_engine", {})
    lines.append(f"- Optionality preserved: {optionality.get('optionality_preserved')}")
    lines.extend(["", "## Control Debt Burndown"])
    control_debt = review.get("control_debt_burndown", {})
    lines.append(f"- Items: {control_debt.get('control_debt_count')}")
    lines.extend(["", "## Executive Dissent Synthesizer"])
    dissent = review.get("executive_dissent_synthesizer", {})
    lines.append(f"- Dissent items: {dissent.get('dissent_count')}")
    lines.extend(["", "## Decision Backtest Simulator"])
    backtest = review.get("decision_backtest_simulator", {})
    lines.append(f"- Available: {backtest.get('backtest_available')}")
    lines.extend(["", "## Governance Drift Detector"])
    drift = review.get("governance_drift_detector", {})
    lines.append(f"- Drift detected: {drift.get('drift_detected')}")
    lines.extend(["", "## Budget Shock Absorber"])
    shock = review.get("budget_shock_absorber", {})
    lines.append(f"- Shock level: {shock.get('shock_level')}")
    lines.extend(["", "## Vendor Leverage Index"])
    vendor = review.get("vendor_leverage_index", {})
    lines.append(f"- Leverage: {vendor.get('leverage_score')} [{vendor.get('leverage_posture')}]")
    lines.extend(["", "## Executive Narrative Diff"])
    diff = review.get("executive_narrative_diff", {})
    lines.append(f"- Diff detected: {diff.get('diff_detected')}")
    lines.extend(["", "## Missing Evidence"])
    for item in review.get("missing_evidence", []):
        lines.append(f"- {item}")
    return "\n".join(lines)


def _autopilot_compact_markdown(review: Dict[str, Any]) -> str:
    readiness = review.get("decision_readiness", {})
    status = review.get("enterprise_status", {})
    budget = review.get("autonomy_risk_budget", {})
    stress = review.get("autonomy_stress_test", {})
    lines = [
        "# Autonomous CIO Operating Review - Compact",
        "",
        f"**Status:** {status.get('overall', '')}",
        f"**Decision Readiness:** {readiness.get('value', '')}",
        f"**Confidence:** {review.get('confidence', '')}",
        "",
        "## Recommendation",
        str(review.get("recommended_action", {}).get("recommendation", "")),
        "",
        "## Top Attention",
    ]
    for bucket in ("act_now", "escalate", "decide"):
        items = review.get("attention_budget", {}).get(bucket, [])[:3]
        if items:
            lines.append(f"### {bucket.replace('_', ' ').title()}")
            for item in items:
                lines.append(f"- {item}")
    lines.extend(["", "## Guarded Autonomy"])
    lines.append(f"- Autonomy risk budget: {budget.get('budget_used_percent')}% [{budget.get('autonomy_posture')}]")
    lines.append(f"- Autonomy stress: {stress.get('stress_score')} [{stress.get('stress_posture')}]")
    lines.append(f"- External execution allowed: {review.get('autonomy_gate', {}).get('external_execution_allowed')}")
    lines.extend(["", "## Missing Evidence"])
    for item in review.get("missing_evidence", [])[:5]:
        lines.append(f"- {item}")
    lines.extend(["", "## Next Actions"])
    for action in review.get("action_ledger", [])[:5]:
        lines.append(f"- {action.get('action_id')}: {action.get('draft_action')} [{action.get('autonomy_level')}]")
    return "\n".join(lines)


def _autopilot_board_markdown(review: Dict[str, Any]) -> str:
    narrative = review.get("executive_narrative_generator", {})
    consequence = review.get("decision_consequence_ledger", {})
    dissent = review.get("executive_dissent_synthesizer", {})
    diff = review.get("executive_narrative_diff", {})
    lines = [
        "# Autonomous CIO Board Pack",
        "",
        f"**Enterprise Status:** {review.get('enterprise_status', {}).get('overall', '')}",
        f"**Decision Readiness:** {review.get('decision_readiness', {}).get('value', '')}",
        "",
        "## Board Narrative",
        str(narrative.get("board_narrative", "")),
        "",
        "## Decision Request",
        str(review.get("decision_packet", {}).get("decision_needed", "")),
        "",
        "## Recommended Motion",
        str(review.get("recommended_action", {}).get("recommendation", "")),
        "",
        "## Board Challenge Questions",
    ]
    for item in review.get("board_objection_simulator", [])[:6]:
        lines.append(f"- {item.get('persona')}: {item.get('likely_objection')}")
    lines.extend(["", "## Consequences and Reversal Signals"])
    for item in consequence.get("consequences", [])[:4]:
        lines.append(f"- {item.get('option')}: {item.get('second_order_effect')} | reversal: {item.get('reversal_signal')}")
    lines.extend(["", "## Dissent to Resolve"])
    for item in dissent.get("dissent_items", [])[:4]:
        lines.append(f"- {item.get('persona')}: {item.get('weak_answer_risk')}")
    lines.extend(["", "## Narrative Reconciliation"])
    lines.append(f"- Diff detected: {diff.get('diff_detected')}")
    for question in diff.get("reconciliation_questions", [])[:3]:
        lines.append(f"- {question}")
    lines.extend(["", "## Evidence Gaps"])
    for item in review.get("missing_evidence", [])[:6]:
        lines.append(f"- {item}")
    lines.extend(["", "## Human-Control Boundary"])
    lines.append(str(review.get("human_control_contract", {}).get("human_control_statement", "")))
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
